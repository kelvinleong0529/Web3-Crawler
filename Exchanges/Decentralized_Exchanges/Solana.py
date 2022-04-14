import requests

class Solana:

    def __init__(self,tokenAddress:str) -> None:
        self.__api = "https://api.solscan.io/token/meta?token={tokenAddress}".format(tokenAddress=tokenAddress)
        self.__headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
        self.__getAllDetails()

    def __getAllDetails(self) -> None:
        while True:
            response = requests.get(self.__api,headers = self.__headers).json()
            if response["succcess"]:
                
                data = response["data"]
                
                # Basic information
                self.symbol = data["symbol"]
                self.name = data["name"]
                self.decimals = data["decimals"]
                self.holders = data["holder"]

                # Image
                self.image = requests.get(data["icon"])

                # Tags
                self.tags = [tag["name"] for tag in data["tag"] if tag]

                # Links
                self.homepage = data["website"]
                
                # Community
                self.twitter = data["twitter"]
                self.GetCoinGeckoId = data["coingeckoId"]

                break
            else:
                continue

temp = Solana("2wmKXX1xsxLfrvjEPrt2UHiqj8Gbzwxvffr9qmNjsw8g")
print(temp.__dict__)
