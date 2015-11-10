## module for two party computation

## server side

import sys

import urllib.request as req
import subprocess
import time
import binascii
import random, string



PathFacet = "../fastgc/"


# index: exclude the header
sindex = {"authorize":977, "cookie_session":344, "cookie_password":900, "Post":691, "Retweet":723}


def Check(keyiv, data):
  print("at Check!")
  print(keyiv)
  print(data)
  print("end")

  cipher = data[13:]
  ciphertext = binascii.hexlify(cipher).decode()
  # decrypt
  key = binascii.hexlify(keyiv[:16]).decode()
  iv = binascii.hexlify(keyiv[16:]).decode() + "00000002"
  print('iv length is:', len(iv))
  
  proc = subprocess.Popen(['./decrypt', ciphertext, iv, key], stdout=subprocess.PIPE)
  print(proc.stdout.readlines())



def toHexString(msg):
  return "".join("{:02x}".format(ord(ch)) for ch in msg)





def AuthSplit(data):
  ind = 1513
  ranwd = randomword(40)
  print("random word is (hex):", binascii.hexlify(ranwd)) 

  res = CipherCombine(data, ranwd, ind)
  
  return res
  


def sxor(s1,s2):    
  # convert strings to a list of character pair tuples
  # go through each tuple, converting them to ASCII code (ord)
  # perform exclusive or on the ASCII code
  # then convert the result back to ASCII (chr)

  # merge the resulting array of characters as a string
  
  return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


# suppose the same length
def bxor(b1, b2):
  res = list()
  for a, b in zip(b1,b2):
    res.append(a^b)
  return bytes(res)
# data: original ciphertext
# passowrd: the password to xor with
# sindex: the index to begin with xor operation

def CipherCombine(data, password, sindex):
  data_len = len(data)
  password_len = len(password)
  
  if(sindex + password_len > data_len):
    print("error: password & data length does not match!")
    print("data length is", len(data))
  
  return data[:sindex] + bxor(password, data[sindex:sindex+password_len]) + data[sindex+password_len:]





# NewMsg = iv + ciphertext (+ tag)
# ciphertext is the new ciphertext

def TagGenerator(H, Pad, NewMsg):
  iv = NewMsg[:8]
  Ciphertext = NewMsg[8:-16]
  
  CipherLen = len(Ciphertext)
  
  aadin = "0000000000000001" + "170303" + "%04x" % CipherLen + "000000"
#  print(binascii.hexlify(bxor(OldMsg, NewMsg)))
#  print (binascii.hexlify(NewMsg))
  
  # feed H and ciphertext addin data into tag generation c program
  # obtain the tag for 2PC

  proc = subprocess.Popen(['./GF', H, aadin, binascii.hexlify(Ciphertext)], stdout=subprocess.PIPE) 
  proc.wait()
  raw = proc.stdout.readline()

  print("pad is: ", Pad)
  print("raw rag is: ", raw)
  
  tag = bxor(binascii.unhexlify(Pad), binascii.unhexlify(raw))
  print("tag is ", tag)
  return tag

def CookieSession(H, Pad, data, Msg, mail):
  print("now at cookie session")

  
  global sindex

  sys.stdout.flush()

  # convert Msg to bytes
  password = binascii.unhexlify(Msg)

  print("password is:", password)
  
  # ciphertext and header
  OldMsg = data[5:]
  header = data[:5]
 
  # combine the two secrets in ciphertext
    # do session
  NewMsg = CipherCombine(OldMsg, password, sindex["cookie_password"] + len(req.pathname2url(mail)))


  
  Tag = TagGenerator(H, Pad, NewMsg)

  res = header + NewMsg[:-16] + Tag

  print("res is: ", res)
  print("data is: ", data)
  
  print(binascii.hexlify(bxor(res, data)))
  return res






