__author__ = 'Sefverl'

import socket
import sys
import getopt

from crypto import Vigenere


class OmniCollectClient(object):
  def __init__ ( self , cipher ) :
    self.connection = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
    self.cipher = cipher

  def send_message ( self , message , address_to_send_to ) :
    self.connection.sendto( self.cipher.cipher( message ).encode( ) , address_to_send_to )
    received_ciphered = self.connection.recv( 1024 ).decode( )
    received = self.cipher.decipher( received_ciphered )
    print("Sent: {}".format( message ))
    print("Received: {}".format( received ))


def main ( argv ) :
  try :
    opts , args = getopt.getopt( argv , "?hp:" , [ "port=" ] )
  except getopt.GetoptError :
    print 'OmniCollect_Client -h HOSTNAME -p PORT e.g. 9999'
    sys.exit( 2 )

  HOST , PORT = "" , 0

  for opt , arg in opts :
    if opt == '-?' :
      print 'OmniCollect_Server -h HOSTNAME -p PORT e.g. 9999'
    elif opt in ('-p') :
      PORT = int( arg )
    elif opt in ('-h') :
      HOST = arg

  cipher = Vigenere.Vigenere( "BEESHMAN" )
  client = OmniCollectClient( cipher )
  client.send_message( "HelloWorld" , (HOST , PORT) )


if __name__ == "__main__":
  main( sys.argv[ 1 : ] )
