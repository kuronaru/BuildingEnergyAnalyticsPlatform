from flask import Blueprint, request, jsonify

from applications.models.model_user import UserModel

# 创建蓝图
login_bp = Blueprint('login', __name__)

# 实例化数据库和消息队列
# mq = MessageQueue()


@login_bp.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 数据库验证用户
    user_model = UserModel()
    if user_model.authenticate_user(username, password):
        # 登录成功，发送消息到消息队列
        # mq.send(f'{username} logged in')
        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401


# @login_bp.route('/recv_msg', methods=['GET'])
# def receive_message():
#     """用于获取队列中的消息"""
#     message = mq.receive()
#     if message:
#         return jsonify({'message': message})
#     return jsonify({'message': 'No messages in the queue'})
