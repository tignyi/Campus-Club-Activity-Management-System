from flask import Flask, request, jsonify, session
from flask_cors import CORS
from db import get_db
import hashlib
from bson import ObjectId

app = Flask(__name__)
CORS(app)
app.secret_key = 'campusclubsecretkey'

def to_json(obj):
    obj = dict(obj)
    obj["_id"] = str(obj["_id"])
    return obj

@app.route('/')
def index():
    return " Campus Club API is running!"


@app.route('/api/ping')
def ping():
    return jsonify({"msg": "pong"})

# 會員註冊
@app.route('/api/register', methods=['POST'])
def register():
    db = get_db()
    data = request.json
    if db.users.find_one({"username": data["username"]}) or db.users.find_one({"email": data["email"]}):
        return jsonify({"success": False, "msg": "帳號或信箱已存在"})
    password_hash = hashlib.sha256(data["password"].encode()).hexdigest()
    user = {
        "username": data["username"],
        "email": data["email"],
        "password_hash": password_hash,
        "role": "student",
        "created_at": __import__('datetime').datetime.utcnow()
    }
    db.users.insert_one(user)
    return jsonify({"success": True, "msg": "註冊成功"})

# 會員登入
@app.route('/api/login', methods=['POST'])
def login():
    db = get_db()
    data = request.json
    user = db.users.find_one({"username": data["username"]})
    if not user:
        return jsonify({"success": False, "msg": "帳號不存在"})
    password_hash = hashlib.sha256(data["password"].encode()).hexdigest()
    if user["password_hash"] != password_hash:
        return jsonify({"success": False, "msg": "密碼錯誤"})
    session['user_id'] = str(user['_id'])
    session['role'] = user['role']
    return jsonify({"success": True, "msg": "登入成功", "user": to_json(user)})

# 活動清單（支援分類/日期篩選）
@app.route('/api/events', methods=['GET'])
def list_events():
    db = get_db()
    category = request.args.get('category')
    date = request.args.get('date')
    query = {}
    if category:
        query['category'] = category
    if date:
        query['date'] = date
    events = [to_json(e) for e in db.events.find(query)]
    return jsonify(events)

# 活動分類
@app.route('/api/categories', methods=['GET'])
def get_categories():
    db = get_db()
    categories = db.events.distinct('category')
    return jsonify(categories)

