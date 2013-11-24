__author__ = 'Sefverl'

import SocketServer
import sys
import getopt
import re
import json

from crypto.Vigenere import Vigenere
from config.ConfigDAO import ConfigDAO
from SensorDataDAO import SensorDataDAO


class OmniCollectServer(object):
  def __init__ ( self , address_to_listen_on , cipher ) :
    self.listening_socket = SocketServer.UDPServer( address_to_listen_on , UDPHandler )

  def connectToDB ( self , db_address , db_name , db_collection ) :
    ''' Connect to a given database and return a handle, requires more thought'''


class UDPHandler( SocketServer.BaseRequestHandler ) :
  def handle ( self ) :
    global cipher
    data = self.request[ 0 ].strip( )
    socket = self.request[ 1 ]
    print("Received {0} from {1}:".format( data.decode( ) , self.client_address[ 0 ] ))

    if cipher and type( cipher ) == Vigenere :
      deciphered = cipher.decipher( data.decode( ) )
    else :
      deciphered = data.decode( )

    print("{0} plain: '{1}'".format( " " * 4 , deciphered ))

    document = self.identify_message( deciphered )
    self.store_message( document )

    #socket.sendto( cipher.cipher( "ACCEPTED" ).encode( ) , self.client_address )

  def identify_message ( self , message ) :

    outer = re.search( '(\{.*\})' , message )

    if len( outer.group( ) ) <= 0 :
      return None

    document = outer.group( 0 )
    record = json.loads( document )

    return record

  def store_message ( self , document ) :

    document = dict( document )

    data = document.get( 'data' )
    timestamp = document.get( 'timestamp' )
    meta_data = document.get( 'meta' )
    origin_id = document.get( 'id' )

    global dbms
    if dbms and type( dbms ) == SensorDataDAO :
      dbms.insert_sensor_data( data , meta_data , origin_id , timestamp )


  def loadCipher ( self , cipher ) :
    self.cipher = cipher


def main ( argv ) :
  try :
    opts , args = getopt.getopt( argv , "hp:" , [ "port=" ] )
  except getopt.GetoptError :
    print 'OmniCollect_Server -p PORT e.g. 9999'
    sys.exit( 2 )

  HOST , PORT = "" , -1

  for opt , arg in opts :
    if opt == '-h' :
      print 'OmniCollect_Server -p PORT e.g. 9999'
    elif opt in ('-p') :
      PORT = int( arg )

  if PORT == -1 :
    sys.exit( 2 )

  cfg_man = ConfigDAO( )

  global cipher
  global dbms

  cipher_cred = cfg_man.load_config( 'cipher' )
  cipher_key = cipher_cred.get( 'key' )

  cipher = Vigenere( cipher_key )

  db_cred = cfg_man.load_config( 'db' )
  db_addr = db_cred.get( 'db_addr' )
  db_name = db_cred.get( 'db_name' )
  db_collection = db_cred.get( 'db_collection' )

  dbms = SensorDataDAO( db_addr , db_name , db_collection )
  server = OmniCollectServer( (HOST , PORT) , cipher )

  if server.listening_socket :
    print("Server is listening on port " , PORT , " for UDP packets...")

  server.listening_socket.serve_forever( )


if __name__ == "__main__":
  main( sys.argv[ 1 : ] )
