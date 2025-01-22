from applications.database.db_user import UserDatabase
from applications.extensions import db


class User(db.Model):
    """
    通过 SQLAlchemy 的查询构建器实现的快捷操作，用于高效地更新数据库中的记录。
    这个方法适用于不需要加载模型实例的场景，而对于需要触发事件或验证逻辑的场景，建议使用实例更新的方法。
    """
    __bind_key__ = 'users'  # 绑定到 users 数据库
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    password = db.Column(db.String(128), comment='密码哈希')


class UserModel:
    """
    常规的数据库模型类实现，对每个单独的功能设置了相对应的函数调用，定义方便但是代码比较长，需要对SQL语言有一定了解。
    """
    def __init__(self):
        self.db = UserDatabase()

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        results = self.db.execute_query(query, (username, password))
        return len(results) > 0

    def create_user(self, username, password):
        try:
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
            self.db.execute_query(query, (username, password))
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
