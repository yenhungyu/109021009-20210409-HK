import requests
import time
import csv
from bs4 import BeautifulSoup
URL ="https://csie.asia.edu.tw/project/semester-{0:03d}.html" #將數列部分改為字串的概念去做列表就不會有010的狀況出現

def generate_urls(url, start_page , end_page): #網頁
    urls = []
    for page in range(start_page , end_page):
        urls.append(url.format(page))
    return urls #收集urls

def get_resource(url):   #假真人爬蟲防止被拒絕爬蟲
    headers = {   #headers假來源
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    return requests.get(url , headers = headers)

def parse_html(html_str):   #解析html變lxml
    return BeautifulSoup(html_str, "lxml")

def get_responsive(soup , file):  #爬蟲開始
    responsive = []
    count = 0
    for table in soup.find_all(class_="nav-pills").find_all("li"):
        url=table.a.get("href")    #抓href的資料
        count += 1
        for responsive_table in soup.find_all(class_="table-responsive"):
        
            for tr in responsive_table.find_all("tr"): #抓responsive裡tr的資料
                for cell in tr.fin_all("td"):
                    for cell in tr.find_all('th'):
                        new_word = []
                        new_word.append(file)
                        new_word.append(str(count))#收集每個資料
                        words.append(new_word)             
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
            time.sleep(3) #先睡個幾秒再繼續抓   
        else:
            print("HTTP request error")
    return hk_reponsive

def save_to_csv(responsive, file): #存檔excel的csv
    with open(file, "w+" , newline="" , encoding="utf-8") as fp: #newline不要加換行
        writer = csv.writer(fp)
        for word in responsive:
            writer.writerow(word)

if __name__ == "__main__":
    urlx = generate_urls(URL , 100 , 109)
    hk_reponsive = web_scraping_bot(urlx)
    for item in hk_reponsive: #可有可無
        print(item)
    save_to_csv(hk_reponsive,"homeworkreponsive_100.csv")