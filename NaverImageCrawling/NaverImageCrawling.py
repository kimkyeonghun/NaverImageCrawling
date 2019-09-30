import os

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
        options.add_argument('headless')
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
        sample = driver.find_element_by_css_selector('#_sau_imageTab > div.photowall._photoGridWrapper > div.more_img > a')

        #페이지 스크롤 늘리기
        """네이버 이미지 검색을 하면 50개만 이미지가 노출이 되고 아래로 스크롤을 내려야 추가적으로 50개씩 이미지가 추가 노출된다."""
        page,remain=divmod(cnt,50)
        for i in range(page):
            driver.execute_script('arguments[0].click();',sample)
            driver.implicitly_wait(5)
            time.sleep(1)
            print("Page Extend!")
        print("Page Extend Completed!")

        print()
        print("Download Start")
        count=0
        for i in range(2,2+page):
            for j in range(1,51):
                count+=1
                try:
                    img=driver.find_element_by_xpath('//*[@id="_sau_imageTab"]/div[1]/div['+str(i)+']/div['+str(j)+']/a[1]/img')
                    driver.implicitly_wait(2)
                    time.sleep(1)
                except:
                    img=driver.find_element_by_xpath('//*[@id="_sau_imageTab"]/div[2]/div['+str(i)+']/div['+str(j)+']/a[1]/img')
                    driver.implicitly_wait(2)
                    time.sleep(1)
                
                link = img.get_attribute('src')
                print(link)
                fullFileName = os.path.join(self.savePath,keyword+str(count)+'.png')
                req.urlretrieve(link,fullFileName)
                driver.implicitly_wait(2)
                time.sleep(1)
                print("=====================================")
                print("{}% Completed!".format(round(count/cnt,6)*100))
                print("=====================================")

        for j in range(1,remain+1):
            count+=1
            try:
                img=driver.find_element_by_xpath('//*[@id="_sau_imageTab"]/div[1]/div['+str(2+page)+']/div['+str(j)+']/a[1]/img')
                driver.implicitly_wait(2)
                time.sleep(1)
            except:
                img=driver.find_element_by_xpath('//*[@id="_sau_imageTab"]/div[2]/div['+str(2+page)+']/div['+str(j)+']/a[1]/img')
                driver.implicitly_wait(2)
                time.sleep(1)
            link = img.get_attribute('src')
            print(link)
            fullFileName = os.path.join(self.savePath,keyword+str(count)+'.png')
            req.urlretrieve(link,fullFileName)
            driver.implicitly_wait(2)
            time.sleep(1)    
            print("=====================================")
            print("{}% Completed!".format(round(count/cnt,6)*100))
            print("=====================================")

        print("Download Finish!")
        driver.quit()