import os


class Config:
    DEBUG = False
    TESTING = False
    REST_DEFAULT_CONTENT_TYPE = 'application/json'
    SQLALCHEMY_DATABASE_URI = 'postgres://{user}:{password}@{url}:{port}/{db}'.format(
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        url=os.environ.get('POSTGRES_DB_ENDPOINT'),
        port=os.environ.get('POSTGRES_PORT', 5432),
        db=os.environ.get('POSTGRES_DB')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VIEWS_PATH = './templates'
    MAIN_VIEW = 'index.html'
    DIST_DIR = '../static/'

    APP_HOST = os.environ.get('APP_HOST', 'localhost')
    APP_PORT = os.environ.get('APP_PORT', 5000)

    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_configuration():
    env = os.environ.get('env')

    if env == 'prod':
        return ProductionConfig()

    if env == 'test':
        return TestingConfig()

    return DevelopmentConfig()
