# Citizens Web Scraper
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from secretsKey import sqlURL
import time
import schedule


def webScrape():
    datesList = []
    titlesList = []
    neighborhoodsList = []
    locationsList = []

    driver = webdriver.Chrome()
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
        elif i.startswith('Y') ==False:
            today = str(today.strftime('%Y-%m-%d'))
            i = today + " " + i
            datesList.append(i)
        else:
            pass
    driver.quit()

    #dataframe
    d = {'date': datesList, 'title': titlesList,
        'location': locationsList, 'neighborhood': neighborhoodsList}
    df = pd.DataFrame(data=d)
    print(df)
    #connection to postgresql/uploading scraped data
    conn_string = sqlURL
    db = create_engine(conn_string)
    conn = db.connect()
    df.to_sql('crime', con=conn, if_exists='append',index=False)# current issue is database will upload duplicates
    conn.commit()
    conn.close()
    print('success')

schedule.every(1).minute.do(webScrape)
while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute