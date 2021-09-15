import pandas as pd
import urllib.request as req    # url 주소 열어주는 함수
from bs4 import BeautifulSoup as BS # HTML파일 태그 검색
#데이터를 담을 리딕셔너리형 리스트 초기화
movie_review = {'영화제목':[],'별점':[],'감상평':[]}
#영화리뷰 1 ~ 10 페이지만 크롤링 하기위해 for문 사용
for i in range(1,11):
    url = 'https://movie.naver.com/movie/point/af/list.nhn?&page='+ str(i)
    data1 = req.urlopen(url)
    response = data1.read()
    soup = BS(response,'html.parser')
    soup_tbody = str(soup.select('tbody'))
    soup_tbody = BS(soup_tbody,'html.parser')
    titles = soup_tbody.select('.movie')
    stars = soup_tbody.select('em')
    reviews = soup_tbody.select('td.title')
    for title in titles:
        movie_review['영화제목'].append(title.text)
    for star in stars:
        movie_review['별점'].append(star.text)
    for review in reviews:
        movie_review['감상평'].append(review.contents[6].strip())
for i in range(len(movie_review['영화제목'])):
    print('영화 제목 :',movie_review['영화제목'][i])
    print('영화 별점 :',movie_review['별점'][i])
    print('영화 리뷰 :',movie_review['감상평'][i])
    print('-'*70)

#csv 형태로 저장
movie_review = pd.DataFrame(movie_review)
movie_review.to_csv('./movie_review_result.csv')