from scrapetasks.movieScrapeTask import MovieScrapeTask
from scrapetasks.peopleScrapeTask import PeopleScrapeTask
from scrapetasks.boxOfficeScrapeTask import BoxOfficeScrapeTask
from scrapetasks.testMoviesScrapeTask import TestMoviesScrapeTask
from scrapetasks.weeklyGrossScrapeTask import WeeklyGrossScrapeTask
from enum import Enum
import configparser


class Mode(Enum):
    weeklyUpdate = 1
    brandNew = 2
    rebuildTables = 3


def run():
    print('Starting scraping data from boxofficemojo.com...')

    weekly_tasks = list()
    weekly_tasks.append(WeeklyGrossScrapeTask("WeeklyGross", [
        'Id',
        'MovieId',
        'WeeklyGross',
        'TheaterCount'
    ], False))

    rebuild_tables_tasks = list()
    rebuild_tables_tasks.append(MovieScrapeTask("Movies", [
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
    ], False))
    rebuild_tables_tasks.append(PeopleScrapeTask("People", [
        'Id',
        'Name',
        'Actor',
        'Director',
        'Producer',
        'ScreenWriter'
    ], False))

    rebuild_tables_tasks.append(BoxOfficeScrapeTask("boxOffice", [
        'MovieId',
        'StartDate',
        'EndDate',
        'Gross',
        'TheaterCount'
    ], False))
    rebuild_tables_tasks.append(TestMoviesScrapeTask('TestMovies', [
        'Id',
        'Name',
        'Studio',
        'DomesticGross'
    ], True))

    for task in rebuild_tables_tasks:
        print('\tExecuting scrape task for table ' + task.tableName + '...', end='')
        task.execute()
        print('DONE!')
    print('Finished scraping data from boxofficemojo.com.')


def read_config():
    config = configparser.ConfigParser()
    config.read('config/worker.ini')
    print(config.sections())


if __name__ == '__main__':
    read_config()
    run()
