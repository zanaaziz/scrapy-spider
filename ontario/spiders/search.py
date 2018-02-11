from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.loader import ItemLoader
from ontario.items import Member

class SearchSpider(Spider):
	name = 'search'
	allowed_domains = ['collegeoftrades.ca']
	start_urls = ['http://collegeoftrades.ca/public-register-search']
	
	def parse(self, response):
		for member in range(13167840, 13168840):
			yield FormRequest.from_response(response, formname = 'frmSearch', formdata = {'tbSearch': str(member)}, callback = self.member_page)

	def member_page(self, response):
		l = ItemLoader(item = Member(), response = response)

		member_name = response.xpath('//tr[@class="ocot-memberHover ocot-table-tr"]/td[2]/text()').extract_first()

		for c in ['\t', '\n']:
			if c in member_name:
				member_name = member_name.replace(c, '')

		l.add_xpath('member_id', '//tr[@class="ocot-memberHover ocot-table-tr"]/td/a[@href="javascript:void(0);"]/text()')
		l.add_value('member_name', member_name)
		l.add_xpath('member_trade', '//tr[@class="ocot-memberHover ocot-table-tr"]/td/span[@style="white-space:nowrap;"]/text()')
		
		return l.load_item()