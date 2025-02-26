import importlib
import logging
import os
from functools import wraps
from logging.handlers import RotatingFileHandler


def setup_logger(module_name, config=None, log_dir='logs'):
    """
    配置并返回模块级别的 logger
    :param module_name: 当前模块名称 (__name__)
    :param config: Flask 应用的全局配置对象
    :param log_dir: 存储日志文件的目录
    :return: 配置好的 logger 对象
    """
    # 创建日志目录（如果不存在）
    os.makedirs(log_dir, exist_ok=True)

    # 从配置中读取日志级别
    if config and config['LOG_LEVELS']:
        # 获取当前模块日志级别
        module_log_levels = config['LOG_LEVELS'].get(module_name.split('.')[-1],
                                                     config['LOG_LEVELS'].get('default', ('INFO', 'INFO')))
        console_level, file_level = map(
            lambda level: getattr(logging, level.upper(), logging.INFO),  # 转换为 logging 中的级别值
            module_log_levels
        )
    else:
        # 使用默认日志级别
        console_level = file_level = logging.DEBUG

    # 创建 logger 对象（模块名称）
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # 设置 logger 总级别为 DEBUG

    # 文件日志处理器
    log_file_path = os.path.join(log_dir, f'{module_name.split(".")[-1]}.log')
    file_handler = RotatingFileHandler(log_file_path, maxBytes=2 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 添加处理器到 logger
    if not logger.hasHandlers():  # 避免重复添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def with_logger(func):
    """
    为函数动态注入该模块的日志器
    """
    logger = logging.getLogger(func.__module__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(logger, *args, **kwargs)

    return wrapper


def initialize_all_loggers(directory: str, app_config):
    """
    遍历目录下的所有 Python 模块，初始化日志
    :param directory: 项目目录路径
    :param app_config: Flask 配置对象
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file)
                module_name = module_path.replace(directory, "").replace("/", ".").replace("\\", ".").strip(".py")
                try:
                    module = importlib.import_module(module_name)
                    setup_logger(module_name, app_config)
                except Exception as e:
                    print(f"Failed to initialize logger for {module_name}: {e}")

