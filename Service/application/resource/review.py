from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort
from application.common import query
from application.common import condition
from application.common import sqlhelper
import datetime


class Review(Resource):

    def get(self, id):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        review_query = query.Query()
        review_query.set_table("Reviews")
        review_query.set_unique_results(True)
        review_query.set_return_columns(["Id", "MovieId", "DateTime", "ReviewText", "ReviewStats"])
        review_query.add_where_clause(condition.Condition('Id', '=', id))
        cursor.execute(review_query.to_sql_query())
        review = cursor.fetchone()

        if review is None:
            abort(404, "Review {0} doesn't exist.".format(id))

        return review_to_json(review)


class Reviews(Resource):

    def get(self):
        offset = request.args.get('offset')
        offset = 0 if offset is None else offset
        max_results = request.args.get('maxResults')
        max_results = 20 if max_results is None else max_results

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        reviews_query = query.Query()
        reviews_query.set_table("Reviews")
        reviews_query.set_return_columns(["Reviews.Id", "MovieId", "Movies.Name", "DateTime", "ReviewStats"])
        reviews_query.add_inner_join('MovieId', 'Movies', 'Id')
        reviews_query.set_order_by_columns(['DateTime'])
        reviews_query.set_results_order(query.ResultsOrder.DESC)
        reviews_query.set_results_offset(offset)
        reviews_query.set_max_results(max_results)

        print(reviews_query.to_sql_query())

        cursor.execute(reviews_query.to_sql_query())
        reviews = cursor.fetchall()

        return {'reviews': reviews_to_json(reviews)}

    def post(self):
        movie_id = request.form['movieId']
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        review_text = request.form['reviewText']
        review_stats = """{ "overall": 3 }"""
        params = (movie_id, date_time, review_text, review_stats)

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        sql = 'INSERT INTO boxofficementat.Reviews (MovieId, DateTime, ReviewText, ReviewStats) VALUES(%s, %s, %s, %s)'
        cursor.execute(sql, params)
        connection.commit()
        connection.close()


def review_to_json(review):
    return {
        'id': review[0],
        'movieId': review[1],
        'dateTime': review[2].strftime("%Y-%m-%d"),
        'reviewText': review[3].decode('utf-8'),
        'reviewStats': review[4]
    }


def reviews_to_json(reviews):
    reviews_json = []
    for review in reviews:
        reviews_json.append({
            'id': review[0],
            'movieId': review[1],
            'movieName': review[2],
            'dateTime': review[3].strftime("%Y-%m-%d"),
            'reviewStats': review[4]
        })
    return reviews_json
