from common import configuration
import os


def log_info(message):
    print(message)
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    if not is_aws:
        log_file_name = configuration.get_config()['logging']['logFileName']
        logs = open(log_file_name, 'a')
        logs.write(message)


def log_error(error_message):
    print(error_message)
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    if not is_aws:
        errors_file_name = configuration.get_config()['logging']['errorFileName']
        errors = open(errors_file_name, 'a')
        errors.write(error_message)
