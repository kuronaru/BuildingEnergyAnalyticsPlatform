from flask_login import UserMixin

from applications.extensions import db
from applications.models.model_user import User


class UserManager(UserMixin):
    """
    用户管理器类，封装对 `User` 模型的所有数据库操作逻辑。
    """

    def __init__(self, user: User = None):
        """
        初始化 `UserManager`，将 User 数据实例化后传入。
        """
        self._user = user  # 使用私有属性存储用户实例
        self.id = user.id

    @property
    def user_info(self) -> dict:
        """
        返回用户的信息字典，而非 User 模型实例。
        """
        if self._user:
            return {
                'id': self._user.id,
                'username': self._user.username,
                'authority': self._user.authority
            }
        return {}

    @staticmethod
    def create_user(username: str, hashed_password: str, authority: int = 1) -> bool:
        """
        创建新用户，返回是否成功。
        """
        try:
            new_user = User(username=username, password=hashed_password, authority=authority)
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            db.session.close()

    @staticmethod
    def find_user_by_name(username: str):
        """
        按用户名查询用户，返回一个 `UserManager` 实例（或 None）。
        """
        user = User.query.filter_by(username=username).first()
        if user:
            return UserManager(user)
        return None

    @staticmethod
    def find_user_by_id(user_id: int):
        """
        按用户 ID 查询用户，返回一个 `UserManager` 实例（或 None）。
        """
        user = User.query.get(user_id)
        if user:
            return UserManager(user)
        return None

    def check_authority(self, authority: int) -> bool:
        """
        检查当前用户的权限是否满足指定要求。
        """
        if self._user:
            return self._user.authority <= authority
        return False

    def update_password(self, new_password: str) -> bool:
        """
        更新用户密码。
        """
        if self._user:
            try:
                self._user.password = new_password
                db.session.commit()
                return True
            except Exception as e:
                print(f"Error updating password: {e}")
                return False
            finally:
                db.session.close()
        return False

    @staticmethod
    def verify_credentials(username: str, password: str) -> bool:
        """
        验证用户名和密码是否匹配。
        """
        from applications import bcrypt
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return True
        return False