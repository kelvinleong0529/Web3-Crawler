from .utility import Utility


class GameFiScraper(Utility):

    __api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}&page={page_index}"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    # function to filter GameFi tokens by category(s), reference website: https://v2.gamefi.org/
    def search_by_category(cls,
                           category: list,
                           limit: int = None,
                           proxy_dict: dict = None) -> list:

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
            api = cls.__api.format(category=category_string,
                                   page_index=page_index)
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
                    token["game_name"] = super().get_value(
                        token_iterator, "game_name")
                    token["verified"] = super().get_value(
                        token_iterator, "verified")
                    token["network"] = super().get_value(
                        token_iterator, "network_available")
                    token["address"] = super().get_value(
                        token_iterator, "token_address")
                    token["category"] = super().get_value(
                        token_iterator, "category")
                    token["developer"] = super().get_value(
                        token_iterator, "developer")
                    token["language"] = super().get_value(
                        token_iterator, "language")
                    token["hashtags"] = super().get_value(
                        token_iterator, "hashtags")
                    token["description"] = super().get_value(
                        token_iterator, "short_description")

                    # gamefi token IGO info
                    token["ido_date"] = super().get_value(
                        token_iterator, "ido_date")
                    token["ido_type"] = super().get_value(
                        token_iterator, "ido_type")
                    token["ido_link"] = super().get_value(
                        token_iterator, "gamefi_ido_link")
                    token["igo_price"] = super().get_value(
                        token_iterator, "token_price")
                    token["igo_roi"] = super().get_value(token_iterator, "roi")

                    # gamefi token pricing info
                    token["price"] = super().get_value(token_iterator, "price")
                    token["price_change_24h"] = super().get_value(
                        token_iterator, "price_change_24h")
                    token["price_change_7d"] = super().get_value(
                        token_iterator, "price_change_7d")
                    token["volume_24h"] = super().get_value(
                        token_iterator, "volume_24h")
                    token["market_cap"] = super().get_value(
                        token_iterator, "market_cap")

                    # gamefi important links and URL
                    token["official_website_link"] = super().get_value(
                        token_iterator, "official_website")
                    token["web_game_link"] = super().get_value(
                        token_iterator, "web_game_link")
                    token["android_link"] = super().get_value(
                        token_iterator, "android_link")
                    token["ios_link"] = super().get_value(
                        token_iterator, "ios_link")
                    token["game_pc_link"] = super().get_value(
                        token_iterator, "game_pc_link")

                    # gamefi token social media info
                    token["twitter"] = super().get_value(
                        token_iterator, "twitter_link")
                    token["medium"] = super().get_value(
                        token_iterator, "medium_link")
                    token["discord"] = super().get_value(
                        token_iterator, "discord_link")
                    token["telegram"] = super().get_value(
                        token_iterator, "official_telegram_link")

                    # gamefi Coin Market Cap info
                    token["cmc_id"] = super().get_value(
                        token_iterator, "cmc_id")
                    token["cmc_slug"] = super().get_value(
                        token_iterator, "coinmarketcap_slug")
                    token["cmc_rank"] = super().get_value(
                        token_iterator, "cmc_rank")

                    token_detail_list.append(token)

                    scraped_count += 1

                if page_index == lastPage:
                    finished_scraping = True
                else:
                    page_index += 1

        return token_detail_list