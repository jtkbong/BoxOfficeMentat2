from scrapetasks.scrapetask import ScrapeTask


class CreditsScrapeTask(ScrapeTask):

    def scrape(self):
        studios = self.getStudiosList()
        for studio in studios:
            self.scrapeStudioMovies(studio['studioName'], studio['href'])
        self.scrapeSuccess = True
