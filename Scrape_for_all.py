import pandas as pd

# To make web request
import requests

# For parsing html content
from bs4 import BeautifulSoup

from datetime import datetime
today = datetime.today().strftime("%d_%b")

href = []

url_ = "https://www.reed.co.uk/courses/discount"


def parse1(url):
    """url: course url to make request"""

    # Make request to the url
    r = requests.get(url)

    # Convert into beautifulsoup object
    s = BeautifulSoup(r.text, "lxml")

    # Extract title
    try:
        global href
        for courseTitle in s.findAll("div", class_="course-overview"):
            href.append("https://www.reed.co.uk" + courseTitle.find("a").attrs.get("href"))
            if href == "" or href is None:
                # href empty tag
                continue
    except:
        pass

def parse(url):
    """url: course url to make request"""
    
    # Make request to the url
    r = requests.get(url)
    
    # Convert into beautifulsoup object
    s = BeautifulSoup(r.text, "lxml")
    
    # Extract title
    try:
        courseTitle = s.find("div", class_="course-title").find("h1").text.strip()
    except:
        courseTitle = "na"

    # Extract subTitle
    try:
        subTitle = s.find("div", class_="course-title").find("h2").text.strip()
    except:
        subTitle = "na"
        
    # Offer price
    try:
        offerPrice = s.find("span", class_="current-price").text.strip()
    except:
        offerPrice = "na"

    # original price
    try:
        originalPrice = s.find("small", class_="vat-status").text.strip()
    except:
        originalPrice = "na"

    # total sold
    try:
        unitSold = s.find(id="number-enquiries-purchases").text.strip()
    except:
        unitSold = "na"

    # total sold
    try:
        saving = s.find("span", class_="icon-savings-tag price-saving").text.strip()
    except:
        saving = "na"


    # Create a df off scraped variables
    df = pd.DataFrame({
        "courseTitle":courseTitle,
        "subTitle":subTitle,
        "offerPrice":offerPrice,
        "unitSold":unitSold,
        "originalPrice":originalPrice,
        "saving":saving
    }, index=[0])
    return df


parse1(url_)

# concat
df = pd.concat(list(map(parse, href))).reset_index(drop=True)


# data cleaning


df.offerPrice = df.offerPrice.str.replace("£", "").str.replace(",", "").astype("float")
df.originalPrice = df.originalPrice.str.split(" ").str[-1].str.replace("£", "").str.replace(")", "").str.replace(",", "").astype("float")
df.unitSold = df.unitSold.str.split(" ").str[0].str.replace(",", "").astype("int")
df.saving = df.saving.str.split(" ").str[-1].str.replace("%","").astype("float")




df.to_csv(f"{today}_demoWebScraping.csv", index=None)

