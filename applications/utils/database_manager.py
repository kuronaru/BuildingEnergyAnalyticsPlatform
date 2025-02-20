import os
import sqlite3
import threading


class DatabaseManager:
    def __init__(self):
        self.databases = {}  # 数据库字典，存储所有已注册数据库
        self.default_database = None  # 默认数据库名称
        self.local = threading.local()  # 线程本地数据

    def add_database(self, name, db_path):
        """添加数据库"""
        if name in self.databases:
            raise ValueError(f"数据库 '{name}' 已存在，请选择其他名称")

        path = os.path.join('instance', db_path)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))  # 自动创建目录

        connection = sqlite3.connect(path, check_same_thread=False)
        self.databases[name] = path
        self._set_thread_connection(name, connection)

    def remove_database(self, name):
        """移除数据库"""
        if name not in self.databases:
            raise ValueError(f"数据库 '{name}' 不存在")
        self._close_connection(name)  # 优雅关闭连接
        del self.databases[name]
        if self.default_database == name:
            self.default_database = None  # 如果是默认数据库，移除后置为 None

    def select_database(self, name):
        """选择默认数据库"""
        if name not in self.databases:
            raise ValueError(f"数据库 '{name}' 不存在")
        self.default_database = name
        connection = self._get_thread_connection(name)
        return connection

    def execute_query(self, query, params=None, db_name=None):
        """
        执行 SQL 查询语句并返回结果
        :param query: SQL 查询字符串
        :param params: 参数
        :param db_name: 指定数据库名称（可选，不指定则使用默认数据库）
        """
        if db_name is None:
            db_name = self.default_database
        if db_name not in self.databases:
            raise ValueError(f"数据库 '{db_name}' 不存在")

        connection = self._get_thread_connection(db_name)
        cursor = connection.cursor()
        try:
            cursor.execute(query, params or ())  # 执行查询语句
            results = cursor.fetchall()
            connection.commit()  # 提交事务
            return results
        except sqlite3.Error as e:
            connection.rollback()  # 出错时回滚事务
            raise RuntimeError(f"查询执行失败: {str(e)}")
        finally:
            cursor.close()

    def execute_transaction(self, queries, params_list=None, db_name=None):
        """
        执行事务（多个 SQL 语句）
        :param queries: 事务中的 SQL 语句列表
        :param params_list: 每条语句的参数列表
        :param db_name: 指定数据库名称（可选，不指定则使用默认数据库）
        """
        if db_name is None:
            db_name = self.default_database
        if db_name not in self.databases:
            raise ValueError(f"数据库 '{db_name}' 不存在")

        connection = self._get_thread_connection(db_name)
        cursor = connection.cursor()
        try:
            for i, query in enumerate(queries):
                params = params_list[i] if params_list else ()
                cursor.execute(query, params)
            connection.commit()  # 提交事务
        except sqlite3.Error as e:
            connection.rollback()  # 出错时回滚事务
            raise RuntimeError(f"事务执行失败: {str(e)}")
        finally:
            cursor.close()

    def close_all_connections(self):
        """关闭该线程的所有数据库连接"""
        if not hasattr(self.local, 'connections'):
            return
        for db_name, conn in self.local.connections.items():
            try:
                conn.close()
                print(f"已关闭数据库 '{db_name}' 的连接")
            except sqlite3.Error as e:
                print(f"关闭数据库 '{db_name}' 时遇到错误: {str(e)}")
        self.local.connections = {}

    def _get_thread_connection(self, name):
        """获取线程本地数据库连接"""
        if not hasattr(self.local, 'connections'):
            self.local.connections = {}
        if name not in self.local.connections:
            path = self.databases[name]
            self.local.connections[name] = sqlite3.connect(path, check_same_thread=False)
        return self.local.connections[name]

    def _set_thread_connection(self, name, connection):
        """为线程本地存储数据库连接"""
        if not hasattr(self.local, 'connections'):
            self.local.connections = {}
        self.local.connections[name] = connection

    def _close_connection(self, name):
        """关闭指定数据库的连接"""
        if hasattr(self.local, 'connections') and name in self.local.connections:
            try:
                self.local.connections[name].close()
                del self.local.connections[name]
            except sqlite3.Error as e:
                print(f"关闭数据库 '{name}' 时遇到错误: {str(e)}")

    def list_databases(self):
        """列出所有可用的数据库名称"""
        return {"databases": list(self.databases.keys()), "default": self.default_database}