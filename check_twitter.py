from __future__ import absolute_import, unicode_literals
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from steganography.steganography import Steganography
import config
import os,re,requests
import chromedriver_binary

USER = config.USER
BASE_URL = config.BASE_URL
IMG_PATH = config.IMG_PATH

def get_twitter_elements(url, user):
    # ========== Headless Chrome実行 ========== #
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url + user)

    # ========== ツイート欄取得 ========== #
    elements = driver.find_elements_by_class_name("stream")
    return elements

# ========== 画像保存 ========== #
def dl_tweet_img(elems, dir_path):
    for url in get_img_urls(elems):
        path = dir_path + url.split("/")[-1]
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            with open(Path(path),"wb") as f:
                f.write(r.content)
            print("saved image...{}".format(url))
        else:
            print("HttpError:{0} at{1}".format(r.status_code,url))

# ========== 画像付きツイートのURLを探す ========== #
def get_img_urls(elems):
    urls = []
    for elem in elems:
        divs = elem.find_elements_by_class_name("AdaptiveMedia-photoContainer")
        for div in divs:
            urls.append(div.get_attribute("data-image-url"))
    return urls

# ========== 画像からテキストを抽出 ========== #
def extract_txt(dir_path):
    imgs = Path(dir_path).glob("**/*")
    for img in imgs:
        path = dir_path + os.path.basename(img)
        try:
            secret_text = Steganography.decode(path)
            print(secret_text)
            return secret_text
        except:
            print("Failed to extract from: {}".format(path))

def exec_txt(txt):
    print(txt)

def main():
    elements = get_twitter_elements(BASE_URL, USER)
    dl_tweet_img(elements, IMG_PATH)
    txt = extract_txt(IMG_PATH)
    exec_txt(txt)

if __name__ == "__main__":
    main()
