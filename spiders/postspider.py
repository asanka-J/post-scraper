import scrapy
import pandas as pd

class PostSpider(scrapy.Spider):
    name = "posts"
    start_urls= [
        'https://blog.scrapinghub.com/page/1',
        'https://blog.scrapinghub.com/page/2',
    ]
    
    '''  parse the data with with python generators  '''
    def parse(self, response):
        '''
        crawls the data : use following format to run the crawler 
        scrapy crawl posts -o [filename].[filetype] 
        '''
    
        for post in response.css('div.post-item'):
            postheader = post.css('.post-header')
            postbyline = postheader.css('.byline')

            yield {
                'postdate' : postbyline.css('.date a::text').get(),
                'posttitle' : postheader.css('h2 a::text').get(),
                'postauthor' : postbyline.css('.author a::text').get(),
                'postContent' : post.css('.post-content p ::text').get(),
                'postLink' : postheader.css('h2 a::attr(href)').get()
            }



class PostDFdSpider(scrapy.Spider):
    name = "postDF"
    start_urls= [
        'https://blog.scrapinghub.com/page/1',
        'https://blog.scrapinghub.com/page/2',
    ]
    
    '''  parse the data with css  selectors and pd dataframes  '''
    def parse(self, response):
        '''
        crawls the data,manupulate with pd dataframes and save as csv: use following format to run the crawler 
        scrapy crawl postDF  
        '''
    
        page= response.url.split('/')[-1]
        filename = 'posts-%s.csv'%page
        df = pd.DataFrame(columns=['Title','Date','Author', 'Link', 'Content'])

        for post in response.css('div.post-item'):
            postheader = post.css('.post-header')
            postbyline = postheader.css('.byline')

            posttitle = postheader.css('h2 a::text').get()
            postdate = postbyline.css('.date a::text').get()
            postauthor = postbyline.css('.author a::text').get()
            postContent = post.css('.post-content p ::text').get()
            postLink = postheader.css('h2 a::attr(href)').get()

            postdata = dict(Title = posttitle, Date = postdate, Author = postauthor, Link = postLink, Content = postContent)
            df = df.append(postdata, ignore_index=True)
        df.to_csv(filename)
        