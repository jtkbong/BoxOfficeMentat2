from pathlib import Path
from common import configuration
import os


doneIndicator = "###DONE###"


def get_data_file_directory():
    data_info = configuration.get_config()['data']
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    directory = data_info['awsDir'] if is_aws else data_info['localDir']
    return directory


def create_data_file_path(file_name):
    return get_data_file_directory() + file_name


def mark_data_file_complete(writer):
    writer.writerow([doneIndicator])


def is_data_file_complete(file_path):
    if not Path(file_path).is_file():
        return False
    content = Path(file_path).read_text()
    return content.endswith(doneIndicator + "\n")
