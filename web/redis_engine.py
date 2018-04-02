import redis

class RedisEngine:

    def init_redis_component(self):
        self.r = redis.Redis(
            host='master',
            port=6379, 
            )
    
    def get(self, key):
        return self.r.get(key)
    
    def set(self, key, value):
        # set expire after time 60 mins
        self.r.set(key, value, ex = 60 * 60)
        pass
    
    def get_redis(self):
        return self.r
    
    def __init__(self):
        self.init_redis_component()
