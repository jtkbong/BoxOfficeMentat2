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
            selectedRows = rows[1:-1]
            for row in selectedRows:
                cells = row.findAll('td')
                movieNameCell = row.find('a')
                href = movieNameCell.get('href')
                movieId = get_id_from_url(href)
                weeklyGrossCell = cells[4]
                weeklyGross = dollar_text_to_int(weeklyGrossCell.text)
                theaterCountCell = cells[6]
                theaterCount = text_to_int(theaterCountCell.text)
                data.append([movieId, weeklyGross, theaterCount])

        date = ''
        headers = scrape_elements('h2', url, None)
        for header in headers:
            if header.text != 'Weekly Box Office':
                date = header.text.replace(',', '')
        
        fileName = 'WeeklyGross_' + date + '.tsv'
        outfile = open(fileName, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(data)
        mark_data_file_complete(writer)
        self.files.append(fileName)
        self.scrapeSuccess = True
