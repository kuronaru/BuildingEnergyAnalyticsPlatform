from logging import getLogger

from flask import Blueprint, request, jsonify
from flask_login import logout_user

from applications.database.db_user_manager import UserManager
from applications.models.model_bms import BMSModel
from applications.models.model_sensor import SensorModel
from server_status import SUCCESS, FAILURE

homepage_bp = Blueprint('homepage', __name__)
logger = getLogger(__name__)


@homepage_bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    """
    功能：显示用户信息
    """
    data = request.get_json()
    username = data.get('username')
    logger.debug(f"get_user_info {username}")

    user_manager = UserManager.find_user_by_name(username)
    user_info = user_manager.user_info()
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


@homepage_bp.route('/logout', methods=['POST'])
def logout():
    """
    功能：注销并退出登录
    """
    # 断开各个连接，退出登录
    result = logout_user()
    if result:
        return jsonify({'status': SUCCESS, 'message': 'User logged out successfully'})
    else:
        return jsonify({'status': FAILURE, 'message': 'User logout failed'})
