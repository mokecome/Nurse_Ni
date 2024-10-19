#https://heho.com.tw/ #網站連結
#抓取5個新聞標題及簡述，並帶入連結，利用gpt4透過指定prompt進行圖片生成
#最後在linebot上進行展示，並運用Flex Messages卡片進行排版

import json
import requests 
import parsel  
import re

def spider():
    img_urls=[]
    title_urls=[]
    title=[]
    url='https://ml.oxra.com.tw/ra/mktv2/mkt-api-10/0-heho.com.tw/xx123456789/heho.com.tw'                                                             
    response = requests.get(url)
    html_data = response.text
    selector = parsel.Selector(html_data)
    lis = selector.css('script::text').getall()
    pattern = "let ox_mkt_api_10_1000 = (.*);"
    match = re.search(pattern, lis[1:2][0])
    if match:
        result = match.group(1)
        result= json.loads(result)
        for r in result:
            print(r['url'],r['title'],r['img'])
            title_urls.append(r['url'])
            title.append(r['title'])
            img_urls.append(r['img'])

    else:
        print("Pattern not found") 
    return title_urls,title,img_urls
    
