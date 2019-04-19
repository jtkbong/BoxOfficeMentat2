import uuid
from enum import Enum


class AggregateType(Enum):

    COUNT = 1
    SUM = 2
    AVG = 3
    MIN = 4
    MAX = 5


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
        self.subQueries = []
        self.orderByColumns = []
        self.innerQuery = None
        self.resultsOffset = 0
        
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

    def add_aggregate_column(self, aggregate_type, column):
        self.aggregateColumns.append({
            'aggregate_type': aggregate_type,
            'column': column
        })
                
    def set_results_order(self, results_order):
        self.resultsOrder = results_order
                
    def set_max_results(self, max_results):
        self.maxResults = max_results

    def set_results_offet(self, results_offet):
        self.resultsOffset = results_offet
                
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
            query = query + "*"

        if len(self.aggregateColumns) > 0:
            for aggregate_column in self.aggregateColumns:
                query = query + "," + ("%s(%s) AS %s" %
                                       (aggregate_column['aggregate_type'].name,
                                        aggregate_column['column'],
                                        aggregate_column['aggregate_type'].name))

        query = query + " FROM boxofficementat.%s" % self.table
        
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

        if len(self.aggregateColumns) > 0:
            query = query + " GROUP BY " + ",".join(self.columns)

        if len(self.orderByColumns) > 0:
            query = query + " ORDER BY " + ",".join(self.orderByColumns)
            if self.resultsOrder is not None:
                query = query + " " + self.resultsOrder

        if include_limit:
            query = query + " LIMIT %d, %d" % (int(self.resultsOffset), int(self.maxResults))

        return query
