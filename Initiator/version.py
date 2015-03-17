try:
  import ssl
except ImportError:
  print("no ssl module")
else:
  print(ssl.OPENSSL_VERSION)
