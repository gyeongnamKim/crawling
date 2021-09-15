import re
from collections import Counter

file = open("hotel.txt", "r", encoding='utf-8')
data = file.read()
def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', text)
    return result
data = text_cleaning(data)
from konlpy.tag import Okt
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(data)
count = Counter(nouns)

remove_char_counter = Counter({x: count[x] for x in count if len(x) > 1})
korean_stopword = './korean_stopwords.txt'
with open(korean_stopword,encoding='utf-8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

work_stopwords = ['스테이','신라','역삼','호텔','리뷰','후기','블룸']
for word in work_stopwords:
    stopwords.append(word)
remove_char_counter = Counter({x: remove_char_counter[x] for x in count if x not in stopwords})
import pytagcloud
ranked_tag = remove_char_counter.most_common(100)
tag_list = pytagcloud.make_tags(ranked_tag,maxsize=150)
pytagcloud.create_tag_image(tag_list,'wordcloud.jpg',
                            size=(900,900),fontname='NanumBarunGothic',rectangular=False)
file.close()