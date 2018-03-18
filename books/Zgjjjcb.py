#!/usr/bin/env python
# -*- coding:utf-8
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
from calibre.web.feeds.recipes import BasicNewsRecipe
# import datetime,re

def getBook():
    return Zgjjjcb

class Zgjjjcb(BaseFeedBook):
    title               = u'中国纪检监察报'
    description         = u'中央纪委监察部的机关报 | 版本0.2.4'
    language            = 'zh-cn'
    feed_encoding       = "utf-8"
    page_encoding       = "utf-8"
    mastheadfile        = "mh_gongshi.gif"
    coverfile           = 'cv_zgjjjcb.jpg'
    deliver_days        = []

    no_stylesheets = True #不采用页面样式表
    keep_only_tags = [{ 'class': 'content' }] #保留的正文部分
    remove_tags = [{'class' : 'title04'}]


    mainurl_add = 'http://csr.mos.gov.cn/content/2018-03/17/'
    mainurl_add2 = 'http://csr.mos.gov.cn/content/2018-03/17/node_2.htm'
    #datetime_t = str(datetime.date.today()).split('-')  #对日期进行拆分，返回一个['2017', '10', '09']形式的列表

      def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        # mainurl = 'http://csr.mos.gov.cn/'
        #mainurl = 'http://csr.mos.gov.cn/content/' #url前缀
        #mainurl_add = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' #url前缀带日期
        #mainurl_add2 = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' + 'node_2.htm' #头版完整url


        soup = self.index_to_soup(self.mainurl_add2)
        banmianmulu = soup.find('td',{'class':'mulu04'}) #可以有多个属性，比如'table',{'cellpadding':'2','width':'100%'}

        ans0 = []
        #下面的for循环用soupfind找到各版面的url并生成列表，带pdf的链接抛弃
        for link in banmianmulu.find_all('a'):
            articles = []
            if 'pdf' in link['href']:
                continue
            soup = self.index_to_soup(self.mainurl_add + link['href'])
            vol_title = link.contents[0].strip()
            ul = soup.find('ul',{'class':'list01'})#抓取的正文链接框架部分

            for link in ul.findAll('a'):
                videolink = re.compile(r'src="')
                vlinkfind = videolink.find_all(str(link))

                if not vlinkfind:
                    til = self.tag_to_string(link)
                    url = self.mainurl_add + link['href']
            #        a = { 'title':til , 'url': url }

            #        articles.append(a)

            ans = (vol_title, til, url, None)

            ans0.append(ans)

        return ans0
