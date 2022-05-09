import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_extra_feature_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.extra_features_api = "https://api.nftbase.com/web/api/v1/home/list?name={feature}&limit={limit_per_page}&offset={offset}"

    def __get_featured_nft(self, feature: str, limit_per_page: int, limit: int,
                           proxy_lum: dict) -> list:

        featured_nft_list = []

        # validate the input parameters
        limit_per_page = super().validate_limit_per_page(
            limit_per_page=limit_per_page)
        limit = super().validate_limit(limit=limit)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        # scraping parameters
        limit_per_page = limit_per_page if limit_per_page else self.LIMIT_PER_PAGE
        limit = limit if limit else self.LIMIT

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.extra_features_api.format(feature=feature,
                                                 limit_per_page=limit_per_page,
                                                 offset=offset)
            response = requests.get(url=api, proxies=proxy_lum)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for nfts in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
                    featured_nft = {}

                    # featured nft basic details
                    featured_nft["id"] = self.get_value(nfts, "id")
                    featured_nft["name"] = self.get_value(nfts, "name")
                    featured_nft["image_url"] = self.get_value(
                        nfts, "image_url")

                    # featured nft transaction details
                    featured_nft["floor_price"] = self.get_value(
                        nfts, "floor_price")
                    featured_nft["minters"] = self.get_value(nfts, "minters")
                    featured_nft["mint_price"] = self.get_value(
                        nfts, "mint_price")
                    featured_nft["change_in_24h"] = self.get_value(
                        nfts, "change_in_24h")
                    featured_nft["sale_count_1h"] = self.get_value(
                        nfts, "sale_count_1h")
                    featured_nft["whale_count"] = self.get_value(
                        nfts, "whale_count")
                    featured_nft["volume_in_24h"] = self.get_value(
                        nfts, "volume_in_24h")
                    featured_nft["volume_in_7d"] = self.get_value(
                        nfts, "volume_in_7d")
                    featured_nft["volume_total"] = self.get_value(
                        nfts, "volume_total")

                    featured_nft_list.append(featured_nft)

                    scraped_count += 1

                offset += limit_per_page

        return featured_nft_list

    def get_hot_selling_ranking(self,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_lum: dict = None):
        FEATURE = "Hot+Selling"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_volume_ranking(self,
                           limit_per_page: int = None,
                           limit: int = None,
                           time_range: str = "24h",
                           proxy_lum: dict = None):

        # validate to ensure the time_range is a STRING
        if not isinstance(time_range, str):
            raise TypeError("time_range parameter must be STRING type")
        time_range = time_range.strip().lower()
        time_range_list = ["24h", "7d"]

        # validate to ensure the time_range is a valid time_range
        if time_range not in time_range_list:
            raise ValueError("time_range must be in [24h,7d]")

        FEATURE = time_range + "+Volume"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_smart_money_buys_ranking(self,
                                     limit_per_page: int = None,
                                     limit: int = None,
                                     proxy_lum: dict = None):
        FEATURE = "Smart+Money+Buys"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_hot_minting_ranking(self,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_lum: dict = None):
        FEATURE = "Hot+Minting"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_whales_minting_ranking(self,
                                   limit_per_page: int = None,
                                   limit: int = None,
                                   proxy_lum: dict = None):
        FEATURE = "Smart+Money+Mints"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_gainers_ranking(self,
                            limit_per_page: int = None,
                            limit: int = None,
                            proxy_lum: dict = None):
        FEATURE = "Gainers"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)

    def get_discounts_ranking(self,
                              limit_per_page: int = None,
                              limit: int = None,
                              proxy_lum: dict = None):
        FEATURE = "Discounts"
        return self.__get_featured_nft(feature=FEATURE,
                                       limit_per_page=limit_per_page,
                                       limit=limit,
                                       proxy_lum=proxy_lum)
