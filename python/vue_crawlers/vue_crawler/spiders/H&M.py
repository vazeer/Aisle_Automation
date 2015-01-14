'''
Created on July 22, 2014

@author: Vazeer
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class HandMSpider(CrawlSpider):
  name = "HandM"
  allowed_domains = ['hm.com']
  start_urls = ['http://www.hm.com/us/subdepartment/LADIES', 'http://www.hm.com/us/department/MEN']
  rules = (
    #Extract different categories
    Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="folded"]'))),

    #Extract all sub categories
    Rule(SgmlLinkExtractor(restrict_xpaths=('(//ul[@class="products single"]//ul//li)[position()>1]')),callback='parse_item',follow = True),
    
   Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="act leaf"] | //ul[@class="subsubtype"] | //ul[@class="pages bottom"]')),callback='parse_item',follow = True),
    #Extract all pages
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="pages top fixed"]'))),

      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@id="list-products"]')),
         callback='parse_item'),
  )

  def parse_item(self, response):
   # print '*********************************** URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//input[@id="input-article"]/@value').extract()[0]
   # item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "hm.com"
    title = str(sel.xpath('//ul[@class="breadcrumbs"]//li[last()]//strong/text()').extract()[0])
    item['product_title'] = title.strip()
    item['product_item_num'] = item_num_str
    item['product_url'] = response.url
    item['description'] = sel.xpath('//meta[@name="description"]/@content').extract()
    item['image_urls'] = ['http:'+sel.xpath('//ul[@class="large items"]//li//a/@href').extract()[0]]
    
   
    res  = sel.xpath('(//ul[@class="breadcrumbs"]//li/a//text()|//ul[@class="breadcrumbs"]//li/strong//text())[position() > 1]').extract()
    print '*************',res
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        v = v.strip()
        if  v!='/':
            list.append(v)
    item['product_tags'] = list   
    sizes = sel.xpath('//ul[@id="options-variants"]//li//text()').extract()
    
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
    item['product_sizes'] = sizesstripped
    item['product_colors'] = sel.xpath('//ul[@id="options-articles"]//li//text()').extract()
    
    
#    bullet_description = [sel.xpath('//div[@class="description"]//p/text()').extract()[0]]
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())

    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@class="price"]//span/text()').extract()
    item['list_price'] = price[0]


