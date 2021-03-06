from common import configuration
from common import logging
import pymysql
import time
from enum import Enum


class WriteType(Enum):
    insert = 1
    update = 2
    delete = 3


maxTries = 3


def write_rows_to_db_retries(table_name, column_names, write_type, rows, ignore_integrity_errors):
    connection = get_sql_conn()
    cursor = connection.cursor()
    rows = rows[0:len(rows)-1] if rows[-1] == "###DONE###\n" else rows
    for row in rows:
        num_tries = 0
        success = False
        row_remove_new_line = row.replace('\n', '')
        while num_tries < maxTries and not success:
            try:
                if write_type is WriteType.insert:
                    insert_row_to_db(cursor, table_name, column_names, row_remove_new_line)
                elif write_type is WriteType.update:
                    update_row_in_db(cursor, table_name, column_names, row_remove_new_line)
                success = True
                break
            except pymysql.err.IntegrityError:
                if ignore_integrity_errors:
                    success = True
                    continue
                else:
                    logging.log_error(
                        'Integrity Error: %s, [%s]\n' % (table_name, ','.join(row_remove_new_line.split('\t'))))
                    break
            except pymysql.err.OperationalError:
                time.sleep(30)
                num_tries += 1
                continue
        if num_tries == maxTries and not success:
            logging.log_error(
                'Max Tries Reached: %s, [%s]\n' % (table_name, ','.join(row_remove_new_line.split('\t'))))
    connection.commit()
    connection.close()


def insert_row_to_db(cursor, table_name, column_names, row):
    command = get_insert_row_command(table_name, column_names)
    cursor.execute(command, (row.split('\t')))


def update_row_in_db(cursor, table_name, column_names, row):
    command = get_update_row_command(table_name, column_names)
    cursor.execute(command, (row.split('\t')))


def delete_row_in_db(cursor, table_name, row_id):
    command = 'DELETE FROM boxofficementat.' + table_name + \
              ' WHERE Id=%s'
    cursor.execute(command, row_id)


def clear_table(table_name):
    connection = get_sql_conn()
    cursor = connection.cursor()   
    command = 'DELETE FROM boxofficementat.' + table_name
    cursor.execute(command)
    connection.commit()
    connection.close()


def get_insert_row_command(table_name, column_names):
    command = 'INSERT INTO boxofficementat.' + table_name + '(' + ','.join(column_names) + \
              ') VALUES (' + ','.join(['%s'] * len(column_names)) + ')'
    return command


def get_update_row_command(table_name, column_names):
    update_strings = []
    for column_name in column_names:
        update_strings.append(column_name + "=%s")

    command = 'UPDATE boxofficementat.' + table_name + \
              ' SET ' + ','.join(update_strings) + \
              " WHERE Id=%s"
    return command


def get_sql_conn():
    db_info = configuration.get_config()['db']
    db_host = db_info['dbhost']
    db_user = db_info['dbuser']
    db_password = db_info['dbpassword']

    connection = pymysql.connect(host=db_host, user=db_user, password=db_password)
    return connection
