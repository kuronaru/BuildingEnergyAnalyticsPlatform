from datetime import datetime

from applications.extensions import db


class Temperature(db.Model):
    """
    温度数据表
    """
    __bind_key__ = 'app'
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="温度记录 ID")
    ip = db.Column(db.String(15), nullable=False, comment="设备 IP 地址")
    port = db.Column(db.Integer, nullable=False, comment="设备端口号")
    temperature = db.Column(db.Float, nullable=False, comment="温度值（℃）")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment="记录时间")
