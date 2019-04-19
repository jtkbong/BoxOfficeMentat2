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
        studio_query.set_table("Movies")
        studio_query.set_unique_results(True)
        studio_query.set_return_columns(["Studio"])
        studio_query.add_where_clause(condition.Condition('Studio', '=', id))
        cursor.execute(studio_query.to_sql_query())
        studio = cursor.fetchone()

        if studio is None:
            abort(404, "Studio {0} doesn't exist.".format(id))

        return studio


class Studios(Resource):

    def get(self):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studios_query = query.Query()
        studios_query.set_table("Movies")
        studios_query.set_unique_results(True)
        studios_query.set_return_columns(["Studio"])
        studios_query.add_aggregate_column(query.AggregateType.COUNT, '*')
        studios_query.set_max_results(5000)
        print(studios_query.to_sql_query())
        cursor.execute(studios_query.to_sql_query())
        return {'studios': [{'name': i[0], 'count': i[1]} for i in cursor.fetchall()]}
