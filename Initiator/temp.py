from TwitterConnector import TwitterConnector

x = TwitterConnector(1)
(a,b,c) = x.AuthenToken()
print(a)
print(len(a))
print(b)
print(len(b))
print(c)
print(len(c))
