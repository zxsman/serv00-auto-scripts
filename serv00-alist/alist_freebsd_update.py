#!/usr/bin/env python3
'''
說明：脚本文件請放置于Alist FreeBSD程序目錄下，幷命名爲alist_freebsd_auto_update.py，在終端內使用chmod +x alist_freebsd_auto_update.py賦予執行權限，然後執行./alist_freebsd_auto_update.py
測試方法：在Alist FreeBSD程序目錄下執行命令 python3 alist_freebsd_auto_update.py或./alist_freebsd_auto_update.py
'''
import requests
import datetime
import subprocess
import os
import re
  
# GitHub API URL 用于獲取最新版本  
API_URL = "https://api.github.com/repos/uubulb/alist-freebsd/releases/latest"  

# 從 API 獲取最新版本的數據
try:
    response = requests.get(API_URL)
    response.raise_for_status()  # 如果請求返回了一個錯誤狀態碼，將拋出异常
except requests.exceptions.RequestException as e:
    print(f"從 GitHub 獲取最新版本信息出錯: {e}")
    exit(1)
release_data = response.json()

# 檢查 alist 文件是否存在
if not os.path.exists('alist'):
    print("Alist FreeBSD 程序未找到，正在準備下載...")
else:
    # 執行 ./alist version 命令幷獲取輸出
    try:
        version_output = subprocess.check_output(['./alist', 'version'], text=True).strip()
    except subprocess.CalledProcessError as e:
        print("警告：執行查詢Alist版本號命令出錯:", e)
        exit(1)

    # 解析獲取到的版本號
    version_pattern = r"Version: v(\d+\.\d+\.\d+)-\d+-g[a-fA-F0-9]+"
    match = re.search(version_pattern, version_output)
    if match:
        get_version = match.group(1)
        current_version = f"v{get_version}"
        print(f"當前 Alist 版本: {current_version}")
    else:
        print("未能從輸出中找到正確的版本號。")
        exit(1)

    # 從獲取到的json數據中找到版本號
    alist_freebsd_version = release_data.get('name', None)
    if not alist_freebsd_version:
        print("沒有找到 Alist FreeBSD 版本號。")
        exit(1)
    print(f"最新 Alist 版本: {alist_freebsd_version}")  # 打印最新版本號（測試用）

    # 比較版本號
    if current_version == alist_freebsd_version:    # 如果前面沒做v字符，則需要使用alist_freebsd_version.lstrip('v')移除獲取到的GitHub上版本號的'v'
        print(f"當前 Alist FreeBSD 已經是最新版本，不需要更新！\n=============================================\n【Alist FreeBSD 信息如下】\n\n{version_output}\n=============================================\n")
        exit(0)
    else:
        print(f"發現新版本 {alist_freebsd_version}，當前版本爲 {current_version}，正在執行更新...\n")

    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')     # 獲取當前日期和時間幷格式化爲 YYYYMMDDHHMMSS
    new_name = f"{current_datetime}_{current_version}_alist_bak"      # 重命名現有文件，格式爲 YYYYMMDDHHMMSS_alist_bak
    if os.path.exists(new_name):        
        print(f"文件 '{new_name}' 已存在，嘗試生成一個新的文件名...")       # 如果重命名後的文件名已存在，再次循環直到找到一個不存在的文件名
        new_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + f"_{current_version}_alist_bak"
    os.rename('alist', new_name)
    print(f"溫馨提醒：'alist' 文件已存在，以防萬一已重命名爲 '{new_name}'。\n")

# 查找名爲 'alist' 的文件的下載鏈接  
for asset in release_data['assets']:  
    if 'alist' in asset['name'].lower():  
        DOWNLOAD_URL = asset['browser_download_url']          
        #DOWNLOAD_URL = DOWNLOAD_URL.replace("https://github.com", "https://download.nuaa.cf")       # 本地測試加速用，Serv00可能會文件下載不全
        break  
else:  
    print("在發布中未找到名爲 'alist' 的文件。")  
    exit(1)  

# 開始下載文件  
print(f"正在從 {DOWNLOAD_URL} 下載最新 FreeBSD 版 Alist！\n下載中，請稍後...\n")  
response = requests.get(DOWNLOAD_URL, stream=True)  
with open('alist', 'wb') as f:  
    for chunk in response.iter_content(chunk_size=32768):   # 從 HTTP 響應中讀取數據塊（chunks）的大小，8192（8KB）、32768（32KB）、65536（64KB），自己換！
        f.write(chunk)  

# 賦予 alist 文件可執行權限  
os.chmod('alist', 0o755)

# 檢查是否存在 config.json 文件  
if os.path.exists('./data/config.json'):
    new_version_output =  subprocess.check_output(['./alist', 'version'], text=True).strip()
    print(f"---------------------------------------------\n溫馨提示：Alist-FreeBSD 最新版本已經下載完成！\n---------------------------------------------\n【Alist FreeBSD 最新信息如下】\n{new_version_output}\n---------------------------------------------\n")
    # 啓動 alist 服務
    try:
        print("啓動 Alist 服務...")
        result = subprocess.run(['./alist', 'server'], text=True, capture_output=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        print(result.stderr)  # 打印啓動服務的輸出
    except subprocess.CalledProcessError as e:
        exit(1)
    # 使用 pm2 restart alist
    try:
        print("使用 pm2 重啓 Alist 服務...")
        subprocess.run(['pm2', 'restart', 'alist'], check=True, text=True)
    except subprocess.CalledProcessError as e:
        exit(1)
    print("Alist 服務已成功啓動幷重啓。")
else:   
    subprocess.Popen(['./alist', 'server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # 啓動 alist 服務
    print("已下載最新版本的 Alist-FreeBSD ，幷生成 config.json 文件。")   
    print("配置文件 config.json 已成功生成，路徑：./data/config.json ，請自行修改端口！")  
    print("使用命令 cd 命令進入 data 路徑下")  
    print("再使用文本編輯器編輯 config.json 文件，修改 port 字段爲你放行的端口！")  
    print("例如，使用 vim: vim config.json")  
    print("修改完成後，使用命令 cd .. 回到上級目錄")
