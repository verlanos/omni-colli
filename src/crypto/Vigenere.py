import string

from Cipher import Cipher

__author__ = 'Sefverl Balasingam (sb610)'
__email__ = 'sb610@kent.ac.uk'
__datetime__ = '27/10/2013'
__version__ = '1.0.0'
__inspired_source__ = "http://smurfoncrack.com/pygenere/pygenere.py"


class Vigenere( Cipher ) :
  ALPHABET = string.printable
  ALPHA_LEN = len( ALPHABET )

  def __init__ ( self , key ) :
    self.key = key

  # Ciphers the stored text by the given keyword and returns it
  def cipher ( self , message ) :

    ciphered = [ ]

    if not self.key or len( self.key ) < 1 :
      return message

    for letter_at in range( len( list( message ) ) ) :
      letter = message[ letter_at ]
      cur_pos_alpha = self.ALPHABET.index( letter )
      shift_vector = self.ALPHABET.index( self.key[ letter_at % len( self.key ) ] )
      new_pos_alpha = (cur_pos_alpha + shift_vector) % self.ALPHA_LEN
      ciphered.append( self.ALPHABET[ new_pos_alpha ] )

    return "".join( ciphered )

  # Deciphers the stored text by the given keyword and returns it
  def decipher ( self , ciphermessage ) :

    deciphered = [ ]

    if not self.key or len( self.key ) < 1 :
      return ciphermessage

    for letter_at in range( len( list( ciphermessage ) ) ) :
      letter = ciphermessage[ letter_at ]
      cur_pos_alpha = self.ALPHABET.index( letter )
      shift_vector = self.ALPHABET.index( self.key[ letter_at % len( self.key ) ] )
      new_pos_alpha = (cur_pos_alpha + ((shift_vector * -1) % self.ALPHA_LEN)) % self.ALPHA_LEN
      deciphered.append( self.ALPHABET[ new_pos_alpha ] )

    return "".join( deciphered )

  def set_key ( self , key ) :
    self.key = key
