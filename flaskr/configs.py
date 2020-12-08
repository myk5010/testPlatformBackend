import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
  SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
  BASE_DIR = basedir
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True
  # LOG config
  LOG_PATH = os.path.join(basedir, 'logs')
  LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
  LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')


class DevelopmentConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@127.0.0.1:3306/lab_backend"


class TestingConfig(BaseConfig):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@127.0.0.1:3306/lab_backend"


class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mike:123123@192.168.24.239:3306/lab_backend"


config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}

