from applications.protocols.protocols.bacnet_protocol import BACnetProtocol
from applications.database.db_database_manager import DatabaseManager
from flask import Blueprint, request, jsonify
from threading import Thread, Event
import time

bms_bp = Blueprint('bms', __name__)
bms_thread_stop_event = Event()  # 控制数据接收线程
data_collector = None

class DataCollector:
    def __init__(self, device_ip, object_instance=0, interval=10, db_name="data.db"):
        self.device_ip = device_ip
        self.object_instance = object_instance
        self.interval = interval
        self.db_manager = DatabaseManager(db_name)
        self.protocol = BACnetProtocol(device_ip, object_instance)

    def start(self):
        """启动数据接收并存储"""
        self.protocol.connect()
        try:
            while not bms_thread_stop_event.is_set():
                data = self.protocol.read_data()
                print(f"Collected data: {data}")
                self.db_manager.insert_data(time.time(), data)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Data collection stopped.")
        finally:
            self.protocol.disconnect()

@bms_bp.route('/connect_bms', methods=['POST'])
def connect_bms():
    """
    功能：通过BACnet协议连接到BMS服务器并启动数据收集
    """
    data = request.get_json()
    ip = data.get('ip')
    interval = data.get('interval', 10)

    if not ip:
        return jsonify({'status': 'FAILURE', 'message': 'IP is missing.'})

    global data_collector
    data_collector = DataCollector(device_ip=ip, interval=interval)
    thread = Thread(target=data_collector.start)
    thread.start()

    return jsonify({'status': 'SUCCESS', 'message': 'Started data collection.'})

@bms_bp.route('/disconnect_bms', methods=['POST'])
def disconnect_bms():
    """
    功能：停止BMS数据收集
    """
    bms_thread_stop_event.set()
    return jsonify({'status': 'SUCCESS', 'message': 'Stopped data collection.'})

@bms_bp.route('/get_bms_data', methods=['POST'])
def get_bms_data():
    """
    功能：获取BMS数据
    """
    action = request.json.get('action')  # 'start' or 'stop'
    save_data = request.json.get('save_data', False)  # 是否保存数据
    db_name = request.json.get('db_name')  # 数据库名

    # 启动数据收集
    if action == 'start':
        if bms_thread_stop_event.is_set():
            bms_thread_stop_event.clear()
            thread = Thread(target=data_collector.start)
            thread.start()
            return jsonify({'status': 'SUCCESS', 'message': 'Started receiving BMS data.'})
        else:
            return jsonify({'status': 'FAILURE', 'message': 'Data collection is already running.'})

    # 停止数据收集
    elif action == 'stop':
        if not bms_thread_stop_event.is_set():
            bms_thread_stop_event.set()
            return jsonify({'status': 'SUCCESS', 'message': 'Stopped receiving BMS data.'})
        else:
            return jsonify({'status': 'FAILURE', 'message': 'Data collection is already stopped.'})

    else:
        return jsonify({'status': 'FAILURE', 'message': 'Invalid action specified.'})


