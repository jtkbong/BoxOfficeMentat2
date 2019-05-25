import configparser


config = configparser.ConfigParser()
config.read('config/worker.ini')


def get_config():
    return config
