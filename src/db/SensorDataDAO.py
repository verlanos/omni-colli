__author__ = 'Sefverl'

import datetime
from uuid import getnode as get_mac

from pymongo import MongoClient, errors


class SensorDataDAO(object):
    def __init__(self, db_host_address, db_name, db_collection):
        (self.db_hostname, self.db_port) = db_host_address
        self.db_name = db_name

        self.collection_name = db_collection
        self.connected = False
        self.db_handle = None


def insert_sensor_data(self, data, meta_data, device_id=None, timestamp=None, record_id=None):
    """
    Insert sensor record into active collection of current MongoDB database. If no connection has been established
    prior this function call, a new connection will be established.

    'data' - raw value
    'meta_data' - measurement unit of value stored in 'data'
    """
    if not self.connected:
        try:
            client = MongoClient(self.db_hostname, self.db_port)
            db = client[self.db_name]
            self.db_handle = db[self.collection_name]
            self.connected = True
        except errors.PyMongoError as pe:
            print("Connection to ", self.db_hostname, ":", self.db_port, " failed :(\nERROR: ", pe.message)

    if not device_id:
        device_id = str(get_mac())

    if not timestamp:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    if not record_id:
        record_id = str(timestamp) + "#" + str(device_id)

    sensor_record = {"_id": record_id,
                     "created": timestamp,
                     "device_id": device_id,
                     "data": data,
                     "meta": meta_data}

    try:
        self.db_handle.insert(sensor_record)
    except errors.PyMongoError as pe:
        print("Insertion of ", str(sensor_record), " INTO COLLECTION", self.collection_name, " OF DATABASE ",
              self.db_name, ' @ HOST ', self.db_hostname, ":", self.db_port, " failed :(\nERROR: ", pe.message)