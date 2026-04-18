from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# 主页路由
@app.route('/')
def index():
    conn = sqlite3.connect('garden.db')
    members = conn.execute('SELECT name FROM members').fetchall()
    flowers = conn.execute('SELECT name FROM flowers').fetchall()
    conn.close()
    return render_template('index.html', members=members, flowers=flowers)

# 查询接口：查花找人
@app.route('/search/flower', methods=['POST'])
def search_flower():
    flower = request.form.get('flower', '')
    conn = sqlite3.connect('garden.db')
    data = conn.execute('''
    SELECT m.name FROM members m
    JOIN member_flower mf ON m.id = mf.member_id
    JOIN flowers f ON mf.flower_id = f.id
    WHERE f.name LIKE ?
    ''', ("%"+flower+"%",)).fetchall()
    conn.close()
    return jsonify([item[0] for item in data])

# 查询接口：查人找花
@app.route('/search/member', methods=['POST'])
def search_member():
    conn = sqlite3.connect('garden.db')
    data = conn.execute('''
    SELECT f.name FROM flowers f
    JOIN member_flower mf ON f.id = mf.flower_id
    JOIN members m ON mf.member_id = m.id
    WHERE m.name LIKE ?
    ''', ("%"+request.form.get('member', '')+"%",)).fetchall()
    conn.close()
    return jsonify([item[0] for item in data])
if  __name__ == '__main__': app.run(debug=True)