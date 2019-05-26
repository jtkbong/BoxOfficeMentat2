from scrapetasks.scrapetask import ScrapeTask
from common import scrapeutil
from common import datacache
from common import datafile
from common import logging
import csv


class CompleteMovieScrapeTask(ScrapeTask):

    movies = set()

    def scrape(self):
        studios = scrapeutil.get_studios_list()
        for studio in studios:
            self.scrape_studio_movies(studio['studio_id'], studio['href'])
        datacache.set_list('Movies', list(self.movies))
        self.scrapeSuccess = True

    def scrape_studio_movies(self, studio_id, url):
        if studio_id is None or studio_id == '':
            return

        i = 1
        file_name = datafile.create_data_file_path(studio_id + '_Movies.tsv')
        self.files.append(file_name)
        
        if not datafile.is_data_file_complete(file_name):
            outfile = open(file_name, "w", newline='')
            writer = csv.writer(outfile, delimiter='\t')
            logging.log_info("\t\tScraping movies for studio %s...\n", studio_id)
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
                                row_data = scrapeutil.scrape_movie(href, movie_name, studio_id)
                                if row_data is not None:
                                    writer.writerows([row_data])
                                    self.movies.add(row_data[0])
                    i += 1
                else:
                    break
            datafile.mark_data_file_complete(writer)
        else:
            logging.log_info("\t\tSkipped scraping studio %s\n", studio_id)
