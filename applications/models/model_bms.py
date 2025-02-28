from applications.extensions import db
from datetime import datetime
from pytz import timezone
from datetime import datetime, timedelta

class BMSData(db.Model):
    """存储 BACnet 读取的数据"""
    __bind_key__ = 'bms'
    __tablename__ = "bms_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, nullable=False)
    object_type = db.Column(db.String(50), nullable=False)
    object_instance = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.datetime("now", "+8 hours"))
    # timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())




class BMSModel():
    @staticmethod
    def get_bms_info():
        return 222
