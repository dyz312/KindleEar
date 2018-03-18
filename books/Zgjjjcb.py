#!/usr/bin/env python
# -*- coding:utf-8
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import datetime,re

def getBook():
    return Zgjjjcb

class Zgjjjcb(BaseFeedBook):
    title               = u'中国纪检监察报'
    description         = u'中央纪委监察部的机关报 | 版本0.2'
    language            = 'zh-cn'
    feed_encoding       = "utf-8"
    page_encoding       = "utf-8"
    mastheadfile        = "mh_gongshi.gif"
    coverfile           = 'cv_zgjjjcb.jpg'
    deliver_days        = []

    feeds = [
            ('Index', 'http://csr.mos.gov.cn/'),
           ]

    datetime_t = str(datetime.date.today()).split('-')  #对日期进行拆分，返回一个['2017', '10', '09']形式的列表

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        # mainurl = 'http://csr.mos.gov.cn/'
        #mainurl = 'http://csr.mos.gov.cn/content/' #url前缀
        #mainurl_add = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' #url前缀带日期
        #mainurl_add2 = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' + 'node_2.htm' #头版完整url

        mainurl_add = 'http://csr.mos.gov.cn/content/2018-03/17/'
        mainurl_add2 = 'http://csr.mos.gov.cn/content/2018-03/17/node_2.htm'
        urls = [] #保存返回的文章列表
        urladded = set() #用于防止文章重复，不用也可以
        opener = URLOpener(self.host)
        result = opener.open(mainurl_add2) #下载页面
        if result.status_code != 200:
            self.log.warn('fetch rss failed:%s'%mainurl)
            return []

        content = result.content.decode(self.feed_encoding) #解码
        soup = BeautifulSoup(content, "lxml") #生成BeautifulSoup对象，用来解析网页

        banmianmulu = soup.find('td',{'class':'mulu04'})

        for link in banmianmulu.find_all('a'):
            articles = []
            #if link is None:
            #    self.log.warn('link is empty')
            #    continue
            #sectitle = string_of_tag(link).strip()
            #if not sectitle:
            #    self.log.warn('link string is empty')
            #    continue
            #self.log.info('Found section: %s' % section_title)
            if 'pdf' in link['href']:
                continue

            soup = self.index_to_soup(self.mainurl_add + link['href'])
            vol_title = link.contents[0].strip()
            ul = soup.find('ul',{'class':'list01'})#抓取的正文链接框架部分

            # subsection = ''
            for link in ul.find_all('a'):
                title = self.tag_to_string(link)
                url = self.mainurl_add + link['href']
                urls.append((vol_title,title,url,None))

        return urls
