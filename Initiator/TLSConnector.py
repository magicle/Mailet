import binascii

import socket, ssl, pprint
import sys, urllib
import io
import gzip
import select
import time, os
import subprocess
import iv
import binascii
import datetime


# TLSConnector
# TLS level abstraction: enables two parties to compose a single TLS connection
# num:        the number of parallel TLS connections (num-1 will be checked)
# Start:      initiate control channels and num parallel TLS connections
# PickThenReconstruct: pick num-1 to check, and the rest one to complete

class TLSConnector:
  def __init__(self, num):
    self.n = num
    self.category = None

  def SetContent(self, content):
    self.content = content

  def Start(self):
    self.sock_list = list()
    self.tlssock_list = list()
    self.H = list()
    self.pad = list()
    self.key = list()
    self.ivv = list()

    # for tls wrap

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.set_ciphers("AES128-GCM-SHA256")
    context.load_verify_locations("/etc/ssl/certs/VeriSign_Class_3_Public_Primary_Certification_Authority_-_G5.pem");


    # creat multiple tls sockets 
    for i in range(self.n):
      s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock_list.append(s1)
      try:
        s1.connect(('localhost', 2345 + i))



        # signal the Interceptor 
        
        if self.category == "post":
          s1.sendall(b"\x03")
        elif self.category == "retweet":
          s1.sendall(b"\x04")
        else:
          print("error: self.category is not initialized!")

      except (ConnectionRefusedError, ConnectionAbortedError) as e:
        print("error in creating s1 socket")


      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ssl_sock = context.wrap_socket(s)
      ssl_sock.settimeout(30)
      self.tlssock_list.append(ssl_sock)


      try:
        ssl_sock.connect(('localhost', 2345 + i))
      except (ConnectionRefusedError, ConnectionAbortedError) as e:
        print("error in having tls connect!")

      cert = ssl_sock.getpeercert()

      if os.path.isfile("/tmp/PlainMsg"):
        os.remove("/tmp/PlainMsg")

      print("before ssl_sock.sendall()")
      print("environmental variable is:", os.environ['LD_LIBRARY_PATH'])

      ssl_sock.sendall(str.encode(self.content))

      if not os.path.isfile("/tmp/PlainMsg"):
        print("PlainMsg file does not exist, please check environment")

      # read H
      proc = subprocess.Popen(['./H'], stdout=subprocess.PIPE)
      h = proc.stdout.readline()
      self.H.append(h)

      # pad  
      self.pad.append(iv.GCM())

      # iv 
      self.ivv.append( binascii.unhexlify(iv.IV()) )
      # key
      self.key.append(iv.key())

  def PickThenReconstruct(self):
    # receive which value
    self.which = self.sock_list[self.n-1].recv(1024)
    print("which is:", self.which)
    
    # check 
    self.which = int(self.which)
    for i in range(self.n):
      if i != self.which:
        # send key + iv
        self.sock_list[i].sendall(b"\x05" + self.key[i] + self.ivv[i])

    # Reconstruction: H 
    self.sock_list[self.which].sendall(b"\x00" + self.H[self.which]) 
    data = self.sock_list[self.which].recv(1024)
    print("reply to H: ", data)

    # pad 
    self.sock_list[self.which].sendall(b"\x01" + self.pad[self.which])
  
  def ReceiveResponse(self):
    
    # receive 2 messages
    count = 2 
    while True:
      try:
        data = self.tlssock_list[self.which].recv(4096)
        print(data)
        count = count - 1
        print(count)
        if count == 0:
          break
      except socket.timeout:
        print("timeout")
        break
    
    # decode
    data = io.BytesIO(data)
    gzipper = gzip.GzipFile(fileobj=data, mode="rb")
    html = gzipper.read()
    print(html)

