from bs4 import BeautifulSoup
import requests
import json
import time

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
        all_size = []
        productId = productHref.split('/',3)[3].replace('.html','')
        # print(productId)
        prodocutLink =  apiUrl + productId
        response = requests.request("GET", prodocutLink , headers=headers, params='?sitePath=us&region=null')
        product_json_data = json.loads(response.text)
        try:
            product_id = product_json_data["id"]
            model_number = product_json_data["model_number"]
            product_name = product_json_data["name"]
            Standard_price = product_json_data["pricing_information"]["standard_price"]
            current_price = product_json_data["pricing_information"]["currentPrice"]
            standard_price_no_vat = product_json_data["pricing_information"]["standard_price_no_vat"]
            description_title = product_json_data["product_description"]["title"]
            description_usps = product_json_data["product_description"]["usps"]
            # try:
            #     for line in description_usps:
            #         if "%" in line: 
            #             material = line
            #             break
            #         elif "Main materials" in line:
            #             material = line
            #             break
            #         else: 
            #             material += line
            #             break
            # except:
            #     pass
            try:
                description_subtitle = product_json_data["product_description"]["subtitle"]
            except:
                description_subtitle = "NaN"
            description_text = product_json_data["product_description"]["text"]
            product_color = product_json_data["attribute_list"]["color"]
            product_category = product_json_data["attribute_list"]["category"]
            brand =  product_json_data["attribute_list"]["brand"]
            sport =  product_json_data["attribute_list"]["sport"]
            gender = product_json_data["attribute_list"]["gender"] 
            product_type = product_json_data["attribute_list"]["productType"][0]
            image_url = product_json_data["view_list"][0]["image_url"]
        except:
            print("ERROR :::::::::::::::::::::" ,prodocutLink)
        prodocutRateLink =  ratingApi + model_number + '/ratings?sitePath=us&region=null'
        try:
            rate_response = requests.request("GET", prodocutRateLink , headers=headers)
            rate_json_data = json.loads(rate_response.text)
            over_all_rating = rate_json_data["overallRating"]
            recommendation_percentage = rate_json_data["recommendationPercentage"]
            rating_distribution = rate_json_data["ratingDistribution"]
            # review_number = rate_json_data["ratingDistribution"]["rating"]
            # print("rating distribution :", rating_distribution)
            review_count = 0
            for rating in rating_distribution:
                review_count += rating["count"]
        except:
            pass
        
        sizeLink =  apiUrl + productId + '/availability?sitePath=us&region=null'
        size_response = requests.request("GET", sizeLink , headers=headers)
        size_json_data = json.loads(size_response.text)
        size_avail = size_json_data["variation_list"]
        for size in size_avail:
            if size["availability_status"] != 'NOT_AVAILABLE':
                all_size.append(size["size"])
        
        print('------------------------------------------------------------------')
        print("Scraping            No." ,product_number ," product")
        print("* get time              :",time.asctime( time.localtime(time.time())))
        print("* id                    :", product_id)
        print("* model_number          :",model_number)
        print("* product name          :" , product_name)
        print("* standard price        :", Standard_price)
        print("* current price         :", current_price)
        print("* standard price no vat :", standard_price_no_vat)
        print("* material              :", description_usps)
        print("* product color         :", product_color)
        print("* product category      :", product_category)
        print("* product brand         :", brand)
        print("* prodocut Rate Link    :", prodocutRateLink)
        print("* gender                :", gender)
        print("* product type          :", product_type)
        print("* average rating        :", over_all_rating)
        print("* recommendation %      :", recommendation_percentage , "%")
        print("* review number         :", review_count)
        print("* product title         :", description_title)
        print("* product subtitle      :", description_subtitle)
        print("* description text      :", description_text)
        print("* image url             :", image_url)
        print("* all size              :", all_size)
        product_number += 1

if __name__ == "__main__":
    ratingApi = 'https://www.adidas.com/api/models/' #  / ratings?sitePath=us&region=null
    apiUrl = 'https://www.adidas.com/api/products/'  # availibleApi: <model_number> /availability?sitePath=us&region=null
    paserUrl =["https://www.adidas.com/us/women-new_arrivals", "https://www.adidas.com/us/men-new_arrivals"]
    params = {"start": 0}
    adidasusUrl = "https://www.adidas.com"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "55359d59-a093-28b7-fbff-4d8848d99e86",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }
    for url in paserUrl:
        response = requests.request("GET", url, headers=headers, params=params)
        soup = BeautifulSoup(response.text,"html.parser")
        results = soup.findAll("div",{"class":"image"})
        pagesNumbers = soup.find("li",{"class":"paging-total"}).text.split()[1]
        # print(pagesNumbers)
        productHrefs =  get_all_product_href(paserUrl = url)
        paser_products(productHrefList = productHrefs ) 