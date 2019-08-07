

# Might use a singleton controller to handle passing around values
class Controller(object):
    __instance = None

    def __init__(self):
        if Controller.__instance != None:
            raise Exception('This is a singleton controller')
        else:
            Controller.__instance = self

    @staticmethod
    def get_instance():
        if Controller.__instance == None:
            Controller()
        
        return Controller.__instance
