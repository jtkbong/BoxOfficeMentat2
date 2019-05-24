from common import sqlwriter


def test_simple_query():
    command = sqlwriter.get_update_row_command('Movies', ['DomesticGross'])
    assert command == "UPDATE boxofficementat.Movies SET DomesticGross=%s WHERE Id=%s"
    command_with_params = command % (123456, 'marvel2019')
    assert command_with_params == "UPDATE boxofficementat.Movies SET DomesticGross=123456 WHERE Id=marvel2019"
