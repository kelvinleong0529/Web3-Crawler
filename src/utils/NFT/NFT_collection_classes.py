import requests
import datetime

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_collection_activity(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/collection/activities?collection_id={collection_id}&limit={limit_per_page}&offset={offset}"
        self.__collection_activity_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    # function to get NFT most recent transaction details, refernce website: https://www.nftexplorer.app/
    def get_collection_activity(self,
                                collection_id: str,
                                limit_per_page: int = 20,
                                limit: int = 50) -> list:

        # empty the return activity list
        self.__collection_activity_list.clear()

        # variables for scraping
        finished_scraping = False
        offset = 0

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(collection_id=collection_id,
                                    limit_per_page=limit_per_page)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for collection_activities in data:
                    # initialize a dict to store the details
                    collection_activity = {}

                    # transaction details
                    collection_activity["transaction_price"] = self.get_value(
                        collection_activities, "price")
                    collection_activity[
                        "transaction_currency"] = self.get_value(
                            collection_activities, "symbol")
                    collection_activity["action"] = self.get_value(
                        collection_activities, "action")
                    collection_activity["timestamp"] = self.get_value(
                        collection_activities, "timestamp")
                    if collection_activity["timestamp"] != "N/A":
                        collection_activity[
                            "timestamp"] = datetime.datetime.utcfromtimestamp(
                                int(collection_activity["timestamp"])
                            ).strftime('%Y-%m-%d %H:%M:%S')

                    # NFT details
                    item_details = self.get_value(collection_activities,
                                                  "item")
                    collection_activity["nft_id"] = self.get_value(
                        item_details, "token_id")
                    collection_activity["nft_address"] = self.get_value(
                        item_details, "contract_addr")
                    collection_activity["nft_url"] = self.get_value(
                        item_details, "image_url")
                    collection_activity["nft_rarity_rank"] = self.get_value(
                        item_details, "rarity_rank")

                    # buyer details
                    buyer = self.get_value(collection_activities, "to")
                    collection_activity["buyer_name"] = self.get_value(
                        buyer, "name")
                    collection_activity["buyer_address"] = self.get_value(
                        buyer, "address")
                    collection_activity["buyer_is_whale"] = self.get_value(
                        buyer, "is_whale")

                    # seller details
                    seller = self.get_value(collection_activities, "to")
                    collection_activity["seller_name"] = self.get_value(
                        seller, "name")
                    collection_activity["seller_address"] = self.get_value(
                        seller, "address")
                    collection_activity["seller_is_whale"] = self.get_value(
                        seller, "is_whale")

                    self.__collection_activity_list.append(collection_activity)

                offset += limit_per_page

        return self.__collection_activity_list


class NFT_scraper_collection_detail(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/collection/detail?collection_id={collection_id}"
        self.__collection_details = {}

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    # function to get NFT most recent transaction details, refernce website: https://www.nftexplorer.app/
    def get_collection_detail(self, collection_id: str) -> dict:

        # empty the return activity list
        self.__collection_details.clear()

        # make GET request to the API endpoint
        api = self.__api.format(collection_id=collection_id)
        response = requests.get(api)

        # if the request is successful
        if str(response.status_code) == "200":
            data = response.json()["data"]

            # collection basic details
            self.__collection_details["id"] = self.get_value(data, "id")
            self.__collection_details["name"] = self.get_value(data, "name")
            self.__collection_details["image_url"] = self.get_value(
                data, "image_url")
            self.__collection_details["banner_image_url"] = self.get_value(
                data, "banner_image_url")
            self.__collection_details["description"] = self.get_value(
                data, "description")

            # collection social media details
            self.__collection_details["twitter_url"] = self.get_value(
                data, "twitter_url")
            self.__collection_details["instagram_url"] = self.get_value(
                data, "instagram_url")
            self.__collection_details["external_url"] = self.get_value(
                data, "external_url")
            self.__collection_details["discord_url"] = self.get_value(
                data, "discord_url")
            self.__collection_details["open_sea_url"] = self.get_value(
                data, "open_sea_url")

            # collection item details
            self.__collection_details["item_count"] = self.get_value(
                data, "item_count")
            self.__collection_details["owner_count"] = self.get_value(
                data, "owner_count")

            # collection trading / transaction details
            self.__collection_details["volume_in_24h"] = self.get_value(
                data, "volume_in_24h")
            self.__collection_details["floor_price"] = self.get_value(
                data, "floor_price")
            self.__collection_details["mint_price"] = self.get_value(
                data, "mint_price")
            self.__collection_details["blue_index"] = self.get_value(
                data, "blue_index")

        return self.__collection_details


class NFT_scraper_collection_asset(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/graph/asset/search?collection_id={collection_id}&offset={offset}&limit={limit_per_page}"
        self.__collection_asset_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_collection_asset(self,
                             collection_id: str,
                             limit_per_page: int = 20,
                             limit: int = 50) -> list:

        # empty the return activity list
        self.__collection_asset_list.clear()

        # variables for scraping
        finished_scraping = False
        offset = 0

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(collection_id=collection_id,
                                    limit_per_page=limit_per_page,
                                    offset=offset)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                collection_asset = {}

                # collection basic details
                collection_asset["id"] = self.get_value(data, "id")
                collection_asset["name"] = self.get_value(data, "name")
                collection_asset["image_url"] = self.get_value(
                    data, "image_url")
                collection_asset["banner_image_url"] = self.get_value(
                    data, "banner_image_url")
                collection_asset["description"] = self.get_value(
                    data, "description")

                # collection social media details
                collection_asset["twitter_url"] = self.get_value(
                    data, "twitter_url")
                collection_asset["instagram_url"] = self.get_value(
                    data, "instagram_url")
                collection_asset["external_url"] = self.get_value(
                    data, "external_url")
                collection_asset["discord_url"] = self.get_value(
                    data, "discord_url")
                collection_asset["open_sea_url"] = self.get_value(
                    data, "open_sea_url")

                # collection item details
                collection_asset["item_count"] = self.get_value(
                    data, "item_count")
                collection_asset["owner_count"] = self.get_value(
                    data, "owner_count")

                # collection trading / transaction details
                collection_asset["volume_in_24h"] = self.get_value(
                    data, "volume_in_24h")
                collection_asset["floor_price"] = self.get_value(
                    data, "floor_price")
                collection_asset["mint_price"] = self.get_value(
                    data, "mint_price")
                collection_asset["blue_index"] = self.get_value(
                    data, "blue_index")

        return self.__collection_asset_list


class NFT_scraper_collection_class(NFT_scraper_collection_activity,
                                   NFT_scraper_collection_detail):

    def __init__(self) -> None:
        super().__init__()

    def get_collection_activity(self,
                                collection_id: str,
                                limit: int = 20) -> list:
        return super().get_collection_activity(collection_id, limit)

    def get_collection_detail(self, collection_id: str) -> dict:
        return super().get_collection_detail(collection_id)