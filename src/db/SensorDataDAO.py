__author__ = 'Sefverl'

import datetime
from uuid import getnode as get_mac

import pymongo


class SensorDataDAO( object ) :
  def __init__ ( self , db_host_address , db_name , db_collection ) :
    self.db_hostname , self.db_port = db_host_address
    self.db_name = db_name
    self.collection_name = db_collection
    self.connected = False
    self.db_handle = None

  def insert_sensor_data ( self , data , meta_data , device_id=None , timestamp=None , record_id=None ) :

    if not self.connected :
      client = pymongo.MongoClient( self.db_hostname , self.db_port )
      db = client[ self.db_name ]
      self.db_handle = db[ self.collection_name ]
      self.connected = True

    if not device_id :
      device_id = str( get_mac( ) )

    if not timestamp :
      timestamp = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )

    if not record_id :
      record_id = str( timestamp ) + "#" + str( device_id )

    sensor_record = { "_id" : record_id ,
                      "created" : timestamp ,
                      "device_id" : device_id ,
                      "data" : data ,
                      "meta" : meta_data }

    stored_id = self.db_handle.insert( sensor_record )

    return stored_id


dao = SensorDataDAO( ("localhost" , 27017) , 'iot' , 'sensor_data' )

res = dao.insert_sensor_data( 45 , "C" , get_mac( ) )

if res :
  print("Sensor data added")