def Post(H, Pad, data, Msg, mail, status):
  print("now at Post session")

  
  global sindex

  sys.stdout.flush()

  # convert Msg to bytes
  password = binascii.unhexlify(Msg)

  print("password is:", password)
  
  # ciphertext and header
  OldMsg = data[5:]
  header = data[:5]
 
  # combine the two secrets in ciphertext
    # do session
  NewMsg = CipherCombine(OldMsg, password, sindex[status])


  
  Tag = TagGenerator(H, Pad, NewMsg)

  res = header + NewMsg[:-16] + Tag

  print("res is: ", res)
  print("data is: ", data)
  
  print(binascii.hexlify(bxor(res, data)))
  return res
#  return data












# data, Msg, and H are supposed to be byte object
# data    Initiator traffic
# Pad     final pad for generating tag
# Msg     password to xor
# mail    twitter account







def GCM(H, Pad, data, Msg, mail):

  global sindex

  print("[Two Party]\t2PC Start...")
  sys.stdout.flush()

  # convert Msg to bytes
  password = binascii.unhexlify(Msg)


  
  # ciphertext and header
  OldMsg = data[5:]
  header = data[:5]
 
  # combine the two secrets in ciphertext

  

  NewMsg = CipherCombine(OldMsg, password, sindex["authorize"] + len(mail))
  
  # iv
  iv = NewMsg[:8]
  Ciphertext = NewMsg[8:-16]
  
  CipherLen = len(Ciphertext)
  
  aadin = "0000000000000001" + "170303" + "%04x" % CipherLen + "000000"
#  print(binascii.hexlify(bxor(OldMsg, NewMsg)))
#  print (binascii.hexlify(NewMsg))
  
  # feed H and ciphertext addin data into tag generation c program
  # obtain the tag for 2PC

  proc = subprocess.Popen(['./GF', H, aadin, binascii.hexlify(Ciphertext)], stdout=subprocess.PIPE) 
  proc.wait()
  raw = proc.stdout.readline()

  print("pad is: ", Pad)
  print("raw rag is: ", raw)
  
  tag = bxor(binascii.unhexlify(Pad), binascii.unhexlify(raw))
  print("tag is ", tag)
  # start 2PC conversation with the other

  print("TwoParty_XOR is done!") 

  res = header + iv + Ciphertext + tag
  print("res is: ", res)
  print("data is: ", data)
  
  print(binascii.hexlify(bxor(res, data)))
  return res 

  
#  return data




def TwoParty(data, Msg):

  print("[Two Party]\t2PC Start...")
  sys.stdout.flush()


  global PathFacet
#  Msg = toHexString(password)
  password = Msg.decode('hex')
  ProcFacet = subprocess.Popen(["java", "-cp", PathFacet + "dist/FasterGC.jar:" + PathFacet + "extlibs/jargs.jar:" + PathFacet + "extlibs/commons-io-1.4.jar", "Test.TestMailetServer"], stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
  result = ProcFacet.communicate(input=Msg)

#   # record the fastgc output
#  f = open('fastgc_output', 'a')
#  f.write(result[0])
#  f.close()

  ProcFacet.wait()
  Digest = ExtractDigest(result[0])
  NoDigest = data[:-20]
  PassLen = len(password)
  res = NoDigest[:-PassLen] + sxor(password, NoDigest[-PassLen:]) + Digest

  print("[Two Party]\t2PC End")
  sys.stdout.flush()

  return res


def ExtractDigest(response):
  res = ""
  for item in response.split('\n'):
    if "Final Output" in item:
      digest = item.split(":")[1].lstrip(" ")
  for item in digest.split(" "):
    if len(item) == 8:
      cal = int(item[0])*128 + int(item[1])*64 + int(item[2])*32 + int(item[3])*16 + int(item[4])*8 + int(item[5])*4 + int(item[6])*2 + int(item[7])*1
      res = res + chr(cal)
  return res


def randomword(length):
  ran = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
  return ran.encode()

