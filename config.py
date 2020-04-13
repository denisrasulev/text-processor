import os


class Config(object):
    APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or '53afee03b75e8fb022c88fba922bb22e'
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER = '/texts'
    ALLOWED_EXTENSIONS = {'txt'}
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # Max upload size 1MB

