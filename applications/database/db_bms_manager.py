from sqlalchemy.exc import SQLAlchemyError

from applications.extensions import db
from applications.models.model_bms import BMSData

class BMSDataManager:
    """BMS 数据管理器，封装数据库操作"""
    @staticmethod
    def save_data(device_id: str, object_type: str, object_instance: int, value: float):
        """存储 BACnet 读取的数据"""
        try:
            data_entry = BMSData(device_id=device_id, object_type=object_type, object_instance=object_instance, value=value)
            db.session.add(data_entry)
            db.session.commit()

            return True
        except Exception as e:
            print(f"Error saving BMS data: {e}")
            return False
        finally:
            db.session.close()
    @staticmethod
    def get_latest_data(device_id: int, object_type: str, object_instance: int) -> dict:
        """
        获取指定 device_id, object_type 和 object_instance 最新一条数据
        """
        try:
            # 查询最新的一条数据，按 timestamp 降序排序
            latest_data = BMSData.query.filter(
                BMSData.device_id == device_id,
                BMSData.object_type == object_type,
                BMSData.object_instance == object_instance
            ).order_by(BMSData.timestamp.desc()).first()

            # 如果存在数据，格式化返回
            if latest_data:
                return {
                    "device_id": latest_data.device_id,
                    "object_type": latest_data.object_type,
                    "object_instance": latest_data.object_instance,
                    "timestamp": latest_data.timestamp.isoformat()  # 日期格式化为字符串
                }
            else:
                return None  # 如果查询为空，返回 None

        except SQLAlchemyError as e:
            print(f"Error retrieving latest BMS data: {e}")
            return None


    @staticmethod
    def clear_old_data(days: int) -> bool:
        """清除 N 天前的数据"""
        try:
            db.session.query(BMSData).filter(BMSData.timestamp < db.func.date_sub(db.func.current_timestamp(), db.text(f"INTERVAL {days} DAY"))).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error clearing old BMS data: {e}")
            return False
        finally:
            db.session.close()
