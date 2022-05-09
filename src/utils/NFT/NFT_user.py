import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_user_base_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__user_details_api = "https://api.nftbase.com/web/api/v1/user/info/address?address={address}"
        self.user_api = "https://api.nftbase.com/web/api/v1/user/{feature}?user_id={{user_id}}&offset={{offset}}&limit={{limit_per_page}}"
        self.__user_details = {}

    def get_sort_option(self, sort_option: str) -> int:

        if not super().is_str(sort_option):
            raise TypeError("sort_option must be STRING type argument")

        # sort option list
        sort_option_list = ["market cap", "latest", "oldest"]

        # remove any trailing whitespaces and convert the string to lower case
        sort_option = sort_option.strip().lower()
        if sort_option not in sort_option_list:
            raise ValueError(
                "Sort option must be either one of these: [Market Cap, Latest, Oldest]"
            )
        return int(sort_option_list.index(sort_option)) + 1

    def get_user_id_by_address(self,
                               user_address: str,
                               proxy_lum: dict = None) -> str:

        if not super().is_str(user_address):
            raise TypeError("user_address argument must be a STRING type")

        api = self.__user_details_api.format(address=user_address)
        user_id = None
        response = requests.get(url=api, proxies=proxy_lum)
        if str(response.status_code) == "200":
            user_id = response.json()["data"]["id"]
        return user_id

    def get_user_details(self,
                         user_address: str,
                         proxy_lum: dict = None) -> dict:

        # reset the dictionary
        self.__user_details.clear()

        api = self.__user_details_api.format(address=user_address)
        response = requests.get(url=api, proxies=proxy_lum)
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


class NFT_scraper_user_gallery(NFT_scraper_user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="gallery") + "&sort={sort_option}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_gallery(self,
                         user_address: str,
                         limit_per_page: int = None,
                         limit: int = None,
                         sort_option: str = "Market Cap",
                         proxy_lum: dict = None) -> list:

        # instantiate a list to store the scrape results
        user_gallery_list = []

        # --------------------------------------------
        # validate the input parameters
        # --------------------------------------------
        # 1. sort_option
        sort_option = super().get_sort_option(sort_option=sort_option)
        # 2. limit_per_page
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        # 3. limit
        limit = super().validate_limit(limit=limit)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address=user_address,
                                                 proxy_lum=proxy_lum)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit_per_page=limit_per_page,
                                    sort_option=sort_option)
            response = requests.get(url=api, proxies=proxy_lum)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_galleries in data:

                    if scraped_count > limit:
                        break

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

                    # append the result into the list
                    user_gallery_list.append(user_gallery)

                    # increment the scraped count by 1
                    scraped_count += 1

                offset += limit_per_page

        if not super().is_list(user_gallery_list):
            raise TypeError("scraped user_gallery_list should be LIST type")
        user_gallery_list = super().remove_duplicate_in_dict_list(
            user_gallery_list)

        return user_gallery_list


class NFT_scraper_user_collection(NFT_scraper_user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="collection") + "&sort={sort_option}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_collection(self,
                            user_address: str,
                            limit_per_page: int = None,
                            limit: int = None,
                            sort_option: str = "Market Cap",
                            proxy_lum: dict = None) -> list:

        # instantiate a list to store the scrape results
        user_collection_list = []

        # validate the input parameters
        sort_option = super().get_sort_option(sort_option=sort_option)
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit_per_page=limit_per_page,
                                    sort_option=sort_option)
            response = requests.get(url=api, proxies=proxy_lum)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_collections in data:

                    if scraped_count > limit:
                        break

                    # initialize a dict to store the details
                    user_base_collection = {}

                    # NFT collection basic details
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

                        # NFT collection details
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
                        user_collection_list.append(user_collection)

                        scraped_count += 1

                offset += limit_per_page

        if not super().is_list(user_collection_list):
            raise TypeError("scraped user_collection_list should be LIST type")
        user_collection_list = super().remove_duplicate_in_dict_list(
            user_collection_list)
        return user_collection_list


class NFT_scraper_user_activity(NFT_scraper_user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="activities") + "&action={action_list}"

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_user_activity(self,
                          user_address: str,
                          action_list: list = None,
                          limit_per_page: int = None,
                          limit: int = None,
                          proxy_lum: dict = None) -> list:

        # instantiate a list to store the scrape results
        user_activity_list = []

        # validate the input parameters
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        if not super().is_list(action_list):
            raise TypeError("action_list argument must be LIST type")
        # check the action list to see if it's valid
        super().validate_action_list(input=action_list)
        action_list = super().list_to_str(taget_list=action_list)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(user_id=user_id,
                                    offset=offset,
                                    limit_per_page=limit_per_page,
                                    action_list=action_list)
            response = requests.get(url=api, proxies=proxy_lum)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_activities in data:

                    if scraped_count > limit:
                        break

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
                    user_activity["timestamp"] = super().utc_from_timestamp(
                        self.get_value(user_activities, "timestamp"))
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
                    user_activity_list.append(user_activity)

                    scraped_count += 1

                offset += limit_per_page

        if not super().is_list(user_activity_list):
            raise TypeError("scraped user_collection_list should be LIST type")
        user_activity_list = super().remove_duplicate_in_dict_list(
            user_activity_list)


class NFT_scraper_user_class(NFT_scraper_user_collection,
                             NFT_scraper_user_gallery,
                             NFT_scraper_user_activity):

    def __init__(self) -> None:
        super().__init__()