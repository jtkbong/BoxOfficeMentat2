from scrapetasks.scrapetask import ScrapeTask
from common import scrapeutil
from common import datacache
from common import datafile
from common import parsingutil
import csv


class CompleteMovieScrapeTask(ScrapeTask):

    def __init__(self, table_name, table_columns, write_type, execution_mode, task_enabled):
        ScrapeTask.__init__(self, table_name, table_columns, write_type, execution_mode, task_enabled)
        self.movies = set()

    def scrape(self):
        studios = self.get_studios_list()
        for studio in studios:
            self.scrape_studio_movies(studio['studioName'], studio['href'])
        datacache.set_list('Movies', list(self.movies))
        self.scrapeSuccess = True
                            
    def get_studios_list(self):
        studios = datacache.get_list('Studios')
        if studios is None:
            studios = []
            tables = scrapeutil.scrape_tables("https://www.boxofficemojo.com/studio/?view2=allstudios&view=company&p=.htm",
                                   {'border': '0', 'cellspacing': '1', 'cellpadding': '3'})
            for table in tables:
                for row in table.findAll('tr'):            
                    for cell in row.findAll('a'):
                        href = cell.get('href')
                        studio_name = parsingutil.get_studio_from_url(href)
                        studios.append({'studio_name': studio_name, 'href': href})
            datacache.set_list('Studios', studios)
            studios = datacache.get_list('Studios')
        return studios    
                            
    def scrape_studio_movies(self, studio_name, url):
        i = 1
        file_name = datafile.get_data_file_directory() + studio_name + '_Movies.tsv'
        self.files.append(file_name)
        
        if not datafile.is_data_file_complete(file_name):
            outfile = open(file_name, "w", newline='')
            writer = csv.writer(outfile, delimiter='\t')
            while True:
                full_url = ("https://www.boxofficemojo.com/studio/" + url + "&page=%d") % i
                rows = scrapeutil.scrape_table_rows(full_url, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
                if len(rows) > 0:
                    for row in rows:            
                        cell = row.find('a')            
                        if hasattr(cell, 'text'):
                            movie_name = cell.text.replace('&nbsp;', '')
                            if movie_name and movie_name != 'Rank':
                                href = cell.get('href')
                                row_data = scrapeutil.scrape_movie(href, movie_name, studio_name)
                                writer.writerows([row_data])
                                self.movies.add(row_data[0])
                    i += 1
                else:
                    break
            datafile.mark_data_file_complete(writer)
        else:
            print("Skipped scraping " + studio_name)
