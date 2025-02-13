from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from applications.database.db_user_manager import UserManager
from applications.extensions import db
from applications.services.sv_data_mgmt import data_mgmt_bp
from applications.services.sv_homepage import homepage_bp
from applications.services.sv_login import login_bp
from applications.services.sv_machine_learning import ml_bp
from applications.services.sv_sensor import sensor_bp
from applications.services.sv_visualization import viz_bp
from applications.utils.database_manager import DatabaseManager
from applications.utils.thread_pool_manager import ThreadPoolManager
from applications.services.sv_bms_integration import bms_bp
from logging_config import setup_logger


def create_app():
    app = Flask(__name__)

    # 读取配置文件config.py
    app.config.from_object('config.Config')

    # 初始化全局日志
    app_logger = setup_logger('app', app.config)
    app_logger.info("Initializing Flask application...")

    # 初始化Bcrypt
    bcrypt = Bcrypt()
    bcrypt.init_app(app)
    app.bcrypt = bcrypt
    app_logger.debug("Bcrypt initialized")

    # 初始化LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'  # 未登录时重定向的端点
    app.login_manager = login_manager
    app_logger.debug("LoginManager initialized")

    @login_manager.user_loader
    def load_user(user_id):
        """通过用户 ID 加载用户对象，这里返回 UserManager 实例"""
        app_logger.debug(f"Loading user with ID: {user_id}")
        return UserManager.find_user_by_id(user_id)

    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        # Ensure the database tables are created
        for bind_name in app.config['SQLALCHEMY_BINDS']:
            db.create_all(bind_key=bind_name)

    # 实例化DatabaseManager
    db_manager = DatabaseManager()

    # 添加数据库
    db_manager.add_database('users', 'users.db')

    # 添加BMS数据库
    db_manager.add_database('bms', 'bms.db')

    @app.teardown_appcontext
    def close_db(error):
        """在 Flask 应用线程结束时关闭连接"""
        db_manager.close_all_connections()

    # 存储 db_manager 到应用全局上下文
    app.db_manager = db_manager
    app_logger.debug("DatabaseManager initialized")

    # 初始化线程池
    # 通过配置文件设置最大工作线程数，默认 5 个线程
    max_workers = app.config.get("THREAD_POOL_MAX_WORKERS", 5)
    ThreadPoolManager.initialize(max_workers)
    app.thread_pool = ThreadPoolManager  # 将线程池管理器绑定到 app 上
    app_logger.debug(f"ThreadPoolManager initialized with max workers: {max_workers}")

    @app.teardown_appcontext
    def shutdown_thread_pool(error):
        """在 Flask 应用线程结束时关闭线程池"""
        ThreadPoolManager.shutdown()

    # 注册蓝图并初始化模块日志
    blueprints = [login_bp, homepage_bp, data_mgmt_bp, sensor_bp, ml_bp, viz_bp, bms_bp]
    url_prefix = ['/', '/homepage', '/data', '/sensor', '/ml', '/viz', '/bms']
    for bp in blueprints:
        module_name = bp.import_name
        setup_logger(module_name, app.config)
        app_logger.info(f"Logger initialized for blueprint: {module_name}")
        app.register_blueprint(bp, url_prefix=url_prefix.pop(0))

    app_logger.info("Flask app created and initialized")
    return app
