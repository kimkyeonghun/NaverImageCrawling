import base64
import os
import re
from typing import *
import time
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import urllib.parse as rep
import urllib.request as req

class NaverImageCrawling():
    def __init__(self):
        #self.driverPath='path/to/your/chromedriver'
        self.driver_path='./webdriver/chrome/chromedriver.exe'
        self.save_path="./imageDownload"

    def make_download_folder(self, path: str):
        #저장경로 만들기
        if path:
            self.save_path=path
        try:
            if not (os.path.isdir(self.save_path)):
                os.makedirs(os.path.join(self.save_path))
                print("Success to make Folder!")
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Fail to make Folder!")
                raise
    
    def base64decoding(self,link,fullfile_name):
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", link, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")
        else:
            raise Exception("Do not parse!")
        img = base64.urlsafe_b64decode(data)
        file_name = "{}.{}".format(fullfile_name,ext)
        with open(file_name,"wb") as f:
            f.write(img)

    def selenium_option(self):
        options =webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(self.driver_path, chrome_options = options)
        driver.implicitly_wait(2)
        return driver

    def download_image(self, keyword: str, cnt: int, path: str):
        """
            keyword : 검색어
            cnt : 해당 검색어로 크롤링할 이미지의 갯수
            path : 크롤링한 이미지를 다운 받을 폴더 경로 지정, default로는 현재 py 파일이 있는 폴더에 imageDownload를 생성함
        """

        if cnt <=0:
            assert False, "cnt must be over 0"
        
        self.make_download_folder(path)

        #selenium Option 설정
        driver = self.selenium_option()

        #네이버 접속
        base = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
        quote = rep.quote_plus(keyword)
        url = base+quote
        driver.get(url)

        print("\n******************Download Start")
        count=0
        for c in tqdm(range(cnt),desc="Iterable"):
            count += 1
            try:
                img=driver.find_element_by_xpath('//*[@id="main_pack"]/section/div/div[1]/div[1]/div[{}]/div/div[1]/a/img'.format(count))
                driver.implicitly_wait(2)
                time.sleep(1)
            except:
                continue
            link = img.get_attribute('src')
            full_file_name = os.path.join(self.save_path,keyword+str(count))
            #except base64 
            if link[0:4]=='data':
                count-=1
                continue
            else:
                req.urlretrieve(link,full_file_name+'.png')
            driver.implicitly_wait(2)
            time.sleep(1)
            if c % 20 == 0:        
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                driver.implicitly_wait(5)
                time.sleep(1)

        print("\n******************Download Finish!")
        driver.quit()