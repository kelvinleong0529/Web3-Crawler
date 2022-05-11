from .validation import validation_class


class user_base_class(validation_class):

    def __init__(self) -> None:
        super().__init__()
        self.__user_details_api = "https://api.nftbase.com/web/api/v1/user/info/address?address={address}"
        self.user_api = "https://api.nftbase.com/web/api/v1/user/{feature}?user_id={{user_id}}&offset={{offset}}&limit={{limit_per_page}}"

    def validate_user_address(self, user_address: str) -> None:
        if not super().is_str(user_address):
            raise TypeError("user_address argument must be STRING type")

    def get_user_id_by_address(self, user_address: str,
                               proxy_dict: dict | None) -> str | None:
        """ retrieve user_id based on user_address, return "None" if failed to get
        """
        self.validate_user_address(user_address)

        api = self.__user_details_api.format(address=user_address)
        is_success, response = super().get_url_response(url=api,
                                                        proxy_dict=proxy_dict)
        if is_success:
            return response["data"]["id"]

        return None

    def get_user_details(self, user_address: str,
                         proxy_dict: dict | None) -> dict:
        """ retrieve user details based on user_address
        """
        self.validate_user_address(user_address)

        api = self.__user_details_api.format(address=user_address)
        is_success, response = super().get_url_response(url=api,
                                                        proxy_dict=proxy_dict)

        if is_success:

            # create a dicr to store the user details
            user_details = {}

            data = response["data"]

            user_details["id"] = self.get_value(data, "id")
            user_details["avatar_url"] = self.get_value(data, "avatar_url")
            user_details["item_count"] = self.get_value(data, "item_count")
            user_details["email"] = self.get_value(data, "email")
            user_details["followers_count"] = self.get_value(
                data, "followers_count")
            user_details["following_count"] = self.get_value(
                data, "following_count")
            user_details["facebook_url"] = self.get_value(data, "facebook_url")
            user_details["twitter_url"] = self.get_value(data, "twitter_url")
            user_details["intro"] = self.get_value(data, "intro")
            user_details["web_url"] = self.get_value(data, "web_url")
            user_details["banner_image"] = self.get_value(data, "banner_image")

            return user_details

        return {}


class user_gallery(user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="gallery") + "&sort={sort_option}"

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        return super().get_value(input_dict, key)

    def get_user_gallery(self,
                         user_address: str,
                         limit_per_page: int = None,
                         limit: int = None,
                         input_sort_option: str = "Market Cap",
                         proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        user_gallery_list = []

        # validate the input parameters
        sort_option = super().get_sort_option(sort_option=input_sort_option)
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address=user_address,
                                                 proxy_dict=proxy_dict)

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
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_success:
                data = response["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_galleries in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
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

                    # increment the scraped_count by 1
                    scraped_count += 1

                offset += limit_per_page

        user_gallery_list = super().remove_duplicate_in_dict_list(
            user_gallery_list)

        return user_gallery_list


class user_collection(user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="collection") + "&sort={sort_option}"

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        return super().get_value(input_dict, key)

    def get_user_collection(self,
                            user_address: str,
                            limit_per_page: int = None,
                            limit: int = None,
                            input_sort_option: str = "Market Cap",
                            proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        user_collection_list = []

        # validate the input parameters
        sort_option = super().get_sort_option(sort_option=input_sort_option)
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address=user_address,
                                                 proxy_dict=proxy_dict)

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
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_success:
                data = response["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_collections in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
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

        user_collection_list = super().remove_duplicate_in_dict_list(
            user_collection_list)
        return user_collection_list


class user_activity(user_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = self.user_api.format(
            feature="activities") + "&action={action_list}"

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        return super().get_value(input_dict, key)

    def get_user_activity(self,
                          user_address: str,
                          action_list: list = None,
                          limit_per_page: int = None,
                          limit: int = None,
                          proxy_dict: dict = None) -> list:

        # create a list to store the scrape results
        user_activity_list = []

        # validate the input parameters
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        # check the action list to see if it's valid
        super().validate_action_list(input=action_list)
        action_list = super().list_to_str(taget_list=action_list)

        # retrieve the user id from user address
        user_id = super().get_user_id_by_address(user_address=user_address,
                                                 proxy_dict=proxy_dict)

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
            is_sucess, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            # if the request is successful
            if is_sucess:
                data = response["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for user_activities in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
                    user_activity = {}

                    # NFT activity involved user (user who BUY from or SELL to)
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
                    user_activity["timestamp"] = super().timestamp_to_utc(
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

        user_activity_list = super().remove_duplicate_in_dict_list(
            user_activity_list)

        return user_activity_list


class user_class(user_collection, user_gallery, user_activity):

    def __init__(self) -> None:
        super().__init__()
