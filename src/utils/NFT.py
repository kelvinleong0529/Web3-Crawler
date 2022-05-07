import requests
import datetime


class NFT_scraper_base_class:

    def __init__(self) -> None:
        pass

    def get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    def remove_duplicate(self, target_list: list):
        return [dict(t) for t in {tuple(d.items()) for d in target_list}]


class NFT_scraper_get_user_details(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__get_user_id_api = "https://api.nftbase.com/web/api/v1/user/info/address?address={address}"
        self.__user_details = {}

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_id(self, address: str) -> str:
        api = self.__get_user_id_api.format(address=address)
        user_id = None
        response = requests.get(api)
        if str(response.status_code) == "200":
            user_id = response.json()["data"]["id"]
        return user_id

    def get_user_details(self, address: str) -> dict:

        # reset the dictionary
        self.__user_details.clear()

        api = self.__get_user_id_api.format(address=address)
        response = requests.get(api)
        if str(response.status_code) == "200":
            response = response.json()
            data = response["data"]
            self.__user_details["id"] = self.get_value(data, "id")
            self.__user_details["avatar_url"] = self.get_value(
                data, "avatar_url")
            self.__user_details["item_count"] = self.get_value(
                data, "item_count")
            self.__user_details["email"] = self.get_value(data, "email")
            self.__user_details["followers_count"] = self.get_value(
                data, "followers_count")
            self.__user_details["following_count"] = self.get_value(
                data, "following_count")
            self.__user_details["facebook_url"] = self.get_value(
                data, "facebook_url")
            self.__user_details["twitter_url"] = self.get_value(
                data, "twitter_url")
            self.__user_details["intro"] = self.get_value(data, "intro")
            self.__user_details["web_url"] = self.get_value(data, "web_url")
            self.__user_details["banner_image"] = self.get_value(
                data, "banner_image")

        return self.__user_details


class NFT_scraper_get_collection_activity(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/collection/activities?collection_id={collection_id}&limit={limit}"
        self.__collection_activity_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    # function to get NFT most recent transaction details, refernce website: https://www.nftexplorer.app/
    def get_collection_activity(self,
                                collection_id: str,
                                limit: int = 20) -> list:

        # convert the collection id to lowercase and remove all whitespaces
        collection_id = collection_id.lower().replace(" ", "")

        # make GET request to the API endpoint
        api = self.__api.format(collection_id=collection_id, limit=limit)
        response = requests.get(api)

        # empty the return activity list
        self.__collection_activity_list.clear()

        # if the request is successful
        if str(response.status_code) == "200":
            data = response.json()["data"]
            for activities in data:
                # initialize a dict to store the details
                activity = {}

                # transaction details
                activity["transaction_price"] = self.get_value(
                    activities, "price")
                activity["transaction_currency"] = self.get_value(
                    activities, "symbol")
                activity["action"] = self.get_value(activities, "action")
                activity["timestamp"] = self.get_value(activities, "timestamp")
                if activity["timestamp"] != "N/A":
                    activity["timestamp"] = datetime.datetime.utcfromtimestamp(
                        int(activity["timestamp"])).strftime(
                            '%Y-%m-%d %H:%M:%S')

                # NFT details
                item_details = self.get_value(activities, "item")
                activity["nft_id"] = self.get_value(item_details, "token_id")
                activity["nft_address"] = self.get_value(
                    item_details, "contract_addr")
                activity["nft_url"] = self.get_value(item_details, "image_url")
                activity["nft_rarity_rank"] = self.get_value(
                    item_details, "rarity_rank")

                # buyer details
                buyer = self.get_value(activities, "to")
                activity["buyer_name"] = self.get_value(buyer, "name")
                activity["buyer_address"] = self.get_value(buyer, "address")
                activity["buyer_is_whale"] = self.get_value(buyer, "is_whale")

                # seller details
                seller = self.get_value(activities, "to")
                activity["seller_name"] = self.get_value(seller, "name")
                activity["seller_address"] = self.get_value(seller, "address")
                activity["seller_is_whale"] = self.get_value(
                    seller, "is_whale")

                self.__collection_activity_list.append(activity)

        return self.__collection_activity_list


class NFT_scraper_get_user_gallery(NFT_scraper_get_user_details):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/user/gallery?user_id={user_id}&offset={offset}&limit={limit}"
        self.__user_gallery_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_gallery(self, user_address: str, limit: int = 20) -> list:

        # empty the return activity list
        self.__user_gallery_list.clear()

        # retrieve the user id from user address
        user_id = super().get_user_id(user_address)

        # variables for scraping
        finished_scraping = False
        offset = 0

        while not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit=limit)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for galleries in data:
                    # initialize a dict to store the details
                    gallery = {}

                    # NFT gallery details
                    gallery["id"] = self.get_value(galleries, "id")
                    gallery["image_url"] = self.get_value(
                        galleries, "image_url")
                    gallery["token_id"] = self.get_value(galleries, "token_id")
                    gallery["contract_addr"] = self.get_value(
                        galleries, "contract_addr")
                    gallery["has_watched"] = self.get_value(
                        galleries, "has_watched")
                    price = self.get_value(galleries, "price")
                    currency = self.get_value(galleries, "symbol")
                    gallery["price"] = price + " " + currency
                    gallery["collection_name"] = self.get_value(
                        galleries, "collection_name")

                    # append the result into the list and increment the offset value by 1
                    self.__user_gallery_list.append(gallery)
                    offset += 1

        self.__user_gallery_list = super().remove_duplicate(
            self.__user_gallery_list)
        return self.__user_gallery_list


class NFT_scraper_get_user_collection(NFT_scraper_get_user_details):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/user/collection?user_id={user_id}&offset={offset}&limit={limit}"
        self.__user_collection_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_collection(self, user_address: str, limit: int = 20) -> list:

        # empty the return activity list
        self.__user_collection_list.clear()

        # retrieve the user id from user address
        user_id = super().get_user_id(user_address)

        # variables for scraping
        finished_scraping = False
        offset = 0

        while not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit=limit)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for collections in data:
                    # initialize a dict to store the details
                    base_collection = {}

                    # NFT collection details
                    base_collection["collection_name"] = self.get_value(
                        collections, "collection_name")
                    base_collection["collection_id"] = self.get_value(
                        collections, "collection_id")
                    base_collection["collection_image_url"] = self.get_value(
                        collections, "collection_image_url")
                    base_collection["count"] = self.get_value(
                        collections, "count")
                    base_collection["change_in_24h"] = self.get_value(
                        collections, "change_in_24h")

                    items = self.get_value(collections, "items")
                    for item in items:
                        # make a copy of the base collection
                        collection = base_collection.copy()
                        collection["id"] = self.get_value(item, "id")
                        collection["image_url"] = self.get_value(
                            item, "image_url")
                        collection["token_id"] = self.get_value(
                            item, "token_id")
                        collection["contract_addr"] = self.get_value(
                            item, "contract_addr")
                        collection["has_watched"] = self.get_value(
                            item, "has_watched")
                        collection["rarity_rank"] = self.get_value(
                            item, "rarity_rank")
                        price = self.get_value(item, "price")
                        currency = self.get_value(item, "symbol")
                        collection["price"] = price + " " + currency

                        # append the result into the list and increment the offset value by 1
                        self.__user_collection_list.append(collection)

                    offset += 1

        self.__user_collection_list = super().remove_duplicate(
            self.__user_collection_list)
        return self.__user_collection_list


