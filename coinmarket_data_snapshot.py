import requests
from bs4 import BeautifulSoup
from collections import namedtuple


''' Obróbka strony coinmarketcap top coins z wybranego dnia '''


class CoinTable:
    def __init__(self, date):
        page = requests.get(f"https://coinmarketcap.com/historical/{date}")
        soup = BeautifulSoup(page.content, 'html.parser')
        self.table = soup.find_all('table')[-1] # w ostatniej tabelce są interesujace nas dane

    def get_col_names(self):
        headers = self.table.find_all('th')
        return [col.text.strip().replace(' ', '_') for col in headers if col.text.strip()][:6]

    def get_rows(self):
        tbody = self.table.find('tbody')
        return tbody.find_all('tr')

    def extract_row_data(self):

        col_names = self.get_col_names()
        num_cols = len(col_names)
        CoinRecord = namedtuple('CoinRecord', col_names)

        records = []

        for row in self.get_rows():
            row_data = row.find_all('td')
            records.append(CoinRecord._make([rd.text.strip() for rd in row_data[:num_cols]]))
        return records