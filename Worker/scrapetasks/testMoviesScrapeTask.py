from scrapetasks.scrapetask import ScrapeTask
import csv
from datetime import datetime


class TestMoviesScrapeTask(ScrapeTask):
    
    def scrape(self):
        box_office = datetime.today().strftime('%m%d%H%M')

        rows = [
            ['testmovie', 'Test Movie', 'WarnerBros.', box_office]
        ]
                
        outfile = open('WarnerBros.tsv', "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(rows)
        
        self.files.append('WarnerBros.tsv')
        self.scrapeSuccess = True
