from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.datafile import *
from common.parsingutil import *
import csv


class CompletePeopleScrapeTask(ScrapeTask):
    
    def scrape(self):
        self.people = dict()
        self.scrape_people('Actor')
        self.scrape_people('Director')
        self.scrape_people('Producer')
        self.scrape_people('Writer')
        
        file_name = get_data_file_directory() + 'People.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        for person_id, person_data in self.people.items():
            writer.writerows(person_data)
        mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True

    def scrape_people(self, credit_type):
        first_row_keys = list()
        page_count = 1
        while True:
            full_url = "https://www.boxofficemojo.com/people/?view=%s&p=.htm&pagenum=%d" % (credit_type, page_count)
            trs = scrape_table_rows(full_url,
                                    attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5', 'width': '98%'})
            view_type = 'view=' + credit_type
            if len(trs) > 0:
                key = trs[1].text
                if key in first_row_keys:
                    break
                else:
                    first_row_keys.append(trs[1].text)
                    for row in trs:
                        for a in row.findAll('a'):
                            href = a.get('href')
                            if view_type in href and 'chart' in href:
                                person_id = parsingutil.get_id_from_url(href)
                                if person_id not in self.people:
                                    person_data = scrape_person(credit_type, person_id)
                                    self.people[person_id] = person_data
                    page_count += 1
