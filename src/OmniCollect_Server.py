__author__ = 'Sefverl'

import SocketServer
import sys
import getopt

from crypto.Vigenere import Vigenere


class OmniCollectServer(object):
  def __init__ ( self , address_to_listen_on , cipher ) :
    self.listening_socket = SocketServer.UDPServer( address_to_listen_on , UDPHandler )

  def connectToDB ( self , db_address ) :
    ''' Connect to a given database and return a handle, requires more thought
    '''
    pass


class UDPHandler( SocketServer.BaseRequestHandler ) :
  def handle ( self ) :
    global cipher
    data = self.request[ 0 ].strip( )
    socket = self.request[ 1 ]
    print("{} wrote:".format( self.client_address[ 0 ] ))

    deciphered = cipher.decipher( data.decode( ) )
    print(deciphered)

    socket.sendto( cipher.cipher( "ACCEPTED" ).encode( ) , self.client_address )


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

  global cipher
  cipher = Vigenere( "BEESHMAN" )
  server = OmniCollectServer( (HOST , PORT) , cipher )

  if server.listening_socket :
    print("Server is listening on port " , PORT , " for UDP packets...")

  server.listening_socket.serve_forever( )


if __name__ == "__main__":
  main( sys.argv[ 1 : ] )
