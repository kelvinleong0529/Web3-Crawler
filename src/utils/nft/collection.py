from .validation import Validation


class CollectionBaseClass(Validation):

    collection_api = "https://api.nftbase.com/web/api/v1/collection/{feature}?collection_id={collection_id}&limit={limit_per_page}&offset={offset}"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def validate_collection_id(cls, collection_id: str) -> None:
        """ validate the collection_id
        """
        if not super().is_str(collection_id):
            raise TypeError("collection_id argument must be STRING type")


class CollectionActivity(CollectionBaseClass):

    __FEATURE = "activities"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_collection_activity(cls,
                                collection_id: str,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        collection_activity_list = []

        # validate the input parameters
        super().validate_collection_id(collection_id)
        limit_per_page = super().validate_limit_per_page(limit_per_page)
        limit = super().validate_limit(limit)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = cls.collection_api.format(feature=cls.__FEATURE,
                                            collection_id=collection_id,
                                            limit_per_page=limit_per_page,
                                            offset=offset)
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_success:
                data = response["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for collection_activities in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
                    collection_activity = {}

                    # transaction details
                    collection_activity["transaction_price"] = super(
                    ).get_value(collection_activities, "price")
                    collection_activity["transaction_currency"] = super(
                    ).get_value(collection_activities, "symbol")
                    collection_activity["action"] = super().get_value(
                        collection_activities, "action")
                    collection_activity["timestamp"] = super(
                    ).timestamp_to_utc(super().get_value(
                        collection_activities, "timestamp"))

                    # NFT details
                    item_details = super().get_value(collection_activities,
                                                     "item")
                    collection_activity["nft_id"] = super().get_value(
                        item_details, "token_id")
                    collection_activity["nft_address"] = super().get_value(
                        item_details, "contract_addr")
                    collection_activity["nft_url"] = super().get_value(
                        item_details, "image_url")
                    collection_activity["nft_rarity_rank"] = super().get_value(
                        item_details, "rarity_rank")

                    # buyer details
                    buyer = super().get_value(collection_activities, "to")
                    collection_activity["buyer_name"] = super().get_value(
                        buyer, "name")
                    collection_activity["buyer_address"] = super().get_value(
                        buyer, "address")
                    collection_activity["buyer_is_whale"] = super().get_value(
                        buyer, "is_whale")

                    # seller details
                    seller = super().get_value(collection_activities, "to")
                    collection_activity["seller_name"] = super().get_value(
                        seller, "name")
                    collection_activity["seller_address"] = super().get_value(
                        seller, "address")
                    collection_activity["seller_is_whale"] = super().get_value(
                        seller, "is_whale")

                    collection_activity_list.append(collection_activity)

                    scraped_count += 1

                offset += limit_per_page

        return collection_activity_list


class CollectionAsset(CollectionBaseClass):

    __api = "https://api.nftbase.com/web/api/v1/graph/asset/search?collection_id={collection_id}&offset={offset}&limit={limit_per_page}"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_collection_asset(cls,
                             collection_id: str,
                             limit_per_page: int = None,
                             limit: int = None,
                             proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        collection_asset_list = []

        # validate the input parameters
        super().validate_collection_id(collection_id)
        limit_per_page = super().validate_limit_per_page(limit_per_page)
        limit = super().validate_limit(limit)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = cls.__api.format(collection_id=collection_id,
                                   limit_per_page=limit_per_page,
                                   offset=offset)
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_success:
                edges = response["data"]["edges"]

                # if the response returns blank or empty data, break the loop
                if not edges:
                    finished_scraping = True
                    continue

                for edge in edges:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
                    collection_asset = {}

                    asset = edge["node"]["asset"]

                    # collection asset details
                    collection_asset["name"] = super().get_value(asset, "name")
                    collection_asset["image_url"] = super().get_value(
                        asset, "imageUrl")
                    collection_asset["is_delisted"] = super().get_value(
                        asset, "isDelisted")
                    collection_asset["is_frozen"] = super().get_value(
                        asset, "isFrozen")

                    # collection asset transaction details
                    order_data = super().get_value(asset, "orderData")
                    best_ask = super().get_value(order_data, "bestAsk")
                    maker = super().get_value(best_ask, "maker")
                    payment_asset_quantity = super().get_value(
                        best_ask, "paymentAssetQuantity")
                    payment_asset_details = super().get_value(
                        payment_asset_quantity, "asset")

                    # collection asset transaction details
                    collection_asset["opened_timestamp"] = super().get_value(
                        best_ask, "openedAt")
                    collection_asset["order_type"] = super().get_value(
                        best_ask, "orderType")
                    collection_asset["purchased_timestamp"] = super(
                    ).get_value(best_ask, "closedAt")
                    collection_asset["buyer_address"] = super().get_value(
                        maker, "address")
                    collection_asset["buying_price"] = super().get_value(
                        payment_asset_details, "usdSpotPrice")

                    collection_asset_list.append(collection_asset)

                    scraped_count += 1

                offset += limit_per_page

        return collection_asset_list


class CollectionDetail(CollectionBaseClass):

    __api = "https://api.nftbase.com/web/api/v1/collection/detail?collection_id={collection_id}"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_value(cls, input_dict: dict, key: str) -> dict | list | str:
        return CollectionBaseClass.get_value(input_dict, key)

    # function to get NFT most recent transaction details, refernce website: https://www.nftexplorer.app/
    def get_collection_detail(self,
                              collection_id: str,
                              proxy_dict: dict = None) -> dict:

        # create a list to store the scrape results
        collection_details = {}

        # validate the input parameters
        super().validate_collection_id(collection_id)

        # make GET request to the API endpoint
        api = self.__api.format(collection_id=collection_id)
        is_success, response = super().get_url_response(url=api,
                                                        proxy_dict=proxy_dict)

        # if the request is successful
        if is_success:
            data = response["data"]

            # collection basic details
            collection_details["id"] = super().get_value(data, "id")
            collection_details["name"] = super().get_value(data, "name")
            collection_details["image_url"] = super().get_value(
                data, "image_url")
            collection_details["banner_image_url"] = super().get_value(
                data, "banner_image_url")
            collection_details["description"] = super().get_value(
                data, "description")

            # collection social media details
            collection_details["twitter_url"] = super().get_value(
                data, "twitter_url")
            collection_details["instagram_url"] = super().get_value(
                data, "instagram_url")
            collection_details["external_url"] = super().get_value(
                data, "external_url")
            collection_details["discord_url"] = super().get_value(
                data, "discord_url")
            collection_details["open_sea_url"] = super().get_value(
                data, "open_sea_url")

            # collection item details
            collection_details["item_count"] = super().get_value(
                data, "item_count")
            collection_details["owner_count"] = super().get_value(
                data, "owner_count")

            # collection trading / transaction details
            collection_details["volume_in_24h"] = super().get_value(
                data, "volume_in_24h")
            collection_details["floor_price"] = super().get_value(
                data, "floor_price")
            collection_details["mint_price"] = super().get_value(
                data, "mint_price")
            collection_details["blue_index"] = super().get_value(
                data, "blue_index")

        return collection_details


class CollectionHolder(CollectionBaseClass):

    __FEATURE = "holders"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_collection_holder(cls,
                              collection_id: str,
                              limit_per_page: int = None,
                              limit: int = None,
                              proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        collection_holders_list = []

        # validate the input parameters
        super().validate_collection_id(collection_id)
        limit_per_page = super().validate_limit_per_page(limit_per_page)
        limit = super().validate_limit(limit)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = cls.collection_api.format(feature=cls.__FEATURE,
                                            collection_id=collection_id,
                                            limit_per_page=limit_per_page,
                                            offset=offset)
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_success:
                data = response["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for users in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the scraped results
                    collection_holder = {}

                    # collection holder details
                    user = users["user"]
                    collection_holder["name"] = super().get_value(user, "name")
                    collection_holder["id"] = super().get_value(user, "id")
                    collection_holder["address"] = super().get_value(
                        user, "address")
                    collection_holder["avatar_url"] = super().get_value(
                        user, "avatar_url")
                    collection_holder["count"] = super().get_value(
                        users, "Count")
                    collection_holder["is_whale"] = super().get_value(
                        users, "is_whale")

                    collection_holders_list.append(collection_holder)

                    scraped_count += 1

                offset += limit_per_page

        return collection_holders_list


class Collection(CollectionActivity, CollectionAsset, CollectionDetail,
                 CollectionHolder):

    def __init__(self) -> None:
        super().__init__()
