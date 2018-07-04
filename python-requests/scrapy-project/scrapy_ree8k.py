from bs4 import BeautifulSoup
import requests
import json
import time
import csv
def get_all_product_href(paserUrl):
    href_list =[]
    href_list_sorted = []
    url = paserUrl
    for page in range(1, int(pagesNumbers) + 1):
        print("paser : " + paserUrl )
        response = requests.request("GET", paserUrl, headers=headers)
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
    yield_data  = []
    for productHref in productHrefList:
        all_size = []
        # get product ID 
        productId = productHref.split('/',3)[3].replace('.html','')
        # print(productId)
        # call api 'https://www.reebok.com/api/products/' <productID>
        prodocutLink =  apiUrl + productId
        response = requests.request("GET", prodocutLink , headers=headers, params='?sitePath=us&region=null')
        product_json_data = json.loads(response.text)
        # paser Json data
        try:
            product_id = product_json_data["id"]
            model_number = product_json_data["model_number"]
            product_name = product_json_data["name"]
            standard_price = product_json_data["pricing_information"]["standard_price"]
            current_price = product_json_data["pricing_information"]["currentPrice"]
            standard_price_no_vat = product_json_data["pricing_information"]["standard_price_no_vat"]

            description_title = product_json_data["product_description"]["title"]
            description_usps = product_json_data["product_description"]["usps"]
            # sometime you can't get product subtitle so 
            # try:
            #     description_subtitle = product_json_data["product_description"]["subtitle"]
            # except:
            #     description_subtitle = None
            
            description_text = product_json_data["product_description"]["text"]

            product_color = product_json_data["attribute_list"]["color"]
            product_category = product_json_data["attribute_list"]["category"]
            # brand =  product_json_data["attribute_list"]["brand"]
            brand = 'Reebok'
            sport =  product_json_data["attribute_list"]["sport"]
            gender = product_json_data["attribute_list"]["gender"] 
            product_type = product_json_data["attribute_list"]["productType"][0]
            image_url = product_json_data["view_list"][0]["image_url"]
        except:
            print("ERROR :::::::::::::::::::::", prodocutLink)

             # call secound api rating data:https://www.adidas.com/api/models/<model_number>/ratings?sitePath=us&region=null
        prodocutRateLink =  ratingApi + model_number + '/ratings?sitePath=us&region=null'
        print(prodocutLink)
        # paser json data 
        try:
            rate_response = requests.request("GET", prodocutRateLink , headers=headers)
            rate_json_data = json.loads(rate_response.text)
            over_all_rating = rate_json_data["overallRating"]
            recommendation_percentage = rate_json_data["recommendationPercentage"]
            rating_distribution = rate_json_data["ratingDistribution"]
            review_count = 0
            for rating in rating_distribution:
                review_count += rating["count"]
        except:
            pass
        # call finnal api :  <model_number> /availability?sitePath=us&region=null
        sizeLink =  apiUrl + productId + '/availability?sitePath=us&region=null'
        size_response = requests.request("GET", sizeLink , headers=headers)
        size_json_data = json.loads(size_response.text)
        try:
            size_avail = size_json_data["variation_list"]
            for size in size_avail:
                if size["availability_status"] != 'NOT_AVAILABLE':
                    all_size.append(size["size"])
        except:
            size_avail = None

        yield_data.append(product_id)
        yield_data.append(model_number)
        yield_data.append(product_name)
        yield_data.append(standard_price)
        yield_data.append(current_price)
        yield_data.append(standard_price_no_vat)
        yield_data.append(description_usps)
        yield_data.append(product_color)
        yield_data.append(product_category)
        yield_data.append(brand)
        yield_data.append(sport[0])
        yield_data.append(gender)
        yield_data.append(product_type)
        yield_data.append(over_all_rating)
        yield_data.append(recommendation_percentage)
        yield_data.append(review_count)
        yield_data.append(description_title)
        # yield_data.append(description_subtitle)
        yield_data.append(description_text)
        yield_data.append(image_url)
        yield_data.append(all_size)
        yield_data.append(time.asctime(time.localtime(time.time())))
        # print(yield_data)
        write_data_to_csv(yield_data)
        yield_data = []

def write_data_to_csv(yield_data):
    print(yield_data)
    file = open( './reebok_products_data.csv', 'a')
    csvCursor = csv.writer(file)
    logData = [yield_data]
    csvCursor.writerows(logData)
    file.close()


if __name__ == "__main__":
    file = open( './reebok_products_data.csv', 'w')
    csvCursor = csv.writer(file)
    csvHeader = ['id', 'model_number', 'name', 'standard_price', 'current_price'
    , 'standard_price_no_vat', 'material', 'color', 'category', 'brand', 'sport', 'gender'
    , 'type', 'average_rate', 'recommendation_percentage', 'review_count', 'description_title'
    , 'description_text', 'image_url', 'all_size', 'get_data_time']
    csvCursor.writerow(csvHeader)
    file.close()
    paserUrl =["https://www.reebok.com/us/men-apparel-new_arrivals", "https://www.reebok.com/us/women-apparel-new_arrivals"]
    headers = {
        'cache-control': "no-cache",
        'postman-token': "55359d59-a093-28b7-fbff-4d8848d99e86",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }
    apiUrl = 'https://www.reebok.com/api/products/'
    ratingApi = 'https://www.reebok.com/api/models/'
    
    for url in paserUrl:
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text,"html.parser")
        # get product url from img tag
        results = soup.findAll("div",{"class":"image"})
        # get website pages number
        pagesNumbers = soup.find("li",{"class":"paging-total"}).text.split()[1]
        # print(pagesNumbers)
        # print(results)
        productHrefs =  get_all_product_href(paserUrl = url)
        productDatas = paser_products(productHrefList = productHrefs ) 

        
