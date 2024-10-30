import redis
import os

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", 6379),
    db=0,
    decode_responses=True
)

def cache_user_session(session_id, user_data, expiration=3600):
    redis_client.hmset(session_id, user_data)
    redis_client.expire(session_id, expiration)

def get_user_session(session_id):
    return redis_client.hgetall(session_id)
