from .collection import collection_class
from .user import user_class
from .discovery import discovery_class
from .whales import whale_class
from .gas import gas_class


class NFT_scraper(collection_class, user_class, discovery_class, whale_class,
                  gas_class):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def scraper_info():
        print("This scraper is able to generate NFT collection & user details")