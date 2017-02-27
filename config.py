import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    pass