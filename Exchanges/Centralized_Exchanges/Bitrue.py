import requests

class Bitrue:
    
    def __init__(self) -> None:
        self.__api = "https://www.bitrue.com/exchange-web/web/tokenInfo/full?coinName={tokenSymbol}&language=en&appName=Netscape&appCodeName=Mozilla&appVersion=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&userAgent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&cookieEnabled=true&platform=Win32&userLanguage=en-US&vendor=Google+Inc.&onLine=true&product=Gecko&productSub=20030107&mimeTypesLen=4&pluginsLen=3&javaEnbled=false&windowScreenWidth=1920&windowScreenHeight=1080&windowColorDepth=24&bitrueLanguage=en_US&token="

    def GetWebsiteUrl(self,tokenSymbol:str, maxRetries:int=6) -> str:
        api = self.__api.format(tokenSymbol=tokenSymbol)
        websiteUrl = -1
        retries = 0
        while retries < maxRetries:
            try:
                response = requests.get(api).json()
                websiteUrl = response["data"]["coinInfo"]["baseInfo"]["website"]
                break
            except:
                websiteUrl = 0
                retries += 1
        return str(websiteUrl)

    def getCoinName(self,tokenSymbol:str,maxRetries:int=6) -> str:
        api = self.__api.format(tokenSymbol=tokenSymbol)
        coinName = -1
        retries = 0
        while retries < maxRetries:
            try:
                response = requests.get(api).json()
                coinName = response["data"]["coinInfo"]["name3rd"]
                break
            except:
                coinName = 0
                retries += 1
        return str(coinName)


