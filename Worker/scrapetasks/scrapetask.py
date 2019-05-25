from abc import ABC, abstractmethod
from common.sqlwriter import *
from enum import Enum
import os


class ExecutionMode(Enum):
    weeklyUpdate = 1
    completeRewrite = 2


class ScrapeTask(ABC):
    
    def __init__(self,
                 order, table_name, table_columns, write_type, execution_mode, ignore_integrity_errors, task_enabled):
        self.order = order
        self.tableName = table_name
        self.tableColumns = table_columns
        self.writeType = write_type
        self.executionMode = execution_mode
        self.ignoreIntegrityErrors = ignore_integrity_errors
        self.enabled = task_enabled
        self.files = []
        self.scrapeSuccess = False
        self.clearTableSuccess = False
        self.writeToDbSuccess = False
        self.cleanupSuccess = False
    
    def execute(self):
        if self.enabled:
            print("\tScraping web pages now...\n")
            self.scrape()
            if self.scrapeSuccess:
                print("\tScrape successful.\n")
                if self.executionMode is ExecutionMode.completeRewrite:
                    print("\tClearing table...\n")
                    self.clear_table()
                    if self.clearTableSuccess:
                        print("\tCleared table. Started writing to table...\n")
                        self.write_to_db()
                        if self.writeToDbSuccess:
                            print("Finished writing to table. Cleaning up data files...\n")
                            self.cleanup()
                else:
                    print("\tStarted writing to table...\n")
                    self.write_to_db()
                    if self.writeToDbSuccess:
                        print("Finished writing to table. Cleaning up data files...\n")
                        self.cleanup()
        else:
            print("\tTask was disabled. Skipping!\n")
    
    @abstractmethod
    def scrape(self):
        pass
    
    def clear_table(self):
        clear_table(self.tableName)
        self.clearTableSuccess = True

    def write_to_db(self):
        for fileName in self.files:
            file = open(fileName, "r")
            lines = file.readlines()
            write_rows_to_db_retries(
                self.tableName, self.tableColumns, self.writeType, lines, self.ignoreIntegrityErrors)
        self.writeToDbSuccess = True
        
    def cleanup(self):
        for file in self.files:
            try:
                os.remove(file)
            except FileNotFoundError:
                print("\tUnable to find file " + file + " to delete. Please manually verify after cleanup.")
                continue
        self.cleanupSuccess = True
