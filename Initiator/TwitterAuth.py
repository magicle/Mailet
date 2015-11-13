import httplib2
   
h = httplib2.Http(".cache")
r, content = h.request('https://twitter.com/intent/tweet', "GET")
print("r:", r) 
print("content:", content) 
# extract session id and guest id

if "set-cookie" in r:
  for each_field in r["set-cookie"].split(";"):
    # session id
    if "_twitter_sess" in each_field:
      sess = each_field.split("=")[1]
    if "guest_id" in each_field:
      guest_id = each_field.split("guest_id=")[1]

# extract authen token
for item in content.split(b'\n'):
  if b"authenticity_token" in item and b"value=" in item:
    authen = item.split(b"value=")[1].strip(b" ;\"\n>")

print sess, "\n", guest_id, "\n", authen

