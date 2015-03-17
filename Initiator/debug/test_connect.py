import socket, ssl, pprint
import sys, urllib
import io 
import gzip
import select
import time, os





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_REQUIRED

context.set_ciphers("RC4-SHA")


context.load_verify_locations("/etc/ssl/certs/VeriSign_Class_3_Public_Primary_Certification_Authority_-_G5.pem");
ssl_sock = context.wrap_socket(s)

# None  = blocking
# 0     = non-blocking
# n     = internally non-blocking
ssl_sock.settimeout(30)

## require a certificate from the server
#ssl_sock = ssl.wrap_socket(s, ca_certs="/etc/ssl/certs/VeriSign_Class_3_Public_Primary_Certification_Authority_-_G5.pem", cert_reqs=ssl.CERT_REQUIRED)

# try until suceeding

ssl_sock.connect(('twitter.com', 443))


cert = ssl_sock.getpeercert()
#pprint.pprint(ssl_sock.getpeercert())
# note that closing the SSLSocket will also close the underlying socket
#ssl.match_hostname(cert, 'api.twitter.com')




#data = ssl_sock.recv(4096)

