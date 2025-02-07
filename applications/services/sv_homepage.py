from flask import Blueprint, request, jsonify

from applications.models.model_bms import BMSModel
from applications.models.model_sensor import SensorModel
from applications.models.model_user import UserModel
from server_status import SUCCESS, FAILURE

homepage_bp = Blueprint('homepage', __name__)


@homepage_bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    功能：显示用户信息
    """
    data = request.get_json()
    username = data.get('username')

    user_model = UserModel()
    user_info = user_model.get_user_info(username)
    if user_info:
        return jsonify({'status': SUCCESS, 'data': user_info})
    else:
        return jsonify({'status': FAILURE, 'data': None})


@homepage_bp.route('/get_bms_info', methods=['GET'])
def get_bms_info():
    """
    功能：显示 BMS 连接信息
    """
    bms_model = BMSModel()
    bms_info = bms_model.get_bms_info()
    if bms_info:
        return jsonify({'status': SUCCESS, 'data': bms_info})
    else:
        return jsonify({'status': FAILURE, 'data': None})


@homepage_bp.route('/get_sensor_info', methods=['GET'])
def get_sensor_info():
    """
    功能：显示传感器信息
    """
    sensor_model = SensorModel()
    sensor_info = sensor_model.get_sensor_info()
    if sensor_info:
        return jsonify({'status': SUCCESS, 'data': sensor_info})
    else:
        return jsonify({'status': FAILURE, 'data': None})


def logout_user(username):
    return True


@homepage_bp.route('/logout', methods=['POST'])
def logout():
    """
    功能：注销并退出登录
    """
    data = request.get_json()
    username = data.get('username')

    # 断开各个连接，退出登录
    result = logout_user(username)
    if result:
        return jsonify({'status': SUCCESS, 'message': 'User logged out successfully'})
    else:
        return jsonify({'status': FAILURE, 'message': 'User logout failed'})
