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
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        studios_query = query.Query()
        studios_query.set_table("Movies")
        studios_query.set_unique_results(True)
        studios_query.set_return_columns(["Studio"])
        studios_query.add_aggregate_column(query.AggregateType.COUNT, '*')
        studios_query.set_max_results(2000)
        studios_query.set_order_by_columns([query.AggregateType.COUNT.name])
        studios_query.set_results_order("DESC")
        cursor.execute(studios_query.to_sql_query())
        studios = {}
        for s in cursor.fetchall():
            studios[s[0]] = [s[0], None, s[1]]

        studios_name_query = query.Query()
        studios_name_query.set_table("Studios")
        studios_name_query.set_unique_results(True)
        studios_name_query.set_return_columns(["Id", "Name"])
        studios_name_query.set_max_results(2000)
        cursor.execute(studios_name_query.to_sql_query())
        for s in cursor.fetchall():
            if s[0] not in studios:
                studios[s[0]] = [s[0], s[1], 0]
            else:
                studios[s[0]][1] = s[1]

        return {'studios': [studio_to_json(studio) for studio_id, studio in studios.items()]}


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
