class Config:
    _global = {}

    def __init__(self):
        pass

    def set_global(self, key, value):
        self.__class__._global[key] = value
        return self.__class__._global[key]

    def get_global(self, key):
        return self.__class__._global.get(key, None)


config = Config()
