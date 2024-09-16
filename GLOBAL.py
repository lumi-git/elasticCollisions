class GLOBAL:
    SCREENSIZE = (1000,600)
    GRAVITY = 1
    FRICTION = 1
    CELLSIZE = 100
    ID = 0
    DEBUG = False
    @staticmethod
    def getID():
        GLOBAL.ID += 1
        return GLOBAL.ID