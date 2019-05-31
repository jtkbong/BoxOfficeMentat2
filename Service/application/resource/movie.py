from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort
from application.common import query
from application.common.query import AggregateType
from application.common import condition
from application.common import sqlhelper
from datetime import datetime


class Movie(Resource):

    def get(self, id):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        movie_query = query.Query()
        movie_query.set_table("Movies")
        movie_query.add_where_clause(condition.Condition('Id', '=', id))
        command = movie_query.to_sql_query()
        cursor.execute(command)

        movie = cursor.fetchone()

        if movie is None:
            abort(404, "Movie {0} doesn't exist.".format(id))

        box_office_query = query.Query()
        box_office_query.set_table("DomesticBoxOffice")
        box_office_query.add_where_clause(condition.Condition('MovieId', '=', id))
        cursor.execute(box_office_query.to_sql_query())
        weeks = []
        for record in cursor.fetchall():
            week_number = int(record[0].replace(id, ''))
            start_date = datetime.strftime(record[2], '%Y-%m-%d')
            end_date = datetime.strftime(record[3], '%Y-%m-%d')
            gross = int(record[4])
            theater_count = int(record[5])
            weeks.append([week_number, start_date, end_date, gross, theater_count])

        studio_name_query = query.Query()
        studio_name_query.set_table("Studios")
        studio_name_query.add_where_clause(condition.Condition('Id', '=', movie[2]))
        studio_name_query.set_return_columns(['Name'])
        cursor.execute(studio_name_query.to_sql_query())
        studio_name = cursor.fetchone()[0]

        return movie_to_json(movie, weeks, studio_name)


class Genres(Resource):

    def get(self):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studios_query = query.Query()
        studios_query.set_table("Movies")
        studios_query.set_unique_results(True)
        studios_query.set_return_columns(["Genre"])
        print(studios_query.to_sql_query())
        cursor.execute(studios_query.to_sql_query())
        return {'genres': [i[0] for i in cursor.fetchall()]}


class MpaaRatings(Resource):

    def get(self):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studios_query = query.Query()
        studios_query.set_table("Movies")
        studios_query.set_unique_results(True)
        studios_query.set_return_columns(["MpaaRating"])
        print(studios_query.to_sql_query())
        cursor.execute(studios_query.to_sql_query())
        return {'ratings': [i[0] for i in cursor.fetchall()]}


class Movies(Resource):

    def get(self):

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        movies_query = query.Query()
        movies_query.set_table("Movies")

        title = request.args.get('title')
        if title is not None:
            movies_query.add_where_clause(condition.Condition('Name', 'LIKE', "%" + title + "%"))

        studio = request.args.get('studio')
        if studio is not None:
            movies_query.add_where_clause(condition.Condition('Studio', '=', studio))

        genre = request.args.get('genre')
        if genre is not None:
            movies_query.add_where_clause(condition.Condition('Genre', 'LIKE', "%" + genre + "%"))

        rating = request.args.get('rating')
        if rating is not None:
            movies_query.add_where_clause(condition.Condition('MpaaRating', '=', rating))

        release_year = request.args.get('releaseYear')
        if release_year is not None:
            release_year = int(release_year)
            movies_query.add_where_clause(
                condition.Condition('YEAR(ReleasedDate)', '=', release_year))

        release_month = request.args.get('releaseMonth')
        if release_month is not None:
            release_month = int(release_month)
            movies_query.add_where_clause(
                condition.Condition('MONTH(ReleasedDate)', '=', release_month))

        release_day = request.args.get('releaseDay')
        if release_day is not None:
            release_day = int(release_day)
            movies_query.add_where_clause(
                condition.Condition('DAY(ReleasedDate)', '=', release_day))

        person = request.args.get('person')
        if person is not None:
            subquery = query.Query()
            subquery.set_table("Credits")
            subquery.set_return_columns(["MovieId"])
            subquery.add_where_clause(condition.Condition("PersonId", "=", person))
            movies_query.add_subquery("Id", subquery)

        mode = request.args.get('mode')
        if mode is not None and mode != 'results':
            movies_query.set_mode(mode)
            if mode == 'count':
                movies_query.add_aggregate_column(AggregateType.COUNT, 'Id', True)
        else:
            max_results = request.args.get('maxResults')
            if max_results is not None:
                movies_query.set_max_results(max_results)

            offset = request.args.get('offset')
            if offset is not None:
                movies_query.set_results_offset(offset)

        include_limit = False if mode == 'count' else True
        command = movies_query.to_sql_query(include_limit)
        cursor.execute(command)

        if mode == 'count':
            count = cursor.fetchone()
            return {'count': count[0]}
        else:
            movies = cursor.fetchall()
            return {'movies': [movie_to_json(movie) for movie in movies]}


def movie_to_json(movie, weeks=None, studio_name=None):

    movie_json = {
        'id': movie[0],
        'name': movie[1],
        'studio': movie[2],
        'domesticGross': movie[3],
        'distributor': movie[4],
        'releasedDate': movie[5].strftime('%m/%d/%Y'),
        'genre': movie[6],
        'runTime': movie[7],
        'mpaaRating': movie[8],
        'productionBudget': movie[9]
    }

    if weeks is not None:
        weeks.sort(key=lambda w: w[0])
        weeks_json = [
            {
                'weekNumber': week[0],
                'startDate': week[1],
                'endDate': week[2],
                'gross': week[3],
                'theaterCount': week[4]
            } for week in weeks
        ]
        movie_json['weeks'] = weeks_json

    if studio_name is not None:
        movie_json['studio'] = studio_name

    return movie_json

