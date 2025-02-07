from flask import Flask

from applications.database.db_database_manager import DatabaseManager
from applications.extensions import db
from applications.services.sv_data_mgmt import data_mgmt_bp
from applications.services.sv_homepage import homepage_bp
from applications.services.sv_login import login_bp
from applications.services.sv_machine_learning import ml_bp
from applications.services.sv_sensor import sensor_bp
from applications.services.sv_visualization import viz_bp


def create_app():
    app = Flask(__name__)

    # 读取配置文件config.py
    app.config.from_object('config.Config')

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

    # 注册蓝图
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(homepage_bp, url_prefix='/homepage')
    app.register_blueprint(data_mgmt_bp, url_prefix='/data')
    app.register_blueprint(sensor_bp, url_prefix='/sensor')
    app.register_blueprint(ml_bp, url_prefix='/ml')
    app.register_blueprint(viz_bp, url_prefix='/viz')

    return app
