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
                'cookie': 'zguid=23|%24c647ce95-c1ba-4830-a11f-024e21f9f719; zgsession=1|e273033d-9837-45de-895b-0c12e61043f8; _ga=GA1.2.2027091911.1596740448; _gid=GA1.2.1061398697.1596740448; zjs_user_id=null; zjs_anonymous_id=%22c647ce95-c1ba-4830-a11f-024e21f9f719%22; _pxvid=240f4e11-d817-11ea-9409-0242ac120006; _gcl_au=1.1.1572168333.1596740452; KruxPixel=true; DoubleClickSession=true; _fbp=fb.1.1596740456988.505859585; KruxAddition=true; JSESSIONID=46321F0234522651168612CF53CE575F; GASession=true; _px3=7c9c3bbdb1cccba06ea6ab129d78b6d3f500098235fd26fb704339742ce07ff3:wRMvBMb2Ra8IRc2kw02lmphtDQowwkmf9pYmJlVPCXfHKxr/c5h6Qdq5MIMFbrdBRy1Lt8jFPoEWYPfz7ved3A==:1000:8DwcUiSHlO0djN8TGqC9AQm0scO/aZ8JkpGBpYb6p3UVhhg28Ay1afkhS5dWTZ/90G2cwFxn51RrzHtOngEr7q2FJ60n9BG6xjqD17uM2EOGERtnPB59pOYwP8BpUCzssOCDU8h7lBwm+ILbcnAq8eQzjOUnk7+uhusnQYleRaw=; _gat=1; AWSALB=LYeLN2HMkMLsqKxrBkhPy/b6nX6uFmRTydryjMxffRGmum4UrNR+BqUyOiLUCudj6D1inpcxxSZ/D/ogJGePcc7rPyXa1dNmma2V4h2pqGcTCinoS6Qb6QQpLSvS; AWSALBCORS=LYeLN2HMkMLsqKxrBkhPy/b6nX6uFmRTydryjMxffRGmum4UrNR+BqUyOiLUCudj6D1inpcxxSZ/D/ogJGePcc7rPyXa1dNmma2V4h2pqGcTCinoS6Qb6QQpLSvS; search=6|1599379164092%7Crb%3D85139%26rect%3D33.255808%252C-111.965809%252C32.681457%252C-112.424256%26disp%3Dmap%26mdm%3Dauto%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%09417443%09%09%09%09%09%09',
                'referer': 'https://www.zillow.com/homes/85139_rb/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            }

    url = "https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2285139%22%2C%22mapBounds%22%3A%7B%22west%22%3A-112.73610916015626%2C%22east%22%3A-111.65395583984376%2C%22south%22%3A32.48735282963523%2C%22north%22%3A33.44823271034255%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A417443%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=true&includeList=false"

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


            with open("Zillow_Maricopan_AZ_85139.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([property_address, status_text, phone_number])

            # return




if __name__ == "__main__":
    print("-----------------start---------------")

    open("Zillow_Maricopan_AZ_85139.csv", "wb").close()
    header = ["Property Address", "Property Status", "Owner Phone Number"]

    with open("Zillow_Maricopan_AZ_85139.csv", "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()
    
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path)
    driver.get("https://www.zillow.com/")
    time.sleep(2)
    driver.maximize_window()

    main(driver.page_source, driver)