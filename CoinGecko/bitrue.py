import requests

def coinGeckoGetWebisteAddress(coinGeckoId,maxRetries=6) -> str:
    coinGeckoApi = "https://api.coingecko.com/api/v3/coins/{coinId}?tickers=false&market_data=false".format(coinId=coinGeckoId)
    
    WebsiteUrl = -1
    retries = 0
    while retries < maxRetries:
        try:
            response = requests.get(coinGeckoApi).json()
            WebsiteUrl = response["links"]["homepage"]
            break
        except:
            WebsiteUrl = 0
            retries += 1
    
    return str(WebsiteUrl)