import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_whale_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__whales_api = "https://api.nftbase.com/web/api/v1/home/list-v3?home_tab={feature}&action={action_list}&price={price_range}&offset={offset}&limit={limit_per_page}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    # function to validate the "price_range" input parameter
    def __validate_price_range(self, price_range: int) -> str:
        if super().is_none(price_range):
            return ""
        if not super().is_int(price_range):
            raise TypeError("price_range argument must be a INTEGER type")
        return super().int_to_str(price_range)

    # function to scrape the nfts based on the input feature
    def __get_featured_nft(self, feature: str, action_list: list,
                           price_range: int, limit_per_page: int, limit: int,
                           proxy_lum: dict) -> list:

        featured_nft_list = []

        # validate the input parameters
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        if not super().is_list(action_list):
            raise TypeError("action_list argument must be LIST type")
        action_list = super().strip_and_capitalize_list(
            target_list=action_list)
        # check the action list to see if it's valid
        super().validate_action_list(input=action_list)
        action_list = super().list_to_str(input=action_list)

        price_range = self.__validate_price_range(price_range=price_range)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__whales_api.format(feature=feature,
                                           action_list=action_list,
                                           price_range=price_range,
                                           offset=offset,
                                           limit_per_page=limit_per_page)
            response = requests.get(url=api, proxies=proxy_lum)

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

                    # create a dict to store the details
                    featured_nft = {}

                    # featured nft basic details
                    featured_nft["id"] = self.get_value(nfts, "id")
                    featured_nft["token_id"] = self.get_value(nfts, "token_id")
                    price = self.get_value(nfts, "price")
                    currency = self.get_value(nfts, "symbol")
                    featured_nft["price"] = price + " " + currency
                    featured_nft["action"] = self.get_value(nfts, "action")
                    featured_nft["timestamp"] = super().timestamp_to_utc(
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
                        nfts, "collection_name")

                    featured_nft_list.append(featured_nft)

                    scraped_count += 1

                offset += limit_per_page

        return featured_nft_list

    def get_whales_smart_money(self,
                               action_list: list = None,
                               price_range: int = None,
                               limit_per_page: int = None,
                               limit: int = None,
                               proxy_lum: dict = None) -> list:
        FEATURE = "Smart+Money"

        return self.__get_featured_nft(feature=FEATURE,
                                       action_list=action_list,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_whales_famous(self,
                          action_list: list = None,
                          price_range: int = None,
                          limit_per_page: int = None,
                          limit: int = None,
                          proxy_lum: dict = None) -> list:
        FEATURE = "Famous"

        return self.__get_featured_nft(feature=FEATURE,
                                       action_list=action_list,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_whales_art_blocks(self,
                              action_list: list = None,
                              price_range: int = None,
                              limit_per_page: int = None,
                              limit: int = None,
                              proxy_lum: dict = None) -> list:
        FEATURE = "Art+Blocks"

        return self.__get_featured_nft(feature=FEATURE,
                                       action_list=action_list,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_whales_bored_ape_yacht_club(self,
                                        action_list: list = None,
                                        price_range: int = None,
                                        limit_per_page: int = None,
                                        limit: int = None,
                                        proxy_lum: dict = None) -> list:
        FEATURE = "BoredApeYachtClub"

        return self.__get_featured_nft(feature=FEATURE,
                                       action_list=action_list,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_whales_crypto_punks(self,
                                action_list: list = None,
                                price_range: int = None,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_lum: dict = None) -> list:
        FEATURE = "CryptoPunks"

        return self.__get_featured_nft(feature=FEATURE,
                                       action_list=action_list,
                                       price_range=price_range,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)
