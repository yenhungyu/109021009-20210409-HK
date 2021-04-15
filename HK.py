import requests
import time
import csv
from bs4 import BeautifulSoup
from requests import urllib3

def generate_urls(start_page, end_page):
    urls = []
    domain = "https://csie.asia.edu.tw{0}"
    urllib3.disable_warnings()
    # 取得該網址回應參數
    r = requests.get(domain.format("/project"), verify = False)

    if r.status_code == requests.codes.ok:
        # 解析資料
        soup = parse_html(r.text)

        # 要爬蟲的頁面數
        for year in range(start_page, end_page + 1):
            
            # 從soup(已解析資料)中找到每個class_為"nav-pills"數據下所有的"li"標籤內容 存入item
            for item in soup.find(class_ = "nav-pills").find_all("li"):
                # 從item中超連結函式(.a)下的.get函式取得其參數下內容 並儲存為urlf變數
                # PS.從原始碼中可以得知 我們要的網址內容存在a下的href中
                url = item.a.get("href")

                if url.find(str(year)) > -1:
                    urls.append(domain.format(url))
                    break

    else:
        print("Error!!")

    return urls

def get_resource(url):   #假真人爬蟲防止被拒絕爬蟲
    headers = {   #headers假來源
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url , headers = headers, verify = False) #verify憑證要求

def parse_html(html_str):   #解析html變lxml
    return BeautifulSoup(html_str, "lxml")

def get_responsive(soup , file):  #爬蟲開始
    responsive = []
    count = 0
    for responsive_table in soup.find_all("div", class_="table-responsive"):
        rowData = [] 
    
        for tr in responsive_table.find_all("tr"): #抓responsive裡tr的資料
            for cell in tr.find_all("td"):
                rowData.append(cell.text.replace('\t', '').replace('\n', ''))
                rowData.append("\t")
        count += 1
    
    responsive.append(rowData)
    return responsive #統一丟入words的list裡

def web_scraping_bot(urls): #防止爬蟲被擋
    hk_reponsive = []
    for url in urls:
        file = url.split("/")[-1] #讓最後一個值為-1 由後往前-1、-2....
        print("catching: " , file , " web data...")
        r = get_resource(url)
        if r.status_code == requests.codes.ok: #後者等於參數200,網頁連結成功,若為404網頁不存在500則為伺服器有問題
            soup = parse_html(r.text)
            responsive = get_responsive(soup,file)
            hk_reponsive = hk_reponsive + responsive
            print("wait 3 second")
            time.sleep(0.5) #先睡個幾秒再繼續抓   
        else:
            print("HTTP request error")
    return hk_reponsive

def save_to_csv(responsive, file): #存檔excel的csv
    with open(file, "w+" , newline="" , encoding="utf-16") as fp: #newline不要加換行
        writer = csv.writer(fp)
        for word in responsive:
            writer.writerow(word)

if __name__ == "__main__":
    urlx = generate_urls(100 , 108)
    hk_reponsive = web_scraping_bot(urlx)
    for item in hk_reponsive: #可有可無
        print(item)
    save_to_csv(hk_reponsive,"homeworkreponsive_100.csv")