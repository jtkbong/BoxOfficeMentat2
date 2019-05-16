from common.sqlwriter import WriteType
from scrapetasks.scrapetask import ExecutionMode
from scrapetasks.completeMovieScrapeTask import CompleteMovieScrapeTask
from scrapetasks.completePeopleScrapeTask import CompletePeopleScrapeTask
from scrapetasks.completeBoxOfficeScrapeTask import CompleteBoxOfficeScrapeTask
from scrapetasks.testMoviesScrapeTask import TestMoviesScrapeTask
from scrapetasks.weeklyMovieUpdateScrapeTask import WeeklyMovieUpdateScrapeTask
from scrapetasks.weeklyNewMoviesScrapeTask import WeeklyNewMoviesScrapeTask
from scrapetasks.weeklyGrossScrapeTask import WeeklyGrossScrapeTask
import configparser


def run():
    read_config()
    print('Starting scraping data from boxofficemojo.com...')

    weekly_tasks = list()

    weekly_tasks.append(WeeklyMovieUpdateScrapeTask("Movies", [
        'DomesticGross'
    ], WriteType.update, ExecutionMode.weeklyUpdate, True))

    weekly_tasks.append(WeeklyNewMoviesScrapeTask("Movies", [
        'Id',
        'Name',
        'Studio',
        'DomesticGross',
        'Distributor',
        'ReleasedDate',
        'Genre',
        'RunTime',
        'MpaaRating',
        'ProductionBudget'
    ], WriteType.insert, ExecutionMode.weeklyUpdate, True))

    weekly_tasks.append(WeeklyGrossScrapeTask("WeeklyGross", [
        'Id',
        'MovieId',
        'WeeklyGross',
        'TheaterCount'
    ], WriteType.insert, ExecutionMode.weeklyUpdate, False))

    compete_rewrite_tasks = list()
    compete_rewrite_tasks.append(CompleteMovieScrapeTask("Movies", [
        'Id',
        'Name',
        'Studio',
        'DomesticGross',
        'Distributor',
        'ReleasedDate',
        'Genre',
        'RunTime',
        'MpaaRating',
        'ProductionBudget'
    ], WriteType.insert, ExecutionMode.completeRewrite, False))

    compete_rewrite_tasks.append(CompletePeopleScrapeTask("People", [
        'Id',
        'Name',
        'Actor',
        'Director',
        'Producer',
        'ScreenWriter'
    ], WriteType.insert, ExecutionMode.completeRewrite, False))

    compete_rewrite_tasks.append(CompleteBoxOfficeScrapeTask("boxOffice", [
        'MovieId',
        'StartDate',
        'EndDate',
        'Gross',
        'TheaterCount'
    ], WriteType.insert, ExecutionMode.completeRewrite, False))

    compete_rewrite_tasks.append(TestMoviesScrapeTask('TestMovies', [
        'Id',
        'Name',
        'Studio',
        'DomesticGross'
    ], WriteType.insert, ExecutionMode.completeRewrite, True))

    config = configparser.ConfigParser()
    config.read('config/worker.ini')
    tasks = weekly_tasks if config['execution']['executionMode'] == "weeklyUpdate" else compete_rewrite_tasks

    for task in tasks:
        print('\tExecuting ' + type(task).__name__ + ' for table ' + task.tableName + '...', end='')
        task.execute()
        print('DONE!')

    print('Finished scraping data from boxofficemojo.com.')


def read_config():
    config = configparser.ConfigParser()
    config.read('config/worker.ini')
    print(config.sections())


def run_as_lambda(event, context):
    print("Event received: ", event)
    print("Log stream name: ", context.log_stream_name)
    print("Log group name: ", context.log_group_name)
    run()


if __name__ == '__main__':
    run()
