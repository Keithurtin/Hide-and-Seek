

class GlobalInfo:
    __instance = None

    @staticmethod
    def Instance():
        if GlobalInfo.__instance is None:
            GlobalInfo.__instance = GlobalInfo()
        return GlobalInfo.__instance

    def __init__(self):
        self.__global_info = {}

    def getGlobalInfo(self, id):
        if id not in self.__global_info:
            return None
        return self.__global_info.get(id)

    def setGlobalInfo(self, id, value):
        self.__global_info[id] = value
