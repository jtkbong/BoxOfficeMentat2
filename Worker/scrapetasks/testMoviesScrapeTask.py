from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.parsingutil import *
from common.datafile import *
import csv
from datetime import datetime


class TestMoviesScrapeTask(ScrapeTask):
    
    def scrape(self):

        url = 'https://www.boxofficemojo.com/weekly/chart/'
        rows = scrape_table_rows(url, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
        movie_name_cell = rows[1].find('a')
        movie_name = movie_name_cell.text.replace('&nbsp;', '')
        href = movie_name_cell.get('href')
        movie_id = get_id_from_url(href)
        box_office = datetime.today().strftime('%m%d%H%M')

        rows = [
            [movie_id, movie_name, 'BuenaVista', box_office]
        ]

        file_name = get_data_file_directory() + 'WarnerBros.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(rows)
        
        self.files.append(file_name)
        self.scrapeSuccess = True
