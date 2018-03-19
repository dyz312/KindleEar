#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import re
import datetime

def getBook():
    return Jijianjianchabao


class Jijianjianchabao(BaseFeedBook):
    title                 =  u'中国纪检监察报'
    description           =  u'中央纪委监察报机关报纸|ver:0.4.4.7'
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

    def page_to_soup(self, indexurl):
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(indexurl)
        if result.status_code != 200:
            self.log.warn('fetch mainnews failed:%s'%indexurl)

        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        return soup

    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        datetime_t = str(datetime.date.today()).split('-')  #对日期进行拆分，返回一个['2017', '10', '09']形式的列表
        # main = 'http://csr.mos.gov.cn/content/1/'
        mainurl = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' #url前缀带日期
        #mainurl = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' + 'node_2.htm' #头版完整url
        ans = []
        #urladded = set()
        # opener = URLOpener(self.host, timeout=90)
        # result = opener.open(mainurl + 'node_2.htm')
        soup1 = self.page_to_soup(mainurl + 'node_2.htm')
        #if result.status_code != 200:
        #    self.log.warn('fetch mainnews failed:%s'%mainurl)

        # content = result.content.decode(self.page_encoding)
        # soup = BeautifulSoup(content, "lxml")

        #开始解析
        mulu = soup1.find('td',{'class':'mulu04'})
        for banmian in mulu.find_all('a'):
            articles = []
            if 'pdf' in banmian['href']:
                continue
            wenzhangliebiao = self.page_to_soup(mainurl + banmian['href'])
            vol_title = banmian.contents[0].strip()
            ul = wenzhangliebiao.find('ul',{'class':'list01'})#抓取的正文链接框架部分

            for link in ul.find_all('a'):
                til = string_of_tag(link)
                url = mainurl + link['href']
                desc = ''
                #r = .find({'class':'title01'})
                #if r is not None:
                #    desc = self.tag_to_string(r)
                wz = {'fTitle':til, 'url' : url}
                #self.log.warn('href为：%s'%url)
                articles.append(wz)

            ans0 = (vol_title, wz)

            ans.append((vol_title,ans0,None))
                #urladded.add(url)

        if len(ans) == 0:
            self.log.warn('len of urls is zero.')
        return ans
