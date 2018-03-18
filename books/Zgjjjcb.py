#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import re
import datetime

def getBook():
    return Zgjjjcb


class Zgjjjcb(BaseFeedBook):
    title                 =  u'中国纪检监察报'
    description           =  u'中央纪委监察报机关报纸|ver:0.3.0.5'
    language              = 'zh'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif"
    coverfile             = "cv_zgjjjcb.jpg"
    oldest_article        = 1
    # fulltext_by_readability = False
    # keep_image            =  True
    extra_css      = '''
        p { font-size: 1em; font-weight: 600;  text-align: justify;  line-height: 1.5 }
        h1 { font-size: large  }
        '''
    keep_only_tags = [dict(attrs={'class':'content'})]
    remove_classes = [dict(attrs={'class':'title04'})]
    #remove_tags_after = [
#    dict(attrs={'class':[
#            'pblsh'
#    ]})
#    ]


    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        datetime_t = str(datetime.date.today()).split('-')  #对日期进行拆分，返回一个['2017', '10', '09']形式的列表
        # main = 'http://csr.mos.gov.cn/content/1/'
        mainurl = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' #url前缀带日期
        #mainurl = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' + 'node_2.htm' #头版完整url
        urls = []
        urladded = set()
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(mainurl + 'node_2.htm')
        if result.status_code != 200:
            self.log.warn('fetch mainnews failed:%s'%main)

        content = result.content.decode(self.page_encoding)
        soup = BeautifulSoup(content, "lxml")

        #开始解析
        mulu = soup.find('td',{'class':'mulu04'})
        for banmian in mulu.find_all('a'):
            if 'pdf' in banmian['href']:
                continue
                soup = self.index_to_soup(self.mainurl + banmian['href'])
                vol_title = banmian.contents[0].strip()
                ul = soup.find('ul',{'class':'list01'})#抓取的正文链接框架部分

                for link in ul.findAll('a'):
                    til = self.tag_to_string(link)
                    url = self.mainurl + link['href']
                    urls.append((vol_title,til,url,None))
                    urladded.add(url)

        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
