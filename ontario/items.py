from scrapy import Item
from scrapy import Field

class Member(Item):
    member_id = Field()
    member_name = Field()
    member_trade = Field()