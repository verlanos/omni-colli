from OmniEvent import OmniEvent
from OmniModule import OmniModule

__author__ = 'Sefverl'


class Logger(OmniModule):
    def __init__(self, core, filename):
        super(Logger, self).__init__(core)
        self.filename = filename
        self.file = None
        self.log("Hi")

    def init_file(self):
        self.file = open(self.filename, "w")

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
        else:
            log_file.write("I have logged myself now! Hurray!")
            log_file.flush()
            log_file.close()

    def __about__(self):
        return "I am a Logger"

    def __callback__(self, arg):
        self.log(arg)


def init_instance(**kwargs):
    return Logger(**kwargs)