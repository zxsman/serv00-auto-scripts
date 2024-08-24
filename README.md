# Serv00 - 控制面板自動登錄脚本

## 使用方法

1. 在 GitHub 倉庫中，進入右上角`Settings`

2. 在側邊欄找到`Secrets and variables`，點擊展開選擇`Actions`，點擊`New repository secret`
    
3. 然後創建一個名爲`ACCOUNTS_JSON`的`Secret`，將 JSON 格式的賬號密碼字符串作爲它的值，如下格式：  

``` json
[  
  { "username": "qishihuang", "password": "zhanghao", "panelnum": "3" },  
  { "username": "zhaogao", "password": "daqinzhonggong", "panelnum": "1" },  
  { "username": "heiheihei", "password": "shaibopengke", "panelnum": "2" }  
]
```

> 其中`panelnum`參數爲面板編號，即爲你所收到注册郵件的`panel*.serv00.com`中的`*`數值。

## 貢獻

|姓名|主頁|內容|
| :------------: | :------------: | :------------: |
|linzjian666|https://github.com/linzjian666|增加多面板支持|

## 參考信息

|  名稱 |來源|地址|
| :------------: | :------------: | :------------: |
|Limkon|Github|https://github.com/Limkon|

## SSH登錄不上

> 登錄不上是因爲Ban IP, 點擊此處解鎖： [Ban](https://www.serv00.com/ip_unban/)

> 還是登錄不上的話： 請使用下方 `FinalShell`，幷勾上 `智能海外加速`，登錄失敗在彈出框選擇`取消`，在彈出框填入`[郵件中的SSH密碼]`

## FinalShell

FinalShell是一體化的的服務器,網絡管理軟件,不僅是ssh客戶端,還是功能强大的開發,運維工具,充分滿足開發,運維需求.

### 特色功能

雲端同步,免費海外服務器遠程桌面加速,ssh加速,本地化命令輸入框,支持自動補全,命令歷史,自定義命令參數

- Windows X64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_windows_x64.exe>

- macOS Arm版,支持m1,m2,m3 cpu,下載地址: <http://www.hostbuf.com/downloads/finalshell_macos_arm64.pkg>

- macOS X64版,支持舊款intel cpu,下載地址: <http://www.hostbuf.com/downloads/finalshell_macos_x64.pkg>

- Linux X64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_x64.deb>

- Linux Arm64版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_arm64.deb>

- Linux LoongArch64龍芯版,下載地址: <http://www.hostbuf.com/downloads/finalshell_linux_loong64.deb>

## 其他服務

- PHP配置: <https://docs.serv00.com/PHP/#php-version>

- Memcached配置: <https://docs.serv00.com/Memcached/>

  啓動：memcached -s /usr/home/LOGIN/domains/DOMAIN/memcached.sock -d

- Redis配置: <https://docs.serv00.com/Memcached/>
