from abc import ABC, abstractmethod
from common.sqlwriter import *
from enum import Enum
import os


class ExecutionMode(Enum):
    weeklyUpdate = 1
    completeRewrite = 2


class ScrapeTask(ABC):
    
    def __init__(self, table_name, table_columns, write_type, execution_mode, ignore_integrity_errors, task_enabled):
        self.tableName = table_name
        self.tableColumns = table_columns
        self.writeType = write_type
        self.executionMode = execution_mode
        self.ignoreIntegrityErrors = ignore_integrity_errors
        self.enabled = task_enabled
        self.files = []
        self.scrapeSuccess = False
        self.clearDatabaseSuccess = False
        self.writeToDbSuccess = False
        self.cleanupSuccess = False
    
    def execute(self):
        if self.enabled:
            self.scrape()
            if self.scrapeSuccess:
                if self.executionMode is ExecutionMode.completeRewrite:
                    self.clear_database()
                    if self.clearDatabaseSuccess:
                        self.write_to_db()
                        if self.writeToDbSuccess:
                            self.cleanup()
                else:
                    self.write_to_db()
                    if self.writeToDbSuccess:
                        self.cleanup()
        else:
            print("Task was disabled")
    
    @abstractmethod
    def scrape(self):
        pass
    
    def clear_database(self):
        clear_database(self.tableName)
        self.clearDatabaseSuccess = True

    def write_to_db(self):
        for fileName in self.files:
            file = open(fileName, "r")
            lines = file.readlines()
            write_rows_to_db_retries(
                self.tableName, self.tableColumns, self.writeType, lines, self.ignoreIntegrityErrors)
        self.writeToDbSuccess = True
        
    def cleanup(self):
        for file in self.files:
            os.remove(file)
        self.cleanupSuccess = True
