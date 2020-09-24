import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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


if __name__ == "__main__":
    print("-----------------start---------------")

    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    path = "driver\\chromedriver.exe"
    print(path)
    driver = Chrome(executable_path=path, chrome_options = options)
    driver.get("https://www.zillow.com/")
    time.sleep(2)
    driver.maximize_window()

    main(driver.page_source, driver)