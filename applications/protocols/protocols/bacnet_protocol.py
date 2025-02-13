import BAC0
from abc import ABC, abstractmethod
from applications.protocols.protocol_interface.base_protocol import BaseProtocol


class BACnetProtocol(BaseProtocol):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = None

    def connect(self):
        """ 连接到 BACnet 设备 """
        try:
            # 初始化 BACnet 客户端并连接
            self.client = BAC0.lite(self.ip)
            print(f"Connected to BACnet device at {self.ip}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to BACnet device: {str(e)}")
            return False

    def disconnect(self):
        """ 断开与 BACnet 设备的连接 """
        try:
            if self.client:
                BAC0.stop(self.client)  # 停止 BACnet 客户端
                self.client = None
                print(f"Disconnected from BACnet device at {self.ip}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to disconnect from BACnet device: {str(e)}")
            return False

    def read_data(self, object_identifier="analogInput:1", property_name="presentValue"):
        """ 读取 BACnet 设备的实时数据 """
        if not self.client:
            print("BACnet client is not initialized.")
            return None

        try:
            # 读取数据
            value = self.client.read(f"{object_identifier} {property_name}")
            print(f"Read value from BACnet: {value}")
            return value
        except Exception as e:
            print(f"Error reading data from BACnet: {str(e)}")
            return None

    # def write_data(self, object_identifier, property_name, value):
    #     """ 向 BACnet 设备写入数据 """
    #     if not self.client:
    #         print("BACnet client is not initialized.")
    #         return False
    #
    #     try:
    #         # 写入数据
    #         self.client.write(f"{object_identifier} {property_name}", value)
    #         print(f"Written value to BACnet: {value}")
    #         return True
    #     except Exception as e:
    #         print(f"Error writing data to BACnet: {str(e)}")
    #         return False
