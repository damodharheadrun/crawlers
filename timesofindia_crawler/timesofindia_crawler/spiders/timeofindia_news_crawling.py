import scrapy
from scrapy import *
import os
import sys
import hashlib
from timesofindia_crawler.items import *
#import pdb;pdb.set_trace()
print(sys.path)
import datetime
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class timeofindia_news_crawling(Spider):

    name ="timesofindianews"
    start_urls=["https://timesofindia.indiatimes.com"]
    state='West-Bengal'


    def parse(self,response):
        #import pdb;pdb.set_trace()
        for url in self.start_urls:
            state_url=url+''.join(response.xpath(xpath.state_url_xpath%self.state).extract())
        yield Request(url=state_url, callback=self.parse_url,dont_filter=True)


    def pagination_url(self,page_url):
        #import pdb;pdb.set_trace()
        sel=Selector(page_url)
        next_pages=sel.xpath(xpath.pagination_xpath).extract()
        for url in next_pages:
            next_pages_url=self.start_urls[0]+url
            yield Request(url=next_pages_url,callback=self.parse_headlines_url,dont_filter=True)

    def parse_url(self,state_link):
        #import pdb;pdb.set_trace()
        print (state_link.url)
        yield Request(url =state_link.url,callback=self.pagination_url,dont_filter=True)
        yield Request(url=state_link.url,callback=self.parse_headlines_url,dont_filter=True)         

    def parse_headlines_url(self,pages):
        print(pages.url)
        sel=Selector(pages)
        news_headline_url=sel.xpath(xpath.news_headlines_url_xpath).extract()
        for headline_url in news_headline_url:
            news_headlines_link=self.start_urls[0]+headline_url
            yield Request(url=news_headlines_link,callback=self.scrape_new_details,dont_filter=True)

    def scrape_new_details(self,headlines_link):
        print (headlines_link.url)  
        sel=Selector(headlines_link)
        state_news_item=TimesofindiaCrawlerItem()
        state_news_item['state']=self.state
        state_news_item['news_headlines']=sel.xpath(xpath.national_news_headlines_xpath).extract()
        if state_news_item['news_headlines']:
            state_news_item['news_headlines']=''.join(state_news_item['news_headlines']).strip("\n ").encode('ascii','ignore')
        else:
            state_news_item['news_headlines']='None'    
        state_news_item['news_tagline']=sel.xpath(xpath.national_news_tagline_xpath).extract()
        if state_news_item['news_tagline']:
            state_news_item['news_tagline']=state_news_item['news_tagline'][0].strip("\n ").encode('ascii','ignore')  
        else:
            state_news_item['news_tagline']='None'                   
        state_news_item['news_details']=''.join(data for data in sel.xpath(xpath.national_news_details_xpath).extract()).strip(" ").encode('ascii','ignore')
        if state_news_item['news_details']=="":
            state_news_item['news_details']=''.join(data for data in sel.xpath(xpath.national_news_details_alternative_xpath).extract()).strip(" ").encode('ascii','ignore')
        state_news_item['country']=sel.xpath(xpath.national_news_country_xpath).extract()[0].strip("\n,: ").encode("ascii",'ignore')
        state_news_item['news_date']=''.join(sel.xpath(xpath.national_news_date_xpath).extract()).strip("\n ").encode("ascii",'ignore')
        state_news_item['news_updated_at']=''.join(sel.xpath(xpath.national_news_updatedDate_xpath).extract()).strip("\n ").encode("ascii",'ignore')
        state_news_item['news_url']=headlines_url.url
        state_news_item['sk_key']=hashlib.md5(headlines_url.url.encode()).hexdigest()
        state_news_item['dump_updated_at']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield state_news_item              