from operator import index
import os
import sys
import pandas as pd
import numpy as np
import multiprocessing
from tqdm import tqdm

p = os.path.abspath('.')
sys.path.insert(1, p)

# import Coin Gecko, Solana API and modules
from Exchanges.Centralized_Exchanges.Bitrue import Bitrue
from CoinGecko import CoinGecko

def crawler_function(token_symbol) -> list:

    bitrue_website_url = False
    bitrue_coin_name = False
    coingecko_website_url = False
    exists_on_coingecko = False

    # first we scrape the token's info on Bitrue
    bitrue_token = Bitrue(token_symbol)
    bitrue_website_url = bitrue_token.get_website_url()
    bitrue_coin_name = bitrue_token.get_coin_name()
    # return if fail to crawl token's info on Bitrue
    if bitrue_coin_name in ["0","-1"]:
        return [token_symbol,exists_on_coingecko,bitrue_coin_name]
    
    # scrape token's info on CoinGecko
    coingecko_id = bitrue_coin_name.lower().replace(" ","-")
    coingecko_website_url = CoinGecko(coingecko_id).homepages

    # check if the bitrue's website url match with coingecko's website url
    if bitrue_website_url in coingecko_website_url:
        exists_on_coingecko = True
    return [token_symbol,exists_on_coingecko,bitrue_coin_name]


if __name__ == "__main__":

    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\bitrue.csv"

    df = pd.read_csv(path)
    df = df.loc[df["State"] == "not_approved"]
    bitrue_token_symbol_list = df["Symbol"]

    with multiprocessing.get_context("spawn").Pool(processes=40) as pool:
        scraping_result = list(
            tqdm(pool.imap(crawler_function, bitrue_token_symbol_list), total=len(bitrue_token_symbol_list)))

    scraping_result = np.reshape(scraping_result,(-1,3))
    scraping_result = pd.DataFrame(scraping_result,columns=["Symbol","On Coin Gecko?","Coin Gecko Token Name"])
    
    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\bitrue Output.csv"

    scraping_result.to_csv(path,index=False)
