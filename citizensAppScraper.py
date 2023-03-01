# Citizens Web Scraper
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from sqlalchemy import create_engine

datesList = []
titlesList = []
neighborhoodsList = []
locationsList = []

driver = webdriver.Chrome('/Users\Tommy\Documents\python\chromedriver')
driver.get("https://citizen.com/explore")
driver.minimize_window()
driver.implicitly_wait(2)
dates = driver.find_elements(By.CLASS_NAME, 'date')
titles = driver.find_elements(By.CLASS_NAME, 'title')
neighborhoods = driver.find_elements(By.CLASS_NAME, 'neighborhood')
locations = driver.find_elements(By.CLASS_NAME, 'location')

for i in titles:
    titlesList.append(i.text)
for i in locations:
    locationsList.append(i.text)
for i in neighborhoods:
    neighborhoodsList.append(i.text)
for i in dates:
    today = datetime.today()
    yesterday = str((today-timedelta(days=1)).strftime('%Y-%m-%d'))
    i = i.text
    if 'Yesterday' in i:
        i = i.replace('Yesterday', yesterday)
        datesList.append(i)
    else:
        today = str(today.strftime('%Y-%m-%d'))
        i = today + " " + i
        datesList.append(i)
driver.quit()

#dataframe
d = {'date': datesList, 'title': titlesList,
     'location': locationsList, 'neighborhood': neighborhoodsList}
df = pd.DataFrame(data=d)

#connection to postgresql/uploading scraped data
conn_string = 'postgresql://postgres:453VOgReUyVaX4C6O5nx@containers-us-west-34.railway.app:5767/railway'
db = create_engine(conn_string)
conn = db.connect()
df.to_sql('crimes', con=conn, if_exists='append',index=False)# current issue is database will upload duplicates
conn.close()

print('success')