from PIL import Image
myImg = Image.open("./myimage.png")
print(myImg.size) # image size 
print(myImg.filename) # image file name
print(myImg.format) # image format
print(myImg.format_description)
myImg.save('myimage.jpg') # jpg format save