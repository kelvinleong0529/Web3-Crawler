import requests
import datetime

from NFT_scraper_base_class import NFT_scraper_base_class

class NFT_scraper_user_details(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__get_user_id_api = "https://api.nftbase.com/web/api/v1/user/info/address?address={address}"
        self.__user_details = {}

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_id(self, user_address: str) -> str:
        api = self.__get_user_id_api.format(address=user_address)
        user_id = None
        response = requests.get(api)
        if str(response.status_code) == "200":
            user_id = response.json()["data"]["id"]
        return user_id

    def get_user_details(self, user_address: str) -> dict:

        # reset the dictionary
        self.__user_details.clear()

        api = self.__get_user_id_api.format(address=user_address)
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


class NFT_scraper_user_gallery(NFT_scraper_user_details):

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

                for user_galleries in data:
                    # initialize a dict to store the details
                    user_gallery = {}

                    # NFT gallery details
                    user_gallery["id"] = self.get_value(user_galleries, "id")
                    user_gallery["image_url"] = self.get_value(
                        user_galleries, "image_url")
                    user_gallery["token_id"] = self.get_value(
                        user_galleries, "token_id")
                    user_gallery["contract_addr"] = self.get_value(
                        user_galleries, "contract_addr")
                    user_gallery["has_watched"] = self.get_value(
                        user_galleries, "has_watched")
                    price = self.get_value(user_galleries, "price")
                    currency = self.get_value(user_galleries, "symbol")
                    user_gallery["price"] = price + " " + currency
                    user_gallery["collection_name"] = self.get_value(
                        user_galleries, "collection_name")

                    # append the result into the list and increment the offset value by 1
                    self.__user_gallery_list.append(user_gallery)
                    offset += 1

        self.__user_gallery_list = super().remove_duplicate(
            self.__user_gallery_list)
        return self.__user_gallery_list


class NFT_scraper_user_collection(NFT_scraper_user_details):

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

                for user_collections in data:
                    # initialize a dict to store the details
                    user_base_collection = {}

                    # NFT collection details
                    user_base_collection["collection_name"] = self.get_value(
                        user_collections, "collection_name")
                    user_base_collection["collection_id"] = self.get_value(
                        user_collections, "collection_id")
                    user_base_collection[
                        "collection_image_url"] = self.get_value(
                            user_collections, "collection_image_url")
                    user_base_collection["count"] = self.get_value(
                        user_collections, "count")
                    user_base_collection["change_in_24h"] = self.get_value(
                        user_collections, "change_in_24h")

                    items = self.get_value(user_collections, "items")
                    for item in items:
                        # make a copy of the base collection
                        user_collection = user_base_collection.copy()
                        user_collection["id"] = self.get_value(item, "id")
                        user_collection["image_url"] = self.get_value(
                            item, "image_url")
                        user_collection["token_id"] = self.get_value(
                            item, "token_id")
                        user_collection["contract_addr"] = self.get_value(
                            item, "contract_addr")
                        user_collection["has_watched"] = self.get_value(
                            item, "has_watched")
                        user_collection["rarity_rank"] = self.get_value(
                            item, "rarity_rank")
                        price = self.get_value(item, "price")
                        currency = self.get_value(item, "symbol")
                        user_collection["price"] = price + " " + currency

                        # append the result into the list and increment the offset value by 1
                        self.__user_collection_list.append(user_collection)

                    offset += 1

        self.__user_collection_list = super().remove_duplicate(
            self.__user_collection_list)
        return self.__user_collection_list


class NFT_scraper_user_activity(NFT_scraper_user_details):

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

                for user_activities in data:
                    # initialize a dict to store the details
                    user_activity = {}

                    # NFT activity target user (BUY from or SELL to)
                    target = self.get_value(user_activities, "from_or_to")
                    user_activity["target_user_id"] = self.get_value(
                        target, "id")
                    user_activity["target_user_name"] = self.get_value(
                        target, "name")
                    user_activity["target_user_address"] = self.get_value(
                        target, "address")
                    user_activity["target_user_avatar_url"] = self.get_value(
                        target, "avater_url")

                    # NFT activity details
                    user_activity["action"] = self.get_value(
                        user_activities, "action")
                    user_activity["id"] = self.get_value(user_activities, "id")
                    user_activity["token_id"] = self.get_value(
                        user_activities, "token_id")
                    user_activity["timestamp"] = self.get_value(
                        user_activities, "timestamp")
                    if user_activity["timestamp"] != "N/A":
                        user_activity[
                            "timestamp"] = datetime.datetime.utcfromtimestamp(
                                int(user_activity["timestamp"])).strftime(
                                    '%Y-%m-%d %H:%M:%S')
                    price = self.get_value(user_activities, "price")
                    currency = self.get_value(user_activities, "symbol")
                    user_activity["price"] = price + " " + currency

                    # NFT item details
                    item = self.get_value(user_activities, "item")
                    user_activity["nft_id"] = self.get_value(item, "id")
                    user_activity["nft_image_url"] = self.get_value(
                        item, "image_url")
                    user_activity["nft_contract_addreess"] = self.get_value(
                        item, "contract_addr")
                    user_activity["collection_name"] = self.get_value(
                        user_activities, "collection_name")

                    # append the result into the list and increment the offset value by 1
                    self.__user_activity_list.append(user_activity)

                    offset += 1

        self.__user_activity_list = super().remove_duplicate(
            self.__user_activity_list)
        return self.__user_activity_list


class NFT_scraper_user_class(NFT_scraper_user_collection,
                             NFT_scraper_user_gallery,
                             NFT_scraper_user_activity):

    def __init__(self) -> None:
        super().__init__()

    def get_user_details(self, user_address: str) -> dict:
        return super().get_user_details(user_address)

    def get_user_gallery(self, user_address: str, limit: int = 20) -> list:
        return super().get_user_gallery(user_address, limit)

    def get_user_collection(self, user_address: str, limit: int = 20) -> list:
        return super().get_user_collection(user_address, limit)

    def get_user_activity(self, user_address: str, limit: int = 20) -> list:
        return super().get_user_activity(user_address, limit)


