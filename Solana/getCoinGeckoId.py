from email import header
import requests

def solanaGetCoinGeckoId(solanaTokenAddress,maxRetries=6) -> str:
    solanaApi = "https://api.solscan.io/token/meta?token={tokenAddress}".format(tokenAddress=solanaTokenAddress)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}

    coinGeckoId = -1
    retries = 0
    while retries < maxRetries:
        try:
            response = requests.get(solanaApi,headers=headers).json()
            coinGeckoId = response["data"]["coingeckoId"]
            break
        except:
            coinGeckoId = 0
            retries += 1

    return str(coinGeckoId)
