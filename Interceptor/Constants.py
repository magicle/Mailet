# constants used in Mailet





# SOCKET
# PICK-THEN-CHECK MECHANISM: EACH PORT IS A CONNECTION
SOCKET_PARALELL_NUM = 1 

# CONTROL CHANNEL CODES
CONTROL_CODE = {
    # CODE NAME               CODE NUMBER
    'post':                   b"\x03",
    'post_int':               3,
    'retweet':                b"\x04",
    'retweet_int':            4,
    'check':                  b"\x05",    
    'check_int':              5,    
    'H':                      b"\x00",
    'H_int':                  0,
    'pad':                    b"\x01",
    'pad_int':                1,
    
    }
