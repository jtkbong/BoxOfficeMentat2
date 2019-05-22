from scrapetasks.scrapetask import ExecutionMode
from scrapetasks.completeMovieScrapeTask import CompleteMovieScrapeTask
from scrapetasks.completePeopleScrapeTask import CompletePeopleScrapeTask
from scrapetasks.completeBoxOfficeScrapeTask import CompleteBoxOfficeScrapeTask
from scrapetasks.completeCreditsScrapeTask import CompleteCreditsScrapeTask
from scrapetasks.testMoviesScrapeTask import TestMoviesScrapeTask
from scrapetasks.weeklyMovieUpdateScrapeTask import WeeklyMovieUpdateScrapeTask
from scrapetasks.weeklyNewMoviesScrapeTask import WeeklyNewMoviesScrapeTask
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
        table_name = task_data['tableName']
        table_columns = task_data['tableColumns']
        write_type = WriteType[task_data['writeType']]
        execution_mode = ExecutionMode[task_data['executionMode']]
        enabled = task_data['enabled']

        if task_name == "WeeklyMovieUpdate":
            return WeeklyMovieUpdateScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "WeeklyGross":
            return WeeklyGrossScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "WeeklyNewMovies":
            return WeeklyNewMoviesScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "WeeklyCredits":
            return WeeklyCreditsScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "CompleteMovie":
            return CompleteMovieScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "CompletePeople":
            return CompletePeopleScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "CompleteCredits":
            return CompleteCreditsScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "CompleteBoxOffice":
            return CompleteBoxOfficeScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        elif task_name == "TestMovies":
            return TestMoviesScrapeTask(table_name, table_columns, write_type, execution_mode, enabled)
        else:
            return None

