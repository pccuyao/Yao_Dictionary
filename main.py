from logging import exception
import requests
import pyperclip
import os
from bs4 import BeautifulSoup
import urllib.request
from playsound import playsound

#  shoud use 'playsound==1.2.2'

# Mac user needs 'pip3 install -U PyObjC'

import re
ready_status = True

def sK(name):
    KK = [0]
    KK_Split = [0]
    KK_Result = [0, 1]
    v_audio_list = [0]
    url = ("https://tw.dictionary.search.yahoo.com/search;?p=" + name)
    v_title = [0]
    
    if ready_status == True:

        #  爬蟲
        r = requests.get(url) 
        soup = BeautifulSoup(r.text, "lxml") 
        sel = soup.select("div.compList.d-ib")  #  KK音標查詢，以此為標準

        if len(str(sel)) < 10:
            print("\n找不到資料！")
        else:
            v_mean = soup.select("div.compList.mb-25")  #  釋義查詢
            v_pp = soup.find_all('li', attrs={'class': 'ov-a fst lst mt-0 noImg'})  #  詞性變化查詢
            v_title_soup = soup.select("div.compTitle.mt-25.mb-10")  #  標題查詢
            
            #  先取得標題
            for i in v_title_soup:
                v_title = i.text
                v_title = v_title.strip()  #  去除空格

            #  語音處理
            male_female = ['m','f']  #  目前有可能的檔案類別
            for abc in male_female:
                url_for = ("https://s.yimg.com/bg/dict/dreye/live/" + abc + "/" + v_title + ".mp3")
                try: 
                    v_status = urllib.request.urlopen(url_for).code  #  取得連結
                    v_audio_list.append(url_for)  #  若有就納入清單中
                except Exception as err:
                    pass
            v_audio_list.pop(0)  #  刪除第一個空白項

            #  輸出清單
            print('========================')
            print('[' + v_title + ']\n', sep='')
            #  釋義
            for a in v_mean:
                v_meanstr = a.text
                print('釋義:\n' + v_meanstr + '\n')
            #  詞性變化
            for b in v_pp:
                v_ppstr = b.text
                print('詞性變化:\n' + v_ppstr + '\n')
            #  音標
            for s in sel:
                KK.append(s.text)  #  將內容加入列表
            KK.pop(0)  #  去除初始值
            KK_Split = KK[0].split()  # 將預設的音標拆分
            KK.pop(0)  # 將預設的音標去除
            KK_Result = KK_Split + KK  # 將已處理過的音標，剩下的音標相加。
            print('音標:')
            print(KK_Result)
            print('========================\n')

            # 剪貼簿
            Copy_result = (KK_Result[0])  # 取用第一個音標
            Copy_result = Copy_result.replace('KK', '')  # 將KK去除
            pyperclip.copy(Copy_result + ' ' + v_meanstr)

            # 結尾訊息
            print('已複製其KK音標及意思。\n原網址為: ' + url)

            # 聲音撥放
            if len(v_audio_list) == 0:
                print("錯誤：沒有可撥放的發音")
            else:
                for p in range(len(v_audio_list)):
                    audioS = (v_audio_list[p])
                    try :
                        playsound(audioS)
                    except:
                        print("錯誤：無法撥放發音")
    else:
        pass
        

os.system('cls' if os.name == 'nt' else 'clear')
print('單字查詢與複製系統\n可使用【exit】來離開。')
while True:
    print('================================================\n')
    key = input("請輸入要查詢的單字：")
    if not re.match(r"^[A-Za-z]+$", key):
        print('錯誤：只能輸入英文字母')
        ready_status = False
        sK(key)
    elif key == "exit":
        print('程式結束\n')
        break
    else:
        ready_status = True
        sK(key)