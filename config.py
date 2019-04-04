import os


class Config(object):
    DEBUG = True
    
    SECRET_KEY = "RfIOJIOjIjI42hUU"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), "app", "data.db")
