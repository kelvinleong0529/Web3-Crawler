import requests
import json

class Bitrue:
    
    def __init__(self,token_symbol:str) -> None:
        self.__api = "https://www.bitrue.com/exchange-web/web/tokenInfo/full?coinName={token_symbol}&language=en&appName=Netscape&appCodeName=Mozilla&appVersion=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&userAgent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&cookieEnabled=true&platform=Win32&userLanguage=en-US&vendor=Google+Inc.&onLine=true&product=Gecko&productSub=20030107&mimeTypesLen=4&pluginsLen=3&javaEnbled=false&windowScreenWidth=1920&windowScreenHeight=1080&windowColorDepth=24&bitrueLanguage=en_US&token=".format(token_symbol=token_symbol)
        self.__api_response = self.__get_api_response()

    # function to get the API endpoint response in JSON
    def __get_api_response(self) -> json:
        while True:
            response = requests.get(self.__api)
            if str(response.status_code) == "200":
                return response.json()
            else:
                continue

    # function to get the token's website URL
    def get_website_url(self) -> str:
        response = self.__api_response
        try:
            website_url = response["data"]["coinInfo"]["baseInfo"]["website"]
        except:
            website_url = 0
        return str(website_url)

    # function to get the token's full name
    def get_coin_name(self) -> str:
        response = self.__api_response
        try:
            coin_name = response["data"]["coinInfo"]["name3rd"]
        except:
            coin_name = 0
        return str(coin_name)