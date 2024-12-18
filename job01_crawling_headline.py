from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

# 뉴스 카테고리 정의
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# 데이터 저장을 위한 빈 데이터프레임 초기화
df_titles = pd.DataFrame()

# 각 카테고리에 대해 데이터 수집
for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)  # 카테고리별 URL 생성
    resp = requests.get(url)  # HTTP 요청
    soup = BeautifulSoup(resp.text, 'html.parser')  # HTML 파싱
    title_tags = soup.select('.sa_text_strong')  # 뉴스 제목 추출

    titles = []
    for title_tags in title_tags:
        title = re.compile('[^가-힣 ]').sub('', title_tags.text)  # 제목 정리 (한글과 공백만 유지)
        titles.append(title)

    # 데이터프레임 생성 및 카테고리 추가
    df_section_title = pd.DataFrame(titles, columns=['title'])
    df_section_title['category'] = category[i]

    # 기존 데이터에 현재 데이터 추가
    df_titles = pd.concat([df_titles, df_section_title], axis='rows', ignore_index=True)

# 데이터 확인 및 저장
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

# 결과 데이터 저장
df_titles.to_csv('./crawling.data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%y%m%d')), index=False)
