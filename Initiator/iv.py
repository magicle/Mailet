
import sys
import subprocess
import time
import binascii


def IV():
  f = open('/tmp/PlainMsg', 'r')
  SSLdump = f.readlines()

  for index, each in enumerate(SSLdump):
    if "50 4f 53 54 20 2f" in each:
      iv = SSLdump[index-1]
      return iv.split()[1]

def key():
  f = open('/tmp/key_material', 'br')
  return f.read(16)

def GCM():
  proc = subprocess.Popen(['./Pad', IV() + "00000001"], stdout=subprocess.PIPE)
  Cover = proc.stdout.readline().strip()
  return Cover

