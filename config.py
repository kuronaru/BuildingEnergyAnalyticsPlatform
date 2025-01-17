class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # 使用 SQLite 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
