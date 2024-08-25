import requests
import pyperclip
import os
from bs4 import BeautifulSoup
import urllib.request
from playsound import playsound
import time
import webbrowser

# should use 'playsound == 1.2.2'
# Python 3.11
# Mac user needs 'pip3 install -U PyObjC'

ready_status = True
copy_status = True
audio_status = True
logger = ['Log List']
v_audio_remove = []
log_number = 0
nowTime = ""
previous_temp = ""

# 檢查暫存資料夾是否存在

if os.path.isdir('temp'):
    pass
else:
    os.makedirs('temp')
if os.path.isdir('log'):
    pass
else:
    os.makedirs('log')

# 取得時間


def Get_Now_Time():
    timeGet = time.localtime(time.time())
    nowTime = (
        str(timeGet.tm_year) + '-' + str(timeGet.tm_mon) + '-'
        + str(timeGet.tm_mday) + '-' + str(timeGet.tm_hour) + '-'
        + str(timeGet.tm_min) + '-' + str(timeGet.tm_sec))
    return nowTime


# 檢查識別檔是否存在

identify_file_name = ('log/.' + str(os.name) + '-' + Get_Now_Time())
identify_file = open(identify_file_name, 'a+')


def sK(name):

    KK = []
    KK_Split = [0]
    KK_Result = [0]
    v_audio_list = []
    url = ("https://tw.dictionary.search.yahoo.com/search;?p=" + name)
    v_title = []

    if ready_status is True:

        log_write('Search: ' + name)

        #  爬蟲

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        sel = soup.select("div.compList.d-ib")  # KK音標查詢，以此為標準

        if len(str(sel)) < 10:
            v_possible = soup.select("div.compTitle.fz-16.lh-36.w-100p.h-36")
            for i in v_possible:
                print(i.text)
            log_write('Could not find: ' + name)
        else:
            v_mean = soup.select("div.compList.mb-25")  # 釋義查詢
            v_pp = soup.find_all(
                'li',
                attrs={'class': 'ov-a fst lst mt-0 noImg'})  # 詞性變化查詢
            v_title_soup = soup.select("div.compTitle.mt-25.mb-10")  # 標題查詢

            # 先取得標題

            for i in v_title_soup:
                v_title = i.text
                v_title = v_title.strip()  # 去除空格

            # 語音處理

            male_female = ['m', 'f']  # 目前有可能的檔案類別
            for abc in male_female:
                url_for = (
                    "https://s.yimg.com/bg/dict/dreye/live/" +
                    abc + "/" + v_title + ".mp3")
                try:
                    urllib.request.urlopen(url_for)  # 取得連結
                    v_audio_filename = ('temp/' + v_title + '_' + abc + '.mp3')
                    if os.path.isfile(v_audio_filename):
                        pass
                    else:
                        urllib.request.urlretrieve(url_for, v_audio_filename)
                    v_audio_list.append(v_audio_filename)  # 若有就納入清單中
                except Exception as e:
                    log_write('[' + url_for + ']: ' + str(e))

            # 輸出清單

            print('========================')
            print('[' + v_title + ']\n', sep='')

            # 釋義

            for a in v_mean:
                v_meanstr = a.text
                print('釋義:\n' + v_meanstr + '\n')

            # 詞性變化

            for b in v_pp:
                v_ppstr = b.text
                print('詞性變化:\n' + v_ppstr + '\n')

            # 音標

            for s in sel:
                KK.append(s.text)  # 將內容加入列表
            KK_Split = KK[0].split()  # 將預設的音標拆分
            KK.pop(0)  # 將預設的音標去除
            KK_Result = KK_Split + KK  # 將已處理過的音標，剩下的音標相加。
            print('音標:')
            print(KK_Result)
            print('========================')

            # 網址檢視

            print('原網址為: ' + url)
            global previous_temp
            previous_temp = (url)
            
            # 剪貼簿

            if (copy_status is True):
                Copy_result = (KK_Result[0])  # 取用第一個音標
                Copy_result = Copy_result.replace('KK', '')  # 將KK去除
                pyperclip.copy(v_title + ' ' + Copy_result + ' ' + v_meanstr)
                print('已複製其KK音標及意思。')
            else:
                print('複製模式已關閉')

            # 聲音撥放
            if audio_status is True:
                if len(v_audio_list) == 0:
                    print("錯誤：沒有可撥放的發音")
                else:
                    for p in range(len(v_audio_list)):
                        audioS = (v_audio_list[p])
                        v_audio_remove.append(v_audio_list[p])
                        try:
                            playsound(audioS)
                        except Exception as e:
                            log_write(e)
                            print("錯誤：無法撥放發音")
            else:
                print('發音模式已關閉')
                print(v_audio_remove)
        pass


