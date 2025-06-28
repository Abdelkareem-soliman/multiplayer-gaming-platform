import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

# ------------------ START MATCH ------------------

def test_start_match_success(client):
    response = client.post('/start_match', json={
        "player1": "Ahmed",
        "player2": "Mandoh",
        "match_id": 1
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == "match started"
    assert "match_id" in data

def test_start_match_missing_field(client):
    response = client.post('/start_match', json={
        "player1": "Ahmed",
        "match_id": 1
    })
    assert response.status_code in (400, 500)
    assert b"player2" in response.data or b"error" in response.data

# ------------------ UPDATE HEALTH ------------------

def test_update_health_success(client):
    # Step 1: Start a match
    start_resp = client.post('/start_match', json={
        "player1": "Ahmed",
        "player2": "Mandoh",
        "match_id": 1
    })
    start_data = start_resp.get_json()
    match_id = start_data["match_id"]

    # Step 2: Now update health
    response = client.post('/update_health', json={
        "player": "p1",        # Must match field like 'p1_hp'
        "match_id": match_id,
        "damage": 15
    })

    data = response.get_json()
    assert response.status_code == 200
    assert data.get("status") == "health updated"
    assert "p1_hp" in data


# ------------------ END MATCH ------------------

def test_end_match_success(client):
    response = client.post('/end_match', json={
        "match_id": "match-123",
        "winner": "Ahmed",
        "loser": "Mandoh"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data.get("status") == "match ended and stats updated"  # ✅ exact match

# ------------------ LEADERBOARD ------------------

def test_leaderboard(client):
    response = client.get('/leaderboard')
    data = response.get_json()
    assert response.status_code == 200
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)
