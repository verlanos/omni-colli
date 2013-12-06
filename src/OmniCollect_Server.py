__author__ = 'Sefverl'

import SocketServer
import sys
import getopt
import re
import json

from config.ConfigDAO import ConfigDAO
from SensorDataDAO import SensorDataDAO

class OmniCollectServer(object):
    def __init__(self, address_to_listen_on):
        self.listening_socket = SocketServer.UDPServer(address_to_listen_on, UDPHandler)


class UDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print("Received {0} from {1}:".format(data.decode(), self.client_address[0]))

        decoded = data.decode()

        print("{0} plain: '{1}'".format(" " * 4, decoded))

        document = self.identify_message(decoded)
        self.store_message(document)

    def identify_message(self, message):
        """
        Parse 'message' for JSON document, return 'dict' if successful, 'None' otherwise

        :param message:
        """
        outer = re.search('(\{.*\})', message)

        if len(outer.group()) <= 0:
            return None

        document = outer.group(0)
        record = json.loads(document)

        return record

    def store_message(self, document):
        """
        Extract required fields of 'document' and pass onto 'dbms' (Database connection handle)

        :param document:
        """
        document = dict(document)

        data = document.get('data')
        timestamp = document.get('timestamp')
        meta_data = document.get('meta')
        origin_id = document.get('id')

        global dbms
        if dbms and type(dbms) == SensorDataDAO:
            dbms.insert_sensor_data(data, meta_data, origin_id, timestamp)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hp:", ["port="])
    except getopt.GetoptError:
        print 'OmniCollect_Server -p PORT e.g. 9999'
        sys.exit(2)

    host, port = "", -1

    for opt, arg in opts:
        if opt == '-h':
            print 'OmniCollect_Server -p PORT e.g. 9999'
        elif opt in '-p':
            port = int(arg)

    if port == -1:
        sys.exit(2)

    cfg_man = ConfigDAO()

    global dbms

    db_cred = cfg_man.load_config('db')
    db_host = db_cred.get('db_host_name')
    db_port = db_cred.get('db_host_port')
    db_name = db_cred.get('db_name')
    db_collection = db_cred.get('db_collection')

    print("Database host: ", db_host)
    print("Database interface port: ", db_port)
    print("Database name: ", db_name)
    print("Active collection: ", db_name, ".", db_collection)

    dbms = SensorDataDAO((db_host, db_port), db_name, db_collection)
    server = OmniCollectServer((host, port))

    server.listening_socket.serve_forever()

    if server.listening_socket:
        print("Server is listening on port ", port, " for UDP packets...")


if __name__ == "__main__":
    main(sys.argv[1:])
