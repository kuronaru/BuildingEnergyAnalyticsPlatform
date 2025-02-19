from applications.extensions import db
class BMSData(db.Model):
    """存储 BACnet 读取的数据"""
    __tablename__ = "bms_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    object_type = db.Column(db.String(50), nullable=False)
    object_instance = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())