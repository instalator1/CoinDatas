import pandas as pd
from pathlib import Path

'''
Skrypt do poprawy indeksu z dziennych danych z CoinGecko, usuwa czas z formatu dd-mm-yyyy h:m:s.
Plik jest nadpisywany spowrotem w to samo miejsce także można rozważyć kopię zapasową przed uruchomieniem

'''
# Zmienic ewentualnie folder:
folder = "Top_from_28_03_2021"

p = Path(f"./{folder}")

for file in p.glob("*.csv"):
    df = pd.read_csv(file, index_col=0, parse_dates=True)
    if not df.empty:
        df.index = df.index.date
        df.index.set_names('date', inplace=True)
        df.to_csv(file)

