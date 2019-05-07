from scrapetasks.scrapetask import ScrapeTask
import csv


class TestMoviesScrapeTask(ScrapeTask):
    
    def scrape(self):
        columnNames = ["Id", "Name", "Studio", "DomesticGross"]

        rows = [
            ['darkknight', 'The Dark Knight', 'WarnerBros.', '533345358'],
            ['batman3', 'The Dark Knight Rises', 'WarnerBros.', '448139099'],
            ['wonderwoman', 'Wonder Woman', 'WarnerBros.', '412563408'],
            ['harrypotter72', 'Harry Potter and the Deathly Hallows Part 2', 'WarnerBros.', '381011219'],
            ['americansniper', 'American Sniper', 'WarnerBros.', '350126372'],
            ['batmanreturns', 'Batman Returns', 'WarnerBros.', '162831698']
        ]
                
        outfile = open('WarnerBros.tsv', "w", newline='')
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows(rows)
        
        self.files.append('WarnerBros.tsv')
        self.scrapeSuccess = True
