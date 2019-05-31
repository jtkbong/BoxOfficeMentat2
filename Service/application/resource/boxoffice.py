from flask_restful import Resource
from application.common import query
from application.common.query import AggregateType
from application.common import sqlhelper


class Latest(Resource):

    def get(self):

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        latest_query = query.Query()
        latest_query.set_table('DomesticBoxOffice')
        latest_query.add_inner_join('MovieId', 'Movies', 'Id')
        latest_query.set_return_columns(['DomesticBoxOffice.Id', 'MovieId', 'Movies.Name', 'StartDate', 'EndDate', 'Gross', 'TheaterCount'])

        last_week_query = query.Query()
        last_week_query.set_table('DomesticBoxOffice')
        last_week_query.add_aggregate_column(AggregateType.MAX, 'EndDate')
        last_week_query.set_mode('max')

        latest_query.add_subquery('EndDate', last_week_query)

        command = latest_query.to_sql_query(include_limit=False)
        cursor.execute(command)

        records = cursor.fetchall()
        return {'records': [record_to_json(record) for record in records]}


def record_to_json(record):
    return {
        'id': record[0],
        'movieId': record[1],
        'movieName': record[2],
        'startDate': record[3].strftime("%m-%d-%Y"),
        'endDate': record[4].strftime("%m-%d-%Y"),
        'gross': record[5],
        'theaterCount': record[6]
    }
