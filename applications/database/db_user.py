import sqlite3


class UserDatabase:
    def __init__(self, db_path='instance/users.db'):
        self.db_path = db_path

    def get_connection(self):
        """创建一个数据库连接"""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=()):
        """执行查询"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def init_user_db(self):
        """初始化 users.db 数据库"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('test_user', '123456'))
        conn.commit()
        conn.close()
