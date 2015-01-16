'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re
import nltk
from nltk.collocations import *
from nltk.stem import *



from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem
import urlparse
import urllib
from scrapy.selector import Selector

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors import LinkExtractor

class ExpressTagsSpider(CrawlSpider):
  name = "expressTags"
  allowed_domains = ['express.com']
  start_urls = [
    'http://www.express.com/clothing/women/new-arrivals/cat/cat120002',
    'http://www.express.com/clothing/women/dresses/cat/cat550007?zf=sr:dress',
    'http://www.express.com/clothing/women/jumpsuits-rompers/cat/cat320051',
    'http://www.express.com/clothing/women/tops/cat/cat430028?zf=sr:top',
    'http://www.express.com/clothing/women/sweaters-cardigans/cat/cat2012?zf=sr:sweater',
    'http://www.express.com/clothing/women/sweatshirts/cat/cat1040010',
    'http://www.express.com/clothing/women/portofino-shirts/cat/cat1660006',
    'http://www.express.com/clothing/women/jeans/cat/cat2005'
    'http://www.express.com/clothing/women/pants/cat/cat2008',
    'http://www.express.com/clothing/women/editor-pants/cat/cat1540021',
    'http://www.express.com/clothing/women/columnist-pants/cat/cat1540022',
    'http://www.express.com/clothing/women/leggings/cat/cat1620001',
    'http://www.express.com/clothing/women/skirts/cat/cat2011',
    'http://www.express.com/clothing/women/shorts/cat/cat320019',
    'http://www.express.com/clothing/women/jackets/cat/cat320022',
    'http://www.express.com/clothing/women/suits/cat/cat760006',
    'http://www.express.com/clothing/women/coats-outerwear/cat/cat320021',
    'http://www.express.com/clothing/women/activewear/cat/cat1070014',
    'http://www.express.com/clothing/women/yoga-lounge/cat/cat910043',
    'http://www.express.com/clothing/women/shoes-boots/cat/cat2010',
    'http://www.express.com/clothing/women/accessories/cat/cat740011',
    'http://www.express.com/clothing/sale-women/clearance-women/cat/cat890004'
    'http://www.express.com/clothing/women/online-exclusives/cat/cat1730035',
    
     
    'http://www.express.com/clothing/men/new-arrivals/cat/cat120009', 
    'http://www.express.com/clothing/men/1mx-dress-shirts/cat/cat270001',
    'http://www.express.com/clothing/men/shirts/cat/cat1020003?zf=sr:top_men',
    'http://www.express.com/clothing/men/suits/cat/cat1620002',
    'http://www.express.com/clothing/men/suit-separates/cat/cat1260002',
    'http://www.express.com/clothing/men/blazers-vests/cat/cat560005',
    'http://www.express.com/clothing/men/sweaters-cardigans/cat/cat1490005?zf=sr:sweater_men',
    'http://www.express.com/clothing/men/hoodies-sweatshirts/cat/cat1490006',
    'http://www.express.com/clothing/men/polos/cat/cat1006',
    'http://www.express.com/clothing/men/jeans/cat/cat400003',
    'http://www.express.com/clothing/men/casual-pants-jogger-pants/cat/cat320038',
    'http://www.express.com/clothing/men/tees-henleys/cat/cat430030',
    'http://www.express.com/clothing/men/coats-outerwear/cat/cat1490017',
    'http://www.express.com/clothing/men/graphic-tees/cat/cat1002',
    'http://www.express.com/clothing/men/dress-pants/cat/cat280012',
    'http://www.express.com/clothing/men/shoes-boots/cat/cat280006',
    'http://www.express.com/clothing/men/ties/cat/cat280005',
    'http://www.express.com/clothing/men/shorts/cat/cat1490010',
    'http://www.express.com/clothing/men/cold-weather-accessories/cat/cat1600002',
    'http://www.express.com/clothing/men/underwear-lounge/cat/cat1490012',
    'http://www.express.com/clothing/men/accessories/cat/cat400001',
    'http://www.express.com/clothing/men/workout-essentials/cat/cat1770065',
    'http://www.express.com/clothing/men/online-exclusives/cat/cat1750025',
    'http://www.express.com/clothing/sale-men/clearance-men/cat/cat890006'
    
  ]
  
  rules = (
  Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="mobile-two"]|//li[@class="two mobile-two"]'),callback='parse_item'),
 # Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="ItemImage"]//a[1]'),callback='parse_item'),
  )
  
  def myParserTest(self,response):
      print '**************test********************* URL:', response.url
           
    
        
  def parse_item(self, response):
 #   print '************* URL:', response.url
    #sel = Selector(response)
    hxs = Selector(response)
    
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
  
    item['product_item_num']  = str(response.url)
 
    
    productIDs = hxs.xpath('//div[@class="image-container"]//a[@class="ev-icon"]/@data-product-id').extract()
   
    res  = hxs.xpath('//ul[@id="selected-filters"]//li/@data-value').extract()
    tg2 = hxs.xpath('//h1[@id="total-products"]/text()').extract()[0]
    tg1 = hxs.xpath('//li[@class="open"]//text()').extract()[0]
    
    list = []
    list.append(tg1)
    list.append(tg2)  
    for index in range(len(res)):
        v = (res[index])
        v = v.strip()
        if v!='/':
          list.append(v)
     
            
    item['tag'] = list 
    item['tag_product_ids']  = productIDs
      
  
    return item

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     
     res = par["ProductID"]
     return res[0]
 
   
 