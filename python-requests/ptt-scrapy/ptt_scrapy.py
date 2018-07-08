from bs4 import BeautifulSoup
import requests

url = 'https://www.ptt.cc/'

def get_articles_content(this_page_article_href):
    for url in this_page_article_href:
        print('------------------------------------')
        print("https://www.ptt.cc" + url )
        r = requests.get("https://www.ptt.cc" + url )
        soup = BeautifulSoup(r.text,"html.parser")
        try:
            author = soup.select('span.article-meta-value')[0].text
            board = soup.select('span.article-meta-value')[1].text
            title = soup.select('span.article-meta-value')[2].text
            time = soup.select('span.article-meta-value')[3].text
            print('作者:', author)
            print(board,' 看版')
            print('標題:', title)
            print('時間:', time)
        except:
            pass
        try:
            # content_1 = soup.select('span.f6').text
            content_2 = soup.select('span.f2')[0].text
            # print(content_1, content_2)
            print(content_2)
        except:
            print('err')

        
def get_all_articles_href(page_url="https://www.ptt.cc/bbs/<board name>/index.html"):
    article_href =[]
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.findAll("div",{"class":"title"})
    for item in results:
        try:
            item_href = item.find("a").attrs["href"]
            article_href.append(item_href)
        # title.append(item.text.split('\n')[1])
        except:
            pass
    # print(article_href)
    return article_href

def main_function(url="https://www.ptt.cc/bbs/<board name>/index.html"):
    # first time requests
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    # get this page all articles url
    this_page_article_href = get_all_articles_href(page_url=url)
    get_articles_content(this_page_article_href=this_page_article_href)
    
    # get next page btn url
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    # change page   
    next_page_url = 'https://www.ptt.cc' + up_page_href
    main_function(url=next_page_url)

main_function()
