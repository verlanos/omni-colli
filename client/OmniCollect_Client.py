__author__ = 'Sefverl'

import socket
from crypto import Vigenere


class OmniCollectClient(object):
	def __init__(self, cipher):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.cipher = cipher

	def send_message(self, message, address_to_send_to):
		self.connection.sendto(self.cipher.cipher(message).encode(), address_to_send_to)
		received_ciphered = self.connection.recv(1024).decode()
		received = self.cipher.decipher(received_ciphered)
		print("Sent: {}".format(message))
		print("Received: {}".format(received))


def main():
	HOST, PORT = "iotx.dyndns-server.com", 47777
	cipher = Vigenere.Vigenere("BEESHMAN")
	client = OmniCollectClient(cipher)
	client.send_message("HelloWorld", (HOST, PORT))


if __name__ == "__main__":
	main()
