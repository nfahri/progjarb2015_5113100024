import socket

HOST, PORT='', 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.bind((HOST, PORT))
client.listen(1)
print 'Host %s Port %s . . .' % (HOST,PORT)
while True:
  clientConnection, clientAddress=client.accept()
  request = clientConnection.recv(1024)
  print request
  http_body = "<html><title>Naufal Fakhri</title><body><h1>test2</h1></body></html>"
  http_response = """\
HTTP/1.1 200 OK
Content-type:text/html;charset=utf8

%s
""" % http_body
  clientConnection.sendall(http_response)
  clientConnection.close()