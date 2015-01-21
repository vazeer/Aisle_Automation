'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem


class ExpressSpider(CrawlSpider):
  name = "express"
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
    
     Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="mobile-two"]|//li[@class="two mobile-two"]')),
      # Extract the different items on the page.
    Rule(SgmlLinkExtractor(
      restrict_xpaths=('//ul[@class="product-info"]')),
      callback='parse_item'),
    # Extract the different pages on the main site side menu.
    Rule(SgmlLinkExtractor(restrict_xpaths=('//ul[@class="link-list"]'))),
#     # Extract page number links
#     Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="twelve columns"]'))),
  )

  def parse_item(self, response):
    print '************* URL:', response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
    item['source_site'] = "express.com"
    item['product_title'] = str(sel.xpath('//h2[@itemprop="name"]//text()').extract()[0])
    item_num_str = sel.xpath('//input[@id="productId"]/@value').extract()[0]
    item_num = re.findall(r'\d+', item_num_str)[0]
    item['product_item_num'] = item_num
    self.ProductNumExtract(item, response.url)
    item['product_url'] = response.url
    item['description'] = sel.xpath('//div[@class="product-panel four columns"]'
                                    '//div[@class="product-description"]'
                                    '//p/text()').extract()
    # Express dynamically loads there images so we cant easily scrap them.
    bullet_description = sel.xpath('//div[@class="product-description"]//ul//li/text()').extract()
    for desc_bullet in bullet_description:
      if desc_bullet.strip():
        item['description'].append(desc_bullet.strip())
        
    sizes = sel.xpath('(//select[@name="express-view-sizes-dropdown"]//option/text())[position()>1]').extract()
    item['image_urls'] = ['http:'+sel.xpath('//div[@class="product-exp-view-image"]//a/@href').extract()[0]]
  
         
    sizesstripped = [];
    for index in range(len(sizes)):
        v = str(sizes[index])
        v = v.strip()
        if  v!='':
          sizesstripped.append(v)
    item['product_sizes'] = sizesstripped
    item['product_colors'] = sel.xpath('//ul[@id="express-view-colors"]//label/@title').extract()
    list = []
    item['product_tags'] = list 
    
    return item

  def PriceExtractor(self, item, selector):
    prod_price = selector.xpath('//h2[@itemprop="name"]//text()').extract()
    price = selector.xpath('//span[@itemprop="price"]//text()').extract()
    item['list_price'] = price[0]
    for price in prod_price:
      if re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)
      if re.search(r"Reg. (\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"Reg. (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"Sale (\$\d*\.\d\d)", price):
        item['sale_price'] = re.search(r"Sale (\$\d*\.\d\d)", price).group(1)
      elif re.search(r"(\$\d*\.\d\d)", price):
        item['list_price'] = re.search(r"(\$\d*\.\d\d)", price).group(1)

  def ProductNumExtract(self, item, response_url):
    if re.search(r"(/\d+/)", response_url):
      item['product_item_num'] = re.search(r"/(\d+)/", response_url).group(1)