class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False