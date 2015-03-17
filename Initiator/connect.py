import socket, ssl, pprint
import sys, urllib
import io 
import gzip
import select
import time, os

f = open("temp", "r")

post = f.readline()

f.close()


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

flag = 1
while flag == 1:
  try:
    flag = 0
    ssl_sock.connect(('localhost', 9090))
#    ssl_sock.connect(('enochroot-umh.cs.umn.edu', 1023))
  except (ConnectionRefusedError, ConnectionAbortedError) as e:
    flag = 1
    time.sleep(0.5)
    continue

# connection has been established, signal by deleting temp
os.remove("temp")

cert = ssl_sock.getpeercert()
#pprint.pprint(ssl_sock.getpeercert())
# note that closing the SSLSocket will also close the underlying socket
#ssl.match_hostname(cert, 'api.twitter.com')

header1 = "POST /oauth/authorize HTTP/1.1\r\nHost: api.twitter.com\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"
header2 = "Referer: https://api.twitter.com/oauth/authorize?oauth_token=" + sys.argv[2] + "\r\n"


header3 = "Connection: keep-alive\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"

#print(post)
httpmeg = header1 + header2 + header3 + post






ssl_sock.sendall(str.encode(httpmeg))

#ss = select.select
#inputready, outputready, exceptready = ss([].append(ssl_sock), [],[])
sys.stdout.flush()


# twitter will send 2 packages
count = 2 
while True:
  try:
    data = ssl_sock.recv(4096)
    count = count - 1
    print(count)
    if count == 0:
      break
    
  except socket.timeout:
    print("timeout")
    break



#try:
#  data = ssl_sock.recv(4096)
#except socket.timeout:
#  print("Socket Timeout: Nothing Received") 
#




data = io.BytesIO(data)
gzipper = gzip.GzipFile(fileobj=data, mode="rb")
html = gzipper.read()
print(html)
#pprint.pprint(data.split("\r\n"))
#pprint.pprint(ssl_sock.recv(1024).split(b"\r\n"))
ssl_sock.close()

