'''
Created on sept 13, 2014

@author: vazeer

'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ModdealsSpider(CrawlSpider):
  name = "moddeals"
  allowed_domains = ['moddeals.com']
  start_urls = [
  'http://www.moddeals.com/list/womens-cheap-tops',
    'http://www.moddeals.com/list/womens-cheap-dresses',
    'http://www.moddeals.com/list/womens-bottoms',
    'http://www.moddeals.com/list/womens-activewear',
    'http://www.moddeals.com/list/womens-coats-jackets',
    'http://www.moddeals.com/list/basics',
    'http://www.moddeals.com/list/cheap-swimwear-women',
    'http://www.moddeals.com/list/workwear',
    'http://www.moddeals.com/list/cheap-intimate-apparel',
    'http://www.moddeals.com/list/trends',
    
    
    'http://www.moddeals.com/list/cheap-shoes-womens-flats',
    'http://www.moddeals.com/list/womens-cheap-sandals',
    'http://www.moddeals.com/list/cheap-wedges-shoes',
    'http://www.moddeals.com/list/womens-cheap-sneakers',
    'http://www.moddeals.com/list/womens-shoes-cheap-heels-pumps',
    'http://www.moddeals.com/list/womens-cheap-boots',
    'http://www.moddeals.com/list/cheap-athletic-shoes-for-women',
    
    
    'http://www.moddeals.com/list/cheap-womens-sunglasses',
    'http://www.moddeals.com/list/womens-scarves',
    'http://www.moddeals.com/list/cheap-womens-watches',
    'http://www.moddeals.com/list/belts',
    'http://www.moddeals.com/list/womens-hair-accessories',
    'http://www.moddeals.com/list/hats',
    
    
    'http://www.moddeals.com/list/cheap-womens-jewelry',
    'http://www.moddeals.com/list/cheap-premium-jewelry',
    'http://www.moddeals.com/list/womens-rings',
    'http://www.moddeals.com/list/womens-earrings',
    'http://www.moddeals.com/list/womens-necklaces',
    'http://www.moddeals.com/list/womens-bracelets',
    
    'http://www.moddeals.com/list/cheap-womens-handbags',
    'http://www.moddeals.com/list/womens-clutches',
    'http://www.moddeals.com/list/womens-wallets'
    
  ]
  rules = (
   Rule(SgmlLinkExtractor(restrict_xpaths='//ul[@class="product_filter_scroll"]//li[@class="sub_categories"]')),
   Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="paging paging-product-list-1"]//a'),callback='parse_item',follow=True),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="quickview"]'), callback='parse_item')
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item_num_str = sel.xpath('//a[@class="review_link write_review"]/@reviewid').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "moddeals.com"
    item['product_title'] = str(sel.xpath('//h1[@itemprop="name"]//text()').extract()[0])
    item['product_item_num'] = item_num
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@itemprop="description"]//p[@class="maindesc"]/text()').extract()
    item['image_urls'] = [sel.xpath('//img[@itemprop="image"]/@src').extract()[0]]
    
    
     # Express dynamically loads there images so we cant easily scrap them.
    bullet_description = sel.xpath('//table[@class="altrowstable"]//td//text()|//ul[@class="jake"]//li//text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(str(desc_bullet.strip()))
    
    
    res  = sel.xpath('(//div[@id="breadcrumbs"]//a/text())[position()>1]').extract()
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        v = v.strip()
        if  v!='/':
            list.append(v)
    item['product_tags'] = list
    
    
    
    item['product_sizes'] = sel.xpath('//ul[@id="product_size_box"]//li/@id').extract()
    item['product_colors'] = sel.xpath('//ul[@id="product_color_swatch"]//li/@id').extract()
    
#    bullet_description = sel.xpath('//ul[@class="product-description"]//li/text()').extract()
#    for desc_bullet in bullet_description:
#      if desc_bullet.strip():
#        item['description'].append(desc_bullet.strip())
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//span[@itemprop="price"]/text()').extract()
    item['list_price'] = price[0]