class NFT_scraper_get_user_activity(NFT_scraper_get_user_details):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/user/activities?user_id={user_id}&offset={offset}&limit={limit}"
        self.__user_activity_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_activity(self, user_address: str, limit: int = 20) -> list:

        # empty the return activity list
        self.__user_activity_list.clear()

        # retrieve the user id from user address
        user_id = super().get_user_id(user_address)

        # variables for scraping
        finished_scraping = False
        offset = 0

        while not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit=limit)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for activities in data:
                    # initialize a dict to store the details
                    activity = {}

                    # NFT activity target user (BUY from or SELL to)
                    target = self.get_value(activities, "from_or_to")
                    activity["target_user_id"] = self.get_value(target, "id")
                    activity["target_user_name"] = self.get_value(
                        target, "name")
                    activity["target_user_address"] = self.get_value(
                        target, "address")
                    activity["target_user_avatar_url"] = self.get_value(
                        target, "avater_url")

                    # NFT activity details
                    activity["action"] = self.get_value(activities, "action")
                    activity["id"] = self.get_value(activities, "id")
                    activity["token_id"] = self.get_value(
                        activities, "token_id")
                    activity["timestamp"] = self.get_value(
                        activities, "timestamp")
                    if activity["timestamp"] != "N/A":
                        activity[
                            "timestamp"] = datetime.datetime.utcfromtimestamp(
                                int(activity["timestamp"])).strftime(
                                    '%Y-%m-%d %H:%M:%S')
                    price = self.get_value(activities, "price")
                    currency = self.get_value(activities, "symbol")
                    activity["price"] = price + " " + currency

                    # NFT item details
                    item = self.get_value(activities, "item")
                    activity["nft_id"] = self.get_value(item, "id")
                    activity["nft_image_url"] = self.get_value(
                        item, "image_url")
                    activity["nft_contract_addreess"] = self.get_value(
                        item, "contract_addr")
                    activity["collection_name"] = self.get_value(
                        activities, "collection_name")

                    # append the result into the list and increment the offset value by 1
                    self.__user_activity_list.append(activity)

                    offset += 1

        self.__user_activity_list = super().remove_duplicate(
            self.__user_activity_list)
        return self.__user_activity_list


class NFT_scraper_get_user_details(NFT_scraper_get_user_collection,
                                   NFT_scraper_get_user_gallery):

    def __init__(self) -> None:
        super().__init__()

    def get_user_gallery(self, user_id: str, limit: int = 20) -> list:
        return super().get_user_gallery(user_id, limit)

    def get_user_collection(self, user_id: str, limit: int = 20) -> list:
        return super().get_user_collection(user_id, limit)


class NFT_scraper(NFT_scraper_get_activity, NFT_scraper_get_user_details):

    def __init__(self) -> None:
        super().__init__()

    def get_activity(self, collection_id: str, limit: int = 20) -> list:
        return super().get_activity(collection_id, limit)

    def get_user_gallery(self, user_id: str, limit: int = 20) -> list:
        return super().get_user_gallery(user_id, limit)

    def get_user_collection(self, user_id: str, limit: int = 20) -> list:
        return super().get_user_collection(user_id, limit)


my_NFT_scraper = NFT_scraper()
print(my_NFT_scraper.get_user_gallery(user_id=4337377))
print('------------------------------------------------------------')
print(my_NFT_scraper.get_user_collection(user_id=4337377))

# api = "https://api.nftbase.com/web/api/v1/user/gallery?user_id=4337377&offset=0&limit=30"
# response = requests.get(api)
# print(response.json())