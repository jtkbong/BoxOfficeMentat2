from scrapetasks.scrapetask import ScrapeTask
from common import scrapeutil
from common import parsingutil
from common import datacache
from common import datafile
from common import sqlwriter
import calendar
import datetime
import csv
from retrying import retry


class CompleteBoxOfficeScrapeTask(ScrapeTask):

    MAX_RETRIES = 5

    def scrape(self):
        movies = self.get_movie_list()
        for studio, movies in movies.items():
            file_name = datafile.create_data_file_path('BoxOfficeGrossComplete_' + studio + '.tsv')
            if not datafile.is_data_file_complete(file_name):
                studio_data = []
                for movie in movies:
                    studio_data.extend(self.scrape_movie(movie))
                outfile = open(file_name, "w", newline='')
                writer = csv.writer(outfile, delimiter='\t')
                writer.writerows(studio_data)
                datafile.mark_data_file_complete(writer)
            else:
                print("Skipping studio %s." % studio)
            self.files.append(file_name)
        self.scrapeSuccess = True

    def get_movie_list(self):
        movies = datacache.get_list('Movies')
        if movies is None:
            connection = sqlwriter.get_sql_conn()
            cursor = connection.cursor()
            command = 'SELECT Studio, Id FROM boxofficementat.Movies'
            cursor.execute(command)
            rows = cursor.fetchall()
            movies = {}
            for row in rows:
                studio = row[0]
                movie_id = row[1]
                if studio not in movies:
                    movies[studio] = list()
                movies[studio].append(movie_id)

        return movies

    @retry(wait_fixed=5000, stop_max_attempt_number=MAX_RETRIES)
    def scrape_movie(self, movie_id):
        url = 'https://www.boxofficemojo.com/movies/?page=weekly&id=%s.htm' % movie_id
        tables = scrapeutil.scrape_tables(url, attributes={'class': 'chart-wide'})
        movie_rows = []

        for table in tables:
            for row in table.findAll('tr')[1:]:
                cells = row.findAll('td')
                week_text = cells[0].text
                link = row.find('a').attrs['href']
                start_year = int(link[link.index('yr=') + 3:link.index('yr=') + 7])

                start_date_text = week_text[0:week_text.index('–')]
                start_month_text = start_date_text[0:3]
                start_month = list(calendar.month_abbr).index(start_month_text)
                start_day = int(start_date_text[3:])
                start_date = datetime.date(start_year, start_month, start_day)

                end_date_text = week_text[week_text.index('–') + 1:]
                end_month = start_month
                if len(end_date_text) > 3:
                    end_month_text = end_date_text[0:3]
                    end_month = list(calendar.month_abbr).index(end_month_text)
                end_year = start_year
                if end_month == 1 and start_month == 12:
                    end_year += 1
                end_day = int(end_date_text if len(end_date_text) < 3 else end_date_text[end_date_text.index(' ') + 1:])
                end_date = datetime.date(end_year, end_month, end_day)

                gross_text = cells[2].text
                theater_count_text = cells[4].text

                gross = parsingutil.dollar_text_to_int(gross_text)
                theater_count = parsingutil.text_to_int(theater_count_text)

                week_number_cell = cells[-1]
                week_number = parsingutil.text_to_int(week_number_cell.text)

                record_id = movie_id + str(week_number)
                movie_rows.append([record_id, movie_id, start_date, end_date, gross, theater_count])

        return movie_rows
