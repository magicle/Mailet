import subprocess
import os

os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'

mmail = "facetumn@gmail.com"
msg = "hello20"
FNULL = open(os.devnull, 'w')
#proc = subprocess.Popen(['python3.4', 'example_post.py', mmail, msg], stdout=FNULL, stderr=FNULL)
proc = subprocess.Popen(['python3.4', 'example_post.py', mmail, msg])
proc.wait()
print 'return code:', proc.returncode

