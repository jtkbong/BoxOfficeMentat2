from flask import request
from flask_restful import Resource
from werkzeug.exceptions import abort
from application.common import query
from application.common.query import AggregateType
from application.common import condition
from application.common import sqlhelper


class Person(Resource):
    def get(self, id):
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()
        person_query = query.Query()
        person_query.set_table("People")
        person_query.add_where_clause(condition.Condition('Id', '=', id))
        command = person_query.to_sql_query()
        cursor.execute(command)
        person = cursor.fetchone()

        if person is None:
            abort(404, "Person {0} doesn't exist.".format(id))

        return person_to_json(person)


class SearchPeople(Resource):
    def get(self):

        offset = request.args.get('offset')
        offset = 0 if offset is None else offset
        max_results = request.args.get('maxResults')
        max_results = 2000 if max_results is None else max_results

        name = request.args.get('name')
        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()

        search_query = query.Query()
        search_query.set_table("People")
        search_query.add_where_clause(condition.Condition("Name", "LIKE", "%" + name + "%"))

        mode = request.args.get('mode')
        if mode is not None and mode != 'results':
            search_query.set_mode(mode)
            if mode == 'count':
                search_query.add_aggregate_column(AggregateType.COUNT, 'Id', True)
        else:
            max_results = request.args.get('maxResults')
            if max_results is not None:
                search_query.set_max_results(max_results)

            offset = request.args.get('offset')
            if offset is not None:
                search_query.set_results_offset(offset)

        search_query.set_order_by_columns(["Name"])

        include_limit = False if mode == 'count' else True
        command = search_query.to_sql_query(include_limit)
        cursor.execute(command)

        if mode == 'count':
            count = cursor.fetchone()
            return {'count': count[0]}
        else:
            people = cursor.fetchall()
            return {'people': [person_to_json(person) for person in people]}


def person_to_json(person):
    return {
        'id': person[0],
        'name': person[1],
        'actor': person[2],
        'director': person[3],
        'producer': person[4],
        'screenWriter': person[5]
        }
