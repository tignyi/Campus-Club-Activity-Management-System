# 校園社團活動管理系統

本專案為一套以原生技術實作的「校園社團活動管理系統」網站，提供學生與社團幹部一個集中式的平台用來瀏覽活動、線上報名、留言互動與後台管理，並具備多角色權限與統計分析功能。

## 功能總覽

### 一般學生
- 註冊 / 登入系統
- 活動列表瀏覽、分類與搜尋
- 活動詳情查詢與線上報名 / 取消
- 留言互動、投票參與

### 社團幹部
- 活動新增 / 修改 / 刪除
- 報名名單查詢與匯出 CSV
- 留言管理（回覆 / 刪除）
- 活動審核進度追蹤

### 校方 / 系統管理員
- 使用者帳號與權限管理
- 社團基本資料管理
- 系統統計圖表（活動數量、登入次數、報名人次等）

## 技術架構

| 類別     | 技術                            |
|----------|---------------------------------|
| 前端     | HTML5, CSS3, JavaScript（原生）, Bootstrap |
| 後端     | Python（Flask 或純 CGI）, Hashlib, Session/Cookie |
| 資料庫   | MySQL                           |
| 圖表     | Chart.js                        |
| API 測試 | Postman / curl                  |

## 頁面一覽

- `index.html`：首頁活動瀏覽
- `register.html`：會員註冊
- `login.html`：會員登入
- `events.html`：活動列表與篩選
- `event_detail.html`：活動詳情與留言
- `events_manage.html`：社團幹部活動管理
- `registration_admin.html`：報名名單管理
- `user_admin.html`：使用者後台管理
- `dashboard.html`：系統統計分析
- `poll.html`：投票互動功能頁

## 專案部署與展示

若已開啟 GitHub Pages，可透過以下網址預覽前端畫面：

網址範例：`https://tignyi.github.io/Campus-Club-Activity-Management-System/`
