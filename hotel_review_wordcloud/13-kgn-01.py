import time

from selenium import webdriver
driver = webdriver.Chrome('chromedriver.exe')
url = "https://hotel.naver.com/hotels/item?hotelId=hotel:Shilla_Stay_Yeoksam&destination_kor=%EC%8B%A0%EB%9D%BC%EC%8A%A4%ED%85%8C%EC%9D%B4%20%EC%97%AD%EC%82%BC&rooms=2/"
driver.get(url)
time.sleep(3)
review_name = []
review_article = []
for i in range(10):
    review = driver.find_elements_by_css_selector('div.article_wrap > ul > li')
    for i in review:
        name = i.find_element_by_css_selector('div.article_content > div > a')
        article = i.find_element_by_css_selector('div.article_content > div > p')
        if name.text !='':
            review_name.append(name.text)
        if article.text !='':
            review_article.append(article.text)
    driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/div[5]/div[4]/a[2]').click()
with open('hotel.txt', 'w', encoding='utf-8') as f:
    for i in range(len(review_name)):
        f.write(review_name[i]+','+review_article[i]+'\n')
