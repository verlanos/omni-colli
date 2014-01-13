from OmniEvent import OmniEvent

__author__ = 'Sefverl'


class Logger(object):
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def init_file(self):
        self.file = open(self.filename, "a")

    def log(self, arg):

        print("Logging sensor data")

        print("Logger Experimental: Event content: " + str(arg))
        if not self.file:
            self.init_file()

        log_file = self.file

        message_structure = "Timestamp: {0}  Device ID: {1}  Data type: {2}  Data: {3}\n"

        if arg is OmniEvent:
            payload = arg.payload
            timestamp = arg.timestamp
            device_id = arg.device_id
            data_type = payload.get('data_type')
            data = payload.get('data')
            message = message_structure.format(timestamp, device_id, data_type, data)
            print("Logging to file: " + message)
            log_file.write(message)

    def __callback__(self, arg):
        self.log(arg)
