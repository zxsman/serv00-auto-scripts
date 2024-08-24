#!/usr/bin/env python3
import os  
import requests  
import paramiko  
import socket  
from datetime import datetime  
import pytz  
  
# 預先定義的常量  
url = '你檢測的地址，參考下一行注釋'  
# 測試URL 這個URL是個凉了的 url = 'https://edwgiz.serv00.net/'
ssh_info = {  
    'host': 's3.serv00.com',    # 主機地址
    'port': 22,  
    'username': '你的用戶名',       # 你的用戶名，別寫錯了
    'password': '你的SSH密碼'       # 你注册的時候收到的密碼或者你自己改了的密碼
}

WECHAT_ROBOT_KEY  = '你的企業微信機器人的Key部分'      # 需要替換成你的企業微信機器人的Webhook Key，參考 https://open.work.weixin.qq.com/help2/pc/14931
webhook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={WECHAT_ROBOT_KEY}'     # 企業微信機器人的Webhook地址

# 獲取當前脚本文件的絕對路徑
script_dir = os.path.dirname(os.path.abspath(__file__))

# 日志文件將保存在脚本所在的目錄中
log_file_path = os.path.join(script_dir, 'Auto_connect_SSH.log')
wechat_message_sent = False     # 標記是否已經發送了成功的企業微信提醒消息
flush_log_message = []      # 用于存儲日志信息的全局變量
# 寫入日志的函數
def write_log(log_message):
    global flush_log_message
    if not os.path.exists(log_file_path):
        open(log_file_path, 'a').close()  # 創建日志文件
        os.chmod(log_file_path, 0o644)  # 設置#日志文件有可編輯權限（644權限）
    log_info = f"{log_message}"
    flush_log_message.append(log_info)

# 把所有的日志信息寫入日志文件
def flush_log():
    global flush_log_message
    # 獲取當前系統時間、北京時間、星期以及 SSH 用戶名，然後將所有信息合幷爲一行寫到日志裏面
    username = ssh_info['username']
    system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    current_day = datetime.now(pytz.timezone('Asia/Shanghai')).weekday()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    current_weekday_name = weekdays[current_day]
    flush_log_messages = f"{system_time} - {beijing_time} - {current_weekday_name} - {url} - {username} - {' - '.join(flush_log_message)}"
    # 寫入日志文件，幷添加換行符
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(flush_log_messages + '\n')
    # 清空累積的日志信息列表
    flush_log_message.clear()      # 清空累積的消息，避免下一次會有重複消息

# 發送企業微信消息的函數  
def send_wechat_message(message):  
    global wechat_message_sent  # 聲明爲全局變量
    headers = {'Content-Type': 'application/json'}  
    try:  
        response_wechat = requests.post(webhook_url, json=message, headers=headers)  
        response_wechat.raise_for_status()
        wechat_status = "企業微信提醒消息發送成功"  
        print("溫馨提醒：企業微信提醒消息發送成功。")  
    except requests.RequestException as e:
        wechat_status = f"企業微信提醒消息發送失敗，錯誤碼: {e}"  
        print(f"警告：企業微信提醒消息發送失敗！\n錯誤碼: {e}")  
    finally:
        # 測試的時候發現如果碰到又是規定的定期執行時間還有碰巧主機凉了會寫兩遍日志，改爲只有在消息尚未發送的情况下才記錄日志
        if not wechat_message_sent:
            write_log(f"{wechat_status}")
            wechat_message_sent = True  # 消息發送後，將標記設置爲 True
  
# 嘗試通過SSH恢復PM2進程的函數  
def restore_pm2_processes():  
    transport = paramiko.Transport((ssh_info['host'], ssh_info['port']))  
    try:  
        transport.connect(username=ssh_info['username'], password=ssh_info['password'])  
        # 創建SSH通道
        ssh = paramiko.SSHClient()  
        ssh._transport = transport  
        try:    # 執行pm2 resurrect命令
            stdin, stdout, stderr = ssh.exec_command('/home/你的用戶名/.npm-global/bin/pm2 resurrect')  
            print("STDOUT: ", stdout.read().decode())  
            print("STDERR: ", stderr.read().decode())  
            stdout.channel.recv_exit_status()  # 等待命令執行完成
            if stdout.channel.exit_status == 0:
                write_log("通過SSH執行PM2命令成功")
                print("溫馨提醒：PM2進程恢復成功。")
            else:
                write_log(f"通過SSH執行PM2命令時出錯，錯誤信息：{stderr.read().decode()}")
                print("警告：PM2進程恢復失敗！\n錯誤信息：", stderr.read().decode())
        except Exception as e:  
            write_log(f"通過SSH執行PM2命令時出錯: {e}")
            print(f"通過SSH執行命令時出錯: {e}")  
    finally:  
        ssh.close()  # 關閉SSHClient
        transport.close()    # 關閉Transport連接

