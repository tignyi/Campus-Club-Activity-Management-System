# 校園社團活動管理系統 MongoDB 資料結構範例

# 會員 users
user_example = {
    "_id": "ObjectId",  # MongoDB 自動產生
    "username": "string",  # 唯一
    "email": "string",     # 唯一
    "password_hash": "string",
    "role": "student",     # student/staff/admin
    "created_at": "datetime"
}

# 活動 events
event_example = {
    "_id": "ObjectId",
    "title": "string",
    "category": "string",
    "date": "datetime",
    "organizer": "string",  # 主辦社團名稱
    "image": "string",      # 圖片網址
    "description": "string",
    "approval_status": 1,    # 0:草稿, 1:待審核, 2:通過, 3:駁回
    "club_id": "ObjectId"   # 所屬社團
}

# 報名 registrations
registration_example = {
    "_id": "ObjectId",
    "user_id": "ObjectId",
    "event_id": "ObjectId",
    "created_at": "datetime"
}

# 留言 comments
comment_example = {
    "_id": "ObjectId",
    "user_id": "ObjectId",
    "event_id": "ObjectId",
    "content": "string",
    "created_at": "datetime"
}

# 投票 polls
poll_example = {
    "_id": "ObjectId",
    "event_id": "ObjectId",
    "title": "string",
    "options": [
        {"option_id": "ObjectId", "text": "string", "votes": 0}
    ],
    "created_at": "datetime"
}

# 社團 clubs
club_example = {
    "_id": "ObjectId",
    "name": "string",
    "president_id": "ObjectId",
    "intro": "string",
    "contact": "string"
}

# ...可依需求擴充/調整...