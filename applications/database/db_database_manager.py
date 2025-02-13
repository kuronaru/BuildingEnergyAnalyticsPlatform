import os
import sqlite3
import threading


class DatabaseManager:
    def __init__(self):
        self.databases = {}
        self.local = threading.local()

    def add_database(self, name, db_path):
        path = os.path.join('instance', db_path)
        self.databases[name] = sqlite3.connect(path)


    def close_all_connections(self):
        """关闭线程本地的所有数据库连接"""
        if hasattr(self.local, 'connections'):
            for conn in self.local.connections.values():
                conn.close()
            self.local.connections.clear()
