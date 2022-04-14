import requests
from typing import Tuple

class CoinGecko:

    def __init__(self) -> None:
        self.__api = "https://api.coingecko.com/api/v3/coins/{Id}?tickers=false&market_data=false"

    def getWebsiteUrl(self,coinGeckoId:str,maxRetries:int=6) -> str:
        api = self.__api.format(Id=coinGeckoId)
        
        WebsiteUrl = -1
        retries = 0
        while retries < maxRetries:
            try:
                response = requests.get(api).json()
                WebsiteUrl = response["links"]["homepage"]
                break
            except:
                WebsiteUrl = 0
                retries += 1
        
        return str(WebsiteUrl)

    def getSolanaTokenDetails(self,coinGeckoId,maxRetries=6) -> Tuple[str,str]:
        api = self.__api.format(Id=coinGeckoId)
        
        solanaTokenAddress = -1
        solanaTokenName = -1
        retries = 0
        while retries < maxRetries:
            try:
                response = requests.get(api).json()
                solanaTokenAddress = response["platforms"]["solana"]
                solanaTokenName = response["name"]
                break
            except:
                solanaTokenAddress = 0
                solanaTokenName = 0
                retries += 1
    
        return (str(solanaTokenAddress),str(solanaTokenName))