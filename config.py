class Config:
    # SERVER_NAME = '127.0.0.1:5000'
    DEBUG = True
    SECRET_KEY = '114514'

    # 默认数据库路径（不要使用）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.db'

    # 绑定数据库路径
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///users.db',
        'bms': 'sqlite:///bms.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 日志配置
    LOG_LEVELS = {
        # 日志配置格式
        # '模块名': {'控制台输出日志级别', '文件输出日志级别'}
        # 未配置的模块使用默认级别default
        'default': ('INFO', 'DEBUG'),
        'app': ('DEBUG', 'DEBUG'),
        'db_manager': ('DEBUG', 'DEBUG'),
        'sv_homepage': ('DEBUG', 'DEBUG'),
        'sv_login': ('DEBUG', 'DEBUG'),
        'sv_machine_learning': ('DEBUG', 'DEBUG'),
        'sv_visualization': ('DEBUG', 'DEBUG'),
        'sv_sensor': ('DEBUG', 'DEBUG'),
    }

    # 线程池配置
    THREAD_POOL_MAX_WORKERS = 5
