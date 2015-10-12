# @credit : xin wang

import socket
import threading
import logging
import time
import sys

HOST = ''
PORT = 8018
TIMEOUT = 5
BUF_SIZE = 1024

class server(threading.Thread):

	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
		self.ip = self.addr[0]
		self.username = ''

	def printMessage(self, msg):
		self.conn.send('%s' % (msg,))

	def login(self):
		global client
		global pesan
		global accounts
		global online

		logging.info('Connected from : %s %s' % (self.addr[0], self.addr[1]))
		# client.add((self.conn, self.addr))
		msg = 'Username : '
		self.printMessage(msg)
		username = self.conn.recv(BUF_SIZE).strip()

		while username in accounts:
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
					if(password != accounts[self.username]['password']):
						msg = 'Password yang anda masukkan salah.\nPassword :'
						self.printMessage(msg)
						password = self.conn.recv(BUF_SIZE).strip()
						break						
					else:
						self.printMessage('--- Selamat Datang Kembali %s, Login terakhir %s ' % (username, accounts[username]['terakhirLogin']))
						self.username = username
						accounts[self.username]['terakhirLogin'] = time.ctime()
						return
						

		msg = 'Password : '		
		self.printMessage(msg)
		self.username = username
		password = self.conn.recv(BUF_SIZE).strip()
		# accounts[self.username] = {
		# 	'pass' = password,
		# 	'lastlogin' = time.ctime()
		# }
		accounts[self.username] = {
            'password': password,
        	'terakhirLogin': time.ctime()
        }
		online[self.username] = self.conn
		# print accounts
		return

	def controller(self, readInput):
		global online
		# print 'masuk controller'

		if(readInput.find('sendall@')==0):
			self.sendall(readInput, online)
		elif(readInput.find('sendto@')==0):
			self.sendto(readInput, online)
		elif(readInput.find('list@')==0):
			self.list(online)
		elif(readInput.find('help@')==0):
			self.help()
		else:
			msg = 'fitur yang anda masukkan belum terdaftar, ketik help@ untuk melihat daftar fitur yang ada'
			self.printMessage(msg)

	def sendall(self, msg, online):
		# print 'masuk sendall'
		# print online
		# print msg
		msg = msg.split(' ',1)[1]
		# print msg
		for username in online:
			# print 'print to'+username
			# print online[username]
			if(self.username != username):
				online[username].send('[ %s ] : %s' % (self.username, msg))
			else:
				self.printMessage('[ you - all ] : %s' % (msg))

	def sendto(self, msg, online):
		if(msg.find('"')==7):
			receiver = msg.split('"')[1]
			msg = msg.split('"')[2]
		else:
			receiver = msg.split()[0][7:]
			msg = msg.split(' ', 1)[1]

		if(receiver not in online):
			msg = 'penerima sedang offline'
			self.printMessage(msg)
		elif(self.username == receiver):
			msg = 'tidak dapat mengirim pesan kediri sendiri'
			self.printMessage(msg)
		else:
			online[receiver].send('[ #%s ] : %s' % (self.username,msg))			
			self.printMessage('[ #you - %s ] : %s' % (receiver, msg))

	def help(self):
		fitur = '1. sendto@pengguna_aktif [ jika nama pengguna_aktif dipisahkan spasi, gunakan "pengguna_aktif" ]\n'
		fitur += '2. sendall@ [ mengirim ke semua pengguna_aktif ]\n'
		fitur += '3. list@ [ melihat daftar pengguna_aktif ]\n'
		fitur += '4. help@ [ melihat daftar fitur yang ada ]'
		self.printMessage('Daftar perintah : \n %s' % (fitur))

	def list(self, online):
		listOnline = online.keys()
		num = 1
		msg = 'Daftar pengguna yang sedang online :\n'
		for user in listOnline:
			msg += '%s. %s\n' % (num, user)
			num+=1
		self.conn.send('%s' % msg)


	def run(self):
		global client
		global pesan
		global accounts
		self.login()
		# self.conn.send('Welcome, enjoy your chat')
		msg = 'Selamat datang (:\n'
		self.printMessage(msg)
		# print 'Selamat datang, selamat menikmati percakapan anda (:'

		while 1:
			# print 'masuk while 1 run'
			try:
				# print 'masuk try'+self.username
				# self.conn.settimeout(TIMEOUT)
				readInput = self.conn.recv(BUF_SIZE).strip()
				# print 'dapet readInput'
				logging.info('%s: %s' % (self.username, readInput))				
				self.controller(readInput)
			except Exception, e:
				pass



def main():
	global client
	global pesan
	global accounts
	global online

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

	client = set()
	pesan = {}
	accounts = {}
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
			# print 'Leave'
			sys.exit()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Quited'