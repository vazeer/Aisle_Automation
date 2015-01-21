import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from vue_crawler.items import VueCrawlerItem
import urlparse
import urllib
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor

class JabongTags(CrawlSpider):
    name = 'jabongTags'
    allowed_domains = ['jabong.com']
    start_urls =['http://www.jabong.com/women/clothing/summer-jackets-shrugs/']
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="cat-filter catTreeLvl1"]')),
        Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="facet_brand"]//a'),callback='parse_item'),
    )
    
    def parse_item(self, response):
     
      hxs = Selector(response)
      item = VueCrawlerItem()
      item['product_item_num']  = str(response.url)   
      productIDs = hxs.xpath('//a[@unbxdattr="product"]/@unbxdparam_sku').extract()     
      taglist1  = hxs.xpath('(//div[@class="breadcrumbs mb8"]//a/@title)[position() > 1]').extract()
      taglist2  = hxs.xpath('(//div[@class="fl ml5 c999 LastFilterValue"]//span/text())|(//a[@id="qa-filterItem"]/text())').extract()
      
      list = []
      for index in range(len(taglist1)):
        v = (taglist1[index])
        v = v.strip()
        if v!='/' and  v:
          list.append(v)
      for index in range(len(taglist2)):
        v = (taglist2[index])
        v = v.strip()
        if v!='/' and  v:
          list.append(v)    
      item['tag'] = list 
      item['tag_product_ids']  = productIDs     
      return item
  
    
