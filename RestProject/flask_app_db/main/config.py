import os

basedir=os.path.abspath(os.path.dirname(__file__))

class config():
    SECRET_KEY = os.getenv('SECRET_KEY', 'thissecretkey')
    DEBUG = False
    UPLOAD_FOLDER='Upload_Files'
    ALLOWED_EXTENSIONS={'xml'}
    #MAX_CONTENT-PATH=16 * 1024 * 1024

class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestingConfig(config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProdcutionConfig(config):
    DEBUG = False

config_by_name=dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProdcutionConfig
)

key = config.SECRET_KEY
