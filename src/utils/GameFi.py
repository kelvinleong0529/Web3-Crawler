import requests


class GameFi_scraper:

    def __init__(self) -> None:
        pass

    def __get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return str(input_dict[key]) if key in input_dict else "N/A"
        return "N/A"

    # function to filter GameFi tokens by category(s), reference website: https://v2.gamefi.org/
    def search_by_category(self, category: list) -> list:
        page_index = 1
        category = ",".join(category)
        token_detail_list = []
        finished_scraping = False
        while not finished_scraping:
            api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}&page={page_index}".format(
                category=category, page_index=page_index)
            response = requests.get(api)
            if str(response.status_code) == "200":

                # get the total number of pages
                lastPage = response.json()["pageProps"]["data"]["lastPage"]
                data = response.json()["pageProps"]["data"]["data"]

                # if the data is empty, meaning no search results is associated with the category
                if not len(data):
                    break
                for index, token_iterator in enumerate(data):
                    # initialize a dict to store the details
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

                if page_index == lastPage:
                    finished_scraping = True
                else:
                    page_index += 1

        return token_detail_list