import requests
r = requests.get("http://google.com")
print("status: ",r.status_code)
# print(r.url) # url
#print(r.text) # get html
f = open("./page/page.html","w+")
f.write(r.text)

