from scrapetasks.scrapetask import ScrapeTask
from common import scrapeutil
from common import datafile
import csv


class CompleteStudiosScrapeTask(ScrapeTask):

    def scrape(self):
        studios = scrapeutil.get_studios_list()
        file_name = datafile.create_data_file_path('Studios.tsv')
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        for studio in studios:
            writer.writerow([studio['studio_id'], studio['studio_name']])
        datafile.mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True
