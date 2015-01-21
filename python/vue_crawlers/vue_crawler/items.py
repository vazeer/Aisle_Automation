# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class VueCrawlerItem(Item):
  """Defines the model for crawler scraped items."""

  # Category of the item
  category = Field()

  # Source site where this item is found or scraped from
  source_site = Field()

  # Title scraped from the page
  product_title = Field()

  # The item id scraped from the page
  product_item_num = Field()

  # URL of the product page
  product_url = Field()

  # Product rating, if available
  rating = Field()

  # Number of reviews, if available
  num_reviews = Field()

  # Detailed description text of the product
  description = Field()

  # List price. This should be present if the item is on sale
  list_price = Field()

  sale_price = Field()

  # Main image url
  image_urls = Field()

  # used to write image.
  # See http://doc.scrapy.org/en/latest/topics/images.html#topics-images
  # for more details
  images = Field()

  # to get all colors of product
  product_colors = Field()

  #to get available sizes of a product
  product_sizes = Field()
  
  #tags to products
  product_tags = Field()
  
  #currency code
  currencyCode = Field()

  tag = Field()
  tag_product_ids = Field()




