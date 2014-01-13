__author__ = 'Sefverl'

import socket
import sys
import getopt
import datetime


class OmniCollectClient(object):
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect_to(self, address_to_connect_to):
        self.connection.connect(address_to_connect_to)

    def send_message(self, message, address_to_send_to):
        self.connection.sendto(message.encode(), address_to_send_to)
        print("Sent: {}".format(message))

    def receive_message(self, buffer_size):
        return self.connection.recv(buffer_size).decode()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "?h:p:m:", ["host=", "port=", "message="])
    except getopt.GetoptError:
        print 'OmniCollect_Client -h HOSTNAME -p PORT -m VALUE:UNIT e.g. 40:C:TEMPERATURE'
        sys.exit(2)

    host, port = "", 0
    data_raw, data_meta, data_type = None, None, None

    for opt, arg in opts:
        if opt == '-?':
            print 'OmniCollect_Client -h HOSTNAME -p PORT -m VALUE:UNIT:TYPE e.g. 40:C:TEMPERATURE'
        elif opt in '-p':
            port = int(arg)
        elif opt in '-h':
            host = arg
        elif opt in '-m':
            data_pair = arg.split(':')
            data_raw = data_pair[0].strip()
            data_meta = data_pair[1].strip()
            data_type = data_pair[2].strip()

    client = OmniCollectClient()
    print(host, "@", port)
    client.connect_to((host, port))

    if (data_raw and data_meta) and data_type:
        #device_id = get_mac()
        device_id = "test"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        message_template = '''{{"data":"{0}","meta":"{1}","id":"{2}","timestamp":"{3}","data_type":"{4}"}}'''
        message = message_template.format(str(data_raw), str(data_meta), str(device_id), str(timestamp), str(data_type))

        print('Message content: ' + message)
        client.send_message(message, (host, port))


if __name__ == "__main__":
    main(sys.argv[1:])
