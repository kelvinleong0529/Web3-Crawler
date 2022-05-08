import datetime
from multiprocessing.sharedctypes import Value


class NFT_scraper_base_class:

    def __init__(self) -> None:
        self.__LIMIT_PER_PAGE = 20
        self.__LIMIT = 50

    def get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    # validate the "limit_per_page" input paramter
    def validate_limit_per_page(self, limit_per_page: int) -> int:
        if limit_per_page is None:
            return self.__LIMIT_PER_PAGE
        if not isinstance(limit_per_page, int):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page

    # validate the "limit" input parameter
    def validate_limit(self, limit: int) -> int:
        if limit is None:
            return self.__LIMIT
        if not isinstance(limit, int):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    # function to remove duplicates in a dictionary list
    def remove_duplicate_in_dict_list(self, target_list: list) -> dict:
        return [dict(t) for t in {tuple(d.items()) for d in target_list}]

    # function to join a list with "," and convert it to string
    def action_list_to_str(self, target_list: list) -> str:
        # return empty string if the target_list is None
        if target_list is None:
            return ""
        if not isinstance(target_list, list):
            raise TypeError("You should pass a LIST of actions")

        # remove any trailing whitespace and capitilize the first letter of each element in the list
        target_list = [data.strip().capitalize() for data in target_list]

        # list of actions allowed
        action_list = ["buy", "sell", "mint", "receive", "send"]

        if not set(target_list).issubset(set(action_list)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return ",".join(target_list)

    # function to convert timestamp to utc time format
    def utc_from_timestamp(self, timestamp: str) -> str:
        try:
            return str(
                datetime.datetime.utcfromtimestamp(
                    int(timestamp)).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return "N/A"