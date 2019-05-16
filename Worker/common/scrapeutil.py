import requests
from bs4 import BeautifulSoup
from common import parsingutil


def scrape_element(element_type, url, attributes):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")    
    element = soup.find(element_type, attrs=attributes)
    return element


def scrape_elements(element_type, url, attributes):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")    
    element = soup.findAll(element_type, attrs=attributes)
    return element


def scrape_list(url, attributes):
    return scrape_element('ul', url, attributes)


def scrape_table(url, attributes):
    return scrape_element('table', url, attributes)


def scrape_tables(url, attributes):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")
    tables = soup.findAll('table', attrs=attributes)
    return tables


def scrape_table_rows(url, attributes):
    table = scrape_table(url, attributes)
    if hasattr(table, 'findAll'):
        rows = table.findAll('tr')
        return rows
    else:
        return []


def scrape_movie(url, movie_name, studio_name):
    full_url = "https://www.boxofficemojo.com" + url
    attributes = {'border': '0', 'cellspacing': '1', 'cellpadding': '4', 'bgcolor': '#dcdcdc', 'width': '95%'}
    table = scrape_table(full_url, attributes)
    if hasattr(table, 'findAll'):
        cells = table.findAll('b')
        offset = 0
        if len(cells) == 8:
            offset += 1
        id = url[url.lower().index('id=') + 3:url.lower().index('.htm')]
        domestic_gross = parsingutil.dollar_text_to_int(cells[0].text)
        distributor = cells[1 + offset].text
        release_date = parsingutil.text_to_release_date(cells[2 + offset].text).strftime("%Y-%m-%d")
        genre = cells[3 + offset].text
        run_time = parsingutil.text_to_minutes(cells[4 + offset].text)
        mpaa_rating = cells[5 + offset].text
        production_budget = parsingutil.production_budget_to_int(cells[6 + offset].text)
        row_data = [id, movie_name, studio_name, domestic_gross, distributor, release_date, genre, run_time, mpaa_rating, production_budget]
        return row_data
