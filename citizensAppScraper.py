# Citizens Web Scraper
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Chrome('/Users\Tommy\Documents\python\chromedriver')
driver.get("https://citizen.com/explore")
driver.implicitly_wait(5)

dates = driver.find_elements(By.CLASS_NAME, 'date')
titles = driver.find_elements(By.CLASS_NAME, 'title')
neighborhoods = driver.find_elements(By.CLASS_NAME, 'neighborhood')
locations = driver.find_elements(By.CLASS_NAME, 'location')
datesList = []
titlesList = []
neighborhoodsList = []
locationsList = []
for i in titles:
    titlesList.append(i.text)
for i in locations:
    locationsList.append(i.text)
for i in dates:
    datesList.append(i.text)
for i in neighborhoods:
    neighborhoodsList.append(i.text)


x = 0
while x < len(titlesList):
    print(titlesList[x])
    print(neighborhoodsList[x])
    print(locationsList[x])
    print(datesList[x])
    print('')
    x += 1
