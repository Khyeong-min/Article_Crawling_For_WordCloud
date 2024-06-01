import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import pandas as pd
from konlpy.tag import Okt

line = []

# 텍스트 읽어오기
f1 = open("조선일보_아동학대.txt", 'rt', encoding='utf-8')
lines = f1.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f1.close()

f2 = open("동아일보_아동학대.txt", 'rt', encoding='utf-8')
lines = f2.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f2.close()

f3 = open("중앙일보_아동학대.txt", 'rt', encoding='utf-8')
lines = f3.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f3.close()

f4 = open("한겨레_아동학대.txt", 'rt', encoding='utf-8')
lines = f4.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f4.close()

f5 = open("MBC_아동학대.txt", 'rt', encoding='utf-8')
lines = f5.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f5.close()

f6 = open("SBS_아동학대.txt", 'rt', encoding='utf-8')
lines = f6.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f6.close()

f7 = open("경향신문_아동학대.txt", 'rt', encoding='utf-8')
lines = f7.readlines()
for i in range(len(lines)):
    line.append(lines[i])
f7.close()

# 특수문자 제거하기
compile = re.compile("[^ ㄱ-ㅣ가-힣]+")
for i in range(len(line)):
    a = compile.sub("", line[i])
    line[i] = a


# 문장분석-> 명사만 추출
okt = Okt()
result = []
result = [okt.nouns(i) for i in line]  # 명사만 추출
final_result = []
for i in result:
    for r in i:
        if len(r) > 1:
            final_result.append(r)
print(final_result)

# 텍스트 빈도수 별로 정렬
korean = pd.Series(final_result).value_counts()
korean.to_csv('text_crawled_정인이.txt')


f_in = open('text_crawled_정인이.txt', 'r', encoding='utf-8')
print(f_in)

before_wordcloud_dict = {}
for i, line in enumerate(f_in):
    if i >= 7:
        count = 0
        for letter in line:
            if letter != ',':
                count += 1
            else:
                break
        key = line[0:count]
        value = line[count+1:-1]
        before_wordcloud_dict[key] = float(value)

print(before_wordcloud_dict)

wc = WordCloud(background_color="white", max_words=100, width=1000, height=800, font_path='C:/Windows/Fonts/malgun.ttf')
plt.figure(figsize=(30, 30))

wc = wc.generate_from_frequencies(before_wordcloud_dict)
plt.imshow(wc)
plt.axis('off')
plt.show()