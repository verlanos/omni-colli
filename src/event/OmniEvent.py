__author__ = 'Sefverl'


class OmniEvent(object):
    def __init__(self, device_id, payload, timestamp=None):
        self.timestamp = timestamp
        self.device_id = device_id
        self.payload = payload