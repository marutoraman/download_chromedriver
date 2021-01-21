import os
import sys
from webdriver_manager.utils import chrome_version
import urllib.request
import requests
import zipfile
from selenium.webdriver import Chrome, ChromeOptions
import time

CHROME_DRIVER_RELEASE_VEARSION_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" # + メジャーバージョン
CHROME_DRIVER_DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/###CHROME_DRIVER_VERSION###/chromedriver_###OS###.zip"
CHROME_DRIVER_DIR_PATH="./"
CHROME_DRIVER_ZIPFILE_TEMP_NAME="_download_temp.zip"

def get_chrome_version():
    return chrome_version()

def download_file(url:str):
    zip_filepath="_download_temp.zip"
    urllib.request.urlretrieve(url,zip_filepath)
    
def extract_zip(zip_filepath:str,save_dir_path:str):
    with zipfile.ZipFile(zip_filepath) as existing_zip:
        existing_zip.extractall(save_dir_path)

def download_driver(check_mode:bool=True):
    # chromeバージョンを取得
    version=get_chrome_version()
    print(f"chrome version:{version}")
    if not version.find(".") >=1: #バージョンが正常に取得できない場合
        print(f"chrome versionエラー:{version}")
        return False
    
    # chromedriverのバージョンを取得
    url= CHROME_DRIVER_RELEASE_VEARSION_URL + version[:version.find(".")]
    res=requests.get(url)
    if res.status_code != 200:
        return False
    chromedriver_version = res.text
    print(f"chromedriver version:{chromedriver_version}")
    if not chromedriver_version.find(".") >=1: #バージョンが正常に取得できない場合
        print(f"chromedriver versionエラー:{chromedriver_version}")
        return False
    
    # chromedriverをダウンロード
    try:
        #chromedriverダウンロードURLを作成
        url = CHROME_DRIVER_DOWNLOAD_URL.replace("###CHROME_DRIVER_VERSION###",chromedriver_version)\
                                        .replace("###OS###",check_os()) 
        print(f"ダウンロードURL:{url}")
        urllib.request.urlretrieve(url,CHROME_DRIVER_ZIPFILE_TEMP_NAME)
        extract_zip(CHROME_DRIVER_ZIPFILE_TEMP_NAME,CHROME_DRIVER_DIR_PATH)
    
        # ダウンロードしたzipファイルを削除
        os.remove(CHROME_DRIVER_ZIPFILE_TEMP_NAME)
    
        # 起動チェック
        if check_mode:
            check_driver()
        else:
            print("ダウンロードが完了しました")
            
    except Exception as e:
        print(f"chromedriverダウンロードエラー:{e}")
        return False   

    return True

def check_os():
    if os.name == 'nt': #Windows
        return "win32"
    elif os.name == 'posix': #Mac
        return "mac64"
    else:
        return None

def check_driver():
    try:
        driver=Chrome(os.path.join(CHROME_DRIVER_DIR_PATH,"chromedriver.exe"))
        driver.get("https://www.google.co.jp")
        driver.execute_script("alert('ダウンロードが成功しました。画面を閉じてください')")
        print("正常に起動しました")
        time.sleep(100)
    except Exception as e:
        print(f"起動エラー:{e}")
        
        
if __name__ == "__main__":
    check_mode = True
    if len(sys.argv)>=2:
        check_mode = False if sys.argv[1]=="NOCHECK" else True
    download_driver(check_mode)
