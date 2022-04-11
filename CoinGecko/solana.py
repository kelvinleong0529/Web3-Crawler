import requests
from typing import Tuple

def coinGeckoSetSolanaTokenDetails(coinGeckoId,maxRetries=6) -> Tuple[str,str]:
    coinGeckoApi = "https://api.coingecko.com/api/v3/coins/{coinId}?tickers=false&market_data=false".format(coinId=coinGeckoId)
    
    solanaTokenAddress = -1
    solanaTokenName = -1
    retries = 0
    while retries < maxRetries:
        try:
            response = requests.get(coinGeckoApi).json()
            solanaTokenAddress = response["platforms"]["solana"]
            solanaTokenName = response["name"]
            break
        except:
            solanaTokenAddress = 0
            solanaTokenName = 0
            retries += 1
    
    return (str(solanaTokenAddress),str(solanaTokenName))