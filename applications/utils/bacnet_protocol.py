import asyncio
from logging import getLogger
from typing import Optional

import BAC0

logger = getLogger(__name__)

# 全局BACnet客户端
bacnet_client: Optional[BAC0.scripts.Lite.Lite] = None


def read_property_request(request_properties):
    ip = request_properties.get('device_ip')
    port = request_properties.get('device_port')
    device_port = request_properties.get('device_port')
    object_type = request_properties.get('object_type')
    object_instance = request_properties.get('object_instance')
    property_name = request_properties.get('property_name')
    request = f"{ip}:{port} {object_type} {object_instance} {property_name}"
    return request


def write_property_request(request_properties):
    ip = request_properties.get('device_ip')
    port = request_properties.get('device_port')
    object_type = request_properties.get('object_type')
    object_instance = request_properties.get('object_instance')
    property_name = request_properties.get('property_name')
    value = request_properties.get('value')
    index = request_properties.get('index')
    priority = request_properties.get('priority')

    if index:
        value = f"{value} {index}"
    if priority:
        value = f"{value} {priority}"

    request = f"{ip}:{port} {object_type} {object_instance} {property_name} {value}"
    return request


async def async_read(request_properties, timeout=3):
    """
    异步读取 BACnet 属性（带超时控制）。
    :param request_properties: 包含读取属性的参数字典
    :param timeout: 超时时间（秒）
    :return: 读取数据（成功）或 None（超时）
    """
    request = read_property_request(request_properties)
    try:
        # 使用 asyncio.wait_for 为读取操作添加超时控制
        return bacnet_client.read(request, timeout=timeout)
    except asyncio.TimeoutError:
        # 超时处理逻辑，可以选择记录日志并返回一个特定值
        logger.warning(f"Read timeout for request: {request}")
        return None
    except Exception as e:
        # 捕获其他异常并记录
        logger.error(f"Error reading property {request}: {e}")
        return None


async def async_write(request_properties, timeout=3):
    """
    异步写入 BACnet 属性（带超时控制）。
    :param request_properties: 包含写入属性的参数字典
    :param timeout: 超时时间（秒）
    :return: 写入结果（成功 True 或失败 None）
    """
    request = write_property_request(request_properties)
    try:
        # 使用 asyncio.wait_for 为写操作添加超时控制
        return await asyncio.wait_for(bacnet_client.write(request), timeout=timeout)
    except asyncio.TimeoutError:
        # 超时处理逻辑，记录超时报告并返回 None
        logger.warning(f"Write timeout for request: {request}")
        return None
    except Exception as e:
        # 捕获其他异常并记录
        logger.error(f"Error writing property {request}: {e}")
        return None


async def async_connect(ip, port):
    """
    异步连接到 BACnet 设备。
    """
    global bacnet_client
    try:
        bacnet_client = BAC0.lite(ip, port)
        logger.info(f"BACnet client created at {ip}:{port}")
        return True
    except Exception as e:
        logger.error(f"Failed to create BACnet client: {e}")
        return False


async def async_disconnect(ip, port):
    """
    异步断开 BACnet 设备的连接。
    """
    global bacnet_client
    try:
        if bacnet_client:
            bacnet_client.disconnect()
            bacnet_client = None
            logger.info(f"Disconnected from BACnet device at {ip}:{port}")
        return True
    except Exception as e:
        logger.error(f"Failed to disconnect BACnet device: {e}")
        return False


async def get_object_list():
    """
    获取远程BACnet服务器上的所有对象列表。
    # object_list example:
    # Objects for device 2883673: [('device', 2883673), ('analogInput', 0), ('analogInput', 1),
    #                              ('analogInput', 2), ('analogValue', 0), ('analogValue', 1),
    #                              ('analogValue', 2), ('analogValue', 3), ('characterstringValue', 1),
    #                              ('binaryValue', 0), ('binaryValue', 1), ('multiStateValue', 0),
    #                              ('multiStateValue', 1)]

    :return: 对象列表
    """
    device_id = None
    device_address = None

    try:
        # Who-Is 请求，发现设备
        devices = bacnet_client.whois()
        if not devices:
            logger.info("No BACnet devices found on the network.")
            return []

        logger.info(f"Found BACnet devices: {devices}")

        all_objects = []

        # 查询每个设备的对象列表
        for device in devices:
            try:
                # 获取设备 ID 和地址
                device_id = device['device_id']
                device_address = device['address']

                logger.info(f"Fetching objects for device ID: {device_id}, Address: {device_address}")

                # Query the object list
                object_list = bacnet_client.read(f"{device_address} device {device_id} objectList")
                logger.info(f"Objects for device {device_id}: {object_list}")

                if object_list:
                    all_objects.extend(object_list)
            except Exception as e:
                logger.info(f"Error fetching objects for device {device_id} at {device_address}: {str(e)}")

        return all_objects

    except Exception as e:
        logger.info(f"Failed to fetch remote objects: {str(e)}")
        return []

