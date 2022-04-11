from operator import index
import os
import sys
import pandas as pd
import numpy as np
from multiprocessing import set_start_method
import multiprocessing
from tqdm import tqdm

p = os.path.abspath('.')
sys.path.insert(1, p)

# import Coin Gecko & Solana API and modules
from Bitrue.getWebsiteUrlAndCoinName import bitrueGetWebsiteUrlAndCoinName
from CoinGecko.bitrue import coinGeckoGetWebisteAddress

def crawlerFunction(tokenSymbol):

    WebsiteUrlFromBitrue = False
    WebsiteUrlFromCoinGecko = False
    coinName = False
    existsOnCoinGecko = False

    WebsiteUrlFromBitrue,coinName = bitrueGetWebsiteUrlAndCoinName(tokenSymbol)
    if coinName in ["0","-1"]:
        return [tokenSymbol,existsOnCoinGecko,coinName]
    coinNameInput = coinName.lower().replace(" ","-")
    WebsiteUrlFromCoinGecko = coinGeckoGetWebisteAddress(coinNameInput)
    if WebsiteUrlFromBitrue in WebsiteUrlFromCoinGecko:
        existsOnCoinGecko = True
    return [tokenSymbol,existsOnCoinGecko,coinName]


if __name__ == "__main__":

    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\bitrue.csv"

    df = pd.read_csv(path)
    df = df.loc[df["State"] == "not_approved"]
    bitrueTokenSymbolList = df["Symbol"]

    with multiprocessing.get_context("spawn").Pool(processes=40) as pool:
        output = list(
            tqdm(pool.imap(crawlerFunction, bitrueTokenSymbolList), total=len(bitrueTokenSymbolList)))

    output = np.reshape(output,(-1,3))
    output = pd.DataFrame(output,columns=["Symbol","On Coin Gecko?","Coin Gecko Token Name"])
    
    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\bitrue Output.csv"

    output.to_csv(path,index=False)
