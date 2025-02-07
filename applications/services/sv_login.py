from flask import Blueprint, request, jsonify

from applications.models.model_user import UserModel
from server_status import SUCCESS, FAILURE

# 创建蓝图
login_bp = Blueprint('login', __name__)


@login_bp.route('/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': FAILURE, 'message': "Username and password are required"}), 400

    # 创建数据库模型实例
    user_model = UserModel()

    # 验证密码
    if user_model.check_credential(username, password):
        return jsonify({'status': SUCCESS, 'message': 'Login successful'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Invalid credentials'}), 401
