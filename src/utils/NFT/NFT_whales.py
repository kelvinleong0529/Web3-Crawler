from msilib.schema import Error
from numpy import isin
import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_whale_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__whales_api = "https://api.nftbase.com/web/api/v1/home/list-v3?home_tab={feature}&action={action}&price={price_range}&offset={offset}&limit={limit_per_page}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def __list_to_str(self, target_list: list) -> str:
        if not isinstance(target_list, list):
            raise TypeError("You should pass a LIST of actions")
        
        # remove any trailing whitespace and capitilize the first letter of each element in the list
        target_list = [data.strip().capitalize() for data in target_list]
        return ",".join(target_list)

    def get_whales_crypto_punks(self,
                                action: list = None,
                                price_range: int = None,
                                offset: int = None,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_lum=proxy_lum):

        FEATURE = "CryptoPunks"

        action = self.__list_to_str(action)
        
        # variables for scraping
        finished_scraping = False
        offset = 0

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__whales_api.format(feature=FEATURE,action=action,price_range=price_range,offset=offset,limit_per_page=limit_per_page)

            response = requests.get(api,
                                                          proxies=proxy_lum)