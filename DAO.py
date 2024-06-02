CACHE = {}
class DAO:
    def __init__(self):
        pass
    def getUser(self, key):
        return CACHE.get(key)
    def setUser(self, key, value):
        o_value = CACHE.get(key)
        if o_value:
            o_value.update(value)
            CACHE[key] = o_value
        else:
            CACHE[key] = value
        print(CACHE)
        return CACHE[key]
    def delete(self, key):
        return CACHE.pop(key)
