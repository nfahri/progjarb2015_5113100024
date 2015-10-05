#WhattsUp Server
#

# Yet another simple socket multi-user chating program

# Please use `telnet IP PORT` to log in
#

# @author:   Xin Wang <sutarshow#gmail.com>

# @version:  1.0

# @since:    16-09-2013
#

import socket
import threading
import time
import logging

HOST = ''
PORT = 8018
TIMEOUT = 5
BUF_SIZE = 1024

class WhatsUpServer(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.ip = self.addr[0]
        self.name = ''

    def print_indicator(self, prompt):
        self.conn.send('%s\n>> ' % (prompt,))

    def login(self):
        global clients
        global messages
        global accounts

        logging.info('Koneksi dari : %s:%s' %
                     (self.addr[0], self.addr[1]))
        clients.add((self.conn, self.addr))
        msg = '\n--- Tekan `#q` untuk keluar\n'

        # new user
        print accounts
        if self.ip not in accounts:
            msg += '--- Masukkan username anda :'
            self.print_indicator(msg)
            accounts[self.ip] = {
                'name': '',
                'pass': '',
                'lastlogin': time.ctime()
            }
            while 1:
                name = self.conn.recv(BUF_SIZE).strip()
                if name in messages:
                    self.print_indicator(
                        '--- Username telah digunakan')
                else:
                    break
            accounts[self.ip]['name'] = name
            self.name = name
            logging.info('%s login sebagai %s' % (self.addr[0], self.name))
            messages[name] = []
            self.print_indicator(
                '--- %s, silakan masukkan password anda' % (self.name,))
            password = self.conn.recv(BUF_SIZE)
            accounts[self.ip]['pass'] = password.strip()
            self.print_indicator('--- Selamat datang')
        else:
            self.name = accounts[self.ip]['name']
            msg += '--- %s, silakan masukkan password anda' % (self.name,)
            # print accounts
            self.print_indicator(msg)
            while 1:
                password = self.conn.recv(BUF_SIZE).strip()
                if password != accounts[self.ip]['pass']:
                    self.print_indicator(
                        '--- Password yang anda masukkan tidak salah')
                else:
                    self.print_indicator(
                        '--- Selamat datang, terakhir login : %s' %
                        (accounts[self.ip]['lastlogin'],))
                    accounts[self.ip]['lastlogin'] = time.ctime()
                    break

    def logoff(self):
        global clients
        self.conn.send('## Selamat tingggal.!\n')
        self.conn.close()
        exit()

    def run(self):
        global messages
        global accounts
        global clients
        self.login()

def main():
    global clients
    global messages
    global accounts

    # initialize global vars
    clients = set()
    messages = {}
    accounts = {}

    # set up socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)

    while 1:
        try:
            conn, addr = sock.accept()
            server = WhatsUpServer(conn, addr)
            server.start()
        except Exception, error:
            print error

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Quited'
