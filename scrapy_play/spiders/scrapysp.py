from scrapy.spider import Spider
from scrapy.http import Request

from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy_play.items import Post

import re


# command line:
# scrapy shell "https://apps.komen.org/forums/rss-m360601.ashx"
    # sel.xpath('//a[contains(@class, "forumlink")]').extract()
    # sel.xpath('//a[contains(@class, "forumlink")]/@href').extract()
    # sel.select('//select[contains(@name, "timefilterdd")]/option[position()>1]').extract()
    # hxs.select('//select/option[position()>1]/text()').extract()
    # select name contains timefilterdd
# cd /Users/lubagloukhov/GitHub/scrapy_play/scrapy_play
# scrapy crawl scrapy_play -o items2.json
# scrapy crawl scrapy_play # with pipeline



# class KomenSpider3(CrawlSpider):
class KomenSpider3(CrawlSpider):
    # follows to forum rss-feed and then message rss-feed, scrapes that
    # scrapes the messages. Uses <s>XMLFeedSpider</s>

    name = "scrapy_play"
    allowed_domains = ["apps.komen.org"]

    start_urls = [
        "https://apps.komen.org/Forums/",
    ]
    #
    rules = (
        Rule(LinkExtractor(allow=('forumid', )), follow= True),
        # from the start page, scrapy follows each forum id links
        # such as https://apps.komen.org/forums/tt.aspx?forumid=41
        # since no callback means follow=True by default
        Rule(LinkExtractor(allow=('rss-f', )), follow= True),
        Rule(LinkExtractor(allow=('fb.ashx', )), follow= True), #follow= True),
        Rule(LinkExtractor(allow=('rss-m', )), callback='parse_rss')
        # Rule(LinkExtractor(allow=('&p=', )), follow= True),
        # Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="paging"]',)), follow= True),
        # from each forum id link, scrapy follows to the rss link
        # such as https://apps.komen.org/forums/rss-f41.ashx
        # since no callback means follow=True by default
        # for some reason, rss feed not being followed

        # https://apps.komen.org/Forums/tt.aspx?forumid=41
        # https://apps.komen.org/Forums/tm.aspx?m=280617

        # Rule(LinkExtractor(allow=('fb.ashx', )), callback='parse_item'),
        # from each rss link, scrapy follows to the message link
        # and runs parse_item() on the message link
        # such as https://apps.komen.org/forums/fb.ashx?m=360440
    )

    def parse_rss(self, response):
        xxs = XmlXPathSelector(response)
        items = xxs.select('//item')
        title = xxs.select('//channel/title/text()').extract()[0]

        Iitems=[]
        for i in items:
            item = Post()
            item['title'] = title
            item['messURL'] = i.select('link/text()').extract()[0]
            item['subject'] = i.select('title/text()').extract()[0]
            item['message'] = i.select('description/text()').extract()[0]
            item['date'] = i.select('pubDate/text()').extract()[0]
            Iitems.append(item)
            # request = Request(url=urli[0], callback=self.parse1)
        return Iitems

    # def parse1(self, response):
    #     sel = HtmlXPathSelector(response)
    #
    #     items = []
    #     item = Post()
    #     item['messURL'] = response.url
    #     item['redirURL'] = response.request.meta['redirect_urls']
    #     item['refURL'] = response.request.headers.get('Referer', None)
    #     item['depth'] = response.meta["depth"]
    #
    #     u=item['messURL']
    #     idNum = re.findall('\d{6}', u)[0] # extract idNum (6 digit number) from url
    #
    #     # message contained in: div id="msg360440",
    #     item['message'] = ''.join(sel.xpath('//div[@id="msg%s"]/text()'%str(idNum)).extract()).strip().replace('\n', ' ').replace('\r', '').replace(u'\xa0', u' ')
    #     item['subject'] = ''.join(sel.xpath('//span[@id="subject%s"]/text()' %str(idNum)).extract()).strip().replace('\n', ' ').replace('\r', '').replace(u'\xa0', u' ')
    #     item['date'] =  ''.join(sel.xpath('//span[@id="date%s"]/text()' %str(idNum)).extract()).replace('\n', ' ').replace('\r', '').replace('-', '').replace(u'\xa0', u' ').strip()
    #
    #     items.append(item)
    #
    #     return items