def log_write(name):
    global log_number
    Get_Now_Time()
    log_content = ('[' + str(Get_Now_Time()) + ']('
                   + str(log_number) + '): ' + str(name))
    logger.append(log_content)
    log_number = log_number + 1


def program_close():

    # 檔案刪除 ( Windows 系統須等到程式結束才會消失)

    if len(v_audio_remove) > 1:
        for i in range(len(v_audio_remove)):
            try:
                os.remove(v_audio_remove[i])
                log_write('[' + str(v_audio_remove[i]) + '] :'
                            + 'has been deleted')
            except Exception as e:
                log_write(e)

    # 記錄存檔

    log_write('The program has been carefully closed')
    for i in range(len(logger)):
        identify_file.write(str(logger[i]) + '\n')
    identify_file.close()

    # 關閉

    print('程式結束\n')
    os._exit


def program_start():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('單字查詢與複製系統\n可使用【vhelp】查詢指令，【exit】來離開。')
    log_write('The program has been carefully started')


program_start()
while True:
    print('================================================')
    key = input("輸入：")
    if key == "vcopy":
        if copy_status is True:
            copy_status = False
            log_write('Copy mode has been closed')
            print('複製模式已關閉')
        else:
            copy_status = True
            log_write('Copy mode has been opened')
            print('複製模式已開啟')
        ready_status = False
    elif key == "errlog":
        for i in range(len(logger)):
            print(str(logger[i]))
        ready_status = False
    elif key == "delog":
        for dirPath, dirNames, fileNames in os.walk('log/.'):
            for f in fileNames:
                deleteFiles = ('log/' + f)
                if str(f) not in str(identify_file_name):
                    try:
                        os.remove(deleteFiles)
                        log_write(
                            'File :[' + deleteFiles + '] has been deleted')
                        print('檔案 [' + deleteFiles + '] 已被刪除')
                    except Exception as e:
                        log_write(e)
                else:
                    print('equal')
        ready_status = False
    elif key == 'vhelp':
        print("指令說明\n"
              "[vcopy]: 開啟、關閉複製模式\n"
              "[vaudio]: 開啟、關閉發音模式\n"
              "[vopen]: 開啟最後查詢過的單字連結\n"
              "[errlog]: 檢視紀錄\n"
              "[delog]: 刪除記錄檔\n"
              "[vhelp]: 檢視說明\n"
              "[exit]: 離開程式")
        ready_status = False
    elif key == 'vaudio':
        if audio_status is True:
            audio_status = False
            log_write('Audio mode has been closed')
            print('發音模式已關閉')
        else:
            audio_status = True
            log_write('Audio mode has been opened')
            print('發音模式已開啟')
        ready_status = False
    elif key == 'vopen':
        try:
            if len(previous_temp) < 10:
                print('沒有可開啟的連結')
                log_write('URL is empty, could not open.')
            else:
                webbrowser.open(previous_temp)
                log_write('Open: ' + previous_temp)
        except Exception as e:
            log_write(e)
        ready_status = False
    elif key == "exit":
        program_close()
        ready_status = False 
        break
    else:
        ready_status = True
    sK(key)
