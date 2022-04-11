import requests
import json
from typing import Tuple

def bitrueGetWebsiteUrlAndCoinName(tokenSymbol, maxRetries=6) -> Tuple[str,str]:
    BitrueApi = "https://www.bitrue.com/exchange-web/web/tokenInfo/full?coinName={tokenSymbol}&language=en&appName=Netscape&appCodeName=Mozilla&appVersion=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&userAgent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&cookieEnabled=true&platform=Win32&userLanguage=en-US&vendor=Google+Inc.&onLine=true&product=Gecko&productSub=20030107&mimeTypesLen=4&pluginsLen=3&javaEnbled=false&windowScreenWidth=1920&windowScreenHeight=1080&windowColorDepth=24&bitrueLanguage=en_US&token=".format(tokenSymbol=tokenSymbol)

    officialWebsiteUrl = -1
    coinName = -1
    retries = 0
    while retries < maxRetries:
        try:
            response = requests.get(BitrueApi).json()
            coinName = response["data"]["coinInfo"]["name3rd"]
            officialWebsiteUrl = response["data"]["coinInfo"]["baseInfo"]["website"]
            break
        except:
            coinName = 0
            officialWebsiteUrl = 0
            retries += 1

    return (str(officialWebsiteUrl),str(coinName))
