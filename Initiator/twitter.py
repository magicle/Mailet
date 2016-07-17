import Constants
import socket, ssl


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.set_ciphers(Constants.CIPHERSUITE)
context.load_verify_locations(Constants.VERIFY_LOCATION);

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = context.wrap_socket(s)
ssl_sock.settimeout(30)

ssl_sock.connect(('twitter.com', 443))



header1 = "GET / HTTP/1.1\r\n"
header2 = "Host: twitter.com\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nAccept: text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"


cookie = "cookie:guest_id=v1%3A145862309065992410; _ga=GA1.2.182479840.1459617903; _gat=1; kdt=thfM79S8ZxlKZOGArEYC27QLPzi4ODiEE8qyL3vR; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCAg8CfFVAToMY3NyZl9p%250AZCIlNGU3YTUzODA4ZDAwOTMzM2FiNzQzMGQwNjY4MGEwMDE6B2lkIiU2NGRm%250AZjUzNmNiN2I0YzdjOWM2M2IyY2FmYWYxYTJiZDoJdXNlcmwrB0mRi7Q%253D--a614a0e78cf4e38aa7fb5f36b67c826f32392ef4; remember_checked_on=0; twid=\"u=3029045577\"; auth_token=777bef7044538ca2ec2869d48ae75c0d9f6b2dd3\r\nreferer:https://twitter.com/\r\nupgrade-insecure-requests:1\r\n"


result = header1 + header2 + cookie

ssl_sock.sendall(result.encode("utf-8"))
response = ssl_sock.recv(4096)
print("response:", response)
