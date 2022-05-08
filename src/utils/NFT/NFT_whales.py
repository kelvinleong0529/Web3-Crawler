from msilib.schema import Error
from weakref import proxy
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

    def __get_featured_nft(self, feature: str, action: list, price_range: int,
                           limit_per_page: int, limit: int,
                           proxy_lum: dict) -> list:

        featured_nft_list = []

        # scraping parameters
        limit_per_page = limit_per_page if limit_per_page else self.LIMIT_PER_PAGE
        limit = limit if limit else self.LIMIT
        action = self.__list_to_str(action)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__whales_api.format(feature=feature,
                                           action=action,
                                           price_range=price_range,
                                           offset=offset,
                                           limit_per_page=limit_per_page)
            response = requests.get(api, proxies=proxy_lum)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for nfts in data:

                    if scraped_count > limit:
                        break

                    # initialize a dict to store the details
                    featured_nft = {}

                    # featured nft basic details
                    featured_nft["id"] = self.get_value(nfts, "id")
                    featured_nft["token_id"] = self.get_value(nfts, "token_id")
                    price = self.get_value(nfts, "price")
                    currency = self.get_value(nfts, "symbol")
                    featured_nft["price"] = price + " " + currency
                    featured_nft["action"] = self.get_value(nfts, "action")
                    featured_nft["timestamp"] = super().utc_from_timestamp(
                        self.get_value(nfts, "timestamp"))

                    # featured nft relevant user details
                    user = self.get_value(nfts, "user")
                    featured_nft["user_id"] = self.get_value(user, "id")
                    featured_nft["user_name"] = self.get_value(user, "name")
                    featured_nft["user_address"] = self.get_value(
                        user, "address")
                    featured_nft["user_avatar_url"] = self.get_value(
                        user, "avatar_url")
                    featured_nft["user_item_count"] = self.get_value(
                        user, "item_count")

                    # featured nft details
                    item = self.get_value(nfts, "item")
                    featured_nft["item_id"] = self.get_value(item, "id")
                    featured_nft["item_image_url"] = self.get_value(
                        item, "image_url")
                    featured_nft["item_contract_address"] = self.get_value(
                        item, "contract_addr")
                    featured_nft["item_collection_name"] = self.get_value(
                        item, "collection_name")

                    featured_nft_list.append(featured_nft)

                    scraped_count += 1

                offset += limit_per_page

        return featured_nft_list

    def get_whales_smart_money(self,
                               action: list = [],
                               price_range: int = "",
                               limit_per_page: int = None,
                               limit: int = None,
                               proxy_lum: dict = None) -> list:
        FEATURE = "Smart+Money"

        return self.__get_featured_nft(feature=FEATURE,
                                       action=action,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

