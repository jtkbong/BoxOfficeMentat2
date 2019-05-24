from scrapetasks.scrapetask import *
from scrapetasks.scrapetask_factory import create_tasks_from_config
from common import sqlwriter
import configparser


def clear_all_tables():
    sqlwriter.clear_table('Credits')
    sqlwriter.clear_table('DomesticBoxOffice')
    sqlwriter.clear_table('People')
    sqlwriter.clear_table('Movies')


def run_tasks(tasks):
    for task in tasks:
        print('\tExecuting ' + type(task).__name__ + ' for table ' + task.tableName + '...', end='')
        task.execute()
        print('DONE!')


def run():
    print('Starting scraping data from boxofficemojo.com...')

    tasks = create_tasks_from_config()
    config = configparser.ConfigParser()
    config.read('config/worker.ini')

    if config['execution'] is not None:
        if config['execution']['purgeExistingData'] is not None:
            if config['execution']['purgeExistingData'] == 'True':
                clear_all_tables()
        if config['execution']['executionMode'] is not None:
            execution_mode = ExecutionMode[config['execution']['executionMode']]
            filtered_tasks = filter(lambda t: t.executionMode == execution_mode, tasks)
            run_tasks(filtered_tasks)
        else:
            run_tasks(tasks)

    print('Finished scraping data from boxofficemojo.com.')


def run_as_lambda(event, context):
    print("Event received: ", event)
    print("Log stream name: ", context.log_stream_name)
    print("Log group name: ", context.log_group_name)
    run()


if __name__ == '__main__':
    run()
