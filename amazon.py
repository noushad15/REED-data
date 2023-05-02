from selenium import webdriver
import pandas as pd
from datetime import datetime
today = datetime.today()
import time
import requests
from bs4 import BeautifulSoup

path = "./chromedriver"
driver = webdriver.Chrome(path)

def getData(url):
    global driver
    driver.get(url)

    try:
        title = driver.find_element_by_class_name("DVWebNode-retail-nav-wrapper.DVWebNode.av-native-stick").find_element_by_class_name("av-retail-m-nav-container  ").find_element_by_tag_name("a").text
    except:
        time.sleep(9)
        title = "na"
    fl = {
        "url":url,
        "type":title
    }
    print(fl)

    return pd.DataFrame([fl])




url = "https://www.amazon.com/Mp3-Tubidy-Free-Song-Music/dp/B07CL46WL3"
l2 = []
l1 = pd.read_csv('apex_reed.csv')
# print(l1.values[0][0])
for i in l1.values:
    l2.append(i[0])

# tuype = getData(url)
# print(tuype)

# t1 = time.time()
df = pd.concat(list(map(getData, l2))).reset_index(drop=True)

driver.close()
df.to_csv("amazon.csv")
