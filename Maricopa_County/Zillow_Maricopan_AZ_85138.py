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


def main(htmlstring, driver):


    header = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }

    url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2285138%22%2C%22mapBounds%22%3A%7B%22west%22%3A-112.20716283007813%2C%22east%22%3A-111.66608616992188%2C%22south%22%3A32.77485850048854%2C%22north%22%3A33.25504954983835%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A417442%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D&includeMap=true&includeList=false"

    # url = "https://www.zillow.com/homes/85138_rb/"

    response = requests.get(url, headers=header)
    result = response.json()
    properties_infos = result["searchResults"]["mapResults"]
    print(len(properties_infos))

    for i in range(0, len(properties_infos)):
        property_url = "https://www.zillow.com/" + properties_infos[i]["detailUrl"]
        status_text = properties_infos[i]["statusText"]
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


            with open("Zillow_Maricopan_AZ_85138.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([property_address, status_text, phone_number])

            # return




if __name__ == "__main__":
    print("-----------------start---------------")

    open("Zillow_Maricopan_AZ_85138.csv", "wb").close()
    header = ["Property Address", "Property Status", "Owner Phone Number"]

    with open("Zillow_Maricopan_AZ_85138.csv", "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()
    
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path)
    driver.get("https://www.zillow.com/")
    time.sleep(2)
    driver.maximize_window()

    main(driver.page_source, driver)