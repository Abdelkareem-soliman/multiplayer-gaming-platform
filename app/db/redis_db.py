import redis

def init_redis(app):
    app.redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
