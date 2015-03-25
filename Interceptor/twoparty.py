## module for two party computation

## server side

import sys

import urllib
import subprocess
import time

#password = urllib.quote("271412shuai!")

#password = "\x7f\x74\x44\x1e\x47\x79\x7f\x1d\x1e\x2b\x7c\x01\x53\x2c"



#PathFacet = "/home/shuai/Desktop/fastgc/"
PathFacet = "../fastgc/"



def toHexString(msg):
  return "".join("{:02x}".format(ord(ch)) for ch in msg)


def sxor(s1,s2):    
  # convert strings to a list of character pair tuples
  # go through each tuple, converting them to ASCII code (ord)
  # perform exclusive or on the ASCII code
  # then convert the result back to ASCII (chr)

  # merge the resulting array of characters as a string
  return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


def TwoParty(data, Msg):

  print "[Two Party]\t2PC Start..."
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

  print "[Two Party]\t2PC End"
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








