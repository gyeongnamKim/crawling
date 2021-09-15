import random
import re

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
driver = webdriver.Chrome('../text-mining/chromedriver.exe')
url = 'https://www.naver.com'
driver.get(url)
class naver_start:
    total = {'title':[],'writer':[],'date':[],'article_type':[],\
             'preview':[],'write_url':[],'detail':[]}
    def __init__(self,id,pw):
        self.id = id
        self.pw = pw
    def login_naver(self):
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="account"]/a').click()
        pyperclip.copy(self.id)
        driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.CONTROL, 'v')
        pyperclip.copy(self.pw)
        driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.CONTROL, 'v')
        driver.find_element_by_xpath('//*[@id="log.login"]').click()
    def myfeed_in(self):
        self.login_naver()
        time.sleep(1)
        driver.get('https://myfeed.naver.com/index.nhn')
        last_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(random.uniform(1.5, 2))
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1.5, 2))
            new_height = last_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    def myfeed_read(self):
        self.myfeed_in()
        temp = driver.find_elements_by_css_selector('#container > div.section._section > div.contents._contents > div.thrd_contents._news_box > div.lst_area._lst_area > ul > li')
        for i in temp:
            self.total['title'].append(i.find_element_by_css_selector('div > div > div > h4 > a').text)
            self.total['writer'].append(i.find_element_by_css_selector('div > div > div > p > span.h_title > a').text)
            self.total['date'].append(i.find_element_by_css_selector('div > div > div > h4 > span').text)
            self.total['article_type'].append(i.find_element_by_css_selector('div > div > div > p > span.svc_name > a').text)
            self.total['preview'].append(i.find_element_by_css_selector('div > div > div > div > p > a').text)
            self.total['write_url'].append(i.find_element_by_css_selector('div > div > div > h4 > a').get_attribute('href'))
        self.write_detail()
    def write_detail(self):
        for i in self.total['write_url']:
            driver.get(i)
            ex = driver.find_elements_by_css_selector('div.se_component_wrap.sect_dsc.__se_component_area > div')
            text = ''
            for j in ex:
                a = str(j.get_attribute("innerText"))
                text += a.replace('\n',' ')
            self.total['detail'].append(text)
    def text_cleaning(self):
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        result = hangul.sub('', self.total['preview'])
        result2 = hangul.sub('',self.total['detail'])
        return result,result2
my = naver_start('y3ef95','!rudska1885')
my.myfeed_read()
df = pd.DataFrame(my.total)
df.columns = ['제목','작성자','작성날짜','종류','미리보기내용','URL 정보','정보상세내역']
df.to_csv('./crawl.csv',index=False)