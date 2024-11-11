from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

baseurl = 'https://warframe.fandom.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

#selenium code to perform http requests and access elements that need to wait for javascript scripts to finish running in order to have data.
driver = webdriver.Chrome()
driver.get('https://warframe.fandom.com/wiki/Warframes')
sleep(1)
website = driver.page_source

#use this code to utilize selenium when scrapping a dynamic site that uses javascript to populate its data
# website = requests.get('https://warframe.fandom.com/wiki/Warframes')

#use this code when scrapping a static site that has all its data directly stored in its html document
soup = BeautifulSoup(website, 'lxml')

warframeList = soup.find_all('span', class_='WarframeNavBoxText')

frameLinks = []
frameList = []

i = 0
for warframe in warframeList:
    for link in warframe.find_all('a', href=True):
        frameLinks.append(baseurl + link['href'])
    print(f'working for entry {i}')
    i = i+1

i = 0
for link in frameLinks:
    #use this code to utilize selenium when scrapping a dynamic site that uses javascript to populate its data
    driver.get(link)
    page = driver.page_source
    
    #use this code when scrapping a static site that has all its data directly stored in its html document
    # page = requests.get(link, headers=headers)
    
    soup = BeautifulSoup(page, 'lxml')
    Sex = soup.find('div', {'data-source': 'Sex'}).div.text.strip()
    Name = soup.find('aside', class_='portable-infobox pi-background pi-border-color pi-theme-wikia pi-layout-default').h2.b.text.strip()

    frame = {
        'Name': Name,
        'Sex': Sex
    }   
    
    frameList.append(frame)
    print(f'working for entry {i}')
    i = i+1

print(frameList)

print('')
print('')

import pandas as pd
df = pd.DataFrame.from_dict(frameList)

df.to_csv('Warframes.csv', index=False)

print(df)

driver.close()
