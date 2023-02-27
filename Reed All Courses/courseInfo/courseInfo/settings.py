import pandas as pd
today = pd.to_datetime("today").strftime("%d_%b_%y")


BOT_NAME = 'courseInfo'

SPIDER_MODULES = ['courseInfo.spiders']
NEWSPIDER_MODULE = 'courseInfo.spiders'

FEED_FORMAT = "csv"
FEED_URI = f"{today}_all_courses.csv"

# Save the data in the specified order of columns
FEED_EXPORT_FIELDS=['date',
 'courseId',
 'courseTitle',
 'courseLink',
 'subtitle',
 'courseProvider',
 'offerPrice',
 'originalPrice',
 'unitSold',
 'category',
 'haveCpd',
 'cpdPoint',
 'awardingBody',
 'qualName',
 'isRegulated',
 'hasProfCert',
 'soldOrEnq',
 'savingsPercent',
 'broadCategory1',
 'broadCategory2',
 'subCategory1',
 'subCategory2',
  'OnDemand']

# Obey robots.txt rules
ROBOTSTXT_OBEY = True