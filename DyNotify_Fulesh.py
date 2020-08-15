from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time
from tqdm import tqdm

browser = webdriver.Chrome('/Users/fuleshkumardahiya/Downloads/chromedriver')
browser.get('https://www.amazon.com')

srch = input()
xpath_search = '//*[@id="twotabsearchtextbox"]'
search = browser.find_element_by_xpath(xpath_search)
search.clear()
search.send_keys(srch)
time.sleep(4)
search_click = browser.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
search_click.click()

product_list = browser.find_elements_by_class_name('s-result-item')

link_list = []
flag = True
while(flag):
    product_list = browser.find_elements_by_class_name('s-result-item')
    i=0
    for product in product_list:
        try:
            link_list.append(product.find_element_by_tag_name('h2').find_element_by_tag_name('a').get_property('href'))
            #print(i)
        except:
            pass
        i=i+1
        
    try:
        pg = browser.find_element_by_class_name("a-pagination")
        ls_pg = pg.find_elements_by_tag_name('li')
        url_next = ls_pg[-1].find_element_by_tag_name('a').get_property('href')
        browser.get(url_next)
        #print("in try")
    except:
        #print("in except")
        flag = False
        
#print(len(link_list))       
        
details = []
for link in tqdm(link_list):
    try:
        browser.get(link)
        try:
            ttl = browser.find_element_by_id('productTitle').text
        except:
            ttl = ''
        try:
            rating = browser.find_elements_by_id('acrCustomerReviewText')[1].text
        except:
            rating = ''
        #rivew = browser.find_elements_by_id('acrCustomerReviewText')[1].click()
        try:
            star = browser.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text
        except:
            star = ""
        try:
            try:
                price = browser.find_element_by_id('priceblock_ourprice').text
            except:
                price = browser.find_element_by_id('priceblock_saleprice').text
        except:
            price = ''
        
            
        temp = {'Title': ttl, 
                'Star':  star,
                'Rating': rating,
                'Price': price,
                'URL': link}
        #json_object = json.dumps(temp, indent = 2)   
        details.append(temp)
    except:
        None
        
        
with open("Output.json", "w") as write_file:
    for dt in details:
        json.dump(dt, write_file)