from .validation import Validation


class Discovery(Validation):

    __api = "https://api.nftbase.com/web/api/v1/home/list?name={feature}&limit={limit_per_page}&offset={offset}"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def _get_featured_nft(cls, feature: str, limit_per_page: int | None,
                          limit: int | None, proxy_dict: dict | None) -> list:

        featured_nft_list = []

        # validate the input parameters
        limit_per_page = super().validate_limit_per_page(limit_per_page)
        limit = super().validate_limit(limit)

        # variables for scraping
        finished_scraping = False
        offset = 0
        scraped_count = 1

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = cls.__api.format(feature=feature,
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

                for nfts in data:

                    if scraped_count > limit:
                        break

                    # create a dict to store the details
                    featured_nft = {}

                    # featured nft basic details
                    featured_nft["id"] = super().get_value(nfts, "id")
                    featured_nft["name"] = super().get_value(nfts, "name")
                    featured_nft["image_url"] = super().get_value(
                        nfts, "image_url")

                    # featured nft transaction details
                    featured_nft["floor_price"] = super().get_value(
                        nfts, "floor_price")
                    featured_nft["minters"] = super().get_value(
                        nfts, "minters")
                    featured_nft["mint_price"] = super().get_value(
                        nfts, "mint_price")
                    featured_nft["change_in_24h"] = super().get_value(
                        nfts, "change_in_24h")
                    featured_nft["sale_count_1h"] = super().get_value(
                        nfts, "sale_count_1h")
                    featured_nft["whale_count"] = super().get_value(
                        nfts, "whale_count")
                    featured_nft["volume_in_24h"] = super().get_value(
                        nfts, "volume_in_24h")
                    featured_nft["volume_in_7d"] = super().get_value(
                        nfts, "volume_in_7d")
                    featured_nft["volume_total"] = super().get_value(
                        nfts, "volume_total")

                    featured_nft_list.append(featured_nft)

                    scraped_count += 1

                offset += limit_per_page

        return featured_nft_list

    @classmethod
    def get_hot_selling_ranking(cls,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_dict: dict = None):
        FEATURE = "Hot+Selling"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_volume_ranking(cls,
                           limit_per_page: int = None,
                           limit: int = None,
                           time_range: str = "24h",
                           proxy_dict: dict = None):

        # validate to ensure the time_range is a STRING
        if not super().is_str(time_range):
            raise TypeError("time_range parameter must be STRING type")
        time_range = super().str_strip(time_range)
        time_range = super().str_lower(time_range)
        TIME_RANGE_LIST = ["24h", "7d"]

        # validate to ensure the time_range is a valid time_range
        if time_range not in TIME_RANGE_LIST:
            raise ValueError("time_range must be in [24h,7d]")

        FEATURE = time_range + "+Volume"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_smart_money_buys_ranking(cls,
                                     limit_per_page: int = None,
                                     limit: int = None,
                                     proxy_dict: dict = None):
        FEATURE = "Smart+Money+Buys"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_hot_minting_ranking(cls,
                                limit_per_page: int = None,
                                limit: int = None,
                                proxy_dict: dict = None):
        FEATURE = "Hot+Minting"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_whales_minting_ranking(cls,
                                   limit_per_page: int = None,
                                   limit: int = None,
                                   proxy_dict: dict = None):
        FEATURE = "Smart+Money+Mints"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_gainers_ranking(cls,
                            limit_per_page: int = None,
                            limit: int = None,
                            proxy_dict: dict = None):
        FEATURE = "Gainers"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)

    @classmethod
    def get_discounts_ranking(cls,
                              limit_per_page: int = None,
                              limit: int = None,
                              proxy_dict: dict = None):
        FEATURE = "Discounts"
        return cls._get_featured_nft(feature=FEATURE,
                                     limit_per_page=limit_per_page,
                                     limit=limit,
                                     proxy_dict=proxy_dict)
