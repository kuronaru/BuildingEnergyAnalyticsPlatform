from flask import Blueprint, request, jsonify
from applications.extensions import db
from datetime import datetime
import re
from applications.models.model_temperature import Temperature
from server_status import SUCCESS, FAILURE, DATA_INVALID
import logging
import pytz

SGT = pytz.timezone('Asia/Singapore')

class TemperatureService:
    """
    温度数据存储处理
    """
    @staticmethod
    def is_valid_ip(ip):
        """验证IP地址是否合法"""
        pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
        return re.match(pattern, ip) is not None

    @staticmethod
    def is_valid_port(port):
        """ 验证端口号是否合法（0-65535）"""
        return isinstance(port, int) and port >= 0 and port <= 65535

    @staticmethod
    def is_valid_temperature(temp):
        """ 验证温度值是否合法（-200 到 200 摄氏度之间） """
        return isinstance(temp, (int, float)) and -200 <= temp <= 200

    @staticmethod
    def store_temperature(ip, port, temperature):
        """ 存储温度数据 """
        # 数据校验
        if not TemperatureService.is_valid_ip(ip):
            return {'status': DATA_INVALID, "message": "Invalid IP address"}
        if not TemperatureService.is_valid_port(port):
            return {'status': DATA_INVALID, "message": "Invalid port"}
        if not TemperatureService.is_valid_temperature(temperature):
            return {'status': DATA_INVALID, "message": "Invalid temperature"}
        try:
            # 将数据存入数据库中
            local_time = datetime.now(SGT)  # 直接存新加坡时间
            new_entry = Temperature(ip = ip, port = port, temperature = temperature, timestamp = local_time)
            db.session.add(new_entry)
            db.session.commit()
            return {'status': SUCCESS, 'data':  {
                    'id': new_entry.id,
                    'ip': new_entry.ip,
                    'port': new_entry.port,
                    'temperature': new_entry.temperature,
                    'timestamp': new_entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # 转换时间格式
                }
                            }
        except Exception as e:
            db.session.rollback()
            logging.error(f"Database error: {e}")  # 记录日志
            print(f"Database error: {e}")  # 打印错误信息
            return {'status': FAILURE, "message": "Data storage failure, please try again later."}
        # finally:
        #     db.session.close()

