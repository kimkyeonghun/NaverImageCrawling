import os
import re
import base64
from tqdm import tqdm

class NaverImageCrawling():
    def __init__(self):
        #self.driverPath='path/to/your/chromedriver'
        self.driverPath='./webdriver/chrome/chromedriver.exe'
        self.savePath="./imageDownload"

    def makeDownloadFolder(self,path):
        #저장경로 만들기
        if path:
            self.savePath=path
        try:
            if not (os.path.isdir(self.savePath)):
                os.makedirs(os.path.join(self.savePath))
                print("Success to make Folder!")
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Fail to make Folder!")
                raise
    
    def base64decoding(self,link,fullFileName):
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", link, re.DOTALL)
        if result:
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")
        else:
            raise Exception("Do not parse!")
        img = base64.urlsafe_b64decode(data)
        fileName = "{}.{}".format(fullFileName,ext)
        with open(fileName,"wb") as f:
            f.write(img)

    def downloadImage(self,keyword,cnt,path=None):
        """keyword : 검색어
           cnt : 해당 검색어로 크롤링할 이미지의 갯수(최대 1000개)
           path : 크롤링한 이미지를 다운 받을 폴더 경로 지정, default로는 현재 py 파일이 있는 폴더에 imageDownload를 생성함"""

        if cnt > 1000:
            print("You Can't Crawling over 1000 images")
            cnt=1000
            print("Change Image Count Number to 1000")        
        keyword =str(keyword)
        
        import urllib.parse as rep
        import urllib.request as req
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time

        #selenium Option 설정
        options =webdriver.ChromeOptions()
        #options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        driver = webdriver.Chrome(self.driverPath,chrome_options=options)
        driver.implicitly_wait(2)

        self.makeDownloadFolder(path)

        #네이버 접속
        base = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
        quote = rep.quote_plus(keyword)
        url = base+quote
        driver.get(url)

        print()
        print("Download Start")
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
            fullFileName = os.path.join(self.savePath,keyword+str(count))
            if link[0:4]=='data':
                continue
            else:
                req.urlretrieve(link,fullFileName+'.png')
                c-=1
            driver.implicitly_wait(2)
            time.sleep(1)
            if c % 10 == 0:        
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                driver.implicitly_wait(5)
                time.sleep(1)

        print("Download Finish!")
        driver.quit()