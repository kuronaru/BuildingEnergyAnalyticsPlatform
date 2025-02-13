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
    authority = db.Column(db.Integer, comment='权限等级')
