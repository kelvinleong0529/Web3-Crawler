import datetime


class NFT_scraper_base_class:

    def __init__(self) -> None:
        self.__LIMIT_PER_PAGE = 20
        self.__LIMIT = 50
        self.__ACTION_LIST = ["buy", "sell", "mint", "receive", "send"]

    def get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    # validate the "limit_per_page" input paramter
    def validate_limit_per_page(self, limit_per_page: int) -> int:
        if self.is_none(limit_per_page):
            return self.__LIMIT_PER_PAGE
        if not self.is_int(input=limit_per_page):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page

    # validate the "limit" input parameter
    def validate_limit(self, limit: int) -> int:
        if self.is_none(limit):
            return self.__LIMIT
        if not self.is_int(input=limit):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    # function to remove duplicates in a dictionary list
    def remove_duplicate_in_dict_list(self, input: list) -> dict:
        return [dict(t) for t in {tuple(d.items()) for d in input}]

    # check and validate the action list is valid
    def validate_action_list(self, input: list) -> bool:

        input = [self.str_strip(element) for element in input]
        input = [self.str_capitalize(element) for element in input]

        if not set(input).issubset(set(self.__ACTION_LIST)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return True

    def is_int(self, input: int) -> bool:
        return True if isinstance(input, int) else False

    def is_list(self, input: list) -> bool:
        return True if isinstance(input, list) else False

    def is_str(self, input: str) -> bool:
        return True if isinstance(input, str) else False

    def is_dict(self, input: dict) -> bool:
        return True if isinstance(input, dict) else False

    def is_none(self, input: None) -> bool:
        return True if input is None else False

    def int_to_str(self, input: int) -> str:
        return str(input)

    def str_strip(self, input: str) -> str:
        return input.strip()

    def str_capitalize(self, input: str) -> str:
        return input.capitalize()

    # function to join the target list with "," and merge into a string
    def list_to_str(self, input: list) -> str:
        return ",".join(input)

    # function to convert timestamp to utc time format
    def utc_from_timestamp(self, timestamp: str) -> str:
        try:
            return str(
                datetime.datetime.utcfromtimestamp(
                    int(timestamp)).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return "N/A"