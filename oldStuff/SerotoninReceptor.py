
class serotoninReceptor(object):

    def __init__(self, serotoninLevel = 50):
        self.serotoninLevel = serotoninLevel



    def setSerotoninLevel(self, serotoninLevel):
        self.serotoninLevel = serotoninLevel

    def getSerotoninLevel(self, serotoninLevel):
        return self.serotoninLevel

    def setTarget(self, target):
        self.target = target

    def getType(self):
        return "undefined"

    def setActivity(self, function):
        self.activity(function)

