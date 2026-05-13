# 資料庫欄位規劃 DB Design

## 資料表名稱
machines

## 欄位設計

| 欄位名稱 | 資料型別 | 限制 | 用途 |
|---|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 洗衣機資料識別碼 |
| machine_number | TEXT | NOT NULL | 洗衣機編號 |
| location | TEXT | NOT NULL | 洗衣機所在樓層或位置 |
| status | TEXT | NOT NULL | 狀態：空閒、使用中、故障 |
| remaining_time | INTEGER | 不可為負數 | 剩餘使用時間，單位為分鐘 |
| updated_at | TEXT | 自動更新 | 最後更新時間 |

## 狀態限制
status 只能包含：
- 空閒
- 使用中
- 故障

## 範例資料

| id | machine_number | location | status | remaining_time | updated_at |
|---|---|---|---|---|---|
| 1 | A01 | 福星宿舍 1 樓洗衣間 | 空閒 | 0 | 2026-05-14 10:00 |
| 2 | A02 | 福星宿舍 1 樓洗衣間 | 使用中 | 25 | 2026-05-14 10:05 |
| 3 | B01 | 福星宿舍 2 樓洗衣間 | 故障 | 0 | 2026-05-14 09:50 |
