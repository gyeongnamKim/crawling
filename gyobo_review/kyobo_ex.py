import time
import random
from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome("../text-mining/chromedriver.exe")
driver.get('http://www.kyobobook.co.kr/index.laf')
time.sleep(random.uniform(1,3))
# selected_tag = driver.find_elements_by_css_selector(\
#     "#header > div.navigation_bar > ul.gnb_sub > li:nth-child(1) > a")
# driver.switch_to.window(driver.window_handles[1]) # 팝업창을 선택
# driver.close() # 팝업창 삭제

# 베스트셀러 click
driver.find_element_by_xpath('//*[@id="header"]/div[3]/ul[2]/li[1]/a').click()

# 베스트셀러 초기 화면
selected_tag = driver.find_elements_by_css_selector(\
    #"#main_contents > ul")
    "#main_contents > ul > li")
time.sleep(random.uniform(4,7))
jemoks_list = []
urls_list = []
for item in selected_tag:
    #print(item)
    # 제목,  url
    jemok = item.find_element_by_css_selector("div.detail > div.title > a").text
    jemoks_list.append(jemok)
    link = item.find_element_by_css_selector("div.detail > div.title > a")
    print(link.get_attribute('href'))
    urls_list.append(str(link.get_attribute('href')))

print(urls_list)
print(len(urls_list))

# buttone test
# page repeat print
selected_button = driver.find_element_by_css_selector( \
    "#main_contents > div:nth-child(6) > div.list_paging > a.btn_next")
Next_page_flag = selected_button.is_enabled()
print(Next_page_flag)
time.sleep(5)
while Next_page_flag == True:
    print(" 계속 반복 ")
    time.sleep(1)
    try:
        # button click
        selected_button = driver.find_element_by_css_selector( \
            "#main_contents > div:nth-child(6) > div.list_paging > a.btn_next")

        # try:
        Next_page_flag = selected_button.is_enabled()
        selected_button.click()
        time.sleep(5)
        #----------------------
        selected_tags = driver.find_elements_by_css_selector( \
            # "#main_contents > ul")
            "#main_contents > ul > li")
        for item in selected_tags:
            # print(item)
            # 제목,  url
            jemok = item.find_element_by_css_selector("div.detail > div.title > a").text
            jemoks_list.append(jemok)
            link = item.find_element_by_css_selector("div.detail > div.title > a")
            print(link.get_attribute('href'))
            urls_list.append(str(link.get_attribute('href')))
    except:
        print("error exit")
        break
        # time.sleep(1)
print(len(urls_list))


#--------- selenium test -------- 1건
from selenium import webdriver
driver = webdriver.Chrome('../text-mining/chromedriver.exe')
print(urls_list[0])
driver.get(urls_list[0])
selected_class = driver.find_element_by_class_name('title_detail_basic2')
print(selected_class)
print(selected_class.tag_name)
print(selected_class.text)
selected_detail = driver.find_element_by_class_name('box_detail_article')
print(selected_detail)
print(selected_detail.tag_name)
print(selected_detail.text)

import pandas as pd
#--------------------------
#columns = ['title', 'content_text']
columns = ['content_text']
df = pd.DataFrame(columns=columns)
# for문 으로 여러건 작업
driver = webdriver.Chrome('../text-mining/chromedriver.exe')
for page_url in urls_list:
    print(type(page_url))
    driver.get(page_url)
    selected_detail = driver.find_element_by_class_name\
        ('box_detail_article')
    print(selected_detail)
    print(selected_detail.tag_name)
    print(selected_detail.text)
    content_corpus_list = selected_detail.text
    row = [content_corpus_list]
    series = pd.Series(row, index=df.columns)
    df = df.append(series, ignore_index=True)
df
df.head(5)
print(df.index)
print(df.columns)
df.info()

#------------------------------
import matplotlib.pyplot as plt
import re
# ### [텍스트 데이터 전처리]
# 텍스트 정제 함수 : 한글 이외의 문자는 전부 제거합니다.
def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글의 정규표현식을 나타냅니다.  '[^ ㄱ-ㅣ가-힣]+'
    result = hangul.sub('', text)
    return result
print(text_cleaning(df['content_text'][0]))
df['content_text'] = df['content_text'].apply\
    (lambda x: text_cleaning(x))
df.head(5)
# ### [말뭉치 만들기]
# 각 피처마다 말뭉치를 생성합니다.
content_corpus = "".join(df['content_text'].tolist())
print(content_corpus)
len(content_corpus)
# ### [konlpy를 이용한 키워드 추출]
from konlpy.tag import Okt
from collections import Counter
# konlpy의 형태소 분석기로 명사 단위의 키워드를 추출합니다.
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(content_corpus)
count = Counter(nouns)
count
type(count)
# 그래프 그리기
sr = pd.Series(count)
sr
sr.index
sr.values
plt.plot(sr.index, sr.values)

# ### [키워드 가다듬기]
# ##### 한글자 키워드 제거
# 한글자 키워드를 제거합니다.
remove_char_counter = Counter({x : count[x] for x in count if len(x) > 1})
print(remove_char_counter)
# ##### 불용어 제거
# 한국어 약식 불용어사전 예시 파일입니다. 출처 - (https://www.ranks.nl/stopwords/korean)
korean_stopwords_path = "./korean_stopwords.txt"
# 텍스트 파일을 오픈합니다.
with open(korean_stopwords_path, encoding='utf8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]
print(stopwords[:10])

# 키워드 데이터에서 불용어를 제거합니다.
remove_char_counter = Counter({x : remove_char_counter[x] for x in count if x not in stopwords})
print(remove_char_counter)

# # 워드 클라우드 시각화
# ### [pytagcloud 사용하기]

#    pip install pytagcloud pygame simplejson,
# - 그리고 아래와 같은 경로에 한글 폰트(예: NanumBarunGothic.ttf) 파일을 옮깁니다.
#     - Windosw OS : project 환경 \Lib\site-packages\pytagcloud\fonts
#     - `폰트 다운로드 : http://hangeul.naver.com/webfont \
#     /NanumGothic/NanumGothic.ttf`
#     - 위의 경로에서 fonts.json 파일을 편집합니다.
#     - 아래와 같은 코드를 추가하고 fonts.json 파일을 저장합니다.
#     - {
#                 "name": "NanumGothic",
#                 "ttf": "NanumGothic.ttf",
#                 "web": "http://fonts.googleapis.com \
#                 /css?family=Nanum+Gothic"
#         },
import random
import pytagcloud
import webbrowser
# 가장 출현 빈도수가 높은 80개의 단어를 선정합니다.
ranked_tags = remove_char_counter.most_common(80)
# 연습문제   - 80단어 그래프를 그리세요 ?

import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties\
        (fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

print(ranked_tags)
print(type(ranked_tags))
df = pd.DataFrame(ranked_tags,columns=['단어','횟수'])
df.set_index('단어',inplace=True)
df.head()
df.index
df.columns
df.head()
plt.figure()
df['횟수'].sort_values().plot(kind='barh',grid=True,figsize=(12,10))

# pytagcloud로 출력할 40개의 단어를 입력합니다. 단어 출력의 최대 크기는 80으로 제한합니다.
taglist = pytagcloud.make_tags(ranked_tags, maxsize=80)
# pytagcloud 이미지를 생성합니다. 폰트는 나눔 고딕을 사용합니다.
pytagcloud.create_tag_image(taglist, 'wordcloud-BOOK.jpg', \
 size=(900, 600), fontname='NanumGothic', rectangular=False)