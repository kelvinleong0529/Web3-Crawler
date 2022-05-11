from collection import Collection
from user import User
from discovery import Discovery
from whales import Whale
from gas import Gas


class NftScraper(Collection, User, Discovery, Whale, Gas):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def scraper_info():
        print("This scraper is able to generate NFT collection & user details")