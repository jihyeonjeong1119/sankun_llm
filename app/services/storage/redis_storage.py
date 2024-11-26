import redis
import json

class RedisStorage:
    def __init__(self, host='3.34.78.166', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key: str, value: dict, expire: int = 3600):
        """Set a value in Redis with an optional expiration time."""
        self.client.set(key, json.dumps(value), ex=expire)

    def get(self, key: str) -> dict:
        """Get a value from Redis by key."""
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete(self, key: str):
        """Delete a key from Redis."""
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        return self.client.exists(key) > 0