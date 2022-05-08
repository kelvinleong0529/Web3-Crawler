import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_gas_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_gas() -> str:
        gas_api = "https://api.nftbase.com/web/api/v1/gas"
        gas_price = None
        response = requests.get(gas_api)
        if str(response.status_code) == "200":
            gas_price = response.json()["data"]
        return gas_price