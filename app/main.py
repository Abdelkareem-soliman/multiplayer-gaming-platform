from flask import Flask
from app.db.postgres import init_postgres
from app.db.mongo import init_mongo
from app.db.redis_db import init_redis
from app.routes.player import player_bp
from flask_cors import CORS


app = Flask(__name__)

# Initialize databases
CORS(app)  # This enables frontend ↔ backend communication
init_postgres(app)
init_mongo(app)
init_redis(app)

# Register routes
app.register_blueprint(player_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader = False)
