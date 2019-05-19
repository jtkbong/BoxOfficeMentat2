from scrapetasks.scrapetask import ScrapeTask
from common.scrapeutil import *
from common.datafile import *
import csv


class CompletePeopleScrapeTask(ScrapeTask):
    
    def scrape(self):
        self.people = dict()
        self.scrapePeople('Actor')
        self.scrapePeople('Director')
        self.scrapePeople('Producer')
        self.scrapePeople('Writer')
        
        fileName = get_data_file_directory() + 'People.tsv'
        outfile = open(fileName, "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        for id, v in self.people.items():
            writer.writerows([[id, v[0], v[1]]])
        mark_data_file_complete(writer)
        self.files.append(fileName)
        self.scrapeSuccess = True

    def scrapePeople(self, type):        
        firstRowKeys = list()
        pageCount = 1
        while True:
            fullUrl = "https://www.boxofficemojo.com/people/?view=%s&p=.htm&pagenum=%d" % (type, pageCount)
            trs = scrape_table_rows(fullUrl, attributes={'border': '0', 'cellspacing': '1', 'cellpadding': '5', 'width': '98%'})
            searchType = 'view=' + type
            if len(trs) > 0:
                key = trs[1].text
                if key in firstRowKeys:
                    break
                else:
                    firstRowKeys.append(trs[1].text)
                    for row in trs:
                        for a in row.findAll('a'):
                            href = a.get(('href'))
                            if searchType in href and 'chart' in href:
                                name = a.text.replace('&nbsp;', '')
                                id = href[href.index('id=') + 3:href.index('.htm')]
                                roles = self.getPersonRoles(type, href)
                                if id not in self.people:
                                    self.people[id] = [name, roles]
                    pageCount += 1
    
    def getPersonRoles(self, type, url):
        fullUrl = 'https://www.boxofficemojo.com/people/' + url.replace('./', '')
        navTabs = scrape_list(fullUrl, {'class': 'nav_tabs'})
        roles = ''
        if navTabs is None:
            roles += type[0:1]
        else:
            for tab in navTabs.findAll('li'):
                roles += tab.text[0:1]
        return roles
