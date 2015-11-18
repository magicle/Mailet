import subprocess
import os, sys
sys.path.append(os.getcwd() + "/CredentialHandler/")

from CookieManager import CookieManager

os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'

mmail = "skymomo10@163.com"

cook = CookieManager('./cookie/')
cookie = cook.Read(mmail)

FNULL = open(os.devnull, 'w')
print('cookie:', cookie)
print('mmail:', mmail)
#proc = subprocess.Popen(['python3.4', 'example_post.py', mmail, msg], stdout=FNULL, stderr=FNULL)
proc = subprocess.Popen(['python3.4', 'proxy.py', cookie, mmail])
proc.wait()
print 'return code:', proc.returncode

