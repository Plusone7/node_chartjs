from bs4 import BeautifulSoup
import requests

search = input("Search for:")
params = {"q":search}
r = requests.get("http://www.bing.com/search?",params=params)

soup = BeautifulSoup(r.text,"html.parser")

results = soup.find("ol",{"id":"b_results"})
links = results.findAll("li",{"class":"b_algo"})

for item in links:
    item_text = item.find("a").text
    item_href = item.find("a").attrs["href"] 
    if item_href and item_text:
        # print("title: "+ item_text)
        # print("href: "+item_href)
        children = item.find("h2")
        print('next sibling of h2: ',children.next_sibling,'\n')
        
        