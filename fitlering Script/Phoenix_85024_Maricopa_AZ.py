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
    
    pagination = ""
    usersSearchTerm = "85024"
    west = "-112.1006243178711"
    east = "-111.9914476821289"
    south = "33.629352331477186"
    north = "33.660382567016846"
    regionId = "94740"
    regionType = "7"
    mapZoom = "13"
    includeList = "true"

    # https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={%22pagination%22:{},%22usersSearchTerm%22:%2285006%22,%22mapBounds%22:{%22west%22:-112.07973577801513,%22east%22:-112.01665022198486,%22south%22:33.43522122804253,%22north%22:33.494937169247144},%22regionSelection%22:[{%22regionId%22:94722,%22regionType%22:7}],%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22sort%22:{%22value%22:%22globalrelevanceex%22}},%22isListVisible%22:true}&includeMap=false&includeList=true

    default_first_url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{0},"usersSearchTerm":"{1}","mapBounds":{"west":{2},"east":{3},"south":{4},"north":{5}},"regionSelection":[{"regionId":{6},"regionType":{7}}],"isMapVisible":true,"mapZoom":{8},"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":true}&includeMap=false&includeList={9}'


    first_case_url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{' + pagination + '},' + '"usersSearchTerm":"' + usersSearchTerm + '","mapBounds":{"west":' + west + ',"east":' + east + ',"south":' + south + ',"north":' + north + '},"regionSelection":[{"regionId":' + regionId + ',"regionType":' + regionType + '}],"isMapVisible":true,"mapZoom":' + mapZoom + ',"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":true}&includeMap=false&includeList=' + includeList
    

    # first_url = default_first_url.format(pagination, usersSearchTerm, west, east, south, north, regionId, regionType, mapZoom, includeList)
    print(first_case_url)
    # return
    
    default_page_url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":' + pagination + '},' + '"usersSearchTerm":"' + usersSearchTerm + '","mapBounds":{"west":' + west + ',"east":' + east + ',"south":' + south + ',"north":' + north + '},"regionSelection":[{"regionId":' + regionId + ',"regionType":' + regionType + '}],"isMapVisible":true,"mapZoom":' + mapZoom + ',"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":true}&includeMap=false&includeList=' + includeList

    counts = 1

    for page in range(1, 4):

        default_page_url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{"currentPage":' + str(page) + '},' + '"usersSearchTerm":"' + usersSearchTerm + '","mapBounds":{"west":' + west + ',"east":' + east + ',"south":' + south + ',"north":' + north + '},"regionSelection":[{"regionId":' + regionId + ',"regionType":' + regionType + '}],"isMapVisible":true,"mapZoom":' + mapZoom + ',"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":true}&includeMap=false&includeList=' + includeList

        if page == 1:
            url = first_case_url
        else:
            url = default_page_url

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
                


                driver.get(property_url)
                time.sleep(10)

                # street_add = driver.find_element_by_xpath("//h1[@class='ds-address-container']/span[1]").text
                # property_address = street_add + ", " + city + ", " + state + " " + zipcode

                # phone_number = driver.find_element_by_xpath("//span[@class='listing-field']").text
                phones = re.findall(r'[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}', driver.page_source)
                for phone in range(1, len(phones) + 1):
                    phone_number = phones[phone - 1]
                    
                print("Property Address--------------------> : ", property_address)
                print("Property Url------------------------> : ", property_url)
                print("Property Status---------------------> : ", status_text)    
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