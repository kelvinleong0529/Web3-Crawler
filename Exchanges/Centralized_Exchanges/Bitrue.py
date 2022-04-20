import requests

class Bitrue:
    
    def __init__(self,token_symbol:str, max_retries:int=6) -> None:
        self.__api = "https://www.bitrue.com/exchange-web/web/tokenInfo/full?coinName={token_symbol}&language=en&appName=Netscape&appCodeName=Mozilla&appVersion=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&userAgent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&cookieEnabled=true&platform=Win32&userLanguage=en-US&vendor=Google+Inc.&onLine=true&product=Gecko&productSub=20030107&mimeTypesLen=4&pluginsLen=3&javaEnbled=false&windowScreenWidth=1920&windowScreenHeight=1080&windowColorDepth=24&bitrueLanguage=en_US&token="
        self.token_symbol = token_symbol
        self.max_retries = max_retries

    # function to get the token's website URL
    def get_website_url(self) -> str:
        api = self.__api.format(token_symbol=self.token_symbol)
        website_url = -1
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(api).json()
                website_url = response["data"]["coinInfo"]["baseInfo"]["website"]
                break
            except:
                website_url = 0
                retries += 1
        return str(website_url)

    # function to get the token's full name
    def get_coin_name(self) -> str:
        api = self.__api.format(token_symbol=self.token_symbol)
        coin_name = -1
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(api).json()
                coin_name = response["data"]["coinInfo"]["name3rd"]
                break
            except:
                coin_name = 0
                retries += 1
        return str(coin_name)


