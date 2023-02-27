# Import required modules
import scrapy
import pandas as pd
from ..items import CourseinfoItem
import numpy as np


class CourseInfoScraper(scrapy.Spider):
	name="infoScraper"

	# Read in course link file
	today = pd.to_datetime("today").strftime("%d_%b_%y")
	linkDf = pd.read_csv(f"{today}_all_courseLink.csv")

	# Make absolute links. This part keeps the unique course links only
	linkDf.courseLink = "https://www.reed.co.uk" + linkDf.courseLink
	linkDf = linkDf.squeeze() # Dataframe into series
	splitTempSeries = linkDf.astype("str").str.split("/", expand=True)
	splitTempSeries.columns = ["a","b","c","d","e","f","g","h"]
	duplicatesDropped = splitTempSeries.drop_duplicates("f", keep="first").reset_index(drop=True)
	courseLink = duplicatesDropped.apply(lambda x: "/".join(x.values.astype("str")), axis=1) # This returns a series of course links
	start_urls = courseLink.tolist()


	def parse(self, response):
		item = CourseinfoItem()

		# Insert date
		item["date"] = pd.to_datetime("today").strftime("%d_%b_%y")

		# Scrape Title
		try:
			item["courseTitle"] = response.css("div.course-title h1::text").get(default="No title").strip()
		except:
			item["courseTitle"] = response.css("h1.main-title.me-2::text").get(default="No title").strip()

		# Scrape subtitle
		try:
			try:
				item["subtitle"] = response.css("div.course-title h2::text").get(default="No subtitle").strip()
			except:
				item["subtitle"] = response.css("h2.new-subtitle.mb-3.me-2::text").get(default="No subtitle").strip()
		except:
			item["subtitle"] = 'No subtitle'

		# Scrape course provider
		try:
			try:
				item["courseProvider"] = response.css("div.col-lg-8.summary-content>a::text").get().strip()
			except:
				item["courseProvider"] = response.css("div.d-block.d-md-none.mb-3>span::text").get().strip()
		except:
			item["courseProvider"] = 'No provider'

		# Scrape offer price
		try:
			offerPrice = response.css("span.current-price::text").get().replace(",", "").replace("£", "").replace(
				"Free", "0")
			item["offerPrice"] = pd.to_numeric(offerPrice, errors="coerce")
		except:
			item["offerPrice"] = 0

		# Scrape original price
		try:
			originalPrice = response.css("small.vat-status::text").re(r"£\d*,?\d*")[0].replace(",", "").replace("£", "")
			item["originalPrice"] = pd.to_numeric(originalPrice, errors="coerce")
		except:
			item["originalPrice"] = 0

		# Scrape unit sold
		try:
			if bool(response.css("#courseStats>div>div>div::text").get()) and response.css(
					"#courseStats > div > div.icon.me-1 > span").get() == '<span class="icon-students-white"></span>':
				item["unitSold"] = int(response.css("#courseStats>div>div>div::text").get().replace(",", ""))
			# item['condition']=1
			elif bool(response.css("#palnelStats>div>div>div::text").get()) and response.css(
					"#palnelStats > div > div.icon.me-1 > span").get() == '<span class="icon-students-white"></span>':
				item["unitSold"] = int(response.css("#palnelStats>div>div>div::text").get().replace(",", ""))
			elif bool(response.css("#courseStats>div>div>div::text").get()) and response.css(
					"#courseStats > div > div.icon.me-1 > span").get() == '<span class="icon-students"></span>':
				item["unitSold"] = int(response.css("#courseStats>div>div>div::text").get().replace(",", ""))
			# item['condition']=1
			elif bool(response.css("#palnelStats>div>div>div::text").get()) and response.css(
					"#palnelStats > div > div.icon.me-1 > span").get() == '<span class="icon-students"></span>':
				item["unitSold"] = int(response.css("#palnelStats>div>div>div::text").get().replace(",", ""))
			elif bool(response.css('#number-enquiries-purchases strong::text').get()):
				item["unitSold"] = int(response.css('#number-enquiries-purchases strong::text').get().replace(",", ""))
			else:
				item["unitSold"] = 0
		except:
			item["unitSold"] = 0

		# Check if the course was sold or enquired
		try:
			item["soldOrEnq"] = 2 if (response.css('button#addToBasket>span') or response.css(
				'button#addToBasket')) and (response.css('button#enquireNow>span') or response.css('button#enquireNow')) \
				else 0 if (response.css('button#enquireNow>span')) or (response.css('button#enquireNow>')) \
				else 1
		except:
			item["soldOrEnq"] = 1

		# Scrape savings
		try:
			item["savingsPercent"] = int(response.css("div.new-saving-text::text").get().replace("Save", "").replace("%", "").strip())
		except:
			try:
				item["savingsPercent"] = int(
					response.css(".icon-savings-tag.price-saving::text").get().replace("Save", "").replace("%",
																										   "").strip())
			except:
				item["savingsPercent"] = 0


		# Extract course link
		item["courseLink"] = response.url

		# CPD point of the course
		# Extract text starts with min 1 and max 3 digits, followed by "CPD hours / points"
		try:
			if bool(response.xpath("string(//body)").re(r"\d{1,3} CPD hours / points")):
				cpdPoint = response.xpath("string(//body)").re(r"\d{1,3} CPD hours / points")
				cpdPoint = cpdPoint[0].strip().split("CPD")[0].strip()
				item["cpdPoint"] = int(cpdPoint)
				item["haveCpd"] = 1
			elif bool(response.css("div.align-popover>div::text").get().strip().split("CPD")[0].strip()):
				item["cpdPoint"] = int(
					response.css("div.align-popover>div::text").get().strip().split("CPD")[0].strip())
				item["haveCpd"] = 1
			else:
				item["cpdPoint"] = 0
				item["haveCpd"] = 0
		except:
			item["cpdPoint"] = 0
			item["haveCpd"] = 0

		# Awarding body of the course if any
		try:
			try:
				# Executes if the course is "Endorsed by"
				item["awardingBody"] = response.css("div.col a::text").get().strip()
			except:
				# Executes if the course is "Awarded by"
				item["awardingBody"] = response.css("div.small div a::text").get().strip()
		except:
			item["awardingBody"] = "na"

		# Qualification name of the course if any, only for awarded courses
		item["qualName"] = response.css("div.small h3.h4::text").get(default="na").strip()

		# Is the course regulated?
		item["isRegulated"] = 1 if response.css("div.badge.badge-dark.badge-regulated.mt-2").get() \
			else 0

		# Does the course have professional certification?
		item["hasProfCert"] = 1 if response.css("div.badge.badge-dark.badge-professional.mt-2").get() \
			else 0

		# Scrape category, broad categories and sub categories
		category = [x.strip() for x in response.css("div.breadcrumbs.breadcrumbs-lower>div>a::text").getall()]
		category = list(filter(lambda x: x, category))
		category1 = [value for value in category if value not in ("Online courses", "Free courses")]

		# Course category of the course
		item["category"] = category1

		# Extract broad category 1
		try:
			item["broadCategory1"] = category1[1]
		except:
			item["broadCategory1"] = "na"

		# Extract sub category 1
		try:
			item["subCategory1"] = category1[2]
		except:
			item["subCategory1"] = "na"

		# Extract broad category 2
		try:
			item["broadCategory2"] = category1[-2]
		except:
			item["broadCategory2"] = "na"

		# Extract sub category 2
		try:
			item["subCategory2"] = category1[-1]
		except:
			item["subCategory2"] = "na"

		# Extract course id from course link
		item["courseId"] = int(item["courseLink"].split("/")[5].replace("#", ""))

		# On_demand_or_Not
		try:
			if bool(response.css("span.on-demand::text").get().strip()):
				item["OnDemand"] = 1
			else:
				item["OnDemand"] = 0
		except:
			item["OnDemand"] = 0

		yield item
