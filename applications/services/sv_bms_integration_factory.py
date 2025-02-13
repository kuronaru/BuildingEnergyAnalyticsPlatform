from flask import Flask, request, jsonify
from applications.protocols.protocols.modbus_protocol import ModbusProtocol  # 根据需求引入相应协议实现
from applications.protocols.protocols.bacnet_protocol import BACnetProtocol
from server_status import SUCCESS, FAILURE

app = Flask(__name__)

# 连接和断开函数，可以通过协议工厂类来管理协议
@app.route('/bms/connect_bms', methods=['POST'])
def connect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': 'IP or port is missing.'})

    # 示例连接方式，可以根据协议类型选择不同实现
    protocol = BACnetProtocol(ip, port)  # 根据需要选择协议
    connection_status = protocol.connect()

    if connection_status:
        return jsonify({'status': SUCCESS, 'message': f'Connected to BMS at {ip}:{port}.'})
    else:
        return jsonify({'status': FAILURE, 'message': f'Failed to connect to BMS at {ip}:{port}.'})

@app.route('/bms/disconnect_bms', methods=['POST'])
def disconnect_bms():
    data = request.get_json()
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({'status': FAILURE, 'message': 'IP or port is missing.'})

    # 示例断开方式，根据协议类型进行断开
    protocol = ModbusProtocol(ip, port)  # 根据需要选择协议
    disconnection_status = protocol.disconnect()

    if disconnection_status:
        return jsonify({'status': SUCCESS, 'message': f'Disconnected from BMS at {ip}:{port}.'})
    else:
        return jsonify({'status': FAILURE, 'message': f'Failed to disconnect from BMS at {ip}:{port}.'})

if __name__ == '__main__':
    app.run(debug=True)
