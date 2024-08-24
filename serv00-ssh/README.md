# Serv00 - 免費主機脚本集合（大水庫）
## 當前脚本

|  脚本名稱 |  用途 |備注 |
| :------------: | :------------: | :------------: |
|Auto_connect_SSH.py|自動SSH登錄以續期||
|alist_freebsd_update.py|自動從uubulb/alist-freebsd拉取最新版本更新||

# 自動續期脚本說明

## 說明
　　本項目基于[LINUX DO](https://linux.do)論壇佬友`maohai`的[脚本](https://linux.do/t/topic/66483/15)進行修改，在其基礎上增加了`發送通知`、以及`運行日志`功能。

## 發送說明

|  主機狀態/設置條件 |  說明 |發送內容 |執行動作 |
| :------------: | :------------: | :------------: | :------------: |
|  200 |  正常 |不發送|無|
|   502|  機子凉了 |服務不可用|通過SSH執行PM2命令|
|   [Errno 1] Address family for hostname not supported| 解析凉了  |解析失敗|無|
|  自定義日期 |  固定日啓動連接 |每月固定SSH連接提醒|連接SSH|

## 使用方法

　　將脚本放到`domains`目錄下，使用`chmod +x Auto_connect_SSH.py`給`Auto_connect_SSH.py`添加可執行權限。  
  
　　在Serv00控制台的定時任務裏面新建一個定時任務，`命令`如下：

```shell
/home/你的用戶名/domains/Auto_connect_SSH.py
```

#### 參考設置圖

![參考圖片](https://cdn.linux.do/uploads/default/optimized/3X/f/6/f6516994395858a19637f5acf5baeecec96ea3fa_2_690x445.png)

# Alist自動更新脚本說明

　　將脚本放到`domains`目錄下你的 `Alist` 存儲路徑中，使用`chmod +x alist_freebsd_update.py`給`alist_freebsd_update.py`添加可執行權限。 
　　然後自己到控制台創建一個定時任務。

#### 運行效果圖

  ![沒有Alist文件](https://cdn.linux.do/uploads/default/original/3X/1/f/1f5b378d086d1935cfaf3927c9fc6c33d531eeb7.jpeg)
  ![已經是最新版](https://cdn.linux.do/uploads/default/original/3X/e/7/e72105ffe5f1ee572cca2ded4138472241553bdb.jpeg)
  ![正常更新](https://cdn.linux.do/uploads/default/original/3X/f/5/f58f94d755825005eae30df9dce0ad1f0b661f43.jpeg)
  
## 參考來源

|  名稱 |來源|地址|
| :------------: | :------------: | :------------: |
|Saika|Github|https://github.com/k0baya|
|Eric Lee|Github|https://github.com/giturass|
|maohai|LINUX DO|https://linux.do/t/topic/66483/15|

## SSH登錄不上

> 登錄不上是因爲Ban IP, 點擊此處解鎖： [Ban](https://www.serv00.com/ip_unban/)

> 還是登錄不上的話： 請使用下方 `FinalShell`，幷勾上 `智能海外加速`，登錄失敗在彈出框選擇`取消`，在彈出框填入`[郵件中的SSH密碼]`

## FinalShell

FinalShell是一體化的的服務器,網絡管理軟件,不僅是ssh客戶端,還是功能强大的開發,運維工具,充分滿足開發,運維需求.

### 特色功能:

雲端同步,免費海外服務器遠程桌面加速,ssh加速,本地化命令輸入框,支持自動補全,命令歷史,自定義命令參數

- Windows X64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_windows_x64.exe>

- macOS Arm版,支持m1,m2,m3 cpu,下載地址: <http://www.hostbuf.com/downloads/finalshell_macos_arm64.pkg>

- macOS X64版,支持舊款intel cpu,下載地址: <http://www.hostbuf.com/downloads/finalshell_macos_x64.pkg>

- Linux X64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_x64.deb>

- Linux Arm64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_arm64.deb>

- Linux LoongArch64龍芯版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_loong64.deb>
