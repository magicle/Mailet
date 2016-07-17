import socket, ssl
import binascii
from TwitterConnector import TwitterConnector
import Constants
import binascii, io, gzip






def AuthLocator():

  # construct ssl connection to twitter
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  context.verify_mode = ssl.CERT_REQUIRED
  context.set_ciphers(Constants.CIPHERSUITE)
  context.load_verify_locations(Constants.VERIFY_LOCATION);

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ssl_sock = context.wrap_socket(s)
  ssl_sock.settimeout(30)

  ssl_sock.connect(('twitter.com', 443))

  
  # construct cookie html
  username = Constants.USERNAME
  passcode = binascii.hexlify(str.encode(Constants.PASSCODE))

  con = TwitterConnector(1)
  con.InitConn('cookie', {'username':username, 'passcode':passcode})

  ssl_sock.sendall(str.encode(con.content))
  data = ssl_sock.recv(4096)

  print("data:", data)
  

  # search the position of auth_token=
  st_pos = data.index(b"auth_token=") + 11
#  print("st_pos:", st_pos)
#  print("check:", data[st_pos:-1])
  
  return st_pos

