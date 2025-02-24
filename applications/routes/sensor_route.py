from logging import getLogger

from flask import Blueprint, request, jsonify
from threading import Thread, Event
import time

# 假设有模型类负责与数据库通信
from applications.models.model_sensor import SensorModel
from server_status import SUCCESS, FAILURE

sensor_bp = Blueprint('sensor', __name__)
logger = getLogger(__name__)

# 全局变量控制传感器数据接收线程
receive_thread_stop_event = Event()


@sensor_bp.route('/receive_data', methods=['POST'])
def receive_data():
    """
    功能：控制传感器数据接收
    启动或停止线程、预览或存储数据
    """
    data = request.get_json()
    action = data.get('action')  # 'start' or 'stop'
    save_data = data.get('save_data', False)  # 是否存储接收到的数据
    db_name = data.get('db_name')  # 选择存储的数据库

    # 启动传感器数据接收
    if action == 'start':
        if receive_thread_stop_event.is_set():
            receive_thread_stop_event.clear()
            thread = Thread(target=receive_sensor_data, args=(save_data, db_name))
            thread.start()
            return jsonify({'status': SUCCESS, 'message': 'Started receiving data.'})
        else:
            return jsonify({'status': FAILURE, 'message': 'Data receiving is already running.'})

    # 停止传感器数据接收
    elif action == 'stop':
        if not receive_thread_stop_event.is_set():
            receive_thread_stop_event.set()
            return jsonify({'status': SUCCESS, 'message': 'Stopped receiving data.'})
        else:
            return jsonify({'status': FAILURE, 'message': 'Receiving is already stopped.'})

    else:
        return jsonify({'status': FAILURE, 'message': 'Invalid action specified.'})


def receive_sensor_data(save_data=False, db_name=None):
    """
    传感器数据接收线程：模拟持续接收数据
    """
    while not receive_thread_stop_event.is_set():
        # 模拟接收数据
        sensor_data = {
            'sensor_id': 'SENSOR-001',
            'timestamp': time.time(),
            'value': 30  # Random sensor value
        }

        print(f"Received data: {sensor_data}")

        # 如果需要存储到数据库
        if save_data and db_name:
            sensor_model = SensorModel()
            sensor_model.save_sensor_data(sensor_data, db_name)

        # 模拟接收频率
        time.sleep(1)


@sensor_bp.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    """
    功能：显示传感器数据
    """
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    limit = data.get('limit', 10)  # 显示最新的 10 条数据

    sensor_model = SensorModel()
    sensor_data = sensor_model.get_sensor_data(sensor_id, limit)

    if sensor_data:
        return jsonify({'status': SUCCESS, 'data': sensor_data})
    else:
        return jsonify({'status': FAILURE, 'data': None})


@sensor_bp.route('/add_sensor', methods=['POST'])
def add_sensor():
    """
    功能：添加传感器连接
    """
    data = request.get_json()
    sensor_info = data.get('sensor_info')

    sensor_model = SensorModel()
    result = sensor_model.add_sensor(sensor_info)

    if result:
        return jsonify({'status': SUCCESS, 'message': 'Sensor added successfully.'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Failed to add sensor.'})


@sensor_bp.route('/modify_sensor', methods=['PUT'])
def modify_sensor():
    """
    功能：修改传感器连接
    """
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    new_info = data.get('new_info')

    sensor_model = SensorModel()
    result = sensor_model.modify_sensor(sensor_id, new_info)

    if result:
        return jsonify({'status': SUCCESS, 'message': 'Sensor modified successfully.'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Failed to modify sensor.'})


@sensor_bp.route('/refresh_sensor', methods=['POST'])
def refresh_sensor():
    """
    功能：重新连接传感器
    """
    data = request.get_json()
    sensor_id = data.get('sensor_id')

    sensor_model = SensorModel()
    result = sensor_model.reconnect_sensor(sensor_id)

    if result:
        return jsonify({'status': SUCCESS, 'message': 'Sensor reconnected successfully.'})
    else:
        return jsonify({'status': FAILURE, 'message': 'Failed to reconnect sensor.'})