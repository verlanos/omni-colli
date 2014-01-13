__author__ = 'Sefverl'


class OmniModule(object):
    def __init__(self, core):
        self.core = core

    def __input__(self):
        return NotImplementedError

    def __output__(self):
        return NotImplementedError

    def __callback__(self, event_obj):
        return NotImplementedError

    def __about__(self):
        return NotImplementedError