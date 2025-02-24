import socket
from logging import getLogger

from flask import Blueprint, request, jsonify

from applications.services.bms_service import connect_to_bms, disconnect_from_bms, start_receive_data_thread, \
    generate_object_key_with_hash, stop_receive_data_thread
from server_status import SUCCESS, FAILURE

bms_bp = Blueprint('bms', __name__)
logger = getLogger(__name__)
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
    ip = data.get('ip')  # 服务器IP
    port = data.get('port')  # 服务器端口
    object_instance = data.get('object_instance')
    interval = data.get('interval')

    read_properties = {
        "device_ip": ip,
        "device_port": port,
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

