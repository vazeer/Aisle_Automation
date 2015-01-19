'''
Created on Jun 13, 2014

@author: Behrooz
'''

import re

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from vue_crawler.items import VueCrawlerItem

import urlparse
import urllib
class NordstromSpider(CrawlSpider):
  name = "nordy"
  allowed_domains = ['shop.nordstrom.com']
  #start_urls = ['http://shop.nordstrom.com/c/womens-clothing?origin=leftnav',
  #              'http://shop.nordstrom.com/c/womens-shoes',
  #              'http://shop.nordstrom.com/c/womens-handbags',
  #
  #]
  #rules = (
  #
  #
  #  Rule(SgmlLinkExtractor(restrict_xpaths='((//h3[@class="nav-entry-clothing"])[1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]|//ul[@class="nav-group"][position()>1]|((//h3[@class="nav-entry-shoes"])[position()>1])//following::ul[1]//li[following-sibling::li[@class="spacer-hack"]]')),
  #  Rule(SgmlLinkExtractor(restrict_xpaths='//div[@id="leftnav"]//a'), callback='parse_item',follow=True),
  #  
  #  Rule(SgmlLinkExtractor(restrict_xpaths='(//ul[@class="numbers"])[1]//li'), callback='parse_item',follow=True),
  #  
  #
  #     
  #  Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="title"]')),
  #       callback='parse_item'),
  #
  #)
  
   
  start_urls = [
                #dresses 
                'http://shop.nordstrom.com/c/womens-mother-of-the-bride-dresses?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-neutral-tone-dresses?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-dusty-pinks-dresses?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-jewel-tone-dresses?origin=leftnav',
                               
                'http://shop.nordstrom.com/c/womens-prom-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-red-dress?origin=leftnav',
                
                'http://shop.nordstrom.com/c/little-black-dress?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-dresses-new?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-dresses-customer-favorites?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-cocktail-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/wedding-guest-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-formal-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-party-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-night-out-club-sexy-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-bridesmaid-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-day-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-workday-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-casual-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-vacation-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-fit-flare-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-maxi-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-little-white-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/lace-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/midi-dresses-women?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-jumpsuits-rompers?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-bodycon-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-sweater-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/adrianna-papell-womens-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/eliza-j-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/tadashi-shoji-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/felicity-and-coco-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/ted-baker-london-womens-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/lauren-by-ralph-lauren-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/diane-von-furstenberg-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/lilly-pulitzer-dresses?origin=leftnav',
                
                'http://shop.nordstrom.com/c/topshop-womens-dresses?origin=leftnav',
                
                #coats
                'http://shop.nordstrom.com/c/womens-coats-new-arrivals?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-designer-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-coats-customer-favorites?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-wool-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/trench-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/raincoats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/parkas?origin=leftnav',
                'http://shop.nordstrom.com/c/down-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/quilted-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/leather-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/fur-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/pea-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-vest?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-performance-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/colorful-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/puffer-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/luxe-trim-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cozy-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/utility-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/the-north-face-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/burberry-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/bernardo-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/michael-michael-kors-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-lauren-ralph-lauren-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/pendleton-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/trina-turk-coats-jackets-womens?origin=leftnav',
                'http://shop.nordstrom.com/c/barbour-womens-coats-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/fleurette-womens-coats-jackets?origin=leftnav',
                
                #tops
                'http://shop.nordstrom.com/c/womens-blouses?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-t-shirts-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-tanks-camisoles?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-night-out-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-tunics?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-plaid-shirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-collared-button-down-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-sweatshirts-pullovers?origin=leftnav',
                'http://shop.nordstrom.com/c/wrap-blouses-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-crop-tops-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-lace-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-graphic-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/free-people-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/halogen-womens-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/eileen-fisher-womens-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/splendid-womens-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/vince-womens-tops-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/t-by-alexander-wang-tops?origin=leftnav',
                
                #sweaters
                'http://shop.nordstrom.com/c/womens-cardigan-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cashmere-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-crewneck-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-turtleneck-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-v-neck-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-tunic-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-graphic-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-printed-and-patterned-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-fuzzy-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cropped-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/free-people-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/halogen-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/vince-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/eileen-fisher-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/wildfox-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/autumn-cashmere-sweaters?origin=leftnav',
                'http://shop.nordstrom.com/c/60183484?origin=leftnav',
                
                #jeans
                'http://shop.nordstrom.com/c/skinny-jeans-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/boyfriend-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cropped-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-bootcut-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-straight-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-ankle-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-trouser-wide-leg-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-slim-bootcut-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-legging-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-flare-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-shorts-jeans?origin=leftnav',
                
                'http://shop.nordstrom.com/c/womens-faded-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/high-waisted-jeans-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-jeans-white?origin=leftnav',
                'http://shop.nordstrom.com/c/paige-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/rag-bone-jean-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/j-brand-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/citizens-of-humanity-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/7-for-all-mankind-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/hudson-jeans-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/ag-jeans-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/joes-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/dl1961-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/true-religion-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/current-elliott-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/nydj-womens-jeans?origin=leftnav',
                'http://shop.nordstrom.com/c/framedenim-womens-jeans?origin=leftnav',
                
                #jackets
                'http://shop.nordstrom.com/c/leather-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/blazers-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/jean-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/bomber-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/tweed-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/vests-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-jacket?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-military-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-moto-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/classiques-entier-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/burberry-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/halogen-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/rag-and-bone-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/theory-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-topshop-jackets?origin=leftnav',
                
                #Active Yoga&outdoor
                'http://shop.nordstrom.com/c/sports-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-tanks?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/performance-coats?origin=leftnav',
                'http://shop.nordstrom.com/c/fleece-jackets-womens?origin=leftnav',
                'http://shop.nordstrom.com/c/winter-coats-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/rain-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/ski-snowboard-jackets-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/softshell-jacket-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-performance-vests?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-pants-capris?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-skirts-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-active-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/athletic-socks?origin=leftnav',
                'http://shop.nordstrom.com/c/athletic-shoes-women?origin=leftnav',
                'http://shop.nordstrom.com/c/yoga-pants-and-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-for-yoga?origin=leftnav',
                'http://shop.nordstrom.com/c/yoga-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/yoga-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/yoga-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-running?origin=leftnav',
                'http://shop.nordstrom.com/c/running-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/running-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/running-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/running-pants-capris?origin=leftnav',
                'http://shop.nordstrom.com/c/active-running-shoes?origin=leftnav',
                'http://shop.nordstrom.com/c/running-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cycling?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-training?origin=leftnav',
                'http://shop.nordstrom.com/c/gym-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/gym-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/gym-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/gym-pants-capris?origin=leftnav',
                'http://shop.nordstrom.com/c/training-shoes-women?origin=leftnav',
                'http://shop.nordstrom.com/c/gym-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-activewear-biking?origin=leftnav',
                'http://shop.nordstrom.com/c/hiking-biking-tops-tees?origin=leftnav',
                'http://shop.nordstrom.com/c/hiking-biking-jackets?origin=leftnav',
                'http://shop.nordstrom.com/c/hiking-biking-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/hiking-biking-shoes?origin=leftnav',
                'http://shop.nordstrom.com/c/hiking-biking-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/ski-snowboard-clothing-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/swimwear-surf-clothing-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-active-golf-tennis?origin=leftnav',
                'http://shop.nordstrom.com/c/tennis-tops?origin=leftnav',
                'http://shop.nordstrom.com/c/tennis-skirt?origin=leftnav',
                'http://shop.nordstrom.com/c/tennis-active-shoes?origin=leftnav',
                'http://shop.nordstrom.com/c/tennis-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-beyond-the-workout?origin=leftnav',
                'http://shop.nordstrom.com/c/nike-womens-activewear?origin=leftnav',
                'http://shop.nordstrom.com/c/patagonia-womens?origin=leftnav',
                'http://shop.nordstrom.com/c/the-north-face-womens-active-wear?origin=leftnav',
                'http://shop.nordstrom.com/c/under-armour-womens-activewear?origin=leftnav',
                'http://shop.nordstrom.com/c/zella-womens-activewear?origin=leftnav',
                
                #shorts
                'http://shop.nordstrom.com/c/womens-denim-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-bermuda-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-high-waist-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-leather-faux-leather-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-active-shorts?origin=leftnav',
                #pants
                'http://shop.nordstrom.com/c/corduroy-pants-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-cropped-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-pants-leggings?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-rompers-jumpsuits?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-skinny-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-straight-leg-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-track-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-trouser-wide-leg-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/theory-womens-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/vince-camuto-womens-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/lafayette-148-new-york-womens-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-halogen-pants-shorts?origin=leftnav',
                'http://shop.nordstrom.com/c/classiques-entier-womens-pants?origin=leftnav',
                'http://shop.nordstrom.com/c/leather-pants-for-women?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-printed-pants?origin=leftnav'
                
                #skirts
                'http://shop.nordstrom.com/c/womens-a-line-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-pencil-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-full-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/mini-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-knee-length-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-midi-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/denim-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-skater-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-body-con-skirts?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-feminine-flirty-skirts?origin=leftnav',
                
                #bras,Lingerie
                'http://shop.nordstrom.com/c/womens-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/dd-plus?origin=leftnav',
                'http://shop.nordstrom.com/c/backless-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/bandeau-bra?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-bralette?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-bustier?origin=leftnav',
                'http://shop.nordstrom.com/c/convertible-bra?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-demi?origin=leftnav',
                'http://shop.nordstrom.com/c/bra-fitter-favorites?origin=leftnav',
                'http://shop.nordstrom.com/c/long-line-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/nursing-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/amoena-prosthesis-bras?origin=leftnav',
                'http://shop.nordstrom.com/c/push-up-bra?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-racerback?origin=leftnav',
                'http://shop.nordstrom.com/c/sports-bras-women?origin=leftnav',
                'http://shop.nordstrom.com/c/strapless-bra?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-t-shirt?origin=leftnav',
                'http://shop.nordstrom.com/c/sheer-bras-unlined?origin=leftnav',
                'http://shop.nordstrom.com/c/bras-wireless?origin=leftnav',
                'http://shop.nordstrom.com/c/womens-panties?origin=leftnav',
                'http://shop.nordstrom.com/c/panties-bikini?origin=leftnav',
                'http://shop.nordstrom.com/c/boyshort?origin=leftnav',
                'http://shop.nordstrom.com/c/panties-brief?origin=leftnav',
                'http://shop.nordstrom.com/c/panties-hipster?origin=leftnav',
                'http://shop.nordstrom.com/c/panties-high-cut?origin=leftnav',
                'http://shop.nordstrom.com/c/tanga-underwear-women?origin=leftnav',
                'http://shop.nordstrom.com/c/panties-thong?origin=leftnav',
                'http://shop.nordstrom.com/c/lingerie-sets?origin=leftnav',
                'http://shop.nordstrom.com/c/sexy-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/bridal-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/camisoles?origin=leftnav',
                'http://shop.nordstrom.com/c/lingerie-chemise?origin=leftnav',
                'http://shop.nordstrom.com/c/seamless-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/slimming-shapewear?origin=leftnav',
                'http://shop.nordstrom.com/c/slips?origin=leftnav',
                'http://shop.nordstrom.com/c/lingerie-accessories?origin=leftnav',
                'http://shop.nordstrom.com/c/betsey-johnson-intimates-womens-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/calvin-klein-intimates-womens-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/chantelle-intimates-womens-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/free-people-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/hanky-panky-womens-panties?origin=leftnav',
                'http://shop.nordstrom.com/c/natori-womens-lingerie?origin=leftnav',
                'http://shop.nordstrom.com/c/wacoal-womens-lingerie?origin=leftnav'
                
                #shapeWear
                'http://shop.nordstrom.com/c/backside?origin=leftnav',
                'http://shop.nordstrom.com/c/hips-thighs?origin=leftnav',
                'http://shop.nordstrom.com/c/midsection?origin=leftnav',
                'http://shop.nordstrom.com/c/commando-hosiery-women?origin=leftnav',
                'http://shop.nordstrom.com/c/dkny-hosiery-women?origin=leftnav',
                'http://shop.nordstrom.com/c/star-power-by-spanx-shapewear?origin=leftnav',
                'http://shop.nordstrom.com/c/spanx-shapewear-women?origin=leftnav',
                'http://shop.nordstrom.com/c/yummie-tummie-hosiery-women?origin=leftnav',
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                

                
                
                ]
  rules = (

    Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="filter category" or @class="filter standard size" or @class="filter standard color small" or @class="filter standard"]//li')),
    Rule(SgmlLinkExtractor(restrict_xpaths='(//li[@class="next"])[1]'),callback='parse_item',follow=True),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="title"]')),callback='parse_item'),
  
  )

  def parse_item(self, response):
