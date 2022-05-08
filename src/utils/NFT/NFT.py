from NFT_collection import NFT_scraper_collection_class
from NFT_user import NFT_scraper_user_class
from NFT_discovery import NFT_scraper_extra_feature_class
from NFT_whales import NFT_scraper_whale_class


class NFT_scraper(NFT_scraper_collection_class, NFT_scraper_user_class,
                  NFT_scraper_extra_feature_class, NFT_scraper_whale_class):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def scraper_info():
        print("This scraper is able to generate NFT collection & user details")


my_NFT_scraper = NFT_scraper()
NFT_scraper().scraper_info()
results = my_NFT_scraper.get_collection_asset(collection_id="the-forgotten-cult-oracles",limit=6)
for result in results:
    print(result)