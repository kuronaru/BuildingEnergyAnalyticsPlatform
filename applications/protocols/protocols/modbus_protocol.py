from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from enum import Enum

from applications.protocols.protocol_interface.base_protocol import BaseProtocol


# define the connection method
class ConnectionType(Enum):
    TCP = "tcp"
    SERIAL = "serial"


class ModbusProtocol(BaseProtocol):
    def __init__(self, host=None, port=None, device=None, connection_type=ConnectionType.TCP):
        self.host = host
        self.port = port
        self.device = device
        self.connection_type = connection_type
        self.client = None

    def connect(self):
        if self.connection_type == ConnectionType.TCP:
            # 使用 Modbus TCP 连接
            self.client = ModbusTcpClient(self.host, port=self.port)
        elif self.connection_type == ConnectionType.SERIAL:
            # 使用 Modbus RTU (串行连接)
            self.client = ModbusSerialClient(method="rtu", port=self.device, baudrate=9600)

        if not self.client.connect():
            raise ModbusIOException("Unable to connect to Modbus device.")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Modbus connection closed.")

    def read_data(self, unit_id, address, count):

        if self.connection_type == ConnectionType.TCP:
            result = self.client.read_holding_registers(address, count, unit=unit_id)
        elif self.connection_type == ConnectionType.SERIAL:
            result = self.client.read_holding_registers(address, count, unit=unit_id)
        else:
            raise ValueError("Invalid connection type.")

        if result.isError():
            raise ModbusIOException(f"Error reading data from address {address}.")

        return result.registers

    def write_data(self, unit_id, address, value):

        if self.connection_type == ConnectionType.TCP:
            result = self.client.write_register(address, value, unit=unit_id)
        elif self.connection_type == ConnectionType.SERIAL:
            result = self.client.write_register(address, value, unit=unit_id)
        else:
            raise ValueError("Invalid connection type.")

        if result.isError():
            raise ModbusIOException(f"Error writing data to address {address}.")

        return True
