# 系統架構設計 Architecture

## 技術架構

| 層面 | 技術 |
|---|---|
| 前端 | HTML / CSS / JavaScript |
| 後端 | Python Flask |
| 模板 | Jinja2 |
| 資料庫 | SQLite |
| 版本控制 | GitHub |
| 開發工具 | VS Code、Antigravity |

## 系統說明

使用者透過瀏覽器進入 LaundryNow 網站，前端頁面顯示洗衣機狀態。當使用者新增或更新狀態時，資料會送到 Flask 後端，再由 Flask 操作 SQLite 資料庫，最後回傳最新資料到畫面。

## Mermaid 架構圖

~~~mermaid
flowchart LR
    User[使用者] --> Browser[瀏覽器]
    Browser --> Frontend[HTML CSS JavaScript]
    Frontend --> Flask[Flask 路由]
    Flask --> SQLite[SQLite 資料庫]
    SQLite --> Flask
    Flask --> Frontend
    Frontend --> Browser
    Browser --> User
~~~
