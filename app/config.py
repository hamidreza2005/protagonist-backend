class Config:
    SECRET_KEY = "super-secret"         
    JWT_SECRET_KEY = "jwt-super-secret"  
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

