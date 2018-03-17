import requests 
from io import BytesIO
from PIL import Image

r = requests.get("image url")
print("status: ",r.status_code)
# print(r.url) # url
image = Image.open(BytesIO(r.content)) #r.content is binary data

print(image.size , image.format , image.mode) 
path = "./image/image." + image.format
try:
    image.save( path, image.format)
except IOError:
    print("can't not save image")
