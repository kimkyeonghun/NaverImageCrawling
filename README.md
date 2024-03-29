## 네이버 이미지 크롤러(Naver-Image-Crawler)

Selenium을 사용한 네이버 이미지 크롤러입니다. 네이버 이미지 크롤러는 네이버 이미지 검색에서 나온 결과물을 최대 1000개까지 이미지를 크롤링할 수 있습니다. 학술 및 공부 목적으로 활용 부탁드립니다. 크롤링 데이터의 저작권은 네이버에 있습니다.

* python -ver 3.7.3
* selenium(Chromedriver), urllib.parse, urllib.request를 사용하고 있습니다.

## 사전 준비 사항

1. **Selenium**

   - Selenium와 Chromedriver를 설치해야 합니다.

   - Chromedriver의 webdriver 폴더를 같은 경로 내에 위치 시켜야 합니다.

     

## 사용 방법

1. **Crawling.py**
   - Crawling.py를 수정해서 네이버 이미지를 크롤링 합니다.
   - argparse를 사용해서 keyword, 갯수, path를 입력받습니다.
     - python Crawling --keyword _ --n _ --path _
     - keyword와 n은 필수이며 path는 지정하지 않는 경우 default로 설정된 값으로 생성합니다.
   
   - 위 코드에 keyword에 내가 검색하고 싶은 단어, n에 크롤링하고 싶은 이미지의 갯수를 넣어주면 됩니다.

## 결과

다음과 같이 크롤링의 결과가 나타나며 이미지가 크롤링 됩니다.

![example](https://user-images.githubusercontent.com/41284582/126030574-ac59aa96-71ba-4d3e-b0f5-ea7a9e65bda8.png)

공부 목적으로 만들고 있기 때문에 버그가 있을 수도 있으며 추가 기능이 생길 수 있습니다.
