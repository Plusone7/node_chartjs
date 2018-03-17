# python3 lucky.py "whatwever you want to search"
import requests,sys,webbrowser,bs4
#TODO: open a borwser tab for each result
print('google.....') 
res = requests.get('https://www.google.com/search?q='+' '.join(sys.argv[1:]))
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text,"html5lib")
linkElems = soup.select('.r a') # <h3 class="r">  <a> elments

openNum = min(5,len(linkElems)) #open number 5
for i in range(openNum):
    webbrowser.open('http://google.com'+linkElems[i].get('href'))
