import datetime
import calendar


def dollar_text_to_int(text):
    try:
        return float(text.strip('$').replace(',', '').replace(' ', '').replace('(Estimate)', ''))
    except ValueError:
        return 0


def text_to_release_date(text):
    if ',' not in text:
        if len(text) == 4:
            return datetime.datetime(int(text), 12, 31)
        else:
            return datetime.datetime(int(text[-4::]),
                                     datetime.datetime.strptime(text[0:text.index(' ')], '%B').month, 1)
    
    return datetime.datetime.strptime(text, '%B %d, %Y')


def text_to_minutes(text):
    if text == 'N/A':
        return None
    
    hours = int(text[0:text.index('hrs.')])
    minutes = int(text[text.index('.') + 1:text.index('min.')])
    return 60 * hours + minutes


def production_budget_to_int(text):
    if text == 'N/A':
        return 0
    return dollar_text_to_int(text.replace('million', '000000'))


def get_id_from_url(url):
    if url is None or 'id=' not in url or '.htm' not in url:
        return None
    return url[url.index('id=') + 3: url.index('.htm')]


def get_studio_from_url(url):
    if url is None or 'studio=' not in url or '.htm' not in url:
        return None
    return url[url.index('studio=') + 7: url.index('.htm')]


def text_to_int(s):
    try:
        return int(s.replace(',', ''))
    except ValueError:
        return 0


def week_text_to_start_end_dates(text):
    year_text = text[text.index(',') + 1:].strip()
    start_year = int(year_text)

    start_date_text = text[0:text.index('-')]
    start_month_text = start_date_text[0:start_date_text.index(' ')]
    start_month = list(calendar.month_name).index(start_month_text)
    start_day = int(start_date_text[start_date_text.index(' ') + 1:])

    if 'December' in text and 'January' in text:
        start_year -= 1

    start_date = datetime.date(start_year, start_month, start_day)

    end_date = start_date + datetime.timedelta(days=6)
    return [start_date, end_date]
