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

class Forever21Spider(CrawlSpider):
  name = "forever21"
  allowed_domains = ['forever21.com']
  
  start_urls = [
'http://www.forever21.com/IN/Product/Category.aspx?br=f21&category=dress_casual',

 
                   ]
  rules = (
   
 Rule(SgmlLinkExtractor(restrict_xpaths='(//table[@class="PagerContainerTable"])[1]'),follow=True),
  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="ItemImage"]//a[1]'),callback='myParserTest'),
   
  )
  
  
  def myParserTest(self,response):
      print '*********************************** URL:', response.url
           
      

      
  def parse_item(self, response):
   # print '*********************************** URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@id="ctl00_MainContent_hdProductId"]/@value').extract()[0]
   # item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "forever21.com"
    title = str(sel.xpath('//font[@class="items_name"]/text()').extract()[0])
    item['product_title'] = title.strip()
    item['product_item_num'] = item_num_str
    item['product_url'] = response.url
  # item['description'] = sel.xpath('//span[@id="product_overview"]/ul//li/text()').extract()
    bullet_description = sel.xpath('//span[@id="product_overview"]/ul//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())
    
    
    
    
    item['image_urls'] = sel.xpath('//img[@class="ItemImage"]/@src').extract()[0]
    
   
    res  = sel.xpath('//a[@class="forever21"]/u/text()').extract()
    print '*************',res
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        v = v.strip()
        if  v!='/':
            list.append(v)
    item['product_tags'] = list   
    sizes = sel.xpath('//select[@id="ctl00_MainContent_ddlSize"]//option[position()>1]').extract()
    
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
    item['product_sizes'] = sizesstripped
    item['product_colors'] = sel.xpath('//select[@id="ctl00_MainContent_ddlColor"]//option[position()>1]').extract()
    
    
#    bullet_description = [sel.xpath('//div[@class="description"]//p/text()').extract()[0]]
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//font[@class="items_price"]/text()').extract()
    item['list_price'] = price[0]

  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
    
 
   
 