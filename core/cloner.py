import scrapy
import logging
from scrapy.crawler import CrawlerProcess

logging.getLogger('scrapy').propagate = False

class Cloner(scrapy.Spider):
	
	name = "test"
	
	custom_settings ={
	'LOG_ENABLED': False
	}

	def parse(self, response):
		#filename = response.url.split("/")[-1] + '.html'
		with open('core/cloned.html', 'wb') as f:
			f.write(response.body)

def Clone(url):
	process = CrawlerProcess()
	process.crawl(Cloner,start_urls=[url])
	process.start()