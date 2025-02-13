from flask import Blueprint, request, jsonify
from threading import Event
import BAC0

from applications.models.model_bms import BMSData
from applications.protocols.types.bacnet_protocol import run_bacnet_configurations
from server_status import SUCCESS, FAILURE

bms_bp = Blueprint('bms', __name__)

bms_thread_stop_event = Event()  # 控制BMS数据接收线程
bacnet_client = None  # 管理BACnet客户端

# 启动连接
async def async_connect(ip, port):
    global bacnet_client
    try:
        bacnet_client = BAC0.lite(ip, port)
        print(f"Connected to BACnet device at {ip}:{port}")
        return True
    except Exception as e:
        print(f"Failed to connect to BACnet device: {str(e)}")
        return False

def _connect(ip, port):
    try:
        return asyncio.run(async_connect(ip, port))
    except Exception as e:
        print(f"Error during BACnet connection: {str(e)}")
        return False

# 断开连接
def _disconnect(ip, port):
    global bacnet_client
    try:
        if bacnet_client:
            bacnet_client = None
            print(f"Disconnected from BACnet device at {ip}:{port}")
        return True
    except Exception as e:
        print(f"Failed to disconnect BACnet device: {str(e)}")
        return False

@bms_bp.route('/connect_bms', methods=['POST'])
def connect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': 'IP or port is missing.'})

    connection_status = _connect(ip, port)

    if connection_status:
        return jsonify({'status': SUCCESS, 'message': f'Connected to BMS server at {ip}:{port}.'})
    else:
        return jsonify({'status': FAILURE, 'message': f'Failed to connect to {ip}:{port}.'})

@bms_bp.route('/disconnect_bms', methods=['POST'])
def disconnect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': 'IP or port is missing.'})

    disconnection_status = _disconnect(ip, port)

    if disconnection_status:
        return jsonify({'status': SUCCESS, 'message': f'Disconnected to BMS server at {ip}:{port}.'})
    else:
        return jsonify({'status': FAILURE, 'message': f'Failed to disconnect from {ip}:{port}.'})

@bms_bp.route('/get_bms_data', methods=['POST'])
def get_bms_data():
    data = request.get_json()
    action = data.get('action')  # 'start' or 'stop'
    save_data = data.get('save_data', False)  # 是否存储数据
    db_name = data.get('db_name')  # 存储的数据库名
    ip = data.get('ip')  # 服务器IP
    port = data.get('port')  # 服务器端口

    if action == 'start':
        # if bms_thread_stop_event.is_set():
        bms_thread_stop_event.clear()
        asyncio.run(receive_bms_data(save_data, db_name, ip, port))
        # thread = Thread(target=receive_bms_data, args=(save_data, db_name, ip, port))
        # thread.start()
        return jsonify({'status': SUCCESS, 'message': 'Started receiving BMS data.'})
    # else:
    #     return jsonify({'status': FAILURE, 'message': 'Unable to receive the data.'})

    elif action == 'stop':
        if not bms_thread_stop_event.is_set():
            bms_thread_stop_event.set()
            return jsonify({'status': SUCCESS, 'message': 'Stopped receiving BMS data.'})
        else:
            return jsonify({'status': FAILURE, 'message': 'Receiving is already stopped.'})

    else:
        return jsonify({'status': FAILURE, 'message': 'Invalid action specified.'})

import asyncio


async def receive_bms_data(save_data=False, db_name=None, ip=None, port=None):
    bms_model = BMSData()
    bacnet_config = {
        "local_ip": ip,  # 使用传入的 ip 和 port
        "device_ip": ip,
        "local_port": 47809,
        "device_port": port,
        "read_objects": [("analogInput", 0)],
        "read_attempts": 10,
        "read_interval": 1,  # reading intervals/s
        "write_range": (15, 25),
        "write_object": ("analogValue", 1),  # (object_type, object_instance, value)
        "write_interval": 3,
        "dynamic_write": False,
        "fixed_set_value": 18,
        "property_name": "presentValue",
        "enable_read": True,
        "enable_write": False,
    }

    while not bms_thread_stop_event.is_set():
        try:
            # 获取数据
            data = await run_bacnet_configurations(bacnet_config)  # 使用你的配置进行数据读取
            for entry in data:
                if save_data and db_name:
                    bms_model.save_bms_data(entry, db_name)  # 存储数据到数据库
            await asyncio.sleep(1)  # 异步睡眠，避免阻塞
        except Exception as e:
            print(f"Error receiving BMS data: {str(e)}")
            await asyncio.sleep(1)  # 异常情况下继续等待
