from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
import json

baseurl = 'https://warframe.fandom.com'
headers = {"User-Agent": "Mozilla/5.0"}

# Step 1: Get frame links with Selenium (for the dynamic list page)
driver = webdriver.Chrome()
driver.get('https://warframe.fandom.com/wiki/Warframes')
sleep(2)  # wait for JS
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()  # close browser immediately

frameLinks = [
    baseurl + a['href']
    for span in soup.find_all('span', class_='WarframeNavBoxText')
    for a in span.find_all('a', href=True)
]

# Step 2: Visit each Warframe page with requests (static content)
frameList = []
for i, link in enumerate(frameLinks, start=1):
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')

    # More robust name scraping
    name_tag = soup.select_one("aside.pi-layout-default h2") \
            or soup.select_one("aside.pi-layout-default h1") \
            or soup.select_one("aside.pi-layout-default [data-source='Name']") \
            or soup.find("h1")
    name = name_tag.get_text(strip=True) if name_tag else "Unknown"

    # Sex may be missing too, so add fallback
    sex_div = soup.find("div", {"data-source": "Sex"})
    sex = sex_div.div.get_text(strip=True) if sex_div and sex_div.div else "Unknown"

    frameList.append({"Name": name, "Sex": sex})
    print(f"Scraped {i}/{len(frameLinks)}: {name}")

# Step 3: Save to JSON
with open("Warframes.json", "w", encoding="utf-8") as f:
    json.dump(frameList, f, indent=2, ensure_ascii=False)

print("✅ Scraping complete! Data saved to Warframes.json")