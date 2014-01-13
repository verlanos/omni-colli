__author__ = 'Sefverl'


class OmniComponent(object):
    def __init__(self, core_instance):
        self.core = core_instance

    def getEventManager(self):
        return self.core.getEventManager()