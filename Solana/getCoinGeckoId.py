from email import header
import requests

class Solana:

    def __init__(self) -> None:
        self.__api = "https://api.solscan.io/token/meta?token={tokenAddress}"
        self.__headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}

    def GetCoinGeckoId(self,tokenAddress:str,maxRetries:int=6) -> str:
        api = self.__api.format(tokenAddress=tokenAddress)

        coinGeckoId = -1
        retries = 0
        while retries < maxRetries:
            try:
                response = requests.get(api,headers=self.__headers).json()
                coinGeckoId = response["data"]["coingeckoId"]
                break
            except:
                coinGeckoId = 0
                retries += 1

        return str(coinGeckoId)
