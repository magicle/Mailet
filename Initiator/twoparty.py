## module for two party computation
 
## Client side



import sys
import subprocess
import TwitterAuth
import time

PathFacet = "/home/shuai/Desktop/fastgc/"
#PathFacet = "/home/shuai/tem/fastgc/"
ConType = "17"
#Version = "0303"
Version = "0301"
SeqNum = "0000000000000001"






def TwoParty(MsgHex):
  print "[Two Party]\t2PC Start..."

  KeyHex = ExtractKey()
  KeyHex = KeyPadding(KeyHex)
  ConstHex = ExtractConst(MsgHex)
  PadHex = ExtractPad()
  
  
  ProcFacet = subprocess.Popen(["java", '-cp', PathFacet + "dist/FasterGC.jar:" + PathFacet + "extlibs/jargs.jar:" + PathFacet + "extlibs/commons-io-1.4.jar", "Test.TestMailetClient", "--server", "localhost"], stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)
  out = ProcFacet.communicate(input=KeyHex + "\n" + MsgHex + PadHex + "\n" + ConstHex)

##  check the fastgc output 
#  f = open('fastgc_output', 'w')
#  f.write(out[0])
#  f.close()

  ProcFacet.wait()
  print "[Two Party]\t2PC End"


def KeyPadding(Key):
  KeyLen = len(Key)
  PadLen = 128 - KeyLen
  for i in range(0, PadLen):
    Key = Key + "0"
  return Key

def ExtractKey():
  proc = subprocess.Popen(['./KeyPad'], stdout=subprocess.PIPE)
  for item in proc.stdout.readlines():
    if "MacKey" in item:
      return item.split(":")[1].strip("\n")

def ExtractPad():
  proc = subprocess.Popen(['./KeyPad'], stdout=subprocess.PIPE)
  for item in proc.stdout.readlines():
    if "EncryptPad" in item:
      WholePad = item.split(":")[1].strip("\n")
  plain = ExtractPlain()
  bindex = len(plain) - 40
  eindex = len(plain)
  return WholePad[bindex:eindex]

def ExtractPlain():
  f = open("PlainMsg", "r")
  response = f.readlines()
  plain = TwitterAuth.ExtractPlainText(response)
  return plain


def ExtractConst(MsgHex):
  plain = ExtractPlain()
  Last = -(40 + len(MsgHex))
  return SeqNum + ConType + Version + "%0.4X" % (len(plain)/2-20) + plain[:Last]
