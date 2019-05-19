from scrapetasks.scrapetask import ScrapeTask
from common import datafile
from common import scrapeutil
from common import parsingutil
import csv


class CompleteCreditsScrapeTask(ScrapeTask):

    def scrape(self):

        file_name = datafile.get_data_file_directory() + 'Credits.tsv'
        outfile = open(file_name, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')

        roles = ['Actor', 'Director', 'Producer', 'Writer']

        for role in roles:
            rows = self.scrape_people(role)
            writer.writerows(rows)

        datafile.mark_data_file_complete(writer)
        self.files.append(file_name)
        self.scrapeSuccess = True

    def scrape_people(self, relationship_type):
        first_row_keys = list()
        rows = []
        page_count = 1
        while True:
            full_url = "https://www.boxofficemojo.com/people/?view=%s&p=.htm&pagenum=%d" % (relationship_type, page_count)
            trs = scrapeutil.scrape_table_rows(full_url,
                                               attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5', 'width': '98%'})
            search_type = 'view=' + relationship_type
            if len(trs) > 0:
                key = trs[1].text
                if key in first_row_keys:
                    break
                else:
                    first_row_keys.append(trs[1].text)
                    for row in trs:
                        for a in row.findAll('a'):
                            href = a.get('href')
                            if search_type in href and 'chart' in href:
                                person_id = href[href.index('id=') + 3:href.index('.htm')]
                                rows += self.scrape_person_titles(relationship_type, person_id)
                    page_count += 1
        return rows

    def scrape_person_titles(self, relationship_type, person_id):
        rows = []
        full_url = "https://www.boxofficemojo.com/people/chart/?view=%s&id=%s.htm" % (relationship_type, person_id)
        trs = scrapeutil.scrape_table_rows(full_url,
                                           attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5'})
        for row in trs[1:]:
            anchors = row.findAll('a')
            movie_href = list(filter(lambda anchor: 'id=' in anchor.get('href'), anchors))
            href = movie_href[0].get('href')
            movie_id = parsingutil.get_id_from_url(href)
            rows.append([movie_id, person_id, relationship_type])
        return rows
