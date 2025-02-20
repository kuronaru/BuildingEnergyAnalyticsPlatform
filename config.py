class Config:
    # SERVER_NAME = '127.0.0.1:5000'
    DEBUG = True
    SECRET_KEY = '114514'

    # 数据库配置
    # 配置多个数据库连接的连接串写法示例
    # HOSTNAME: 指数据库的IP地址
    # USERNAME：指数据库登录的用户名
    # PASSWORD：指数据库登录密码
    # PORT：指数据库开放的端口
    # DATABASE：指需要连接的数据库名称
    #
    # MSSQL:    f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=cp936"
    # MySQL:    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
    # Oracle:   f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    # Postgres: f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
    # SQLite:   "sqlite:/// database.db"
    # Oracle的第二种连接方式
    # dsnStr = cx_Oracle.makedsn({HOSTNAME}, 1521, service_name='orcl')
    # connect_str = "oracle://%s:%s@%s" % ('{USERNAME}', ' {PASSWORD}', dsnStr)
    #
    # 在 SQLALCHEMY_BINDS 中设置：'{数据库连接别名}': '{连接串}'
    # 最后在models的数据模型class中，在 __tablename__ 前设置
    #     __bind_key__ = '{数据库连接别名}'
    # 即可，表示该数据模型不使用默认的数据库连接，改用 SQLALCHEMY_BINDS 中设置的其他数据库连接.
    # SQLALCHEMY_BINDS = {
    #     'testMySQL': 'mysql+pymysql://test:123456@192.168.1.1:3306/test?charset=utf8',
    #     'testMsSQL': 'mssql+pymssql://test:123456@192.168.1.1:1433/test?charset=cp936',
    #     'testOracle': 'oracle+cx_oracle://test:123456@192.168.1.1:1521/test',
    #     'testSQLite': 'sqlite:///database.db'
    # }

    # 默认数据库路径
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    # 绑定数据库路径
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///users.db'
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
