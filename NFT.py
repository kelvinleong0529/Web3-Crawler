import requests
import datetime


class NFT_scraper:

    def __init__(self) -> None:
        pass

    def __get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    # function to get NFT most recent transaction details, refernce website: https://www.nftexplorer.app/
    def get_activity(self, collection_id: str, limit: int = 20) -> list:
        collection_id = collection_id.lower().replace(" ", "")
        api = "https://api.nftbase.com/web/api/v1/collection/activities?collection_id={collection_id}&limit={limit}".format(
            collection_id=collection_id, limit=limit)
        activity_list = []
        response = requests.get(api)
        if str(response.status_code) == "200":
            data = response.json()["data"]
            for activities in data:
                # initialize a dict to store the details
                activity = {}

                # transaction details
                activity["transaction_price"] = self.__get_value(
                    activities, "price")
                activity["transaction_currency"] = self.__get_value(
                    activities, "symbol")
                activity["action"] = self.__get_value(activities, "action")
                activity["timestamp"] = self.__get_value(
                    activities, "timestamp")
                if activity["timestamp"]:
                    activity["timestamp"] = datetime.datetime.utcfromtimestamp(
                        int(activity["timestamp"])).strftime(
                            '%Y-%m-%d %H:%M:%S')

                # NFT details
                item_details = self.__get_value(activities, "item")
                activity["nft_id"] = self.__get_value(item_details, "token_id")
                activity["nft_address"] = self.__get_value(
                    item_details, "contract_addr")
                activity["nft_url"] = self.__get_value(item_details,
                                                       "image_url")
                activity["nft_rarity_rank"] = self.__get_value(
                    item_details, "rarity_rank")

                # buyer details
                buyer = self.__get_value(activities, "to")
                activity["buyer_name"] = self.__get_value(buyer, "name")
                activity["buyer_address"] = self.__get_value(buyer, "address")
                activity["buyer_is_whale"] = self.__get_value(
                    buyer, "is_whale")

                # seller details
                seller = self.__get_value(activities, "to")
                activity["seller_name"] = self.__get_value(seller, "name")
                activity["seller_address"] = self.__get_value(
                    seller, "address")
                activity["seller_is_whale"] = self.__get_value(
                    seller, "is_whale")

                activity_list.append(activity)

        return activity_list