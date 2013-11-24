__author__ = 'Sefverl'

import unittest
import random

from crypto.Vigenere import Vigenere


class TestVigenereCipher(unittest.TestCase):
  def setUp ( self ) :
    self.sample_texts = [ ]
    self.sample_keys = [ ]

    self.cypher = Vigenere( "CLASS" )

    for sample_text in range( 0 , 10 ) :
      plain = [ ]
      key = [ ]
      for letter in range( 0 , 10 ) :
        letter_index = random.randint( 0 , self.cypher.ALPHA_LEN - 1 )
        plain.append( self.cypher.ALPHABET[ letter_index ] )

      for key_letter in range( 0 , 10 ) :
        letter_index = random.randint( 0 , self.cypher.ALPHA_LEN - 1 )
        key.append( self.cypher.ALPHABET[ letter_index ] )

      self.sample_texts.append( "".join( plain ) )
      self.sample_keys.append( "".join( key ) )

  def test_cipher ( self ) :

    for test in range( len( self.sample_texts ) ) :
      test_obj = Vigenere( self.sample_keys[ test ] )
      ciphered = test_obj.cipher( self.sample_texts[ test ] )
      deciphered = test_obj.decipher( ciphered )
      self.assertEqual( self.sample_texts[ test ] , deciphered )

  def test_decipher ( self ) :

    for test in range( len( self.sample_texts ) ) :
      test_obj = Vigenere( self.sample_keys[ test ] )
      deciphered = test_obj.cipher( self.sample_texts[ test ] )
      ciphered = test_obj.decipher( deciphered )
      self.assertEqual( self.sample_texts[ test ] , ciphered )

  if __name__ == "__main__" :
    unittest.main( )
