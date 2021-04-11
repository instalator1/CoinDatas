from gecko_coin_downloader import GeckoQuotes, client
from coinmarket_data_snapshot import CoinTable
from pathlib import Path

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-date', type=str, help="format yyyymmdd" )
args = parser.parse_args()

# DANEWEJSCIOWE:
if args.date:
    SNAPSHOT_DATE = args.date
else:
    SNAPSHOT_DATE = '20210404'

FOLDER = f'Dane\\Top_from_{SNAPSHOT_DATE}'

# Uzyskanie listy top altcoinów z zadanej daty ze strony CoinMarketCap
table = CoinTable(SNAPSHOT_DATE)
table_data = table.extract_row_data()
coinmkt_symbols = [coin.Symbol for coin in table_data]

# Obróbka listy altcoinów aby jak najwiecej sciągneło za pierwszym razem
gecko_ids = []
dead_coins = []
gecko_coins = client.get_coins_list()
for csymbol in coinmkt_symbols:
    for gcoin in gecko_coins:
        if csymbol.lower() == gcoin['symbol']:
            gecko_ids.append(gcoin['id'])


class GQ(GeckoQuotes):
    """
    Tutaj mozna zmieniac:
    quotes_folder - folder gdzie zapisujemy dane
    start_date - poczatek sciaganych danych format timestamp
    end_date - koniec sciąganych danych format timestamp
    """
    quotes_folder = FOLDER


if __name__ == '__main__':

    done, fail = 0, 0
    for coin_id in gecko_ids:

        p = Path(str(Path.cwd()) + f'//{GQ.quotes_folder}//{coin_id}_daily.csv')
        if p.exists():
            print(f'{coin_id} in folder skipped')
        else:
            try:
                alt = GQ(coin_id)
                alt.quotes_to_csv()
                print(f"Coins downloaded: {done}  ", end="\r")
                done += 1

            except ValueError as valerr:
                fail += 1
                dead_coins.append(coin_id)
                gecko_ids.remove(coin_id)
                print(f'{valerr} not downloaded symbols ({coin_id}): {fail}')
