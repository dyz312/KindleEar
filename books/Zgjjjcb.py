#!/usr/bin/env python
# -*- coding:utf-8
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
# import datetime,re

def getBook():
    return Zgjjjcb

class Zgjjjcb(BaseFeedBook):
    title               = u'中国纪检监察报'
    description         = u'中央纪委监察部的机关报 | 版本0.2.3'
    language            = 'zh-cn'
    feed_encoding       = "utf-8"
    page_encoding       = "utf-8"
    mastheadfile        = "mh_gongshi.gif"
    coverfile           = 'cv_zgjjjcb.jpg'
    deliver_days        = []

    '''
    feeds = [
            ('Index', 'http://csr.mos.gov.cn/'),
           ]
    '''

    mainurl_add = 'http://csr.mos.gov.cn/content/2018-03/17/'
    mainurl_add2 = 'http://csr.mos.gov.cn/content/2018-03/17/node_2.htm'
    #datetime_t = str(datetime.date.today()).split('-')  #对日期进行拆分，返回一个['2017', '10', '09']形式的列表

   '''
    def FetchDesc(self, url):
        opener = URLOpener(self.host, timeout=60)
        result = opener.open(url)
        if result.status_code != 200:
            self.log.warn('fetch article failed(%d):%s.' % (status_code, url))
            return None
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, 'lxml')
        abstract = unicode(soup.find('div', attrs={'class': 'title01'}))
        article = unicode(soup.find(id='contents'))
        '''
        '''
        pagelist = soup.find('ul', attrs={'class': 'pagelist'})
        if pagelist and pagelist.find('li'):
            page_count_context = pagelist.a.text
            page_count = int(
                page_count_context[1:page_count_context.index(u'页')])
            for i in range(2, page_count + 1):
                page_url = url[:-5] + "_%d.html" % i
                result = opener.open(page_url)
                if result.status_code != 200:
                    self.log.warn(
                        'fetch page failed(%d):%s.' % (status_code, page_url))
                    return None
                content = result.content.decode(self.feed_encoding)
                pagesoup = BeautifulSoup(content, 'lxml')
                article += unicode(pagesoup.find(id='contents'))
        '''
        # return abstract + article

    def ParseFeedUrls(self):
        """ return list like [(section,title,url,desc),..] """
        # mainurl = 'http://csr.mos.gov.cn/'
        #mainurl = 'http://csr.mos.gov.cn/content/' #url前缀
        #mainurl_add = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' #url前缀带日期
        #mainurl_add2 = 'http://csr.mos.gov.cn/content/' + datetime_t[0] + '-' + datetime_t[1] + '/' + datetime_t[2] + '/' + 'node_2.htm' #头版完整url

        '''
        urls = [] #保存返回的文章列表
        # urladded = set() #用于防止文章重复，不用也可以

        opener = URLOpener(self.host, timeout=60)
        result = opener.open(mainurl_add2) #下载页面
        if result.status_code != 200:
            self.log.warn('fetch rss failed:%s'%mainurl)
            return []

        content = result.content.decode(self.feed_encoding) #解码
        soup = BeautifulSoup(content, "lxml") #生成BeautifulSoup对象，用来解析网页

        banmianmulu = soup.find('td',{'class':'mulu04'})

        for pagelink in banmianmulu.find_all('a', attrs={'id': ['pageLink']}):
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

            #soup = self.index_to_soup(self.mainurl_add + link['href'])
            vol_title = pagelink.contents[0].strip()
            ul = soup.find('ul',{'class':'list01'})#抓取的正文链接框架部分

            # subsection = ''
            for link in ul.find_all('a'):
                title = self.tag_to_string(link)
                url = self.mainurl_add + link['href']
                urls.append((vol_title,title,link.a['href'],self.FetchDesc(link.a['href']),None))

        return urls
        '''

        soup = self.index_to_soup(self.url_prefix_add2)
        banmianmulu = soup.find('td',{'class':'mulu04'}) #可以有多个属性，比如'table',{'cellpadding':'2','width':'100%'}

        ans0 = []
        #下面的for循环用soupfind找到各版面的url并生成列表，带pdf的链接抛弃
        for link in banmianmulu.findAll('a'):
            articles = []
            if 'pdf' in link['href']:
                continue
            soup = self.index_to_soup(self.url_prefix_add + link['href'])
            vol_title = link.contents[0].strip()
            ul = soup.find('ul',{'class':'list01'})#抓取的正文链接框架部分

            for link in ul.findAll('a'):
                videolink = re.compile(r'src="')
                vlinkfind = videolink.findall(str(link))

                if not vlinkfind:
                    til = self.tag_to_string(link)
                    url = self.mainurl_add + link['href']
            #        a = { 'title':til , 'url': url }

                    articles.append(a)

            ans = (vol_title, til, url, None)

            ans0.append(ans)

        return ans0
