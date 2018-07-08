from bs4 import BeautifulSoup
import requests 
import shutil
url = 'https://www.ptt.cc/'

def get_articles_content(this_page_article_href):
    image_count = 0
    for url in this_page_article_href:
        print('.................................')
        # print("https://www.ptt.cc" + url )
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
        imgs = soup.findAll('a')
        for img in imgs:
            if '.jpg' in img['href']:
                download_img_from_article(img_url=img['href'], img_name = image_count)
                print(img['href'])
                image_count += 1
    
def download_img_from_article(img_url, img_name):
    r = requests.get(img_url, stream=True)
    file_name = str(img_name + 1)
    print( 'save img to  ./image/'+ file_name + '.jpg')
    try:
        with open('./image/' + file_name + '.jpg', 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
    except:
        print('can not save img', img_url)
        
def get_all_articles_href(page_url="https://www.ptt.cc/bbs/TWICE/index.html"):
    article_href =[]
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.findAll("div",{"class":"title"})
    for item in results:
        try:
            item_href = item.find("a").attrs["href"]
            article_href.append(item_href)
        except:
            pass
    # print(article_href)
    return article_href

def main_function(url="https://www.ptt.cc/bbs/TWICE/index.html"):
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