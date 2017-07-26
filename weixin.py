# -*- coding:utf-8 -*-

'''
----------------------------------------------------------
__datatime__:2017-07-15
__author:__: keal
__purpose__:利用selenium 和PhantomJS 爬取搜狗微信公众号
-----------------------------------------------------------
'''

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time,re,os
import pymysql
class gong_zhong_hao_spider(object):
    def __init__(self,gzh='python6359'):
        self.name=gzh
        self.headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}

    #获取需要爬取的公众号网站入口地址
    def get_entrance(self):
        home_url='http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=y&_sug_type_=,'%self.name
        html = BeautifulSoup(requests.get(home_url, headers=self.headers, timeout=3).text, 'html.parser')
        entrance_url= html.find('p', class_='tit').find('a', target='_blank').get('href')
        return entrance_url

    #利用Selenium和PhantomJS渲染网页JS
    def parse_url(self,entrance_url):
        browser = webdriver.PhantomJS()
        browser.get(entrance_url)
        time.sleep(3)
        html = browser.execute_script("return document.documentElement.outerHTML")#执行js语句，得到整个网页的DOM
        return html

    #获取所有文章地址等信息,同时调用存入数据库和保存网页的函数
    def get_data(self,html):
        articles={}
        bs = BeautifulSoup(html, 'html.parser')
        article_urls = (bs.find_all('div', class_='weui_media_bd'))
        for article in article_urls:
            articles['source_url']='https://mp.weixin.qq.com'+article.find('h4',class_='weui_media_title').get('hrefs').replace('&amp','&')
            articles['title']=article.find('h4', class_='weui_media_title').string.strip()
            articles['summary']=article.find('p', class_='weui_media_desc').string
            articles['datetime']=article.find('p', class_='weui_media_extra_info').string
            articles['local_address']='E:\gongzhonghao\%s\%s.html'%(self.name,articles['title'])
            self.log('准备将数据存入数据库')
            self.store_into_db(articles)
            self.store_page(articles['source_url'],articles['title'])

    #将需要的数据存入数据库
    def store_into_db(self,articles):
        db=pymysql.connect(host='localhost',port=3306,user='root',password='739535841',db='weixin',charset='utf8')
        cursor=db.cursor()
        sql='INSERT INTO gz_hao(title,datetime,source_url,local_address,summary)VALUES(%s,%s,%s,%s,%s)'
        a,b,c,d,e=articles['title'],articles['datetime'],articles['source_url'],articles['local_address'],articles['summary']
        cursor.execute(sql,(a,b,c,d,e))
        db.commit()
        self.log('存入数据成功')
    #将网页保存到本地
    def store_page(self,url,title):
        path='E:\gongzhonghao\%s'%self.name
        if not os.path.exists(path):
            os.makedirs(path)
        file_name='%s\%s.html'%(path,title)
        html=self.parse_url(url)
        with open(file_name,'w',encoding='utf-8')as f:
            f.write(html)
        self.log('网页保存成功')

    def log(self,msg):
        print('%s,%s'%(time.strftime('%Y-%m-%d %H:%M:%S'),msg))

    def run(self):
        self.log('开始尝试爬取公众号')
        entrance=self.get_entrance()
        self.log('进入到公众号首页，开始爬取公众号文章')
        html=self.parse_url(entrance)
        self.get_data(html)
        self.log('爬取完毕')

if __name__ =='__main__':
    name=input('请输入准确的微信公众号，否则将爬取搜索结果的第一个公众号内容，默认爬取Python6359')
    gong_zhong_hao_spider().run()
