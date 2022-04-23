import requests

class Solana_scraper:

    def __init__(self,token_address:str) -> None:
        self.__api = "https://api.solscan.io/token/meta?token={token_address}".format(token_address=token_address)
        self.__headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
        self.__get_all_details()

    # function to get all the details of the token
    def __get_all_details(self) -> None:
        while True:
            response = requests.get(self.__api,headers = self.__headers)
            if str(response.status_code) == "200":
                
                data = response.json()["data"]
                
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
                self.coingecko_id = data["coingeckoId"]

                break
            else:
                continue
