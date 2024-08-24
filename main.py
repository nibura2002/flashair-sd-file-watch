import time
import requests
import os
import logging
from datetime import datetime

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# FlashAirのCGI URL
FLASH_AIR_CGI_URL = "http://flashair.local/command.cgi?op=100&DIR=/DCIM/watch"
DOWNLOAD_DIR = "./downloads"  # ダウンロード先のディレクトリ

# 前回取得したファイルリストを保持するための変数
previous_file_list = set()

def get_file_list():
    try:
        response = requests.get(FLASH_AIR_CGI_URL, timeout=5)
        response.raise_for_status()
        # レスポンスをパースしてファイル名のリストを取得
        file_list = []
        lines = response.text.splitlines()
        for line in lines:
            parts = line.split(',')
            if len(parts) > 1:
                filename = parts[1]
                # 8.3形式のファイル名を除外する
                if not filename.startswith('_') and '~' not in filename:
                    file_list.append((filename, parts[-1]))  # parts[-1]は仮にタイムスタンプと仮定
        # 作成時間順にソート（timestampが数値の場合）
        file_list.sort(key=lambda x: x[1])
        return file_list
    except requests.RequestException as e:
        logging.warning(f"Failed to retrieve file list: {e}")
        return None

def download_file(filename):
    # 現在の日時を取得してタイムスタンプを生成
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # 保存するファイル名にタイムスタンプを追加
    local_filename = os.path.join(DOWNLOAD_DIR, f"{timestamp}_{filename}")
    
    file_url = f"http://flashair.local/DCIM/watch/{filename}"
    
    try:
        with requests.get(file_url, stream=True, timeout=5) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logging.info(f"Downloaded: {local_filename}")
    except requests.RequestException as e:
        logging.warning(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    while True:
        try:
            file_list = get_file_list()
            if file_list:
                # 新しいファイルを検出
                new_files = [f for f in file_list if f[0] not in previous_file_list]
                if new_files:
                    # 作成時間が早い順にソートされているので、最初のファイルをダウンロード
                    new_file = new_files[0]
                    logging.info(f"New file detected: {new_file[0]}")
                    download_file(new_file[0])
                    # ダウンロードしたファイルをprevious_file_listに追加
                    previous_file_list.add(new_file[0])
                else:
                    logging.info("No new files found.")
            else:
                logging.info("Failed to retrieve file list.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        
        time.sleep(5)  # 5秒ごとにチェック
