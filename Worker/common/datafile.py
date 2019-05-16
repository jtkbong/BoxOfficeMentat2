from pathlib import Path
import configparser


doneIndicator = "###DONE###"


def get_data_file_directory():
    config = configparser.ConfigParser()
    config.read('config/worker.ini')
    data_info = config['data']
    directory = data_info['dir']
    return directory


def mark_data_file_complete(writer):
    writer.writerow([doneIndicator])


def is_data_file_complete(file_path):
    if not Path(file_path).is_file():
        return False
    content = Path(file_path).read_text()
    return content.endswith(doneIndicator + "\n")
