from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort
from application.common import query
from application.common import condition
from application.common import sqlhelper


class Studio(Resource):

    def get(self, id):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studio_query = query.Query()
        studio_query.set_table("Studios")
        studio_query.set_unique_results(True)
        studio_query.set_return_columns(["Id", "Name"])
        studio_query.add_where_clause(condition.Condition('Id', '=', id))
        cursor.execute(studio_query.to_sql_query())
        studio = cursor.fetchone()

        if studio is None:
            abort(404, "Studio {0} doesn't exist.".format(id))

        return studio_to_json(studio)


class Studios(Resource):

    def get(self):
        offset = request.args.get('offset')
        offset = 0 if offset is None else offset
        max_results = request.args.get('maxResults')
        max_results = 2000 if max_results is None else max_results

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studios_query = query.Query()
        studios_query.set_table("Movies")
        studios_query.set_return_columns(["Studios.Id", "Studios.Name"])
        studios_query.add_inner_join('Studio', 'Studios', 'Id')
        studios_query.add_aggregate_column(query.AggregateType.COUNT, 'Movies.Id', True)
        studios_query.set_order_by_columns(['COUNT'])
        studios_query.set_results_order("DESC")
        studios_query.set_results_offset(offset)
        studios_query.set_max_results(max_results)
        cursor.execute(studios_query.to_sql_query())
        studios = cursor.fetchall()
        return {'studios': [studio_to_json(studio) for studio in studios]}


def studio_to_json(studio):
    if len(studio) == 2:
        return {
            'id': studio[0],
            'name': studio[1]
        }
    else:
        return {
            'id': studio[0],
            'name': studio[1],
            'count': studio[2]
        }
