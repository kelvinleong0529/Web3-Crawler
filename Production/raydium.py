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
from Solana.getCoinGeckoId import solanaGetCoinGeckoId
from CoinGecko.solana import coinGeckoSetSolanaTokenDetails

def crawlerFunction(tokenAddress):

    solanaTokenAddress = False
    solanaTokenName = False
    existsOnCoinGecko = False

    coinGeckoId = solanaGetCoinGeckoId(tokenAddress)
    if coinGeckoId in ['0','-1']:
        return [tokenAddress,existsOnCoinGecko,solanaTokenName]
    solanaTokenAddress, solanaTokenName = coinGeckoSetSolanaTokenDetails(coinGeckoId)
    if solanaTokenAddress == tokenAddress:
        existsOnCoinGecko = True
    return [tokenAddress,existsOnCoinGecko,solanaTokenName]


if __name__ == "__main__":

    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\raydium.csv"

    df = pd.read_csv(path)
    # df = df.iloc[:20]
    solanaAddressList = df["Symbol"]

    with multiprocessing.get_context("spawn").Pool(processes=40) as pool:
        output = list(
            tqdm(pool.imap(crawlerFunction, solanaAddressList), total=len(solanaAddressList)))

    output = np.reshape(output,(-1,3))
    output = pd.DataFrame(output,columns=["Symbol","On Coin Gecko?","Coin Gecko Token FE Name"])
    
    path = r"C:\Users\kelvin.leong\Desktop\Crypto\Production\raydium Output.csv"

    output.to_csv(path,index=False)