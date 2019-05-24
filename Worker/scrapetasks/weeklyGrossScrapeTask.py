from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.parsingutil import *
from common.datafile import *
import csv


class WeeklyGrossScrapeTask(ScrapeTask):
    
    def scrape(self):
        url = 'https://www.boxofficemojo.com/weekly/chart/'
        data = []
        rows = scrape_table_rows(url, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
        if len(rows) > 0:

            h2s = scrape_elements('h2', url, {})
            week_text = list(filter(lambda t: t.text != 'Weekly Box Office', h2s))[0].text
            dates = parsingutil.week_text_to_start_end_dates(week_text)

            selected_rows = rows[1:-1]
            for row in selected_rows:
                cells = row.findAll('td')
                movie_name_cell = row.find('a')
                href = movie_name_cell.get('href')
                movie_id = get_id_from_url(href)
                weekly_gross_cell = cells[4]
                weekly_gross = dollar_text_to_int(weekly_gross_cell.text)
                theater_count_cell = cells[6]
                theater_count = text_to_int(theater_count_cell.text)
                week_number_cell = cells[-1]
                week_number = text_to_int(week_number_cell.text)

                record_id = movie_id + str(week_number)
                data.append([record_id, movie_id, dates[0], dates[1], weekly_gross, theater_count])

        date = ''
        headers = scrape_elements('h2', url, None)
        for header in headers:
            if header.text != 'Weekly Box Office':
                date = header.text.replace(',', '')
        
        file_name = 'WeeklyGross_' + date + '.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(data)
        mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True
