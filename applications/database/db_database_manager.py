import os
import sqlite3
import threading


class DatabaseManager:
    def __init__(self):
        self.databases = {}
        self.default_database = None
        self.local = threading.local()

    def add_database(self, name, db_path):
        path = os.path.join('instance', db_path)
        self.databases[name] = sqlite3.connect(path)

    def select_database(self, name):
        self.default_database = name
        return self.databases[name]

    def close_all_connections(self):
        """关闭线程本地的所有数据库连接"""
        if hasattr(self.local, 'connections'):
            for conn in self.local.connections.values():
                conn.close()
            self.local.connections.clear()
