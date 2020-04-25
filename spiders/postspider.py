import scrapy
import pandas as pd

class PostSpider(scrapy.Spider):
    name = "posts"
    start_urls= [
        'https://blog.scrapinghub.com/page/1',
        'https://blog.scrapinghub.com/page/2',
    ]
    

    '''  parse the data with css  selectors  '''

    def parse(self, response):
        page= response.url.split('/')[-1]
        filename = 'posts-%s.csv'%page
        df = pd.DataFrame(columns=['Title','Date','Author', 'Link', 'Content'])

        for post in response.css('div.post-item'):
            postheader = post.css('.post-header')
            posttitle = postheader.css('h2 a::text').get()
            postbyline = postheader.css('.byline')
            postdate = postbyline.css('.date a::text').get()
            postauthor = postbyline.css('.author a::text').get()
            postContent = post.css('.post-content p ::text').get()
            postLink = postheader.css('h2 a::attr(href)').get()

            postdata = dict(Title = posttitle, Date = postdate, Author = postauthor, Link = postLink, Content = postContent)
            df = df.append(postdata, ignore_index=True)

       
        df.to_csv(filename)
        
    # '''  parse the data with xpath selectors  '''

    # def parse(self, response):
    #     page= response.url.split('/')[-1]
    #     filename = 'posts-%s.txt'%page

    #     with open(filename, "a") as myfile:
    #         for post in response.css('div.post-item'):
    #             postheader = post.css('.post-header')
    #             posttitle = postheader.css('h2 a::text').get()
    #             postbyline = postheader.css('.byline')
    #             postdate = postbyline.css('.date a::text').get()
    #             postauthor = postbyline.css('.author a::text').get()
    #             postContent = post.css('.post-content p ::text').get()
    #             postLink = postheader.css('h2 a::attr(href)').get()

    #             data = dict(title =posttitle ,date=postdate, author=postauthor, link= postLink, postContent=postContent)
    #             myfile.write("%s\n" % data)
            