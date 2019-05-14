from scrapetasks.scrapetask import ScrapeTask
import csv
from datetime import datetime


class TestMoviesScrapeTask(ScrapeTask):
    
    def scrape(self):
        box_office = datetime.today().strftime('%m%d%H%M')

        rows = [
            ['testmovie', 'Test Movie', 'BuenaVista', box_office]
        ]

        file_name = '/tmp/WarnerBros.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(rows)
        
        self.files.append(file_name)
        self.scrapeSuccess = True
