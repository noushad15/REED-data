import pandas as pd

# To make web request
import requests

# For parsing html content
from bs4 import BeautifulSoup

from datetime import datetime
today = datetime.today().strftime("%d_%b")



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


urlsToScrape = [
    "https://www.reed.co.uk/courses/food-hygiene-course-level-2/162300#/courses/discount",
    "https://www.reed.co.uk/courses/leadership-management/266620#/courses/discount",
    "https://www.reed.co.uk/courses/office-admin-and-reception-skills/210657#/courses/discount",
    "https://www.reed.co.uk/courses/food-hygiene-and-safety-level-3/274566#/courses/discount",
    "https://www.reed.co.uk/courses/microsoft-excel-complete-course-beginner-intermediate-advanced-cpd/140784#/courses/discount",
    "https://www.reed.co.uk/courses/project-management/98276#/courses/discount",
    "https://www.reed.co.uk/courses/child-psychology-diploma/227506#/courses/discount",
    "https://www.reed.co.uk/courses/risk-management--risk-assessment-diploma/223552#/courses/discount",
    "https://www.reed.co.uk/courses/counselling/202155#/courses/discount",
    "https://www.reed.co.uk/courses/hr-and-payroll-administrator-course/239173#/courses/discount"
]


# concat
df = pd.concat(list(map(parse, urlsToScrape))).reset_index(drop=True)


# data cleaning


df.offerPrice = df.offerPrice.str.replace("£", "").str.replace(",", "").astype("float")
df.originalPrice = df.originalPrice.str.split(" ").str[-1].str.replace("£", "").str.replace(")", "").str.replace(",", "").astype("float")
df.unitSold = df.unitSold.str.split(" ").str[0].str.replace(",", "").astype("int")
df.saving = df.saving.str.split(" ").str[-1].str.replace("%","").astype("float")




df.to_csv(f"{today}_demoWebScraping.csv", index=None)

