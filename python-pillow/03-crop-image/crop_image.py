from PIL import Image
myImg = Image.open("./myimage.png")
print(myImg.size)
croppedImg = myImg.crop((200,250,300,350)) #x1,y1,x2,y2
print(croppedImg.size)
croppedImg.save('cropped.png')
print('save!')
