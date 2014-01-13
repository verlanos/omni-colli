from EventManager import EventManager

__author__ = 'Sefverl'


class OmniCore(object):
    def __init__(self):
        self.evt_mgr = EventManager()

    def getEventManager(self):
        return self.evt_mgr