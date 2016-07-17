# constants used in Mailet

# CRYPTO
CIPHERSUITE = "AES128-GCM-SHA256"
#VERIFY_LOCATION = "/etc/ssl/certs/VeriSign_Class_3_Public_Primary_Certification_Authority_-_G5.pem"

VERIFY_LOCATION = "/etc/ssl/certs/DigiCert_High_Assurance_EV_Root_CA.pem"


# OPENSSL
# OPENSSL_DUMP_FILE CAPTURES SSL PARAMETERS
OPENSSL_DUMP_FILE = "/tmp/PlainMsg"


# SOCKET
# PICK-THEN-CHECK MECHANISM: EACH PORT IS A CONNECTION
SOCKET_PORT_START = 2345
SOCKET_TIMEOUT = 30


# CONTROL CHANNEL CODES
CONTROL_CODE = {
    # CODE NAME               CODE NUMBER
    'post':                   b"\x03",
    'retweet':                b"\x04",
    'check':                  b"\x05",    
    'H':                      b"\x00",
    'pad':                    b"\x01",
    'cookie':                 b"\x02",
    'auth_pos':               b"\x06",
    
    }


#USERNAME = "skymomo10@163.com"
#PASSCODE = "facetfacet"

USERNAME = "shuaileemail@gmail.com"
PASSCODE = "271412shuai!"
