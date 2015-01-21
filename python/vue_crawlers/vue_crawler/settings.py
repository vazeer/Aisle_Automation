# Scrapy settings for test_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'vue_crawler'

SPIDER_MODULES = ['vue_crawler.spiders']
NEWSPIDER_MODULE = 'vue_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_scrapy (+http://www.yourdomain.com)'

ITEM_PIPELINES = {'vue_crawler.pipelines.NordstromPipeline': 1}

IMAGES_STORE = '/Users/Geli/Behrooz/VUE/scraped_imgs/nordstrom'

IMAGES_EXPIRES = 20