#     def parse_forum(self, response):
#         """
#         The lines below is a spider contract. For more info see:
#         http://doc.scrapy.org/en/latest/topics/contracts.html
#         """
#         sel = Selector(response)
#
#         # urls = sel.xpath('//a[contains(@class, "forumlink")]/@href').extract()
#         # names = sel.xpath('//a[contains(@class, "forumlink")]/text()').extract()
#
#         # urls = sel.xpath('//a[contains(@href, ".aspx")]/@href').extract()
#         # names = sel.xpath('//a[contains(@href, ".aspx")]/text()').extract()
#         items = []
#         item = Post()
#         #item['messURL'] = response.url  # only returns 109 links. how does append work? over all paginations??
#                                         # could it be that new list is created for each RSS feed pagination
#                                         # scrape of rss feed gives 2149 links
#         item['maxPages'] = \
#             sel.xpath('//div[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_MessageList_BottomPager"]/text()').extract()
#
#         sel.xpath('//a[contains(@class, "paging")]')
#         sel.xpath('//a[contains(@href, "&p=")]')
#
#
    #
    # def parse_rss(self, response):
    #     """
    #     The lines below is a spider contract. For more info see:
    #     http://doc.scrapy.org/en/latest/topics/contracts.html
    #
    #     @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
    #     @scrapes name
    #     """
    #     sel = Selector(response)
    #
    #     # urls = sel.xpath('//a[contains(@class, "forumlink")]/@href').extract()
    #     # names = sel.xpath('//a[contains(@class, "forumlink")]/text()').extract()
    #
    #     # urls = sel.xpath('//a[contains(@href, ".aspx")]/@href').extract()
    #     # names = sel.xpath('//a[contains(@href, ".aspx")]/text()').extract()
    #     items = []
    #
    #     for i in sel.xpath('//item'):
    #         item = Post()
    #         #item['messURL'] = response.url
    #         #item['redirURL'] = response.request.meta['redirect_urls']
    #         #item['refURL'] = response.request.headers.get('Referer', None)
    #         #item['depth'] = response.meta["depth"]
    #
    #         item['subject'] = i.xpath('title/text()').extract()
    #         item['message'] = i.xpath('description/text()').extract()
    #         item['date'] = i.xpath('pubDate/text()').extract()
    #         item['link'] = i.xpath('link/text()').extract()
    #
    #         items.append(item)
    #
    #     return items
    #
    # def parse_item(self, response):
    #     """
    #     The lines below is a spider contract. For more info see:
    #     http://doc.scrapy.org/en/latest/topics/contracts.html
    #
    #     @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
    #     @scrapes name
    #     """
    #     sel = Selector(response)
    #
    #     # urls = sel.xpath('//a[contains(@class, "forumlink")]/@href').extract()
    #     # names = sel.xpath('//a[contains(@class, "forumlink")]/text()').extract()
    #
    #     # urls = sel.xpath('//a[contains(@href, ".aspx")]/@href').extract()
    #     # names = sel.xpath('//a[contains(@href, ".aspx")]/text()').extract()
    #     items = []
    #     item = Post()
    #     item['messURL'] = response.url  # only returns 109 links. how does append work? over all paginations??
    #                                     # could it be that new list is created for each RSS feed pagination
    #                                     # scrape of rss feed gives 2149 links
    #     item['redirURL'] = response.request.meta['redirect_urls']
    #     item['refURL'] = response.request.headers.get('Referer', None)
    #     item['depth'] = response.meta["depth"]
    #
    #     u=item['messURL']
    #     idNum = re.findall('\d{6}', u)[0] # extract idNum from url
    #
    #     # message contained in: div id="msg360440",
    #     item['message'] = ''.join(sel.xpath('//div[@id="msg%s"]/text()'%str(idNum)).extract()).strip().replace('\n', ' ').replace('\r', '').replace(u'\xa0', u' ')
    #
    #     # subject contained in: span id="subject360440"
    #     item['subject'] = ''.join(sel.xpath('//span[@id="subject%s"]/text()' %str(idNum)).extract()).strip().replace('\n', ' ').replace('\r', '').replace(u'\xa0', u' ')
    #     # date contained in <span id="date360440"
    #     item['date'] =  ''.join(sel.xpath('//span[@id="date%s"]/text()' %str(idNum)).extract()).replace('\n', ' ').replace('\r', '').replace('-', '').replace(u'\xa0', u' ').strip()
    #     # author info
    #     #item['authrURL'] = sel.xpath('//table[@id="msg_tbl%s"]/tr/td/a/@href'%str(idNum)).extract() #have to login to access link
    #     items.append(item)
    #     return items
