__author__ = 'Sefverl'

import socket
import sys
import getopt
import datetime

from uuid import getnode as get_mac


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
        print 'OmniCollect_Client -h HOSTNAME -p PORT -m VALUE:UNIT e.g. 40:C'
        sys.exit(2)

    host, port = "", 0
    data_raw, data_meta = None, None

    for opt, arg in opts:
        if opt == '-?':
            print 'OmniCollect_Client -h HOSTNAME -p PORT -m VALUE:UNIT e.g. 40:C'
        elif opt in '-p':
            port = int(arg)
        elif opt in '-h':
            host = arg
        elif opt in '-m':
            data_pair = arg.split(':')
            data_raw = data_pair[0].strip()
            data_meta = data_pair[1].strip()

    client = OmniCollectClient()
    print(host, "@", port)
    client.connect_to((host, port))

    if data_raw and data_meta:
        device_id = get_mac()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        message = '{"data":"{0}","meta":"{1}","id":"{2}","timestamp":"{3}"}'.format(str(data_raw), str(data_meta),
                                                                                    str(device_id), str(timestamp))

        client.send_message(message, (host, port))


if __name__ == "__main__":
    main(sys.argv[1:])
