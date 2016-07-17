import subprocess
import socket, ssl
import binascii
import Constants
import binascii, io, gzip


# decrypt the response traffic for the cookie category
def Decrypt(data):
  iv2 = binascii.hexlify(data[5:13])
  ciphertext = binascii.hexlify(data[13:])
  
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
# old implementation
#    in_begin = line.index(b"617574685f746f6b656e3d")
#    in_begin = in_begin + 22
#    in_end = line[in_begin:].index(b"3b")
#    auth = line[in_begin:][:in_end]
#    print('extractd auth is:', auth)


    in_twid = line.index(b"747769643d")
    in_twid_semi = line[in_twid:].index(b"3b")
    in_begin = in_twid + in_twid_semi + 62*2
    in_end = in_begin + 40*2
    auth = line[in_begin:in_end]
    print('extractd auth is:', auth)
    print('extractd auth is(unhexlify):', binascii.unhexlify(auth))
    pos = str(int(in_begin/2)).encode('utf-8')
    
    # extract twid 
    in_begin = line.index(b"747769643d")
    in_end = line[in_begin:].index(b"3b")
    res = line[in_begin:][:in_end]
    twid = binascii.unhexlify(res).decode('utf-8')

    return (auth, twid, pos)
  except ValueError:
    print("String not found!")

#    print("auth is (hex): ", auth)
#    print("auth is: ", binascii.unhexlify(auth))
#    print("auth length is: ", len(binascii.unhexlify(auth)))







