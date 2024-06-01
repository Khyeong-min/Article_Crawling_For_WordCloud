import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import random
import time
from webdriver_manager.chrome import ChromeDriverManager

# 크롤링할 언론사 목록과 파일 경로 정의
press_type = ['조선일보', '중앙일보', '동아일보', '경향신문', '한겨레', 'KBS', 'MBC', 'SBS']
save_path = './data/'
base_path = './url/'
path_to_excel = 'NewsResult_20170101-20211231.xlsx'

# 주어진 경로의 엑셀 파일에서 특정 언론사의 URL 목록을 가져오는 함수
def get_url(path, press_type):
    df = pd.read_excel(path, sheet_name='sheet')
    url = df[df['언론사'] == press_type]['URL'].to_list()
    return url

# 영어를 제거하는 함수
def remove_english(text):
    return re.sub(r'\b[a-zA-Z]+\b', '', text)

# Chrome 드라이버 초기화 함수
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창을 표시하지 않음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver

# 주어진 URL을 사용하여 특정 언론사의 기사를 크롤링하는 함수
def fetch_article(driver, url, press):
    try:
        if press == '조선일보':
            return chosun_crawling(driver, url)
        elif press == '중앙일보':
            return joongang_crawling(driver, url)
        elif press == '동아일보':
            return donga_crawling(driver, url)
        elif press == '경향신문':
            return gyunghyang_crawling(driver, url)
        elif press == '한겨레':
            return hangr_crawling(driver, url)
        elif press == 'KBS':
            return kbs_crawling(driver, url)
        elif press == 'MBC':
            return mbc_crawling(driver, url)
        elif press == 'SBS':
            return sbs_crawling(driver, url)
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return None

# 각 언론사의 크롤링 함수 정의
def chosun_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h1', class_='article-header__headline | font--secondary text--black').getText()
    body = bs.find('section', class_='article-body').getText()
    full_text = title + ' ' + body
    return remove_english(full_text)

def joongang_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h1', class_='headline').getText().replace('\n', "")
    body = bs.find('div', class_='article_body fs3').findAll('p')
    body_text = " ".join([p.getText() for p in body])
    full_text = title + ' ' + body_text
    return remove_english(full_text)

def donga_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find_all('h1')[1].getText()
    body = bs.find('section', class_='news_view').getText()
    full_text = title + ' ' + body.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

def hangr_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h3', class_='ArticleDetailView_title__9kRU_').getText()
    body = bs.find_all('p', class_='text')
    body_text = " ".join([p.getText() for p in body])
    full_text = title + ' ' + body_text.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

def gyunghyang_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 5))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h1', class_='headline').getText()
    body = bs.find_all('p', class_='content_text')
    body_text = " ".join([p.getText() for p in body])
    full_text = title + ' ' + body_text.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

def kbs_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h4', class_='headline-title').getText()
    body = bs.find('div', class_='content-body__article').getText()
    full_text = title + ' ' + body.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

def sbs_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h1', class_='article_main_tit').getText()
    body = bs.find('div', class_='text_area').getText()
    full_text = title + ' ' + body.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

def mbc_crawling(driver, url):
    driver.get(url)
    time.sleep(random.uniform(1, 3))
    req = driver.page_source
    bs = BeautifulSoup(req, 'lxml')
    title = bs.find('h2', class_='art_title').getText()
    body = bs.find('div', class_='news_txt').getText()
    full_text = title + ' ' + body.replace("\n", "").replace("\r", "")
    return remove_english(full_text)

# 크롤링한 데이터를 저장하는 함수
def save(save_path, data):
    with open(save_path, 'w', encoding='UTF-8') as f:
        cnt = 1
        for i in data:
            f.write(str(cnt) + " " + i + '\n')
            cnt += 1

# 크롤링을 실행하는 메인 함수
def run(path, keyword, press):
    start_time = time.time()
    text_list = []
    url_list = get_url(path, press_type=press)
    cnt = 0

    driver = init_driver()

    for url in tqdm(url_list, desc="Crawling progress"):
        result = fetch_article(driver, url, press)
        if result:
            text_list.append(result)
        else:
            cnt += 1

    driver.quit()

    s_path = save_path + press + '_' + keyword + '.txt'
    save(s_path, text_list)
    running_time = (time.time() - start_time) / 60
    print("running_time: %.2f minutes" % running_time)

if __name__ == "__main__":
    keyword = '사건'
    path = base_path + 'NewsResult_20180101-20221231.xlsx'
    press = press_type[1]
    run(path, keyword, press)