# 活動詳情
@app.route('/api/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    db = get_db()
    event = db.events.find_one({'_id': ObjectId(event_id)})
    if not event:
        return jsonify({'success': False, 'msg': '活動不存在'})
    return jsonify(to_json(event))

# 報名活動
@app.route('/api/event/<event_id>/register', methods=['POST'])
def register_event(event_id):
    db = get_db()
    user_id = request.json.get('user_id')
    if db.registrations.find_one({'user_id': ObjectId(user_id), 'event_id': ObjectId(event_id)}):
        return jsonify({'success': False, 'msg': '已報名'})
    reg = {
        'user_id': ObjectId(user_id),
        'event_id': ObjectId(event_id),
        'created_at': __import__('datetime').datetime.utcnow()
    }
    db.registrations.insert_one(reg)
    return jsonify({'success': True, 'msg': '報名成功'})

# 取消報名
@app.route('/api/event/<event_id>/cancel', methods=['POST'])
def cancel_event(event_id):
    db = get_db()
    user_id = request.json.get('user_id')
    db.registrations.delete_one({'user_id': ObjectId(user_id), 'event_id': ObjectId(event_id)})
    return jsonify({'success': True, 'msg': '已取消報名'})

# 取得個人報名清單
@app.route('/api/my_registrations', methods=['GET'])
def get_my_registrations():
    db = get_db()
    user_id = request.args.get('user_id')
    regs = [to_json(r) for r in db.registrations.find({'user_id': ObjectId(user_id)})]
    return jsonify(regs)

# 活動留言（載入）
@app.route('/api/event/<event_id>/comments', methods=['GET'])
def get_comments(event_id):
    db = get_db()
    comments = [to_json(c) for c in db.comments.find({'event_id': ObjectId(event_id)})]
    return jsonify(comments)

# 新增留言
@app.route('/api/event/<event_id>/comment', methods=['POST'])
def post_comment(event_id):
    db = get_db()
    user_id = request.json.get('user_id')
    content = request.json.get('content')
    comment = {
        'user_id': ObjectId(user_id),
        'event_id': ObjectId(event_id),
        'content': content,
        'created_at': __import__('datetime').datetime.utcnow()
    }
    db.comments.insert_one(comment)
    return jsonify({'success': True, 'msg': '留言成功'})

# 投票 API（建立、投票、查詢統計）
@app.route('/api/event/<event_id>/poll', methods=['POST'])
def create_poll(event_id):
    db = get_db()
    title = request.json.get('title')
    options = request.json.get('options')  # list of text
    poll = {
        'event_id': ObjectId(event_id),
        'title': title,
        'options': [{'option_id': ObjectId(), 'text': opt, 'votes': 0} for opt in options],
        'created_at': __import__('datetime').datetime.utcnow()
    }
    db.polls.insert_one(poll)
    return jsonify({'success': True, 'msg': '投票建立成功'})

@app.route('/api/poll/<poll_id>/vote', methods=['POST'])
def vote_poll(poll_id):
    db = get_db()
    option_id = request.json.get('option_id')
    db.polls.update_one({'_id': ObjectId(poll_id), 'options.option_id': ObjectId(option_id)}, {'$inc': {'options.$.votes': 1}})
    return jsonify({'success': True, 'msg': '投票成功'})

@app.route('/api/poll/<poll_id>', methods=['GET'])
def poll_result(poll_id):
    db = get_db()
    poll = db.polls.find_one({'_id': ObjectId(poll_id)})
    if not poll:
        return jsonify({'success': False, 'msg': '投票不存在'})
    return jsonify(to_json(poll))

# 社團管理
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    db = get_db()
    clubs = [to_json(c) for c in db.clubs.find()]
    return jsonify(clubs)

@app.route('/api/club/<club_id>', methods=['POST'])
def edit_club(club_id):
    db = get_db()
    data = request.json
    db.clubs.update_one({'_id': ObjectId(club_id)}, {'$set': data})
    return jsonify({'success': True, 'msg': '社團資料已更新'})

# 活動管理（新增/編輯/刪除）
@app.route('/api/event', methods=['POST'])
def create_event():
    db = get_db()
    data = request.json
    data['created_at'] = __import__('datetime').datetime.utcnow()
    db.events.insert_one(data)
    return jsonify({'success': True, 'msg': '活動已新增'})

@app.route('/api/event/<event_id>', methods=['POST'])
def edit_event(event_id):
    db = get_db()
    data = request.json
    db.events.update_one({'_id': ObjectId(event_id)}, {'$set': data})
    return jsonify({'success': True, 'msg': '活動已更新'})

@app.route('/api/event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    db = get_db()
    db.events.delete_one({'_id': ObjectId(event_id)})
    return jsonify({'success': True, 'msg': '活動已刪除'})

# 報名管理（查詢/匯出）
@app.route('/api/event/<event_id>/registrations', methods=['GET'])
def get_registrations(event_id):
    db = get_db()
    regs = [to_json(r) for r in db.registrations.find({'event_id': ObjectId(event_id)})]
    return jsonify(regs)

@app.route('/api/event/<event_id>/registrations/export', methods=['GET'])
def export_registrations_csv(event_id):
    db = get_db()
    regs = list(db.registrations.find({'event_id': ObjectId(event_id)}))
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'event_id', 'created_at'])
    for r in regs:
        writer.writerow([str(r['user_id']), str(r['event_id']), r['created_at']])
    return output.getvalue(), 200, {'Content-Type': 'text/csv'}

# 活動審核
@app.route('/api/event/<event_id>/review', methods=['POST'])
def review_event(event_id):
    db = get_db()
    status = request.json.get('approval_status')
    db.events.update_one({'_id': ObjectId(event_id)}, {'$set': {'approval_status': status}})
    return jsonify({'success': True, 'msg': '審核狀態已更新'})

# 留言管理（回覆/刪除）
@app.route('/api/comment/<comment_id>/reply', methods=['POST'])
def reply_comment(comment_id):
    db = get_db()
    reply = request.json.get('reply')
    db.comments.update_one({'_id': ObjectId(comment_id)}, {'$set': {'reply': reply}})
    return jsonify({'success': True, 'msg': '已回覆'})

@app.route('/api/comment/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    db = get_db()
    db.comments.delete_one({'_id': ObjectId(comment_id)})
    return jsonify({'success': True, 'msg': '留言已刪除'})

# 使用者管理（查詢/停用/刪除/角色切換）
@app.route('/api/users', methods=['GET'])
def manage_users():
    db = get_db()
    users = [to_json(u) for u in db.users.find()]
    return jsonify(users)

@app.route('/api/user/<user_id>/role', methods=['POST'])
def change_role(user_id):
    db = get_db()
    role = request.json.get('role')
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': role}})
    return jsonify({'success': True, 'msg': '角色已更新'})

@app.route('/api/user/<user_id>/disable', methods=['POST'])
def disable_user(user_id):
    db = get_db()
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'disabled': True}})
    return jsonify({'success': True, 'msg': '已停用'})

@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'success': True, 'msg': '使用者已刪除'})

# 系統統計
@app.route('/api/stats', methods=['GET'])
def generate_stats():
    db = get_db()
    stats = {
        'user_count': db.users.count_documents({}),
        'event_count': db.events.count_documents({}),
        'registration_count': db.registrations.count_documents({})
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)