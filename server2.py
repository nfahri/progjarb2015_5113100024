import socket
import threading
import logging
import time

HOST = ''
PORT = 8018
BUF_SIZE = 1024

class server(threading.Thread):

	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.ip = self.addr[0]
		self.username = ''

	def printMessage(self, msg):
		self.conn.send('%s\n>> ' % (msg,))

	def login(self):
		global client
		global pesan
		global akun
		global online

		logging.info('Connected from : %s %s' % (self.addr[0], self.addr[1]))
		msg = 'Username : '
		self.printMessage(msg)
		username = self.conn.recv(BUF_SIZE).strip()

		while username in akun:
			self.printMessage('Username %s telah digunakan, silakan masukkan password anda atau tekan !q untuk mengganti username\nPassword :' % (username))
			password = self.conn.recv(BUF_SIZE).strip()
			if(password.find('!q') == 0):
				while 1:
					msg = 'Username : '
					self.printMessage(msg)
					username = self.conn.recv(BUF_SIZE).strip()
					break
			else:
				while 1:
					self.username = username
					if(password != akun[self.username]['password']):
						msg = 'Password yang anda masukkan salah.\nPassword :'
						self.printMessage(msg)
						password = self.conn.recv(BUF_SIZE).strip()
						break						
					else:
						self.printMessage('--- Selamat Datang Kembali %s, Login terakhir %s ' % (username, akun[username]['terakhirLogin']))
						self.username = username
						akun[self.username]['terakhirLogin'] = time.ctime()
						return
						

		msg = 'Password : '		
		self.printMessage(msg)
		self.username = username
		password = self.conn.recv(BUF_SIZE).strip()
		# akun[self.username] = {
		# 	'pass' = password,
		# 	'lastlogin' = time.ctime()
		# }
		akun[self.username] = {
            'password': password,
        	'terakhirLogin': time.ctime()
        }
		online[self.username] = self.conn
		print akun
		return

	def run(self):
		global client
		global pesan
		global akun
		self.login()

		self.conn.send('Welcome, enjoy your chat')



def main():
	global client
	global pesan
	global akun
	global online

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

	client = set()
	pesan = {}
	akun = {}
	online = {}

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((HOST, PORT))
	sock.listen(5)

	while 1:
		try:
			conn, addr = sock.accept()
			beginServer = server(conn, addr)
			beginServer.start()
		except:
			print 'Leave'

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Quited'