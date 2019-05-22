from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.datafile import *
import csv


class WeeklyCreditsScrapeTask(ScrapeTask):

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
                    movie_id = parsingutil.get_id_from_url(href)
                    row_data = self.scrape_movie_credits(movie_id)
                    data = data + row_data
        date = ''
        headers = scrape_elements('h2', url, None)
        for header in headers:
            if header.text != 'Weekly Box Office':
                date = header.text.replace(',', '')

        file_name = get_data_file_directory() + 'WeeklyCredits_' + date + '.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(data)
        mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = False

    def scrape_movie_credits(self, movie_id):
        full_url = "https://www.boxofficemojo.com/movies/?page=main&id=%s.htm" % movie_id
        roles = []
        anchors = scrape_elements('a', full_url, {})
        for anchor in anchors:
            href = anchor.get('href')
            if '?view=Writer' in href or '?view=Actor' in href or '?view=Director' in href or '?view=Producer' in href:
                person_id = parsingutil.get_id_from_url(href)
                role = href[href.index('view=') + 5: href.index('&')]
                if person_id is not None:
                    roles.append([movie_id, person_id, role])
        return roles
