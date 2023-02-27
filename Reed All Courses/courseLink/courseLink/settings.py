import pandas as pd
import requests
import random
from collections import OrderedDict
today = pd.to_datetime("today").strftime("%d_%b_%y")

BOT_NAME = 'courseLink'

SPIDER_MODULES = ['courseLink.spiders']
NEWSPIDER_MODULE = 'courseLink.spiders'


FEED_FORMAT = "csv" 
FEED_URI = f"{today}_all_courseLink.csv"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# PROXY_POOL_ENABLED = True


# DOWNLOADER_MIDDLEWARES = {
#      'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#      'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# }

# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

headers_list = [
# Firefox 77 Mac
{
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Referer": "https://www.google.com/",
"DNT": "1",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1"
},
# Firefox 77 Windows
{
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "https://www.google.com/",
"DNT": "1",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1"
},
# Chrome 83 Mac
{
"Connection": "keep-alive",
"DNT": "1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Dest": "document",
"Referer": "https://www.google.com/",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
},
# Chrome 83 Windows
{
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Referer": "https://www.google.com/",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9"
}
]
# Create ordered dict from Headers above
ordered_headers_list = []
for headers in headers_list:
     h = OrderedDict()
for header,value in headers.items():
     h[header]=value
     ordered_headers_list.append(h)
url = 'https://httpbin.org/headers'
for i in range(1,4):
#Pick a random browser headers
     headers = random.choice(headers_list)
#Create a request session
r = requests.Session()
r.headers = headers
response = r.get(url)
print("Request #%d\nUser-Agent Sent:%s\n\nHeaders Recevied by HTTPBin:"%(i,headers['User-Agent']))
print(response.json())
print("-------------------")

#Request #1
# User-Agent Sent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
# Headers Recevied by HTTPBin:
{'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Dnt': '1', 'Host': 'httpbin.org', 'Referer': 'https://www.google.com/', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0', 'X-Amzn-Trace-Id': 'Root=1-5ee83553-d3b3cfdd774dec24971af289'}}
#-------------------
#Request #2
# User-Agent Sent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0
# Headers Recevied by HTTPBin:
{'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'identity', 'Accept-Language': 'en-US,en;q=0.5', 'Dnt': '1', 'Host': 'httpbin.org', 'Referer': 'https://www.google.com/', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0', 'X-Amzn-Trace-Id': 'Root=1-5ee83555-2b6fa55c3f38ba905eeb3a9e'}}
#-------------------
#Request #3
# User-Agent Sent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0
# Headers Recevied by HTTPBin:
{'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'identity', 'Accept-Language': 'en-US,en;q=0.5', 'Dnt': '1', 'Host': 'httpbin.org', 'Referer': 'https://www.google.com/', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0', 'X-Amzn-Trace-Id': 'Root=1-5ee83556-58ee2480f33e0b00f02ff320'}}
#-------------------