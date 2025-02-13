import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file="app.log", max_bytes=5 * 1024 * 1024, backup_count=3):
        """
        初始化日志工具
        :param log_file: 日志文件路径
        :param max_bytes: 单个日志文件的最大字节数，默认 5MB
        :param backup_count: 保留的日志文件数量
        """
        self.logger = logging.getLogger("DataCollectorLogger")
        self.logger.setLevel(logging.DEBUG)

        # 创建文件处理器，支持日志文件轮换
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        # 将处理器添加到 logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, message, level="info"):
        """
        记录日志信息
        :param message: 日志内容
        :param level: 日志级别（info, debug, warning, error, critical）
        """
        if level.lower() == "debug":
            self.logger.debug(message)
        elif level.lower() == "warning":
            self.logger.warning(message)
        elif level.lower() == "error":
            self.logger.error(message)
        elif level.lower() == "critical":
            self.logger.critical(message)
        else:
            self.logger.info(message)
