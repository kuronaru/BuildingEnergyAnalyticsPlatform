from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user

from server_status import SUCCESS, FAILURE
from applications.database.db_user_manager import UserManager

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    """
    登录接口，通过用户名和密码验证用户有效性，并完成登录。
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_manager = UserManager.find_user_by_name(username)
    if user_manager and UserManager.verify_credentials(username, password):
        login_user(user_manager)  # 使用 `UserManager` 实例完成 Flask-Login 登录
        return jsonify({
            'status': SUCCESS,
            'message': "Login successful",
            'user_info': user_manager.user_info
        })
    else:
        return jsonify({'status': FAILURE, 'message': 'Invalid username or password'}), 401

@login_bp.route('/register', methods=['POST'])
def register():
    """
    注册接口，通过提交用户名和密码创建一个新用户。
    """
    # 获取请求数据
    data = request.get_json()

    # 从请求中提取字段
    username = data.get('username')
    password = data.get('password')
    authority = data.get('authority', 1)  # 如果未提供 authority，默认为 1

    # 验证输入的字段是否合法
    if not username or not password:
        return jsonify({'status': FAILURE, 'message': 'Username and password are required'}), 400

    if len(username) > 25:
        return jsonify({'status': FAILURE, 'message': 'Username exceeds maximum length of 25'}), 400

    if not isinstance(authority, int) or authority < 0:
        return jsonify({'status': FAILURE, 'message': 'Authority must be a non-negative integer'}), 400

    # 检查用户名是否已存在
    if UserManager.find_user_by_name(username):
        return jsonify({'status': FAILURE, 'message': 'Username already exists'}), 409

    # 使用 Bcrypt 加密用户密码
    from applications import bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 调用 UserManager 中的 create_user 方法创建新用户
    new_user = UserManager.create_user(username=username, hashed_password=hashed_password, authority=authority)

    if new_user:
        return jsonify({
            'status': SUCCESS,
            'message': 'User registered successfully',
            'user_info': {
                'username': username,
                'authority': authority
            }
        }), 201
    else:
        return jsonify({'status': FAILURE, 'message': 'An error occurred while registering the user'}), 500