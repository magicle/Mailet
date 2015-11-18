#!/usr/bin/python
# This is a simple port-forward / pcomputatioiroxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys, os
import ssl, random
import datetime
from StateMachine import StateMachine
import Constants


sys.path.append(os.getcwd() + "/CredentialHandler/")
from CookieManager import CookieManager

# for cookie splitting
# arg[1]      HalfCredential
# arg[2]      username

# for post and retweeting 
# arg[1]      halfcookie
# arg[2]      username

buffer_size = 4096
delay = 0.0001
forward_to = ('api.twitter.com', 443)


#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="./cert.pem", keyfile="./key.pem")


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except ssl.SSLError:
            return False

class TheServer:
    input_list = []
    channel = {}

    client_list = []
    client_state = {}
    client_data = []
    state_machine = {}
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)
        self.n = Constants.SOCKET_PARALELL_NUM 
        self.which = random.randint(0, self.n-1)

    def main_loop(self):
        self.input_list.append(self.server)
        flag = 1
        while flag:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break
#                print("from: ", self.s.getpeername())
                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    flag = 0
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        global context
        forward = Forward().start(forward_to[0], forward_to[1])
        newsocket, clientaddr = self.server.accept()
        clientsock = context.wrap_socket(newsocket, server_side=True)

        if forward:
#            print("[Proxy]\t\t", clientaddr, "connected")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
            self.client_list.append(clientsock)
            self.state_machine[clientsock] = StateMachine(sys.argv[1], sys.argv[2])
        else:
            print("Can't establish connection with remote server.")
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):
#        print('[Proxy]\t\t', self.s.getpeername(), "disconnected")
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
#        print("data is: ", data)
        # here we can parse and/or modify the data before send forward

        if self.s not in self.client_list:
          
        # socket is from the server
          st_machine =  self.state_machine[self.channel[self.s]]
          if st_machine.GetState() == "cookie_1":
            (data, randcode) = st_machine.Run(data, "server")
              # store the cookie split
            cook = CookieManager("./cookie/")
            cook.Write(sys.argv[2], randcode.decode('utf-8'))
          else:
            data = st_machine.Run(data, "server")
          if data != None:
            self.channel[self.s].send(data)
        
        else:
          # socket is from a client
          data = self.state_machine[self.s].Run(data, "client")
          if data != None and 'reply' in data:
            self.s.send(data['reply'])
          elif data != None and 'forward' in data:
            self.channel[self.s].send(data['forward'])

          else:
            # whether send which parameter
            flag = 1
            for eachsock in self.state_machine:
              if self.state_machine[eachsock].IsReadyPick() == False:
                flag = 0
            if flag == 1:
              self.s.send(b"\x00" + str(self.which).encode())
          
if __name__ == '__main__':
        server = TheServer('', 9090)
        try:
            server.main_loop()
            sys.exit(1)
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
