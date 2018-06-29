from bs4 import BeautifulSoup
import requests
import json
def get_all_product_href(paserUrl):
    href_list =[]
    href_list_sorted = []
    url = paserUrl
    for page in range(1, int(pagesNumbers) + 1):
        print("paser : " + paserUrl )
        response = requests.request("GET", paserUrl, headers=headers, params=params)
        soup = BeautifulSoup(response.text,"html.parser")
        results = soup.findAll("div",{"class":"image"})
        paserUrl = url + "?start=" + str(48 * page)
        for item in results:
            item_href = item.find("a").attrs["href"] 
            href_list.append(item_href)
        # href_list ＝sorted(set(href_list),key=l1.index)
    [href_list_sorted.append(p) for p in href_list if not p in href_list_sorted]
    del href_list
    return href_list_sorted

def paser_products(productHrefList):
    bullets = []
    product_number = 1
    for productHref in productHrefList:
        # prodocutLink = adidasusUrl + productHref
        # print(productHref.split('/',3))
        productId = productHref.split('/',3)[3].replace('.html','')
        # print(productId)
        prodocutLink =  apiUrl + productId
        response = requests.request("GET", prodocutLink , headers=headers, params='?sitePath=us&region=null')
        # print(response)
        # soup = BeautifulSoup(response.text,"html.parser")
        json_data = json.loads(response.text)
        try:
            print('-------------------------------------------------------------')
            print("Scraping  No." , product_number , " product")
            print("Product ID      :" ,json_data["id"])
            print("Product Name    :" ,json_data["name"])
            print("Image Url       :", json_data["view_list"][0]["image_url"] )
            print("Standard_price  :", json_data["pricing_information"]["standard_price"])
            print("CurrentPrice    :", json_data["pricing_information"]["currentPrice"])
            print("Standard_price_no_vat: ", json_data["pricing_information"]["standard_price_no_vat"])
            print("Title           :", json_data["product_description"]["title"])
            try:
                print("Subtitle        :", json_data["product_description"]["subtitle"])
            except:
                print("Subtitle        : NaN" )
            print("Text            :", json_data["product_description"]["text"])
            print("Category        :", json_data["attribute_list"]["category"])
            print("Color           :", json_data["attribute_list"]["color"])
            print("Gender          :", json_data["attribute_list"]["gender"])
            print("Product Type    :", json_data["attribute_list"]["productType"][0])
            # print("body: ", json_data["callouts"]["callout_bottom_stack"]["body"])
        except:
            print(prodocutLink)
            print(err)
        product_number += 1
 
if __name__ == "__main__":
    apiUrl = 'https://www.adidas.com/api/products/'
    paserUrl = "https://www.adidas.com/us/men-new_arrivals"
    params = {"start": 0}
    adidasusUrl = "https://www.adidas.com"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "55359d59-a093-28b7-fbff-4d8848d99e86",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }
    response = requests.request("GET", paserUrl, headers=headers, params=params)
    soup = BeautifulSoup(response.text,"html.parser")
    results = soup.findAll("div",{"class":"image"})
    pagesNumbers = soup.find("li",{"class":"paging-total"}).text.split()[1]
    # print(pagesNumbers)
    productHrefs =  get_all_product_href(paserUrl = paserUrl)
    paser_products(productHrefList = productHrefs ) 