# LaundryNow 完整期末 Demo 實作紀錄

## 專案名稱

LaundryNow：宿舍洗衣機即時狀態查詢系統

## 本次完成目標

完成 6/18 期末展示前可操作的 Flask + SQLite 網站版本。

## 已完成功能

- 查看洗衣機狀態
- 新增洗衣機資料
- 回報洗衣機狀態
- 設定剩餘時間
- 編輯洗衣機資料
- 刪除洗衣機資料
- 重置 Demo 資料
- 使用 SQLite 儲存資料
- 使用 Flask 路由處理網頁功能
- 使用 Jinja2 顯示資料
- 使用 CSS 完成響應式畫面設計
- 使用 PowerShell Transcript 保存終端機紀錄

## 使用指令

~~~powershell
Start-Transcript -Path .\terminal_log.txt -Append
pip install -r requirements.txt
python app.py
git add .
git commit -m "Add complete Flask SQLite LaundryNow demo"
git push
Stop-Transcript
~~~
