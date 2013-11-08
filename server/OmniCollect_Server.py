__author__ = 'Sefverl'

import socketserver
from crypto import Vigenere


class OmniCollectServer(object):
	def __init__(self, address_to_listen_on, cipher):
		self.listening_socket = socketserver.UDPServer(address_to_listen_on, UDPHandler)

	def listen(self):
		pass

	def connectToDB(self, db_address):
		''' Connect to a given database and return a handle, requires more thought
		'''
		pass


class UDPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		global cipher
		data = self.request[0].strip()
		socket = self.request[1]
		print("{} wrote:".format(self.client_address[0]))

		deciphered = cipher.decipher(data.decode())
		print(deciphered)

		socket.sendto(cipher.cipher("ACCEPTED").encode(), self.client_address)

	def loadCipher(self, cipher):
		self.cipher = cipher


def main():
	HOST, PORT = "localhost", 9999
	global cipher
	cipher = Vigenere.Vigenere("BEESHMAN")
	server = OmniCollectServer((HOST, PORT), cipher)
	server.listening_socket.serve_forever()


if __name__ == "__main__":
	main()