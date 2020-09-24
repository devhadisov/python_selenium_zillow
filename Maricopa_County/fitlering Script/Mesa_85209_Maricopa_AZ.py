import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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


def main(htmlstring, driver):
    table_name = "maricopa"

    header = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
                'referer': 'https://www.zillow.com/homes/85139_rb/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }

    first_url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2285209%22%2C%22mapBounds%22%3A%7B%22west%22%3A-111.70277420153808%2C%22east%22%3A-111.5752297984619%2C%22south%22%3A33.322955502987284%2C%22north%22%3A33.44250069995446%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A94804%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true"

    default_url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{}%7D%2C%22usersSearchTerm%22%3A%2285209%22%2C%22mapBounds%22%3A%7B%22west%22%3A-111.70277420153808%2C%22east%22%3A-111.5752297984619%2C%22south%22%3A33.322955502987284%2C%22north%22%3A33.44250069995446%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A94804%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22mapZoom%22%3A13%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true"

    counts = 1

    for page in range(1, 5):
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
            
            
            if "by owner" in status_text:
                print("--------------------------------------------------> : ", i + 1)
                print("Property Address--------------------> : ", property_address)
                print("Property Url------------------------> : ", property_url)
                print("Property Status---------------------> : ", status_text)


                driver.get(property_url)
                time.sleep(10)

                # phone_number = driver.find_element_by_xpath("//span[@class='listing-field']").text
                phones = re.findall(r'[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}', driver.page_source)
                for phone in range(1, len(phones) + 1):
                    phone_number = phones[phone - 1]
                print("Owner Phone Number------------------> : ", phone_number)


                string_id = property_address + status_text + phone_number
                m = hashlib.md5()
                m.update(string_id.encode('utf8'))
                identifier = m.hexdigest()
                print("hash-------------------->", identifier)
                create_time = str(datetime.datetime.now())
                update_time = ""

                insertdb = InsertDB()
                data_base.append((property_address, street_add, city, state, zipcode, status_text, phone_number, identifier, create_time, update_time))
                insertdb.insert_document(data_base, table_name)

            # return




if __name__ == "__main__":
    print("-----------------start---------------")


    
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path)
    driver.get("https://www.zillow.com/")
    time.sleep(2)
    driver.maximize_window()

    main(driver.page_source, driver)