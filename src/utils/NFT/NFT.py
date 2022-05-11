from collection import Collection
from discovery import Discovery
from gas import Gas
from user import User
from whales import Whale


class NftScraper(Collection, Discovery, Gas, User, Whale):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def scraper_info():
        print("This scraper is able to generate NFT collection & user details")