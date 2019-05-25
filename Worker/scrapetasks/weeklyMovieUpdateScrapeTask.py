from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.parsingutil import *
from common.datafile import *
import csv


class WeeklyMovieUpdateScrapeTask(ScrapeTask):

    def scrape(self):
        url = 'https://www.boxofficemojo.com/weekly/chart/'
        data = []
        rows = scrape_table_rows(url, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
        if len(rows) > 0:
            selected_rows = rows[1:-1]
            for row in selected_rows:
                cells = row.findAll('td')
                week_number = cells[-1].text
                if week_number != '1' and week_number != '-':
                    movie_name_cell = row.find('a')
                    href = movie_name_cell.get('href')
                    movie_id = get_id_from_url(href)
                    total_gross_cell = cells[9]
                    total_gross = dollar_text_to_int(total_gross_cell.text)
                    data.append([total_gross, movie_id])

        date = ''
        headers = scrape_elements('h2', url, None)
        for header in headers:
            if header.text != 'Weekly Box Office':
                date = header.text.replace(',', '')

        file_name = create_data_file_path('WeeklyMovieUpdate_' + date + '.tsv')
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(data)
        mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True
