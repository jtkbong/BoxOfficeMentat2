from flask_restful import Resource
from application.common import query
from application.common import condition
from application.common import sqlhelper


class Credits(Resource):
    def get(self, movie_id):

        connection = sqlhelper.get_sql_conn()
        cursor = connection.cursor()

        credits_query = query.Query()
        credits_query.set_table("Credits")
        credits_query.set_return_columns(["PersonId", "People.Name", "Relationship"])
        credits_query.add_inner_join("PersonId", "People", "Id")
        credits_query.add_where_clause(condition.Condition("MovieId", "=", movie_id))

        command = credits_query.to_sql_query()
        cursor.execute(command)

        credits = cursor.fetchall()
        return {'credits': [credit_to_json(credit) for credit in credits]}


def credit_to_json(credit):
    return {
        'personId': credit[0],
        'name': credit[1],
        'relationship': credit[2]
        }
