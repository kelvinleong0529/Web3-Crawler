from .utility import utility_cass


class gamefi_scraper(utility_cass):

    def __init__(self) -> None:
        super().__init__()

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        return super().get_value(input_dict, key)

    # function to filter GameFi tokens by category(s), reference website: https://v2.gamefi.org/
    def search_by_category(self,
                           category: list,
                           limit: int = None,
                           proxy_dict: dict = None) -> list:

        # validate the input parameters
        if not super().is_list(category):
            raise TypeError("Category argument should be LIST type")
        category_string = super().list_to_str(category)
        limit = super().validate_limit(limit)

        # create a list to store the details
        token_detail_list = []

        # variables for scraping
        finished_scraping = False
        page_index = 1
        scraped_count = 1

        while not finished_scraping:

            # make GET request to the API endpoint
            api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}&page={page_index}".format(
                category=category_string, page_index=page_index)
            is_success, response = super().get_url_response(
                url=api, proxy_dict=proxy_dict)

            if is_success:

                # get the total number of pages
                lastPage = response["pageProps"]["data"]["lastPage"]
                data = response["pageProps"]["data"]["data"]

                # if the data is empty, meaning no search results is associated with the category
                if not data:
                    finished_scraping = True
                    continue

                for index, token_iterator in enumerate(data):

                    if scraped_count > limit:
                        finished_scraping = True
                        break

                    # create a dict to store the details
                    token = {}

                    # gamefi token details
                    token["game_name"] = self.__get_value(
                        token_iterator, "game_name")
                    token["verified"] = self.__get_value(
                        token_iterator, "verified")
                    token["network"] = self.__get_value(
                        token_iterator, "network_available")
                    token["address"] = self.__get_value(
                        token_iterator, "token_address")
                    token["category"] = self.__get_value(
                        token_iterator, "category")
                    token["developer"] = self.__get_value(
                        token_iterator, "developer")
                    token["language"] = self.__get_value(
                        token_iterator, "language")
                    token["hashtags"] = self.__get_value(
                        token_iterator, "hashtags")
                    token["description"] = self.__get_value(
                        token_iterator, "short_description")

                    # gamefi token IGO info
                    token["ido_date"] = self.__get_value(
                        token_iterator, "ido_date")
                    token["ido_type"] = self.__get_value(
                        token_iterator, "ido_type")
                    token["ido_link"] = self.__get_value(
                        token_iterator, "gamefi_ido_link")
                    token["igo_price"] = self.__get_value(
                        token_iterator, "token_price")
                    token["igo_roi"] = self.__get_value(token_iterator, "roi")

                    # gamefi token pricing info
                    token["price"] = self.__get_value(token_iterator, "price")
                    token["price_change_24h"] = self.__get_value(
                        token_iterator, "price_change_24h")
                    token["price_change_7d"] = self.__get_value(
                        token_iterator, "price_change_7d")
                    token["volume_24h"] = self.__get_value(
                        token_iterator, "volume_24h")
                    token["market_cap"] = self.__get_value(
                        token_iterator, "market_cap")

                    # gamefi important links and URL
                    token["official_website_link"] = self.__get_value(
                        token_iterator, "official_website")
                    token["web_game_link"] = self.__get_value(
                        token_iterator, "web_game_link")
                    token["android_link"] = self.__get_value(
                        token_iterator, "android_link")
                    token["ios_link"] = self.__get_value(
                        token_iterator, "ios_link")
                    token["game_pc_link"] = self.__get_value(
                        token_iterator, "game_pc_link")

                    # gamefi token social media info
                    token["twitter"] = self.__get_value(
                        token_iterator, "twitter_link")
                    token["medium"] = self.__get_value(token_iterator,
                                                       "medium_link")
                    token["discord"] = self.__get_value(
                        token_iterator, "discord_link")
                    token["telegram"] = self.__get_value(
                        token_iterator, "official_telegram_link")

                    # gamefi Coin Market Cap info
                    token["cmc_id"] = self.__get_value(token_iterator,
                                                       "cmc_id")
                    token["cmc_slug"] = self.__get_value(
                        token_iterator, "coinmarketcap_slug")
                    token["cmc_rank"] = self.__get_value(
                        token_iterator, "cmc_rank")

                    token_detail_list.append(token)

                    scraped_count += 1

                if page_index == lastPage:
                    finished_scraping = True
                else:
                    page_index += 1

        return token_detail_list