import re

from collections import  Counter
from selenium import webdriver
driver = webdriver.Chrome('./chromedriver.exe')
url = 'http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=4da'
driver.get(url)
preview = []
link = []
while True:
    select_link = driver.find_elements_by_css_selector('#main_contents > ul > li')
    for i in select_link:
        a = i.find_element_by_css_selector('div.detail > div.title > a').get_attribute('href')
        link.append(a)
    try:
        driver.find_element_by_css_selector('#main_contents > div:nth-child(6) > div.list_paging > a.btn_next').click()
    except:
        break
for i in link:
    driver.get(i)
    pre = driver.find_elements_by_css_selector('#container > div:nth-child(7) > div.content_left > div >div.box_detail_article')
    for j in pre:
        preview.append(j.text)
import pandas as pd
df = pd.DataFrame(preview)
df.to_csv('./kyobo_read.csv',encoding='utf-8')
for i in preview:
    print(i)
def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', text)
    return result
df[0] = df[0].apply(lambda x:text_cleaning(x))
content_corpus = "".join(df[0].tolist())
from konlpy.tag import Okt
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(content_corpus)
count = Counter(nouns)

remove_char_counter = Counter({x: count[x] for x in count if len(x) > 1})
korean_stopword = './korean_stopwords.txt'
with open(korean_stopword,encoding='utf-8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

work_stopwords = ['독자','상위','내용','기자','저자','이야기','베스트셀러','대한','가장','위해','작품','가지']
for word in work_stopwords:
    stopwords.append(word)
remove_char_counter = Counter({x: remove_char_counter[x] for x in count if x not in stopwords})
import pytagcloud
ranked_tag = remove_char_counter.most_common(50)
tag_list = pytagcloud.make_tags(ranked_tag,maxsize=60)
pytagcloud.create_tag_image(tag_list,'wordcloud.jpg',
                            size=(900,900),fontname='NanumBarunGothic',rectangular=False)
