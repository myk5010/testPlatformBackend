import os
import click
from flask import Flask
# 配置
from flaskr.configs import config
# 蓝图
# from flaskr.blueprints import file_manage, jenkins, permission, upload, markdown, pcr_info, fluorescence, test_case, public
from flaskr.blueprints import public
# 扩展
from flaskr.extensions import db, migrate
# 数据库模型
# from flaskr.models.markdown import Markdown_content
# from flaskr.models.image import Up_image
# from flaskr.models.pcr_info import Pcr_info
# from flaskr.models.fluorescence import Fluorescence
# from flaskr.models.test_case import Test_case
# from flaskr.models.test_step import Test_step
# 日志
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('FLASK_ENV', 'production')
  app = Flask(__name__)
  app.config.from_object(config[config_name])


  @app.route('/')
  def hello_world():
    return 'Hello, World!'
  
  # 注册
  register_extensions(app)
  # register_shell_context(app)
  register_blueprints(app)
  register_commands(app)
  register_logger(app)

  return app


# 蓝图
def register_blueprints(app):
  # app.register_blueprint(file_manage.file_manage_bp)
  # app.register_blueprint(jenkins.jenkins_bp)
  # app.register_blueprint(permission.permission_bp)
  # app.register_blueprint(upload.upload_bp)
  # app.register_blueprint(markdown.markdown_bp)
  # app.register_blueprint(pcr_info.pcrInfo_bp)
  # app.register_blueprint(fluorescence.fluorescence_bp)
  # app.register_blueprint(test_case.testCase_bp)
  app.register_blueprint(public.public_bp)


# 初始化扩展
def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)


# 数据库模型
def register_shell_context(app):
  @app.shell_context_processor
  def make_shell_context():
    return dict(
      db               = db, 
      Markdown_content = Markdown_content,
      Up_image         = Up_image,
      Pcr_info         = Pcr_info,
      Fluorescence     = Fluorescence,
      Test_case        = Test_case,
      Test_step        = Test_step,
    )


# 指令:  flask initdb --drop
def register_commands(app):
  @app.cli.command()
  @click.option('--drop', is_flag=True, help='Create after drop.')
  # 初始化数据库
  def initdb(drop):
    """Initialize the database."""
    if drop:
      click.confirm('This operation will delete the database, do you want to continue?', abort=True)
      db.drop_all()
      click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


# 日志
def register_logger(app):
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(process)d %(thread)d '
    '%(pathname)s %(lineno)s %(message)s')
  # FileHandler Info
  file_handler_info = RotatingFileHandler(filename=app.config.get('LOG_PATH_INFO'), maxBytes=10*1024*1024, backupCount=10)
  file_handler_info.setFormatter(formatter)
  file_handler_info.setLevel(logging.INFO)
  info_filter = InfoFilter()
  file_handler_info.addFilter(info_filter)
  app.logger.addHandler(file_handler_info)
  # FileHandler Error
  file_handler_error = RotatingFileHandler(filename=app.config.get('LOG_PATH_ERROR'), maxBytes=10*1024*1024, backupCount=10)
  file_handler_error.setFormatter(formatter)
  file_handler_error.setLevel(logging.ERROR)
  app.logger.addHandler(file_handler_error)


# 过滤日志
class InfoFilter(logging.Filter):

  def filter(self, record):
    """only use INFO
    筛选, 只需要INFO级别的log
    :param record
    :return:
    """
    if logging.INFO <= record.levelno < logging.ERROR:
      # 已经是INFO级别了
      # 然后利用父类, 返回1
      return super().filter(record)
    else:
      return 0

