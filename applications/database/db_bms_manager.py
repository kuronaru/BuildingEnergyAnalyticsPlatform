from applications.extensions import db
from applications.models.model_bms import BMSData

class BMSDataManager:
    """BMS 数据管理器，封装数据库操作"""
    @staticmethod
    def save_data(object_type: str, object_instance: int, value: float):
        """存储 BACnet 读取的数据"""
        try:
            data_entry = BMSData(object_type=object_type, object_instance=object_instance, value=value)
            db.session.add(data_entry)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error saving BMS data: {e}")
            return False
        finally:
            db.session.close()

    @staticmethod
    def get_latest_data() -> list:
        """获取最新的 BACnet 数据"""
        try:
            return BMSData.query.order_by(BMSData.timestamp.desc()).all()
        except Exception as e:
            print(f"Error retrieving BMS data: {e}")
            return []

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
