import socket
import sys
import time
import logging

HOST = 'localhost'
PORT = 8018
BUF_SIZE = 1024

class server():
    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        logging.info('Connecting to %s:%s' % (host, port))
        while 1:
            try:
                buf = self.sock.recv(BUF_SIZE)
                sys.stdout.write(buf)
                cmd = raw_input()
                self.sock.send(cmd)
            except:
                self.sock.close()

def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    client = server()

if __name__ == '__main__':
    main()