# 嘗試通過SSH連接的函數
def ssh_connect():
    try:
        transport = paramiko.Transport((ssh_info['host'], ssh_info['port']))
        transport.connect(username=ssh_info['username'], password=ssh_info['password'])
        ssh_status = "SSH連接成功"
        print("SSH連接成功。")
    except Exception as e:
        ssh_status = f"SSH連接失敗，錯誤信息: {e}"
        print(f"SSH連接失敗: {e}")
    finally:
        transport.close()
        write_log(f"{ssh_status}")

# 檢查是否爲每月的1號
def is_first_day_of_month():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))      # 機子時間是UTC時間，爲了便于識別這裏需要使用東八區北京時間
    print("本來應該是系統時間，但是我要改成北京時間增强辨識度：",now)
    current_day = now.day    # 獲取當前的天數
    return current_day == 1 or current_day == 15    # 設置每個月的哪一天或哪幾天爲每月固定SSH日期（如果只想每個月第一天就只需要保留return current_day == 1即可）        

# 返回當前的天、月和一年中的第幾天
def get_day_info():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))      # 使用東八區北京時間
    print("北京時間：",now)
    current_day = now.day
    current_month = now.month
    current_year_day = now.timetuple().tm_yday  # 今年中的第幾天
    current_weekday = now.weekday()  # 返回一個 0-6 的整數，0 是星期一，6 是星期日
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    current_weekday_name = weekdays[current_weekday]
    return current_day, current_month, current_year_day, current_weekday_name

# 每個月發送僅包含URL和時間的提醒消息
def send_monthly_reminder():
    current_day, current_month, current_year_day, current_weekday_name = get_day_info()
    system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    message = {
        "msgtype": "text",
        "text": {
            "content": f" [鼓掌]每月固定SSH提醒[鼓掌] \n-------------------------------------\n檢測地址:\n{url}\n-------------------------------------\n　　今天是{current_month}月{current_day}日( {current_weekday_name} )，本月的第 {current_day} 天，今年的第 {current_year_day} 天，例行SSH連接已經成功執行，以防萬一空了可以到後臺查看記錄！\n-------------------------------------\n系統時間: {system_time}\n北京時間: {beijing_time}"
        }
    }
    return message

# 每月一次檢查提醒
if is_first_day_of_month():
    message = send_monthly_reminder()
    send_wechat_message(message)
    ssh_connect()

# 檢查URL狀態和DNS的函數  
def check_url_status_and_dns():  
    try:  
        # 嘗試解析URL的域名  
        host = socket.gethostbyname(url.split('/')[2])  
        print(f"解析成功，IP地址爲: {host}")
        write_log(f"{host}")
    except socket.gaierror as e:  
        # 解析失敗，發送通知  
        write_log(f"Error: {e}")
        system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  
        message = {  
            "msgtype": "text",  
            "text": {  
                "content": f"----- [炸彈]解析失敗提醒[炸彈] -----\n地址: {url}\n錯誤: {e}\n[恐懼]抓緊嘗試檢查解析配置或聯繫管事的老鐵。\n-------------------------------------\n系統時間: {system_time}\n北京時間: {beijing_time}"  
            }  
        }  
        send_wechat_message(message)  
        return  
  
    # 嘗試獲取URL的狀態碼  
    response = requests.get(url, timeout=10)  
    if response.status_code != 200:  
        # URL狀態碼不是200，發送通知幷嘗試恢復PM2進程  
        system_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  
        message = {  
            "msgtype": "text",  
            "text": {  
                "content": f"----- [裂開]當前服務不可用[裂開] -----\n地址: {url}\n狀態碼: {response.status_code}\n[加油]正在嘗試通過SSH恢復PM2進程，請稍後手動檢查恢復情况！\n-------------------------------------\n系統時間: {system_time}\n北京時間: {beijing_time}"  
            }  
        }
        write_log(f"主機狀態碼: {response.status_code}")  
        send_wechat_message(message)  
        restore_pm2_processes()  
    else:  
        write_log(f"主機狀態碼: {response.status_code}")
        print(f"主機狀態碼: {response.status_code}")  

if __name__ == '__main__':
    # 檢查URL狀態和DNS
    check_url_status_and_dns()
    # 所有日志信息已經收集完成，寫入日志文件
    flush_log()
