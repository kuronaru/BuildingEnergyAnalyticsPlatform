import socket
from logging import getLogger

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO
from marshmallow.utils import timestamp

from applications.database.db_bms_manager import BMSDataManager

from applications.services.bms_service import connect_to_bms, disconnect_from_bms, start_receive_data_thread, \
    generate_object_key_with_hash, stop_receive_data_thread, get_device_objects_service, get_device_latest_data
from server_status import SUCCESS, FAILURE

bms_bp = Blueprint('bms', __name__)
logger = getLogger(__name__)
socketio = SocketIO()
receive_task_futures = {}


@bms_bp.route('/get_local_ip', methods=['GET'])
def get_local_ip():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        return jsonify({'status': SUCCESS, 'local_ip': local_ip})
    except Exception as e:
        logger.error(f"Error retrieving local IP: {e}")
        return jsonify({'status': FAILURE, 'message': "Error retrieving local IP."})


@bms_bp.route('/connect_bms', methods=['POST'])
def connect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': "IP or port is missing."})

    connection_status = connect_to_bms(ip, port)

    if connection_status:
        return jsonify({'status': SUCCESS, 'message': f"Connected to BMS server at {ip}:{port}."})
    else:
        return jsonify({'status': FAILURE, 'message': f"Failed to connect to {ip}:{port}."})


@bms_bp.route('/disconnect_bms', methods=['POST'])
def disconnect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': "IP or port is missing."})

    disconnection_status = disconnect_from_bms(ip, port)

    if disconnection_status:
        return jsonify({'status': SUCCESS, 'message': f"Disconnected to BMS server at {ip}:{port}."})
    else:
        return jsonify({'status': FAILURE, 'message': f"Failed to disconnect from {ip}:{port}."})


@bms_bp.route('/receive_data', methods=['POST'])
def receive_data():
    """
    启动或管理接收 BMS 数据的任务，并返回操作状态信息
    """
    data = request.get_json()
    action = data.get('action')  # 'start' or 'stop'
    device_id = data.get('device_id') # 设备号
    ip = data.get('ip')  # 服务器IP
    port = data.get('server_port')  # 服务器端口
    device_port = data.get('device_port') # 设备端口
    object_instance = data.get('object_instance')
    interval = data.get('interval')

    read_properties = {
        "device_id": device_id,
        "device_ip": ip,
        "server_port": port,
        "device_port": device_port,
        "object_type": "analogInput",
        "object_instance": object_instance,
        "property_name": "presentValue",
    }

    if action == 'start':
        try:
            # 启动接收数据线程任务
            future = start_receive_data_thread(read_properties, interval)
            if future:  # 如果任务成功提交
                task_key = generate_object_key_with_hash(read_properties)
                receive_task_futures[task_key] = future

                return jsonify({
                    'status': SUCCESS,
                    'message': f"Task started successfully for device at {ip}:{port}, object_instance: {object_instance}."
                })
            else:  # 如果任务启动失败
                return jsonify({
                    'status': FAILURE,
                    'message': f"Failed to start task for device at {ip}:{port}, object_instance: {object_instance}."
                })
        except Exception as e:
            logger.error(f"Error in receive_data: {e}")
            return jsonify({'status': FAILURE, 'message': f"Error in receive_data: {str(e)}"})
    elif action == 'stop':
        try:
            # 生成任务唯一键
            task_key = generate_object_key_with_hash(read_properties)
            future = receive_task_futures.get(task_key)

            # 检查任务是否存在
            if not future:
                return jsonify({
                    'status': FAILURE,
                    'message': f"No running task found for device at {ip}:{port}, object_instance: {object_instance}."
                })

            # 停止任务
            if stop_receive_data_thread(future):
                receive_task_futures.pop(task_key, None)
                return jsonify({
                    'status': SUCCESS,
                    'message': f"Task stopped successfully for device at {ip}:{port}, object_instance: {object_instance}."
                })
            else:
                return jsonify({
                    'status': FAILURE,
                    'message': f"Failed to stop task for device at {ip}:{port}, object_instance: {object_instance}."
                })

        except Exception as e:
            logger.error(f"Error stopping task: {e}")
            return jsonify({
                'status': FAILURE,
                'message': f"Error stopping task for device at {ip}:{port}, object_instance: {object_instance}: {str(e)}"
            })

    else:
        return jsonify({'status': FAILURE, 'message': "Invalid action. Only 'start' or 'stop' is allowed."})

@bms_bp.route('/device_objects', methods=['GET'])
def get_device_objects():
    """
    获取指定 device_id 下的所有 object_type 和 object_instance
    """
    try:
        # 获取前端传递的 device_id 参数
        data = request.get_json()
        device_id = data.get('device_id')
        if device_id is None:
            return jsonify({"error": "Device ID is required"}), 400

        # 调用服务方法获取对象信息
        objects = get_device_objects_service(device_id)

        # 结果为空时返回 404
        if not objects:
            return jsonify({"message": f"No objects found for device_id {device_id}"}), 404

        # 返回查询结果
        return jsonify({"device_id": device_id, "objects": objects}), 200

    except Exception as e:
        logger.error(f"Error handling /device_objects request: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500


@bms_bp.route('/get_object_data', methods=['POST'])
def get_object_data():
    """
    前端点击某个 object 后，后端推送最新数据
    """
    try:
        # 获取前端发送的参数
        data = request.get_json()
        device_id = data.get('device_id')
        object_type = data.get('object_type')
        object_instance = data.get('object_instance')

        if not (device_id and object_type and object_instance):
            return jsonify({"error": "Missing required parameters"}), 400

        # 调用服务层获取最新数据
        latest_data = get_device_latest_data(device_id, object_type, object_instance, timestamp)

        if not latest_data:
            return jsonify({"error": "No data found"}), 404

        # 使用 WebSocket 推送数据到前端
        socketio.emit(
            'update_object_data',
            {
                "device_id": device_id,
                "object_type": object_type,
                "object_instance": object_instance,
                "latest_data": latest_data,
            }
        )

        return jsonify({"message": "Data successfully pushed to front-end"}), 200

    except Exception as e:
        logger.error(f"Error in object_click route: {e}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

