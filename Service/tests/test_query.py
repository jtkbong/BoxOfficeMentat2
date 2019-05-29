import pytest
from application.common.query import Query
from application.common.query import AggregateType
from application.common.query import InnerJoin
from application.common.condition import Condition


def test_simple_query():
    query = Query()
    assert query is not None

    query.set_table("Movies")
    assert query.table == "Movies"

    cmd = query.to_sql_query()
    assert cmd == "SELECT * FROM boxofficementat.Movies LIMIT 0, 100"


def test_table_not_set():
    query = Query()
    query.set_return_columns(["Name", "Studio"])

    with pytest.raises(ValueError):
         query.to_sql_query()


def test_query_return_star():
    query = Query()
    query.set_table("Movies")
    query.set_return_columns(["*"])
    cmd = query.to_sql_query()

    assert cmd == "SELECT * FROM boxofficementat.Movies LIMIT 0, 100"


def test_query_set_return_columns():
    query = Query()
    query.set_table("Movies")
    query.set_return_columns(["Name", "Studio"])
    cmd = query.to_sql_query()

    assert cmd == "SELECT Name,Studio FROM boxofficementat.Movies LIMIT 0, 100"


def test_query_unique_results():
    query = Query()
    query.set_table("Movies")
    query.set_return_columns(["Studio"])
    query.set_unique_results(True)
    cmd = query.to_sql_query()

    assert cmd == "SELECT DISTINCT Studio FROM boxofficementat.Movies LIMIT 0, 100"


def test_query_where_clause():
    query = Query()
    query.set_table("Movies")
    query.add_where_clause(Condition("PersonId", "=", "chrisevans"))
    cmd = query.to_sql_query()

    assert cmd == "SELECT * FROM boxofficementat.Movies WHERE PersonId = 'chrisevans' LIMIT 0, 100"


def test_query_max_results():
    query = Query()
    query.set_table("Movies")
    query.set_max_results(2000)
    cmd = query.to_sql_query()

    assert cmd == "SELECT * FROM boxofficementat.Movies LIMIT 0, 2000"


def test_query_results_offset():
    query = Query()
    query.set_table("Movies")
    query.set_results_offset(200)
    cmd = query.to_sql_query()

    assert cmd == "SELECT * FROM boxofficementat.Movies LIMIT 200, 100"


def test_query_max_results_and_offset():
    query = Query()
    query.set_table("Movies")
    query.set_results_offset(200)
    query.set_max_results(300)
    cmd = query.to_sql_query()

    assert cmd == "SELECT * FROM boxofficementat.Movies LIMIT 200, 300"


def test_query_order_by_and_results_order():
    query = Query()
    query.set_table("Movies")
    query.set_return_columns(["Name", "Studio"])
    query.set_order_by_columns(["Studio"])
    query.set_results_order("DESC")
    cmd = query.to_sql_query()

    assert cmd == "SELECT Name,Studio FROM boxofficementat.Movies ORDER BY Studio DESC LIMIT 0, 100"


def test_subqueries():
    query = Query()
    query.set_table("Movies")

    subquery1 = Query()
    subquery1.set_table("Credits")
    subquery1.set_return_columns(["MovieId"])
    subquery1.add_where_clause(Condition("PersonId", "=", "chrisevans"))
    subquery1.add_where_clause(Condition("Relationship", "=", "Actor"))

    subquery2 = Query()
    subquery2.set_table("Credits")
    subquery2.set_return_columns(["MovieId"])
    subquery2.add_where_clause(Condition("PersonId", "=", "chrishemsworth"))
    subquery2.add_where_clause(Condition("Relationship", "=", "Actor"))

    query.add_subquery("Id", subquery1)
    query.add_subquery("Id", subquery2)

    cmd = query.to_sql_query()
    assert cmd == "SELECT * FROM boxofficementat.Movies " \
                  "WHERE Id IN (SELECT MovieId FROM boxofficementat.Credits " \
                  "WHERE PersonId = 'chrisevans' AND Relationship = 'Actor') " \
                  "AND Id IN (SELECT MovieId FROM boxofficementat.Credits " \
                  "WHERE PersonId = 'chrishemsworth' AND Relationship = 'Actor') LIMIT 0, 100"


def test_inner_join_creation():
    inner_join = InnerJoin('Studios', 'Id', 'Movies', 'Studio')
    sql_condition = inner_join.get_join_condition_sql()
    assert sql_condition == " INNER JOIN boxofficementat.Movies ON " \
                            "boxofficementat.Studios.Id=boxofficementat.Movies.Studio "


def test_inner_join_query():

    query = Query()
    query.set_table("Movies")
    query.set_return_columns(["Studios.Name"])
    query.add_inner_join('Studio', 'Studios', 'Id')
    query.add_aggregate_column(AggregateType.COUNT, 'Movies.Id', True)
    query.set_order_by_columns(['COUNT'])
    query.set_results_offset(80)
    query.set_max_results(20)
    cmd = query.to_sql_query()
    assert cmd == "SELECT Studios.Name,COUNT(DISTINCT Movies.Id) AS COUNT FROM boxofficementat.Movies " \
                  "INNER JOIN boxofficementat.Studios ON boxofficementat.Movies.Studio=boxofficementat.Studios.Id  " \
                  "GROUP BY Studios.Name ORDER BY COUNT LIMIT 80, 20"

