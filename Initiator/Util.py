import subprocess
import binascii

# decrypt the response traffic for the cookie category
def Decrypt(data):
  iv2 = binascii.hexlify(data[5:13])
  ciphertext = binascii.hexlify(data[13:])
  
  print("begin to decrypt")
  proc = subprocess.Popen(['./decrypt', ciphertext, iv2], stdout=subprocess.PIPE)
  print("end to decrypt")
  line = proc.stdout.readline()
  print('decryption result:', line)
  print(binascii.unhexlify(line.strip()))

  # debug write to file
#  f = open("DebugTool/text", "wb")
#  f.write(line.strip())
#  f.close()

  # end of debug

  # extract auth_token: 617574685f746f6b656e3d
  try:
    in_begin = line.index(b"617574685f746f6b656e3d")
    in_begin = in_begin + 22
    in_end = line[in_begin:].index(b"3b")
    auth = line[in_begin:][:in_end]
    print('extractd auth is:', auth)
  except ValueError:
    print("String not found!")

#    print("auth is (hex): ", auth)
#    print("auth is: ", binascii.unhexlify(auth))
#    print("auth length is: ", len(binascii.unhexlify(auth)))
