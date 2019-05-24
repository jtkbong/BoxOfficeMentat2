from common import parsingutil
import datetime


def test_get_start_and_end_dates_mid_month():
    dates = parsingutil.week_text_to_start_end_dates('May 10-16, 2019')
    assert len(dates) == 2
    expected_start_date = datetime.date(2019, 5, 10)
    verify_date(dates[0], expected_start_date)

    expected_end_date = datetime.date(2019, 5, 16)
    verify_date(dates[1], expected_end_date)


def test_get_start_and_end_dates_eoy():
    dates = parsingutil.week_text_to_start_end_dates('December 29-January 4, 2018')
    assert len(dates) == 2
    expected_start_date = datetime.date(2017, 12, 29)
    verify_date(dates[0], expected_start_date)

    expected_end_date = datetime.date(2018, 1, 4)
    verify_date(dates[1], expected_end_date)


def verify_date(actual, expected):
    assert actual.year == expected.year
    assert actual.month == expected.month
    assert actual.day == expected.day
