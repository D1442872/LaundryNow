# LaundryNow：宿舍洗衣機即時狀態查詢系統

## 一、專案簡介

LaundryNow 是一個宿舍洗衣機即時狀態查詢系統，讓住宿生可以先在線上查看洗衣機目前是空閒、使用中或故障，也可以回報剩餘時間，減少白跑一趟。

本系統使用 Flask + SQLite 製作，適合作為期末專題 Demo 展示。

## 二、組別資訊

| 項目 | 內容 |
|---|---|
| 組別 | 第 9 組 |
| 組員 | 許佑僑、林政諠、張佑謙、陳炯任、簡佑霖、何承翰、翁允瑞、張嘉拓 |

## 三、目前已完成功能

| 功能編號 | 功能名稱 | 完成狀態 |
|---|---|---|
| F-01 | 查看洗衣機狀態 | 已完成 |
| F-02 | 回報洗衣機狀態 | 已完成 |
| F-03 | 設定剩餘時間 | 已完成 |
| F-04 | 新增洗衣機資料 | 已完成 |
| F-05 | 編輯與刪除資料 | 已完成 |

## 四、使用技術

- HTML
- CSS
- JavaScript
- Python Flask
- SQLite
- Jinja2
- GitHub
- Antigravity

## 五、專案結構

~~~text
LaundryNow/
├── app.py
├── laundry.db
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_machine.html
│   └── edit_machine.html
├── static/
│   ├── style.css
│   └── script.js
├── docs/
├── preview/
├── antigravity_terminal_record.md
└── terminal_log.txt
~~~

## 六、如何執行

第一次執行請先安裝套件：

~~~powershell
pip install -r requirements.txt
~~~

啟動網站：

~~~powershell
python app.py
~~~

啟動後在瀏覽器開啟：

~~~text
http://127.0.0.1:5000
~~~

## 七、Demo 說明

網站啟動後可操作：

- 查看所有洗衣機狀態
- 新增洗衣機資料
- 更新洗衣機狀態
- 設定剩餘時間
- 編輯洗衣機資料
- 刪除洗衣機資料
- 重置 Demo 資料

## 八、備註

本系統目前不包含：

- 使用者登入註冊
- 真實洗衣機硬體感測器
- 手機 App
- 線上付款
- 洗衣預約
- 自動通知
