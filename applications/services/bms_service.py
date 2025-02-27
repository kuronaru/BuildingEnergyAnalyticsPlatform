import asyncio
import time
from hashlib import md5
from logging import getLogger

from applications.database.db_bms_manager import BMSDataManager
from applications.models.model_bms import BMSData
from applications.extensions import db
from applications.utils.bacnet_protocol import async_connect, async_disconnect, \
    async_read
from applications.utils.thread_pool_manager import ThreadPoolManager

logger = getLogger(__name__)


def connect_to_bms(ip, port):
    async def main_task():
        try:
            # 按顺序运行异步任务
            await async_connect(ip, port)
            return True
        except Exception as e:
            logger.info(f"Error during BACnet connection: {str(e)}")
            return False

    return asyncio.run(main_task())


def disconnect_from_bms(ip, port):
    """
    断开与 BMS 服务器的连接。
    """
    try:
        asyncio.run(async_disconnect(ip, port))
        return True
    except Exception as e:
        logger.error(f"Failed to disconnect from BMS server: {e}")
        return False


def receive_data_loop(request_properties, interval, stop_event=None, app=None):
    """
    同步循环：调用异步读取 BACnet 数据，并处理结果。
    """
    while not stop_event.is_set():
        try:
            # 使用 asyncio.run 调用 async_read，并处理结果
            result = asyncio.run(async_read(request_properties, timeout=1))  # 超时时间为 1 秒
            if result:
                logger.debug(f"Received BMS data: {result}")
                # 数据库存储
                device_id = request_properties.get("device_id")
                object_type = request_properties.get("object_type")
                object_instance = request_properties.get("object_instance")
                with app.app_context():
                    BMSDataManager.save_data(device_id, object_type, object_instance, result)
                    logger.debug(f"Saved BMS data to database")
            else:
                # 超时或错误情况下，跳过该次操作
                logger.warning("No valid data received. Skipping this cycle.")
        except Exception as e:
            logger.error(f"Error in receive_data_loop: {e}")

        # 等待一段时间后进入下一个循环
        time.sleep(interval)


def start_receive_data_thread(read_properties, interval=10, stop_event=None):
    try:
        future = ThreadPoolManager.submit_task(
            receive_data_loop, read_properties, interval, stop_event=stop_event)
        logger.info(f"Started receive data thread with interval: {interval}s")
        return future
    except Exception as e:
        logger.info(f"Error receiving BMS data: {str(e)}")
        return None

def stop_receive_data_thread(future):
    """
    停止接收数据线程任务，并记录状态日志。
    """
    try:
        # 如果任务已经完成，直接返回
        if future.done():
            logger.info("Task is already completed. No need to stop.")
            return True

        # 停止任务
        ThreadPoolManager.stop_task(future)
        logger.info("Stopped receive data thread successfully.")
        return True

    except Exception as e:
        logger.error(f"Error while stopping receive data thread: {str(e)}")
        return False


def generate_object_key_with_hash(read_properties):
    ip = read_properties.get("device_ip")
    port = read_properties.get("device_port")
    object_type = read_properties.get("object_type")
    object_instance = read_properties.get("object_instance")
    property_name = read_properties.get("property_name")
    identifier = f"{ip}:{port}_{object_type}_{object_instance}_{property_name}"
    return md5(identifier.encode()).hexdigest()

def get_device_objects_service(device_id):
    """
    查询指定 device_id 下的所有 object_type 和 object_instance
    """
    try:
        # 从数据库中查询与 device_id 相关的记录
        objects = db.session.query(
            BMSData.object_type, BMSData.object_instance
        ).filter(
            BMSData.device_id == device_id
        ).all()

        # 格式化数据
        results = [
            {"object_type": obj.object_type, "object_instance": obj.object_instance}
            for obj in objects
        ]

        return results

    except Exception as e:
        logger.error(f"Error in get_device_objects_service: {str(e)}")
        raise e

def get_device_latest_data(device_id, object_type, object_instance):
    """
        获取指定 object 的最新数据
        """
    try:
        latest_data = BMSDataManager.get_latest_data(device_id, object_type, object_instance)

        if latest_data:
            return latest_data
        else:
            logger.warning(
                f"No data found for device_id={device_id}, object_type={object_type}, object_instance={object_instance}")
            return None

    except Exception as e:
        logger.error(f"Error in get_object_data_service: {str(e)}")
        raise e



