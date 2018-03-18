#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import re
import datetime

def getBook():
    return Reuters


class Reuters(BaseFeedBook):
    title                 = 'NK News'
    description           = 'News on North Korea'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif"
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
#    deliver_days          = ['Friday']
#    deliver_times         = [18]
    fulltext_by_readability = False
    keep_image            =  False

    keep_only_tags = [
                      dict(attrs={'class':['post-heading','post-subheading']}),
                      dict(id='fullContent')
                     ]

    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'https://www.nknews.org/'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []

        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")

        #开始解析
        def is_cls_wanted(css_class):
            listwanted = ['col-md-7','post-prinicap-row','col-md-12','col-md-6 smallboxclass']
            return css_class in listwanted
#        def not_has_class(tag):
#            return not tag.has_attr('class')
        for section in soup.find_all(class_=is_cls_wanted, limit=8):
            article = section.find('a', string=True)
            title = string_of_tag(article).strip()
            url = article['href']
            if '/pro/' in url:
                continue
            span = article.find('span')
            strong = span.find('strong')
            if not strong:
                timestamp = span
            else:
                timestamp = strong
            timestamp = string_of_tag(timestamp).strip()
            m = re.search(r'\d{4}$', timestamp)
            if m:
                pubtime = datetime.datetime.strptime(timestamp, '%d %B %Y').date()
            else:
                m2 = re.search(r'^\d', timestamp)
                if m2:
                    pubtime = datetime.datetime.strptime(timestamp, '%d %B').date()
                else:
                    pubtime = datetime.datetime.strptime(timestamp, '%B %d').date()

            tnow = datetime.datetime.utcnow()
            tnow = tnow.date()
            delta=(tnow-pubtime).days
            if self.oldest_article > 0 and delta > self.oldest_article:
                continue
                #self.log.info('\tFound article:%s' % title)
            urls.append(('NK News',title,url,None))
        if len(urls) == 0:
            self.log.warn('NK News has no article.')
        return urls

    extra_css= '''
    .post-subheading {font-size: large; font-weight: bold}
    .post-heading {font-size: large; font-weight: bold}
    '''
