from flask import Blueprint, request, jsonify, current_app
import uuid

player_bp = Blueprint('player', __name__)


# --------------------------------------
# ROUTE 1: Start a Match
# --------------------------------------
@player_bp.route('/start_match', methods=['POST'])
def start_match():
    redis_client = current_app.redis_client

    data = request.get_json()
    if not all(k in data for k in ['player1', 'player2']):
        return jsonify({"error": "Missing required fields"}), 400
    player1 = data['player1']
    player2 = data['player2']
    
    match_id = str(uuid.uuid4())
    match_key = f"match:{match_id}:state"

    fields = {
        "p1_id": str(player1),
        "p2_id": str(player2),
        "p1_hp": "100",
        "p2_hp": "100",
        "p1_x": "0",
        "p2_x": "50"
    }
    redis_client.hset(match_key, mapping=fields)

    redis_client.expire(match_key, 1800)  # Auto-expire in 30 minutes

    return jsonify({"match_id": match_id, "status": "match started"})


# --------------------------------------
# ROUTE 2: Update Health
# --------------------------------------
@player_bp.route('/update_health', methods=['POST'])
def update_health():
    redis_client = current_app.redis_client

    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ['match_id', 'player', 'damage']):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate numeric damage
    try:
        damage = int(data['damage'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid damage value"}), 400

    match_id = data['match_id']
    player = data['player']  # Should be 'p1' or 'p2'

    match_key = f"match:{match_id}:state"
    hp_field = f"{player}_hp"

    # Check if key exists in Redis
    if not redis_client.exists(match_key):
        return jsonify({"error": "Match not found"}), 404

    try:
        current_hp = int(redis_client.hget(match_key, hp_field))
    except (TypeError, ValueError):
        return jsonify({"error": f"Invalid HP field for {player}"}), 400

    new_hp = max(current_hp - damage, 0)
    redis_client.hset(match_key, hp_field, new_hp)

    return jsonify({"status": "health updated", f"{player}_hp": new_hp})



# --------------------------------------
# ROUTE 3: End Match and Save Result
# --------------------------------------
@player_bp.route('/end_match', methods=['POST'])
def end_match():
    redis_client = current_app.redis_client
    pg_conn = current_app.pg_conn
    cursor = pg_conn.cursor()

    data = request.get_json()

    # Validate fields
    if not all(k in data for k in ['match_id', 'winner', 'loser']):
        return jsonify({"error": "Missing required fields"}), 400

    # Convert match_id safely
    try:
        match_id = str(data['match_id'])  # changed from int() to str() to avoid datatype mismatch
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid match_id"}), 400

    winner = str(data['winner'])
    loser = str(data['loser'])

    # Update player stats
    for pid, won in [(winner, True), (loser, False)]:
        cursor.execute("SELECT * FROM player_stats WHERE player_id = ?", (pid,))
        if cursor.fetchone():
            if won:
                cursor.execute("UPDATE player_stats SET wins = wins + 1 WHERE player_id = ?", (pid,))
            else:
                cursor.execute("UPDATE player_stats SET losses = losses + 1 WHERE player_id = ?", (pid,))
        else:
            cursor.execute(
                "INSERT INTO player_stats (player_id, wins, losses) VALUES (?, ?, ?)",
                (pid, 1 if won else 0, 0 if won else 1)
            )

    # Update Redis leaderboard
    redis_client.zincrby("leaderboard:arena", 1, f"player:{winner}")

    # Save match history (make sure column types match)
    try:
        cursor.execute(
            "INSERT INTO matches (player_1_id, player_2_id, winner_id) VALUES (?, ?, ?)",
            (winner, loser, winner)
        )
    except Exception as e:
        return jsonify({"error": f"Database insert failed: {str(e)}"}), 400

    pg_conn.commit()
    return jsonify({"status": "match ended and stats updated"})


# --------------------------------------
# ROUTE 4: Leaderboard
# --------------------------------------    

@player_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    redis_client = current_app.redis_client
    data = redis_client.zrevrange("leaderboard:arena", 0, -1, withscores=True)
    return jsonify({"leaderboard": data})