#     print response.url
    sel = Selector(response)
    # Reviews not working seems to dynamically retrieve using javascript
    item = VueCrawlerItem()
    self.PriceExtractor(item, sel)
   # item_num_str = sel.xpath('//div[@class="item-number-wrapper"]/text()').extract()[0]
  #  item_num = re.findall(r'\d+', item_num_str)[0]
    item['source_site'] = "shop.nordstrom.com"
    item['product_title'] = str(sel.xpath('//section[@id="product-title"]//h1/text()').extract()[0])
    
    value = self.AddTags(item,response.url)
    item['product_item_num'] = value
    
    
    item['product_url'] = response.url
    item['description'] = sel.xpath('//section[@id="details-and-care"]//ul[@class="style-features"]//li/text()').extract()
    item['image_urls'] = [sel.xpath('//div[@id="product-image"]//img/@src').extract()[0]]
    res  = sel.xpath('//nav[@id="breadcrumb-nav"]/ul//li//text()').extract()
    
    print '*************',res
    
    list = [];
    for index in range(len(res)):
        v = str(res[index])
        if index!=0 and v!='/':
            list.append(v)
    
    item['product_tags'] = list   
    
    
    
    item['product_sizes'] = sel.xpath('//div[@id="size-buttons"]//button[@class="option-label"]/@value').extract()
    item['product_colors'] = sel.xpath('(//select[@id="color-selector"]//option/text())[position()>1]').extract()
    
    
    sale_text = sel.xpath('(//section[@id="price"]//span[@class="sale-price"]/text()|//section[@id="price"]//span[@class="sale-price long-price"]/text())[1]').extract()
    list_text = sel.xpath('(//section[@id="price"]//span[@class="regular-price"]/text())[1]').extract()
   
    
    print '',
    
    return item

  def PriceExtractor(self, item, selector):
    price = selector.xpath('//section[@id="price"]//td[@class="item-price heading-2"]//span/text()').extract()
    if not price:
      sale_text = selector.xpath('(//section[@id="price"]//span[@class="sale-price"]/text())[1]').extract()
      if sale_text:
        sale_text = str(sale_text[0])  
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%sale ' ,sale_text  
        item['sale_price'] = re.search(r"Now: (\INR \d*\.\d\d)", sale_text).group(1)
      list_text = selector.xpath('(//section[@id="price"]//span[@class="regular-price"]/text())[1]').extract()
      if list_text:
        list_text = str(list_text[0])  
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%regular' ,list_text  
        item['list_price'] = re.search(r"Was: (\INR \d*\.\d\d)", list_text).group(1)
    else:
      item['list_price'] = price[0]  
        
  def AddTags(self,item,url):  
     par = urlparse.parse_qs(urlparse.urlparse(url).query)
     url=urllib.unquote(url).decode('utf8') 
     Segments = url.split('/')
     val = Segments[len(Segments)-1]
     res = val.split('?')
     return res[0]
