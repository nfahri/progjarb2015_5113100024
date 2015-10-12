# @credit : xin wang

import socket
import threading
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
        output = threading.Thread(target=self.getOutput)
        output.start()
        while 1:
            try:
                # print ''
                # buf = self.sock.recv(BUF_SIZE)
                # sys.stdout.write(buf)
                cmd = raw_input()
                if(cmd.find('!quit')==0):
                    self.sock.close()
                    sys.exit()
                self.sock.send(cmd)
                # print ''
            except:
                self.sock.close()
    def getOutput(self):
        while 1:
            print ''
            msg = self.sock.recv(BUF_SIZE)
            sys.stdout.write(msg)


def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    client = server()

if __name__ == '__main__':
    main()