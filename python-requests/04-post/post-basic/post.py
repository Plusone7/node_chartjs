import requests

mydata = {"name":"plusone","email":"plusone@example.com"}
r = requests.post("https://www.w3schools.com/php/welcome.php",mydata)
f = open("myfile.html","w+")
f.write(r.text)