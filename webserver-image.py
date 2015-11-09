from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, sep, getcwd

class GetHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
      self.send_response(200)
      self.send_header('Content-type','image/png')
      self.end_headers()      
      if self.path=="/":
	messages="image.png"
      elif self.path=="/gambar2":
	messages="image2.png"
      elif self.path=="gambar3":
	messages="image3.png"
      elif self.path=="gambar4":
	messages="image4.png"
      else:
	messages="not-found.png"
      image = open(curdir+sep+messages)
      print "ini %s+%s+%s=%s" % (curdir, sep, messages, (curdir+sep+messages))
      print "getcwd = %s, curdir = %s" % (getcwd(), curdir)
      self.wfile.write(image.read())
      return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()