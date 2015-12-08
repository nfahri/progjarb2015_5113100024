from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urllib2
import time

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message =  threading.currentThread().getName()
        print message
        self.wfile.write(message)
        self.wfile.write('\n')
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    servers = {}
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    server2 = ThreadedHTTPServer(('localhost', 8000), Handler)
    for n in range(5):
      for i in range(5):
	  servers[i] = threading.Thread(target=server.serve_forever)
	  servers[i].daemon = True
	  servers[i].start()
	  request = urllib2.Request('http://localhost:8080')
	  response = urllib2.urlopen(request)
      time.sleep(1)
    print 'Starting server, use <Ctrl-C> to stop'
	
    server.shutdown()
    server.server_close()