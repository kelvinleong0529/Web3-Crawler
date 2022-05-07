import requests
import datetime

from NFT_scraper_base_class import NFT_scraper_base_class

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
            for collection_activities in data:
                # initialize a dict to store the details
                collection_activity = {}

                # transaction details
                collection_activity["transaction_price"] = self.get_value(
                    collection_activities, "price")
                collection_activity["transaction_currency"] = self.get_value(
                    collection_activities, "symbol")
                collection_activity["action"] = self.get_value(
                    collection_activities, "action")
                collection_activity["timestamp"] = self.get_value(
                    collection_activities, "timestamp")
                if collection_activity["timestamp"] != "N/A":
                    collection_activity[
                        "timestamp"] = datetime.datetime.utcfromtimestamp(
                            int(collection_activity["timestamp"])).strftime(
                                '%Y-%m-%d %H:%M:%S')

                # NFT details
                item_details = self.get_value(collection_activities, "item")
                collection_activity["nft_id"] = self.get_value(
                    item_details, "token_id")
                collection_activity["nft_address"] = self.get_value(
                    item_details, "contract_addr")
                collection_activity["nft_url"] = self.get_value(
                    item_details, "image_url")
                collection_activity["nft_rarity_rank"] = self.get_value(
                    item_details, "rarity_rank")

                # buyer details
                buyer = self.get_value(collection_activities, "to")
                collection_activity["buyer_name"] = self.get_value(
                    buyer, "name")
                collection_activity["buyer_address"] = self.get_value(
                    buyer, "address")
                collection_activity["buyer_is_whale"] = self.get_value(
                    buyer, "is_whale")

                # seller details
                seller = self.get_value(collection_activities, "to")
                collection_activity["seller_name"] = self.get_value(
                    seller, "name")
                collection_activity["seller_address"] = self.get_value(
                    seller, "address")
                collection_activity["seller_is_whale"] = self.get_value(
                    seller, "is_whale")

                self.__collection_activity_list.append(collection_activity)

        return self.__collection_activity_list