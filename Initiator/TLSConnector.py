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

import Constants, Util
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


  def LocalProxies(self, number):
    os.environ['LD_LIBRARY_PATH'] = ""
    for i in range(number):
      port = Constants.SOCKET_PORT_START + i
      proc = subprocess.Popen(['python3.4', 'localproxy.py', str(port)])


  def Start(self):
    # start local proxy
    self.LocalProxies(self.n)
    time.sleep(1)
    print('localproxies finished')

    self.sock_list = list()
    self.tlssock_list = list()
    self.H = list()
    self.pad = list()
    self.key = list()
    self.ivv = list()

    # for tls wrap

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.set_ciphers(Constants.CIPHERSUITE)
    context.load_verify_locations(Constants.VERIFY_LOCATION);


    # creat multiple tls sockets 
    for i in range(self.n):
      s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock_list.append(s1)
      try:
        s1.connect(('localhost', Constants.SOCKET_PORT_START + i))

        # set remote machine state: signal the Interceptor 
        if self.category not in Constants.CONTROL_CODE:
          print("error in TLSConnector: invalid Control Code!")
#          s1.sendall(b"\x03")
        s1.sendall(Constants.CONTROL_CODE[self.category])

      except (ConnectionRefusedError, ConnectionAbortedError) as e:
        print("error in TLSConnector: failed in creating s1 socket")


      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ssl_sock = context.wrap_socket(s)
      ssl_sock.settimeout(30)
      self.tlssock_list.append(ssl_sock)


      try:
        ssl_sock.connect(('localhost', Constants.SOCKET_PORT_START + i))
      except (ConnectionRefusedError, ConnectionAbortedError) as e:
        print("error in TLSConnector: failed in creating tls connect!")

      cert = ssl_sock.getpeercert()

      if os.path.isfile(Constants.OPENSSL_DUMP_FILE):
        os.remove(Constants.OPENSSL_DUMP_FILE)

      print("before ssl_sock.sendall()")
      print("environmental variable is:", os.environ['LD_LIBRARY_PATH'])

      ssl_sock.sendall(str.encode(self.content))

      if not os.path.isfile(Constants.OPENSSL_DUMP_FILE):
        print("error in TLSConnector: PlainMsg file does not exist, please check environment")

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
        self.sock_list[i].sendall(Constants.CONTROL_CODE['check'] + self.key[i] + self.ivv[i])

    # Reconstruction: H 
    self.sock_list[self.which].sendall(Constants.CONTROL_CODE['H'] + self.H[self.which]) 
    data = self.sock_list[self.which].recv(1024)
    print("reply to H: ", data)

    # pad 
    self.sock_list[self.which].sendall(Constants.CONTROL_CODE['pad'] + self.pad[self.which])
  
  def ReceiveResponse(self):
    
    if self.category != 'cookie':
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
      print("htmlthis", html)
      
      # check output
      if b"error" in html:
        return None
      else:
        return 1


    else:
      # for cookie category, should receive from the control channel
      try:
        data = self.sock_list[self.which].recv(4096)
        print("received original traffic:", data)
      except socket.timeout:
        print("timeout")

      # decrypt the traffic and extract auth_token
      (auth_token, twid) = Util.Decrypt(data)
      print("auth_token:", auth_token)
      print("twid:", twid)
      return (auth_token, twid)
