import pickle

__author__ = 'Sefverl'

import os


class ConfigDAO( object ) :
  def __init__ ( self , default_directory=None ) :
    self.directory = default_directory

  def store_config ( self , key , doc ) :
    key = key.lower( )

    filename = os.path.join( self.directory if self.directory else os.path.curdir , key + ".conf" )
    fd = open( filename , 'w' )
    pickle.dump( doc , fd )

  def list_configs ( self ) :
    directory = self.directory if self.directory else os.path.curdir

    dir_listing = os.listdir( directory )
    json_configs = [ entry for entry in dir_listing if
                     (os.path.isfile( entry ) and ((entry.split( '.' )[ -1 ]) == 'conf') ) ]

    return json_configs

  def load_config ( self , key ) :
    key = key.lower( )

    if key in self.list_configs( ) :
      fd = open( key + ".conf" , 'r' )
      doc = pickle.load( fd )
      return doc

    return { }
