import requests

from NFT_scraper_base_class import NFT_scraper_base_class


class NFT_scraper_hot_selling(NFT_scraper_base_class):

    def __init__(self) -> None:
        super().__init__()
        self.__api = "https://api.nftbase.com/web/api/v1/home/list?name=Hot+Selling&limit={limit_per_page}&offset={offset}"
        self.__hot_selling_list = []

    def get_value(self, input_dict: dict, key: str) -> str:
        return super().get_value(input_dict, key)

    def get_hot_selling(self,
                        limit_per_page: int = 20,
                        limit: int = 50) -> list:
        # empty the return activity list
        self.__hot_selling_list.clear()

        # variables for scraping
        finished_scraping = False
        offset = 0

        while offset <= limit and not finished_scraping:

            # make GET request to the API endpoint
            api = self.__api.format(limit_per_page=limit_per_page,
                                    offset=offset)
            response = requests.get(api)

            # if the request is successful
            if str(response.status_code) == "200":
                data = response.json()["data"]

                # if the response returns blank or empty data, break the loop
                if not data:
                    finished_scraping = True
                    continue

                for hot_selling_nfts in data:
                    # initialize a dict to store the details
                    hot_selling_nft = {}

                    # hot selling nft basic details
                    hot_selling_nft["id"] = self.get_value(
                        hot_selling_nfts, "id")
                    hot_selling_nft["name"] = self.get_value(
                        hot_selling_nfts, "name")
                    hot_selling_nft["image_url"] = self.get_value(
                        hot_selling_nfts, "image_url")

                    # hot selling nft transaction details
                    hot_selling_nft["floor_price"] = self.get_value(
                        hot_selling_nfts, "floor_price")
                    hot_selling_nft["minters"] = self.get_value(
                        hot_selling_nfts, "minters")
                    hot_selling_nft["mint_price"] = self.get_value(
                        hot_selling_nfts, "mint_price")
                    hot_selling_nft["change_in_24h"] = self.get_value(
                        hot_selling_nfts, "change_in_24h")
                    hot_selling_nft["sale_count_1h"] = self.get_value(
                        hot_selling_nfts, "sale_count_1h")
                    hot_selling_nft["whale_count"] = self.get_value(
                        hot_selling_nfts, "whale_count")
                    hot_selling_nft["volume_in_24h"] = self.get_value(
                        hot_selling_nfts, "volume_in_24h")
                    hot_selling_nft["volume_in_7d"] = self.get_value(
                        hot_selling_nfts, "volume_in_7d")
                    hot_selling_nft["volume_total"] = self.get_value(
                        hot_selling_nfts, "volume_total")

                    self.__hot_selling_list.append(hot_selling_nft)

                offset += limit_per_page

        return self.__hot_selling_list