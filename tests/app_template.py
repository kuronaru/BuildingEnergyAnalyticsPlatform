import sys
import threading
import sqlite3
from flask import Flask, jsonify, request
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextBrowser
import requests

# 创建 Flask 应用
app = Flask(__name__)


# SQLite 数据库初始化
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Flask 路由
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # 获取所有用户数据
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()
        return jsonify({"users": [{"id": row[0], "name": row[1], "age": row[2]} for row in rows]})
    elif request.method == 'POST':
        # 添加用户数据
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        if name and age:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            conn.commit()
            conn.close()
            return jsonify({"message": "用户已添加"}), 201
        else:
            return jsonify({"error": "缺少必要的字段"}), 400


# 后端运行线程
def run_flask():
    app.run(debug=False, host='127.0.0.1', port=5000)


# PyQt 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output = None
        self.get_button = None
        self.add_button = None
        self.age_input = None
        self.name_input = None
        self.label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Flask + PyQt + SQLite 桌面应用")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("请输入用户信息：", self)
        layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("姓名")
        layout.addWidget(self.name_input)

        self.age_input = QLineEdit(self)
        self.age_input.setPlaceholderText("年龄")
        layout.addWidget(self.age_input)

        self.add_button = QPushButton("添加用户", self)
        self.add_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_button)

        self.get_button = QPushButton("获取所有用户", self)
        self.get_button.clicked.connect(self.get_users)
        layout.addWidget(self.get_button)

        self.output = QTextBrowser(self)
        layout.addWidget(self.output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_user(self):
        name = self.name_input.text()
        age = self.age_input.text()
        if name and age.isdigit():
            try:
                data = {"name": name, "age": int(age)}
                response = requests.post("http://127.0.0.1:5000/api/users", json=data)
                if response.status_code == 201:
                    self.output.append(f"用户 {name} 添加成功！")
                else:
                    self.output.append(f"添加失败: {response.json().get('error', '未知错误')}")
            except Exception as e:
                self.output.append(f"错误: {e}")
        else:
            self.output.append("请输入有效的姓名和年龄！")

    def get_users(self):
        try:
            response = requests.get("http://127.0.0.1:5000/api/users")
            if response.status_code == 200:
                users = response.json().get("users", [])
                self.output.append("用户列表：")
                for user in users:
                    self.output.append(f"ID: {user['id']}, 姓名: {user['name']}, 年龄: {user['age']}")
            else:
                self.output.append(f"获取失败: {response.status_code}")
        except Exception as e:
            self.output.append(f"错误: {e}")


# 主程序入口
if __name__ == "__main__":
    # 初始化数据库
    init_db()

    # 启动 Flask 服务线程
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.setDaemon(True)  # 守护线程
    flask_thread.start()

    # 启动 PyQt 应用
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
