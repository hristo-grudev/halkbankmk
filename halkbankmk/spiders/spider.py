import scrapy

from scrapy.loader import ItemLoader
from ..items import HalkbankmkItem
from itemloaders.processors import TakeFirst


class HalkbankmkSpider(scrapy.Spider):
	name = 'halkbankmk'
	start_urls = ['http://www.halkbank.mk/novosti.nspx']

	def parse(self, response):
		post_links = response.xpath('//p[@class="more-link"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="alignLeft fullWidth"]//h2//text()').get()
		description = response.xpath('//div[@class="alignLeft fullWidth"]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="alignLeft fullWidth"]//h3//text()').get()

		item = ItemLoader(item=HalkbankmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
