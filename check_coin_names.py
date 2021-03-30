from gecko_coin_downloader import GeckoQuotes
from coinmarketcap_scrap import coin_list
from pathlib import Path
import datetime as dt

# parametry
folder = 'Top_from_28_03_2021'
end_date = int(dt.datetime.timestamp(dt.datetime.now()))  # dzisiejsza data

coin_list = [coin.lower().replace(' ', '-').replace('.', '-') for coin in coin_list]
# lista coinow ktore trzeba podmienic nazwe aby je sciagnelo CoinGecko:
dic = {'xrp': 'ripple',
       'obyte': 'byteball',
       'firstblood': 'dawn',
       'storjcoin-x': 'storj',
       'navcoin': 'nav-coin',
       'agoras-tokens': 'agoras',
       'chrono.tech': 'chronobank',
       'i/o-coin': 'iocoin',
       'gridcoin': 'gridcoin-research',
       'bela': 'belacoin',
       'dubaicoin': 'dubaicoin-dbix',
       'theta': 'theta-token',
       'terra': 'terra-luna',
       'avalanche': 'avalanche-2',
       'bitcoin-sv': 'bitcoin-cash-sv',
       'bittorrent': 'bittorrent-2',
       'sushiswap': 'sushi',
       'synthetix': 'havven',
       'enjin-coin': 'enjincoin',
       'polygon': 'matic-network',
       'pancakeswap': 'pancakeswap-token',
       'holo': 'holotoken',
       'celsius': 'celsius-degree-token',
       'ren': 'republic-protocol',
       'voyager-token': 'ethos',
       'iost': 'iostoken',
       'omg-network': 'omisego',
       'mvl': 'mass-vehicle-ledger',
       'horizen': 'zencash',
       'stormx': 'storm',
       'alpha-finance-lab': 'alpha-finance',
       'binance-coin': 'binancecoin',
       'crypto-com-coin': 'crypto-com-chain',
       'elrond': 'elrond-erd-2',
       'compound': 'compound-governance-token',
       'stacks': 'blockstack',
       'reserve-rights': 'reserve-rights-token',
       'polymath': 'polymath-network',
       'reef': 'reef-finance',
       'orchid': 'orchid-protocol',
       'quant': 'quant-network',
       'skale-network': 'skale',
       'kucoin-token': 'kucoin-shares',
       'kava-io': 'kava',
       'quarkchain': 'quark-chain',
       'hifi-finance': 'mainframe',
       'myneighboralice': 'my-neighbor-alice',
       'travala-com': 'concierge-io',
       'rsk-infrastructure-framework': 'rif-token',
       'wootrade': 'wootrade-network',
       'chromia': 'chromaway',
       'klaytn': 'klay-token',
       'sharetoken': 'sharering',
       'irisnet': 'iris-network',
       'syntropy': 'noia-network',
       'trueusd': 'true-usd'}

coin_list = [dic.get(coin, coin) for coin in coin_list]
dead_coins = []


class GQ(GeckoQuotes):
    """ Tutaj mozna zmieniac folder , koncową datę ewentualnie, datę początkową jako start_date wszystko w
     formacie timestamp """
    quotes_folder = folder
    end_date = end_date


if __name__ == '__main__':

    cnt = 0
    for coin in coin_list:

        p = Path(str(Path.cwd()) + f'//{GQ.quotes_folder}//{coin}_daily.csv')
        if p.exists():
            print(f'{coin} in folder skipped')
        else:
            try:
                alt = GQ(coin)
                alt.quotes_to_csv()

            except ValueError as valerr:
                cnt += 1
                dead_coins.append(coin)
                coin_list.remove(coin)
                print(f'{valerr} not downloaded symbols ({coin}): {cnt}')



