import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv  

driver = webdriver.Firefox()
driver.get("https://www.fda.gov.tw/mlms/H0005.aspx") 

select = Select(driver.find_element_by_id('ddlMedifact'))
select.select_by_value('1')
driver.find_element_by_name('btnSearch').click()
source = driver.page_source
soup = BeautifulSoup(source,'lxml')
table = soup.findAll('td')
mylist = []
for tb in table:
    mylist.append(tb.text.replace('\n',''))
del mylist[-1]
 

def write_data_to_csv(mylist):
    mydic = {}
    for idx in range(0,len(mylist)):
        if idx % 6 == 0:
            mydic['num'] = mylist[idx]
            
        if idx % 6 == 1:
            mydic['name'] = mylist[idx]
           
        if idx % 6 == 2:
           
            mydic['address'] = mylist[idx]
        if idx % 6 == 3:
            
            mydic['pNum'] = mylist[idx]
        if idx % 6 == 4:
            mydic['country'] = mylist[idx]
            
        if idx % 6 == 5:
            mydic['id'] = mylist[idx]
            
            with open('kerry.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=['id','num','name','address','pNum','country'])
                writer.writerow(mydic)

def change_page(page):
        page = str(page)
        print('----------',page,'----------')
        select = Select(driver.find_element_by_id('gvDetail_ddlPageJump'))
        select.select_by_value(page)
        source = driver.page_source
        soup = BeautifulSoup(source,'lxml')
        table = soup.findAll('td')
        mylist = []
        for tb in table:
            mylist.append(tb.text.replace('\n',''))
        del mylist[-1]
        return mylist

for page in range(1,1481):
    every_page_info = change_page(page=page)
    write_data_to_csv(every_page_info)
    

write_data_to_csv()
driver.close()


