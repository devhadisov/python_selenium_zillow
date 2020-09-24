import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import requests
import urllib.request
import json, csv, lxml, time, re
import datetime
import hashlib

from insertdatabase import InsertDB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait(broswer, xpath):

    WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))

def main(htmlstring, driver):
    table_name = "maricopa_30_08_2020"

    header = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
                'cookie' : 'zguid=23|%2410ab80e6-80db-4e0a-9f70-2449ca972d74; _ga=GA1.2.759159145.1599348167; zjs_user_id=null; zjs_anonymous_id=%2210ab80e6-80db-4e0a-9f70-2449ca972d74%22; _gcl_au=1.1.607943717.1599348169; _pxvid=be9ff2f0-efce-11ea-9652-0242ac12000b; __gads=ID=cab593cad6cbce43:T=1599348200:S=ALNI_MaFYrYCZZvPIITKUEoEDXGvXSRYwQ; _gid=GA1.2.1287304564.1599556314; _pin_unauth=dWlkPU9EUXdZamxrTldJdE9ESTBNUzAwWXprMExXSXdNekl0TkdWak0yWTFNVEE1TldJeSZycD1abUZzYzJV; ki_r=; ki_s=; _fbp=fb.1.1599562363584.1440832488; g_state={"i_p":1599570378147,"i_l":1}; ki_t=1599556892885%3B1599556892885%3B1599563330503%3B1%3B19; JSESSIONID=62F47C1DAFBF00B3DB7B301BEA3E6586; zgsession=1|8840c1ee-f8a6-43d7-9a7b-3169df33c987; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_rf=1; _pxff_fp=1; _pxff_bsco=1; _px3=6d722620cec81d0df86c8eff4b631bdd93cef163fb0a14808e80f81013747454:M7trNae6CpAztMArZT97P3Vy9jFLz9FuEZ5p2efYpXeqOJC7Bw+xzsVGxArAYe+PM+vQKNuEI3qytjutx2UEXg==:1000:M1Vo/kdU1lI8Zqky6jJnuwSu45xHxX8ueCLKUiW6KX8rNR+VWAORLQi+1ns4dhilOU7gSCJfJmToj1SeyKN49kHZQZIQ0wSFeFtn+txzkIo/fhFAr2Cq7WvjCVWw7GBx8F3JIjMqHf1BZAAFg0YXqy/IVuCFhvIioSyK35nkm4A=; _gat=1; KruxPixel=true; DoubleClickSession=true; _uetsid=f44fc66ca5c392a6859170ed776b6ae9; _uetvid=dc708dafb2b6d91ab6c6923ac1ae6673; AWSALB=3gLhoP6QCdmf4zskymQ7ej/kbqzRHNkv+QNQMFmS6Y7S9pENaOusdnQVhFHWm1W9z8/1Og/WmO8JK63ys0wmi6ZNwRc4SN8lf4pcoyrm+nj8lLAPLRDIqMaYAEte; AWSALBCORS=3gLhoP6QCdmf4zskymQ7ej/kbqzRHNkv+QNQMFmS6Y7S9pENaOusdnQVhFHWm1W9z8/1Og/WmO8JK63ys0wmi6ZNwRc4SN8lf4pcoyrm+nj8lLAPLRDIqMaYAEte; search=6|1602203173818%7Crb%3DMaricopa%252C-AZ%26rect%3D33.203401%252C-111.882231%252C32.788612%252C-112.512953%26disp%3Dmap%26mdm%3Dauto%26sort%3Ddays%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0932697%09%09%09%09%09%09',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }

    first_url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2285202%22%2C%22mapBounds%22%3A%7B%22west%22%3A-111.90749260076905%2C%22east%22%3A-111.84372039923096%2C%22south%22%3A33.355837968853685%2C%22north%22%3A33.41560852349138%7D%2C%22mapZoom%22%3A14%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A94797%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true"

    default_url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22usersSearchTerm%22%3A%2285202%22%2C%22mapBounds%22%3A{}%7B%22west%22%3A-111.90749260076905%2C%22east%22%3A-111.84372039923096%2C%22south%22%3A33.355837968853685%2C%22north%22%3A33.41560852349138%7D%2C%22mapZoom%22%3A14%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A94797%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true"

    counts = 1

    for page in range(1, 3):
        if page == 1:
            url = first_url
        else:
            url = default_url.format(page)

        response = requests.get(url, headers=header)
        result = response.json()
        properties_infos = result["searchResults"]["listResults"]
        print(len(properties_infos))

        for i in range(0, len(properties_infos)):
            data_base = []
            property_url = properties_infos[i]["detailUrl"]
            status_text = properties_infos[i]["statusText"]
            print(status_text, counts)
            counts += 1
            try:
                street_add = properties_infos[i]["hdpData"]["homeInfo"]["streetAddress"]
            except:
                street_add = ""
            
            try:
                city = properties_infos[i]["hdpData"]["homeInfo"]["city"]
            except:
                city = ""
            
            try:
                state = properties_infos[i]["hdpData"]["homeInfo"]["state"]
            except:
                state = ""
            
            try:
                zipcode = properties_infos[i]["hdpData"]["homeInfo"]["zipcode"]
            except:
                zipcode = ""
        
            property_address = street_add + ", " + city + ", " + state + " " + zipcode
            
            
            try:
                bathrooms = properties_infos[i]["hdpData"]["homeInfo"]["bathrooms"]
            except:
                bathrooms = ""
                
            try:
                bedrooms = properties_infos[i]["hdpData"]["homeInfo"]["bedrooms"]
            except:
                bedrooms = ""
            
            try:
                tax_assessed_value = properties_infos[i]["hdpData"]["homeInfo"]["taxAssessedValue"]
            except:
                tax_assessed_value = ""
                
            try:
                zestimate = properties_infos[i]["hdpData"]["homeInfo"]["zestimate"]
            except:
                zestimate = ""
                
            try:
                rent_zestimate = properties_infos[i]["hdpData"]["homeInfo"]["rentZestimate"]
            except:
                rent_zestimate = ""
                
            try:
                home_type = properties_infos[i]["hdpData"]["homeInfo"]["homeType"]
            except:
                home_type = ""
                
                
            if "by owner" in status_text:
                print("--------------------------------------------------> : ", i + 1)
                


                driver.get(property_url)
                time.sleep(10)
                
                try:
                    wait(driver, "//ul[@class='ds-home-fact-list']")
                except:
                    print("There is no xpath")
               
                # street_add = driver.find_element_by_xpath("//h1[@class='ds-address-container']/span[1]").text
                # property_address = street_add + ", " + city + ", " + state + " " + zipcode

                # phone_number = driver.find_element_by_xpath("//span[@class='listing-field']").text
                phones = re.findall(r'[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}', driver.page_source)
                for phone in range(1, len(phones) + 1):
                    phone_number = phones[phone - 1]
                    
                features_labels = driver.find_elements_by_xpath("//ul[@class='ds-home-fact-list']//span[contains(@class, 'ds-standard-label') and contains(@class, 'ds-home-fact-label')]")
                features_infos = driver.find_elements_by_xpath("//ul[@class='ds-home-fact-list']//span[contains(@class, 'ds-body') and contains(@class, 'ds-home-fact-value')]")
                
                parking = ""
                year_built = ""
                hoa = ""
                heating = ""
                lot = ""
                cooling = ""
                price_sqft = ""
                
                for feature_label, feature_info in zip(features_labels, features_infos):
                    feature_label_txt = feature_label.text
                    
                    if 'Parking' in feature_label_txt:
                        parking = feature_info.text
                    elif 'Year built' in feature_label_txt:
                        year_built = feature_info.text
                    elif 'HOA' in feature_label_txt:
                        hoa = feature_info.text
                    elif 'Heating' in feature_label_txt:
                        heating = feature_info.text
                    elif 'Lot' in feature_label_txt:
                        lot = feature_info.text
                    elif 'Cooling' in feature_label_txt:
                        cooling = feature_info.text
                    elif 'Price/' in feature_label_txt:
                        price_sqft = feature_info.text
                        
                
                    
                print("Property Address--------------------> : ", property_address)
                print("Property Url------------------------> : ", property_url)
                print("Property Status---------------------> : ", status_text)    
                print("Owner Phone Number------------------> : ", phone_number)
                print("BathRooms---------------------------> : ", bathrooms)
                print("BedRooms----------------------------> : ", bedrooms)
                print("Tax Assessed Value------------------> : ", tax_assessed_value)
                print("Zestimate---------------------------> : ", zestimate)
                print("Rent Zestimate----------------------> : ", rent_zestimate)
                print("Home Type---------------------------> : ", home_type)
                print("Parking-----------------------------> : ", parking)
                print("Year Built--------------------------> : ", year_built)
                print("HOA---------------------------------> : ", hoa)
                print("Heating-----------------------------> : ", heating)
                print("Lot---------------------------------> : ", lot)
                print("Cooling-----------------------------> : ", cooling)
                print("Price Sqft--------------------------> : ", price_sqft)
                
               

                string_id = property_address + status_text + phone_number
                m = hashlib.md5()
                m.update(string_id.encode('utf8'))
                identifier = m.hexdigest()
                print("hash-------------------->", identifier)
                create_time = str(datetime.datetime.now())
                update_time = ""

                insertdb = InsertDB()
                data_base.append((property_address, street_add, city, state, zipcode, status_text, phone_number, bathrooms, bedrooms, tax_assessed_value, zestimate, rent_zestimate, home_type, parking, year_built, hoa, heating, lot, cooling, price_sqft, identifier, create_time, update_time))
                insertdb.insert_document(data_base, table_name)




if __name__ == "__main__":
    print("-----------------start---------------")


    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path, chrome_options = options)
    
    driver.get("https://www.zillow.com/")
    time.sleep(2)
    driver.maximize_window()

    main(driver.page_source, driver)