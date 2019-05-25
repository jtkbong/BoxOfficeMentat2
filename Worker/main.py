from scrapetasks.scrapetask import *
from scrapetasks.scrapetask_factory import create_tasks_from_config
from common import sqlwriter
from common import configuration
from common import logging


def clear_all_tables():
    sqlwriter.clear_table('Credits')
    sqlwriter.clear_table('DomesticBoxOffice')
    sqlwriter.clear_table('People')
    sqlwriter.clear_table('Movies')


def run_tasks(tasks):
    tasks.sort(key=lambda t: t.order)
    for task in tasks:
        logging.log_info('Executing ' + type(task).__name__ + ' for table ' + task.tableName + '...\n')
        task.execute()
        logging.log_info('DONE!\n')


def run():
    logging.log_info('Starting scraping data from boxofficemojo.com...\n\n')

    tasks = create_tasks_from_config()
    config = configuration.get_config()

    if config['execution'] is not None:
        if config['execution']['purgeExistingData'] is not None:
            if config['execution']['purgeExistingData'] == 'True':
                clear_all_tables()
        if config['execution']['executionMode'] is not None:
            execution_mode = ExecutionMode[config['execution']['executionMode']]
            filtered_tasks = list(filter(lambda t: t.executionMode == execution_mode, tasks))
            run_tasks(filtered_tasks)
        else:
            run_tasks(tasks)

    logging.log_info('Finished scraping data from boxofficemojo.com.')


def run_as_lambda(event, context):
    logging.log_info("Event received: %s", event)
    logging.log_info("Log stream name: %s", context.log_stream_name)
    logging.log_info("Log group name: %s", context.log_group_name)
    run()


if __name__ == '__main__':
    run()
