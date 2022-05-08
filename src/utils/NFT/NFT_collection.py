import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_collection_base_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.base_api = "https://api.nftbase.com/web/api/v1/collection/{feature}?collection_id={{collection_id}}&limit={{limit_per_page}}&offset={{offset}}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)


class NFT_scraper_collection_activity(NFT_scraper_collection_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.base_api.format(feature="activities")
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
                    collection_activity["timestamp"] = super(
                    ).utc_from_timestamp(
                        self.get_value(collection_activities, "timestamp"))

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


class NFT_scraper_collection_detail(NFT_scraper_collection_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.__api = self.base_api.format(feature="detail")
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


class NFT_scraper_collection_asset(NFT_scraper_collection_base_class):

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
                edges = response.json()["data"]["edges"]

                # if the response returns blank or empty data, break the loop
                if not edges:
                    finished_scraping = True
                    continue

                for edge in edges:

                    asset = edge["node"]["asset"]

                    collection_asset = {}

                    # collection asset details
                    collection_asset["name"] = self.get_value(asset, "name")
                    collection_asset["image_url"] = self.get_value(
                        asset, "imageUrl")
                    collection_asset["is_delisted"] = self.get_value(
                        asset, "isDelisted")
                    collection_asset["is_frozen"] = self.get_value(
                        asset, "isFrozen")

                    # collection asset transaction details
                    order_data = self.get_value(asset, "orderData")
                    best_ask = self.get_value(order_data, "bestAsk")
                    maker = self.get_value(best_ask, "maker")
                    payment_asset_quantity = self.get_value(
                        best_ask, "paymentAssetQuantity")
                    payment_asset_details = self.get_value(
                        payment_asset_quantity, "asset")

                    # collection asset transaction details
                    collection_asset["opened_timestamp"] = self.get_value(
                        best_ask, "openedAt")
                    collection_asset["order_type"] = self.get_value(
                        best_ask, "orderType")
                    collection_asset["purchased_timestamp"] = self.get_value(
                        best_ask, "closedAt")
                    collection_asset["buyer_address"] = self.get_value(
                        maker, "address")
                    collection_asset["buying_price"] = self.get_value(
                        payment_asset_details, "usdSpotPrice")

                    self.__collection_asset_list.append(collection_asset)

            offset += limit_per_page

        return self.__collection_asset_list


class NFT_scraper_collection_holder(NFT_scraper_collection_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.base_api.format(feature="holders")
        self.__collection_holders_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_collection_holder(self,
                              collection_id: str,
                              limit_per_page: int = 20,
                              limit: int = 50) -> list:

        # empty the return activity list
        self.__collection_holders_list.clear()

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

                for users in data:

                    user = users["user"]

                    collection_holder = {}

                    # collection holder details
                    collection_holder["name"] = self.get_value(user, "name")
                    collection_holder["id"] = self.get_value(user, "id")
                    collection_holder["address"] = self.get_value(
                        user, "address")
                    collection_holder["avatar_url"] = self.get_value(
                        user, "avatar_url")
                    collection_holder["count"] = self.get_value(users, "Count")
                    collection_holder["is_whale"] = self.get_value(
                        users, "is_whale")

                    self.__collection_holders_list.append(collection_holder)

            offset += limit_per_page

        return self.__collection_holders_list


class NFT_scraper_collection_class(NFT_scraper_collection_activity,
                                   NFT_scraper_collection_detail,
                                   NFT_scraper_collection_asset,
                                   NFT_scraper_collection_holder):

    def __init__(self) -> None:
        super().__init__()