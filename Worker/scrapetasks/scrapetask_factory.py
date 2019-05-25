from scrapetasks.scrapetask import ExecutionMode
from scrapetasks.completeMovieScrapeTask import CompleteMovieScrapeTask
from scrapetasks.completePeopleScrapeTask import CompletePeopleScrapeTask
from scrapetasks.completeBoxOfficeScrapeTask import CompleteBoxOfficeScrapeTask
from scrapetasks.completeCreditsScrapeTask import CompleteCreditsScrapeTask
from scrapetasks.testMoviesScrapeTask import TestMoviesScrapeTask
from scrapetasks.weeklyMovieUpdateScrapeTask import WeeklyMovieUpdateScrapeTask
from scrapetasks.weeklyNewMoviesScrapeTask import WeeklyNewMoviesScrapeTask
from scrapetasks.weeklyPeopleScrapeTask import WeeklyPeopleScrapeTask
from scrapetasks.weeklyCreditsScrapeTask import WeeklyCreditsScrapeTask
from scrapetasks.weeklyGrossScrapeTask import WeeklyGrossScrapeTask
from common.sqlwriter import WriteType
import json


def create_tasks_from_config():
    with open('config/tasks.json') as json_file:
        data = json.load(json_file)
        tasks = []
        for task_name in data:
            task = create_task_from_config(task_name)
            tasks.append(task)
        return tasks


def create_task_from_config(task_name):
    with open('config/tasks.json') as json_file:
        data = json.load(json_file)
        task_data = data[task_name]
        order = task_data['order']
        table_name = task_data['tableName']
        table_columns = task_data['tableColumns']
        write_type = WriteType[task_data['writeType']]
        ignore_integrity_errors = False if 'ignoreIntegrityErrors' not in task_data \
            else task_data['ignoreIntegrityErrors']
        execution_mode = ExecutionMode[task_data['executionMode']]
        enabled = task_data['enabled']

        params = {
            "order": order,
            "table_name": table_name,
            "table_columns": table_columns,
            "write_type": write_type,
            "execution_mode": execution_mode,
            "ignore_integrity_errors": ignore_integrity_errors,
            "task_enabled": enabled
        }

        if task_name == "WeeklyMovieUpdate":
            return WeeklyMovieUpdateScrapeTask(**params)
        elif task_name == "WeeklyGross":
            return WeeklyGrossScrapeTask(**params)
        elif task_name == "WeeklyNewMovies":
            return WeeklyNewMoviesScrapeTask(**params)
        elif task_name == "WeeklyPeople":
            return WeeklyPeopleScrapeTask(**params)
        elif task_name == "WeeklyCredits":
            return WeeklyCreditsScrapeTask(**params)
        elif task_name == "CompleteMovie":
            return CompleteMovieScrapeTask(**params)
        elif task_name == "CompletePeople":
            return CompletePeopleScrapeTask(**params)
        elif task_name == "CompleteCredits":
            return CompleteCreditsScrapeTask(**params)
        elif task_name == "CompleteBoxOffice":
            return CompleteBoxOfficeScrapeTask(**params)
        elif task_name == "TestMovies":
            return TestMoviesScrapeTask(**params)
        else:
            return None

