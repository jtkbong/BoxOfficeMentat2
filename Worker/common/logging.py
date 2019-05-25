from common import configuration
import os


def log_info(message, params=None):
    print_message = message if params is None else message % params
    print(print_message)
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    if not is_aws:
        log_file_name = configuration.get_config()['logging']['logFileName']
        logs = open(log_file_name, 'a')
        logs.write(print_message)


def log_error(error_message, params=None):
    print_error = error_message if params is None else error_message % params
    print(print_error)
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    if not is_aws:
        errors_file_name = configuration.get_config()['logging']['errorFileName']
        errors = open(errors_file_name, 'a')
        errors.write(print_error)
