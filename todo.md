# 校園社團活動管理系統 - 功能開發優化清單

## 技術棧
- 後端：Python（Flask/FastAPI，MySQL，hashlib，session/cookie）
- 前端：HTML5 + CSS3 + JavaScript（原生）+ Bootstrap（排版/元件）
- 資料庫：MySQL
- 圖表：Chart.js
- 測試：Postman/curl

---

## 一、會員系統（註冊 / 登入）

- [ ] 設計 MySQL 資料表 `users`
    - 欄位：id (PK, AI), username (唯一), password_hash, email, role (student/staff/admin), created_at
- [ ] 建立 `register.py`
    - [ ] 接收註冊表單（username, email, password）
    - [ ] 檢查帳號/信箱唯一性
    - [ ] 密碼使用 hashlib 加密
    - [ ] 寫入 DB
    - [ ] 回傳 JSON 結果（成功/失敗/錯誤訊息）
- [ ] 建立 `login.py`
    - [ ] 接收登入表單（username, password）
    - [ ] 驗證帳號密碼（hash 比對）
    - [ ] 登入成功產生 session，設置 cookie
    - [ ] 回傳 JSON 結果（含登入狀態/錯誤訊息）
- [ ] 前端 `register.html`
    - [ ] Bootstrap 表單（username, email, password, confirm password）
    - [ ] JavaScript 驗證（必填、格式、密碼一致）
    - [ ] AJAX POST 至 `register.py`
    - [ ] 顯示註冊成功/失敗提示
- [ ] 前端 `login.html`
    - [ ] Bootstrap 表單（username, password）
    - [ ] JavaScript 驗證
    - [ ] AJAX POST 至 `login.py`
    - [ ] 登入成功導向首頁，失敗顯示提示

---

## 二、活動瀏覽（清單 / 分類）

- [ ] 設計 MySQL 資料表 `events`
    - 欄位：id, title, category, date, organizer, image, description, approval_status
- [ ] 建立 `list_events.py`
    - [ ] 回傳所有活動（支援 category、日期篩選，JSON 格式）
- [ ] 建立 `get_categories.py`
    - [ ] 回傳所有活動分類（JSON）
- [ ] 前端 `events.html`
    - [ ] Bootstrap 卡片顯示活動
    - [ ] 下拉選單過濾分類/日期
    - [ ] JavaScript 動態載入/篩選

---

## 三、活動詳情

- [ ] 建立 `event_detail.py`
    - [ ] 根據 event_id 回傳活動詳細資訊（JSON）
- [ ] 前端 `event_detail.html`
    - [ ] 顯示活動資訊、主辦社團、圖片
    - [ ] 若已登入，顯示報名/取消報名按鈕

---

## 四、活動報名

- [ ] 設計 MySQL 資料表 `registrations`
    - 欄位：id, user_id, event_id, created_at
- [ ] 建立 `register_event.py`
    - [ ] POST 新增報名（需登入）
    - [ ] 檢查是否重複報名
- [ ] 建立 `cancel_event.py`
    - [ ] POST 取消報名（需登入）
- [ ] 建立 `get_my_registrations.py`
    - [ ] 回傳目前使用者報名清單
- [ ] 前端 `event_detail.html`
    - [ ] 顯示「已報名/可報名/取消報名」按鈕
    - [ ] 呼叫 API 並即時刷新狀態

---

## 五、學生互動（留言 / 問答 / 投票）

- [ ] 設計 MySQL 資料表 `comments`
    - 欄位：id, user_id, event_id, content, created_at
- [ ] 建立 `post_comment.py`
    - [ ] 新增留言（需登入）
- [ ] 建立 `get_comments.py`
    - [ ] 載入留言（依 event_id）
- [ ] 前端 `event_detail.html`
    - [ ] 留言輸入框＋發送按鈕
    - [ ] 留言顯示區塊（即時更新）
- [ ] 設計資料表 `polls`、`poll_options`、`poll_votes`
- [ ] 建立投票 API（建立、投票、查詢統計）
- [ ] 前端 `poll.html`
    - [ ] 投票選項＋結果圖示

---

## 【社團幹部管理端】

### 一、活動管理

- [ ] 設計 `events` 表加入社團ID、審核狀態
- [ ] 建立 `create_event.py`（新增活動）
- [ ] 建立 `edit_event.py`（修改活動）
- [ ] 建立 `delete_event.py`（刪除活動）
- [ ] 前端 `events_manage.html`
    - [ ] 活動列表＋新增/編輯/刪除按鈕
    - [ ] JS 彈跳表單/modal 編輯

### 二、報名管理

- [ ] 建立 `get_registrations.py`（查詢活動報名名單）
- [ ] 建立 `export_registrations_csv.py`（匯出 CSV）
- [ ] 前端 `registration_admin.html`
    - [ ] 報名清單＋匯出按鈕

### 三、活動審核

- [ ] `events` 表 approval_status 欄位（0: 草稿, 1: 待審核, 2: 通過, 3: 駁回）
- [ ] 建立 `review_event.py`（送審/審核/駁回）
- [ ] 前端 `event_review.html`
    - [ ] 顯示審核狀態＋操作按鈕

### 四、留言管理

- [ ] 建立 `get_comments.py`（查詢留言）
- [ ] 建立 `reply_comment.py`（回覆留言）
- [ ] 建立 `delete_comment.py`（刪除留言）
- [ ] 前端 `comment_moderation.html`
    - [ ] 留言內容＋回覆/刪除按鈕

---

## 【後台管理（校方/系統管理員）】

### 一、使用者管理

- [ ] `users` 表 role 欄位（student/staff/admin）
- [ ] 建立 `manage_users.py`（查詢/停用/刪除/角色切換）
- [ ] 前端 `user_admin.html`
    - [ ] 使用者清單、篩選、停權/提升權限

### 二、社團管理

- [ ] 設計 `clubs` 表（名稱、社長ID、簡介、聯絡方式）
- [ ] 建立 `get_clubs.py`（查詢社團）
- [ ] 建立 `edit_club.py`（編輯社團）
- [ ] 前端 `club_admin.html`
    - [ ] 社團卡片展示、編輯

### 三、系統統計

- [ ] 建立 `generate_stats.py`（報名人次/登入次數/活動數量）
- [ ] 前端 `dashboard.html`
    - [ ] 圓餅圖/長條圖（Chart.js）
    - [ ] 每月/社團別分析

### 四、權限管理

- [ ] `users` 表設計角色與權限
- [ ] 前端 `role_manage.html`
    - [ ] 下拉選單切換角色，限制功能
- [ ] 所有管理功能後端加上 `if user.role == 'admin'` 權限判斷
