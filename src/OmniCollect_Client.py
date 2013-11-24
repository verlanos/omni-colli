__author__ = 'Sefverl'

import socket
import sys
import getopt
import datetime

from uuid import getnode as get_mac

from config.ConfigDAO import ConfigDAO
from crypto.Vigenere import Vigenere

class OmniCollectClient(object):
  def __init__ ( self , cipher ) :
    self.connection = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
    self.cipher = cipher

  def connect_to ( self , address_to_connect_to ) :
    self.connection.connect( address_to_connect_to )

  def send_message ( self , message , address_to_send_to ) :
    self.connection.sendto( self.cipher.cipher( message ).encode( ) , address_to_send_to )
    received_ciphered = self.connection.recv( 1024 ).decode( )
    received = self.cipher.decipher( received_ciphered )
    print("Sent: {}".format( message ))
    print("Received: {}".format( received ))


def main ( argv ) :
  try :
    opts , args = getopt.getopt( argv , "?h:p:" , [ "host=" , "port=" ] )
  except getopt.GetoptError :
    print 'OmniCollect_Client -h HOSTNAME -p PORT'
    sys.exit( 2 )

  HOST , PORT = "" , 0

  for opt , arg in opts :
    if opt == '-?' :
      print 'OmniCollect_Server -h HOSTNAME -p PORT'
    elif opt in ('-p') :
      PORT = int( arg )
    elif opt in ('-h') :
      HOST = arg

  cfg_man = ConfigDAO( )
  cipher_cred = cfg_man.load_config( 'cipher' )
  cipher_key = cipher_cred.get( 'key' )

  cipher = Vigenere( cipher_key )

  client = OmniCollectClient( cipher )
  print(HOST , "@" , PORT)
  client.connect_to( (HOST , PORT) )

  data = 40
  meta_data = "C"
  device_id = get_mac( )
  timestamp = datetime.datetime.now( ).strftime( "%Y%m%d%H%M%S" )

  message = '{"data":"{0}","meta":"{1}","id":"{2}","timestamp":"{3}"}'.format( str( data ) , str( meta_data ) ,
                                                                               str( device_id ) , str( timestamp ) )

  client.send_message( message , (HOST , PORT) )


if __name__ == "__main__":
  main( sys.argv[ 1 : ] )
