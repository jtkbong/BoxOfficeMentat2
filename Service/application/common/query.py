import uuid
from enum import Enum


class AggregateType(Enum):

    COUNT = 1
    SUM = 2
    AVG = 3
    MIN = 4
    MAX = 5


class InnerJoin:

    def __init__(self, self_table, self_column, join_table, join_column):
        self.selfTable = self_table
        self.selfColumn = self_column
        self.joinTable = join_table
        self.joinColumn = join_column

    def get_join_condition_sql(self):
        return " INNER JOIN boxofficementat.%s ON boxofficementat.%s.%s=boxofficementat.%s.%s " % \
               (self.joinTable, self.selfTable, self.selfColumn, self.joinTable, self.joinColumn)


class Query:
    
    DefaultNumResults = 100
    
    def __init__(self):
        self.id = uuid.uuid4()
        self.table = None
        self.resultsOrder = None
        self.maxResults = Query.DefaultNumResults
        self.uniqueResults = False
        self.columns = []
        self.aggregateColumns = []
        self.whereClauses = []
        self.innerJoins = []
        self.subQueries = []
        self.orderByColumns = []
        self.innerQuery = None
        self.resultsOffset = 0
        self.mode = None
        
    def set_table(self, table):
        self.table = table
        
    def set_unique_results(self, unique_results):
        self.uniqueResults = unique_results
    
    def set_return_columns(self, columns):
        self.columns = columns
        
    def add_where_clause(self, condition):
        self.whereClauses.append(condition)
        
    def set_order_by_columns(self, columns):
        self.orderByColumns = columns

    def add_aggregate_column(self, aggregate_type, column='*', use_distinct=False):
        self.aggregateColumns.append({
            'aggregate_type': aggregate_type,
            'column': column,
            'use_distinct': use_distinct
        })
                
    def set_results_order(self, results_order):
        self.resultsOrder = results_order
                
    def set_max_results(self, max_results):
        self.maxResults = max_results

    def set_results_offset(self, results_offet):
        self.resultsOffset = results_offet

    def set_mode(self, mode):
        self.mode = mode

    def add_inner_join(self, self_column, join_table, join_column):
        self.innerJoins.append(InnerJoin(self.table, self_column, join_table, join_column))

    def add_subquery(self, column, subquery):
        self.subQueries.append([column, subquery])
    
    def to_sql_query(self, include_limit=True):
        
        if self.table is None:
            raise ValueError("Table not set for query.")
        
        query = "SELECT "
        
        if len(self.columns) > 0:
            if self.uniqueResults is True:
                query = query + "DISTINCT "
            query = query + ",".join(self.columns)
        else:
            if self.mode != 'count':
                query = query + "*"

        if len(self.aggregateColumns) > 0:
            if len(self.columns) > 0:
                query = query + ","
            for aggregate_column in self.aggregateColumns:
                query = query + ("%s(%s %s) AS %s" %
                                       (aggregate_column['aggregate_type'].name,
                                        'DISTINCT' if aggregate_column['use_distinct'] else '',
                                        aggregate_column['column'],
                                        aggregate_column['aggregate_type'].name))

        query = query + " FROM boxofficementat.%s" % self.table

        if len(self.innerJoins) > 0:
            for inner_join in self.innerJoins:
                query = query + inner_join.get_join_condition_sql()
        
        if len(self.whereClauses) > 0 or len(self.subQueries) > 0:
            query = query + " WHERE "

            if len(self.whereClauses) > 0:
                where_clauses_sql = []
                for whereClause in self.whereClauses:
                    where_clauses_sql.append(whereClause.to_sql_condition())
                query = query + " AND ".join(where_clauses_sql)
            
            if len(self.subQueries) > 0:
                sub_queries_sql = []
                for column, subQuery in self.subQueries:
                    sub_queries_sql.append(column + " IN (" + subQuery.to_sql_query(False) + ")")
                if len(self.whereClauses) > 0:
                    query = query + " AND "
                query = query + " AND ".join(sub_queries_sql)

        if len(self.aggregateColumns) > 0 and len(self.columns) > 0:
            query = query + " GROUP BY " + ",".join(self.columns)

        if len(self.orderByColumns) > 0:
            query = query + " ORDER BY " + ",".join(self.orderByColumns)
            if self.resultsOrder is not None:
                query = query + " " + self.resultsOrder

        if include_limit:
            query = query + " LIMIT %d, %d" % (int(self.resultsOffset), int(self.maxResults))

        return query
