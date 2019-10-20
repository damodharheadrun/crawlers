import scrapy
from scrapy import *
import os
import sys
from hindunews.items import *
#import pdb;pdb.set_trace()
print(sys.path)
sys.path.insert(0,os.getcwd()+'/xpath')
import xpath


class hindunews(Spider):
    
    name="hindunews"
    start_urls=['https://www.thehindu.com/']

    def __init__(self):
        self.national_otherstorycardnews_headlines_url=[]
        self.national_storycardnews_headlines_urls=[]
        self.national_otherstorycardnews_headlines_url=[]
        self.national_news_headlines_url=[]

    def parse(self,response):
        #import pdb;pdb.set_trace()
        #print (response.body)
        sel=Selector(response)
        url=sel.xpath(xpath.url_xpath).extract()
        print(url)
        for url in url:
        	if "news" in url:
        		news_url=url
        yield Request(news_url, callback=self.parse_news_url,dont_filter=True)

    def parse_news_url(self,news_url):
        print (news_url.url)
        #print (news_url.body) 
        sel=Selector(news_url)
        different_news_urls=sel.xpath(xpath.different_news_xpath).extract()
        print(different_news_urls)
        for urls in different_news_urls:
            #import pdb;pdb.set_trace()
            if '/national' in urls:
                yield Request(url=urls,callback=self.parse_national_news_url,dont_filter=True)
            elif '/international' in urls:
                yield Request(url=urls,callback=self.parse_international_news_url,dont_filter=True)    
            elif '/state' in urls:
                yield Request(url=urls,callback=self.parse_states_news_url,dont_filter=True)
            elif '/cities' in urls:
                yield Request(url=urls,callback=self.parse_cities_news_url,dont_filter=True)
            elif '/multimedia' in urls:
                yield Request(url=urls,callback=self.parse_multimedia_news_url,dont_filter=True)
            elif '/entertainment' in urls:
                yield Request(url=urls,callback=self.parse_entertainment_news_url,dont_filter=True)
            elif '/sport' in urls:
                yield Request(url=urls,callback=self.parse_sports_news_url,dont_filter=True)
            elif '/business' in urls :
                yield Request(url=urls,callback=self.parse_business_news_url,dont_filter=True)
            elif '/science' in urls:
                yield Request(url=urls,callback=self.parse_science_news_url,dont_filter=True)
            elif '/health' in urls:
                yield Request(url=urls,callback=self.parse_health_news_url,dont_filter=True)
            elif '/technology' in urls:
                yield Request(url=urls,callback=self.parse_technology_news_url,dont_filter=True)
            elif '/education' in urls:
                yield Request(url=urls,callback=self.parse_education_news_url,dont_filter=True)
            else:
                print ("The url is not valid",urls) 

    def parse_national_news_url(self,national_news_page_url):
        #import pdb;pdb.set_trace()
        if national_news_page_url is not None:
            yield Request(url=national_news_page_url.url,callback=self.national_news_headlines_url,dont_filter=True)
        #import pdb;pdb.set_trace()    
        yield Request(url=national_news_page_url.url,callback=self.national_news_pagination,dont_filter=True)

    def national_news_pagination(self,national_news_page_url):
        #import pdb;pdb.set_trace()
        sel=Selector(national_news_page_url)
        self.national_news_nextpage_url=sel.xpath(xpath.news_pagination_xpath).extract()
        if self.national_news_nextpage_url:
            yield Request(url=self.national_news_nextpage_url[0],callback=self.parse_national_news_url,dont_filter=True)    

    def national_news_headlines_url(self,national_news_page_urls):
        #import pdb;pdb.set_trace()
        print("\n")
        print(national_news_page_urls.url)  
        sel=Selector(national_news_page_urls)
        self.national_storycardnews_headlines_urls=sel.xpath(xpath.national_storycard_new_xpath).extract() 
        self.national_otherstorycardnews_headlines_url=sel.xpath(xpath.national_otherstorycard_news_xpath).extract()
        if self.national_storycardnews_headlines_urls or self.national_otherstorycardnews_headlines_url:
            self.national_news_headlines_url=self.national_storycardnews_headlines_urls+self.national_otherstorycardnews_headlines_url
        for headlines_urls in self.national_news_headlines_url:
            yield Request(url=headlines_urls,callback=self.national_news_details,dont_filter=True)

    def national_news_details(self,headlines_url):
        sel=Selector(headlines_url)
        national_news_item=Hindu_national_newsItem()
        national_news_item['news_headlines']=(sel.xpath('//div[@class=" "]/h1/text()').extract())[0].strip("\n ")
        national_news_item['news_tagline']=sel.xpath(('//div[@class=" "]/h2/text()').extract())[0].strip("\n ")
        national_news_item['news_details']=''.join(data for data in sel.xpath('//div[@class=" "]/div[@id]/p/text()').extract()).strip(" ")
        national_news_item['country']=sel.xpath('//div[@class=" "]/div/div[@class="ut-container"]/span/text()').extract()[0].strip("\n, ")
        national_news_item['date']=sel.xpath('//div[@class=" "]/div/div[@class="ut-container"]/span/none/text()').extract()[0].strip("\n ")
        national_news_item['updated_at']=sel.xpath('//div[@class=" "]/div/div[@class="ut-container"]/div/span/none/text()').extract()[0].strip("\n ")




    def parse_international_news_url(self,international_news_url):
        pass

    def parse_entertainment_news_url(self,entertainment_news_url):
        pass    
    def parse_states_news_url(self,states_news_url):
        pass
    def parse_cities_news_url(self,cities_news_url):
        pass 
    def parse_multimedia_news_url(self,multimedia_news_url):
        pass 
    def parse_sports_news_url(self,sports_news_url):
        pass 
    def parse_business_news_url(self,business_news_url):
        pass 
    def parse_science_news_url(self,science_news_url):
        pass
    def parse_health_news_url(self,health_news_url):
        pass
    def parse_technology_news_url(self,technology_news_url):
        pass
    def parse_education_news_url(self,education_news_url):
        pass


                
                          
                    
                
                
                    
                    
        