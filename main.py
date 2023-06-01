from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
import os

#change this driver path
DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
category = "figurative"
# creating directories for saving labeled images

columns = ['Title', 'Artist Name', 'Year Created', 'Url', 'Refrence No']
df = pd.DataFrame(columns=columns)

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

url = f"a"
driver.get(url)
time.sleep(2)

def get_urls(url):
    driver.get(url)
    time.sleep(3)
    div_tags = driver.find_elements(By.XPATH, "//div[@class='unsnax snax-collection-item']")
    a_tags = {}
    for div in div_tags:
        h3_tags = div.find_elements(By.TAG_NAME,"h3")
        for h3 in h3_tags:
            cc = h3.get_attribute("class")
            if(cc == "product-title"):
                a_tag = h3.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
        image = div.find_element(By.TAG_NAME,"img")
        refrence_no = image.get_attribute("data-wood-src")
        a_tags[refrence_no] = href
    return a_tags

def get_data(a_tags):
    i = 0
    for refrence in a_tags.keys():
        print(i)
        title = "None"
        artist = "None"
        year_created = "None"
        refrence_no = refrence+".jpg"
        a_tag = a_tags[refrence]
        driver.get(a_tag)
        time.sleep(2)
        aside_tag = driver.find_element(By.TAG_NAME, "aside")
        h1 = aside_tag.find_element(By.TAG_NAME, "h1")
        div_tags = aside_tag.find_elements(By.TAG_NAME, "div")
        download_buttons = []
        for div in div_tags:
            cc = div.get_attribute("class")
            if(cc == "tartist"):
                artist = div.text
                pass
            if(cc == "ml-3 dlnk prem"):
                download_buttons.append(div)
        download_buttons[0].click()
        # shifting
        time.sleep(1)
            
        title = h1.text
        bracketed_list = re.findall(r'\([^()]+\)', title)
        if(len(bracketed_list) != 0):
            year_list = re.findall(r'\b\d{4}\b', bracketed_list[-1])
            if(year_list != 0):
                year_created = bracketed_list[-1]
                year_created = year_created.replace("(","")
                year_created = year_created.replace(")","")
        print("Title: ",title)
        print("Artist: ",artist)
        print("Year Created: ",year_created)
        print("Refrence: ",refrence_no)
        print("")
        data = [title,artist,year_created,a_tag,refrence_no]
        df.loc[len(df)] = data
        i = i + 1
    pass

def save_data():
    with open(f"{category}.csv", mode='a', newline='') as file:
        df.to_csv(file, header=file.tell()==0, index=False)

page = 111 
while(page <= 125):
    print("page: ",page)
    print("")
    a_tags = get_urls(f"https://artvee.com/c/{category}/page/{page}/?per_page=70")
    print("Total links: ",len(a_tags))
    get_data(a_tags)
    page = page + 1

driver.quit()
save_data()