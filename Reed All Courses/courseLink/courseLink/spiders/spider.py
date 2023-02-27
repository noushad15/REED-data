# Import required modules
import requests
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup
import requests
import scrapy
import numpy as np
from ..items import CourselinkItem


class CourseLinkScraper(scrapy.Spider):
    name = "courseLink"
    page_number = 2
    start_urls = [
        'https://www.reed.co.uk/courses/online?pageno=1&pagesize=100'
    ]

    def parse(self, response):
        items = CourselinkItem()
        for all in response.css("article.course-card"):
            link = all.css("h2.course-card-title>a::attr(href)").get()
            yield {
                'courseLink': link
                # 'courseId':id,
                # 'unitSold':s
            }
        r = requests.get("https://www.reed.co.uk/courses/online?pageno=1&pagesize=100")
        s = BeautifulSoup(r.text, "lxml")
        totalCourse = int(s.find("span", class_="h1").text.strip().replace(",", ""))
        totalPage = int(np.ceil(totalCourse / 100))

        next_page = "https://www.reed.co.uk/courses/online?pageno=" + str(
            CourseLinkScraper.page_number) + "&pagesize=100"
        if CourseLinkScraper.page_number < totalPage+1:
            CourseLinkScraper.page_number += 1
            yield response.follow(next_page, callback=self.parse)
