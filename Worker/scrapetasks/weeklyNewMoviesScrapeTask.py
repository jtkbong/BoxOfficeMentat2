from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.datafile import *
import csv


class WeeklyNewMoviesScrapeTask(ScrapeTask):

    def scrape(self):
        url = 'https://www.boxofficemojo.com/weekly/chart/'
        data = []
        rows = scrape_table_rows(url, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
        if len(rows) > 0:
            selected_rows = rows[1:-1]
            for row in selected_rows:
                cells = row.findAll('td')
                week_number = cells[-1].text
                if week_number == '1':
                    movie_name_cell = row.find('a')
                    href = movie_name_cell.get('href')
                    movie_name = movie_name_cell.text
                    studio_href = row.findAll('a')[1].get('href')
                    studio_name = parsingutil.get_studio_from_url(studio_href)
                    row_data = scrape_movie(href, movie_name, studio_name)
                    data.append(row_data)
        date = ''
        headers = scrape_elements('h2', url, None)
        for header in headers:
            if header.text != 'Weekly Box Office':
                date = header.text.replace(',', '')

        file_name = get_data_file_directory() + 'WeeklyNewMovies_' + date + '.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(data)
        mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True
