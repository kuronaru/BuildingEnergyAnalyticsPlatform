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
from logging_config import setup_logger

bcrypt = Bcrypt()
login_manager = LoginManager()
app_logger = None  # 创建全局应用日志


def create_app():
    app = Flask(__name__)

    # 读取配置文件config.py
    app.config.from_object('config.Config')

    # 初始化全局日志
    global app_logger
    app_logger = setup_logger('app', app.config)

    # 初始化
    app_logger.info("Initializing Flask application...")
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'  # 未登录时重定向的端点

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

    @app.teardown_appcontext
    def close_db(error):
        """在每个线程结束时关闭连接"""
        db_manager.close_all_connections()

    # 存储 db_manager 到应用全局上下文
    app.db_manager = db_manager

    # 注册蓝图并初始化模块日志
    blueprints = [login_bp, homepage_bp, data_mgmt_bp, sensor_bp, ml_bp, viz_bp]
    url_prefix = ['/', '/homepage', '/data', '/sensor', '/ml', '/viz']
    for bp in blueprints:
        module_name = bp.import_name
        setup_logger(module_name, app.config)
        app_logger.info(f"Logger initialized for blueprint: {module_name}")
        app.register_blueprint(bp, url_prefix=url_prefix.pop(0))

    app_logger.info("Flask app created and initialized")
    return app
