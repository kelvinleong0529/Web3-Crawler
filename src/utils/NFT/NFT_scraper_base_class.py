import datetime


class NFT_scraper_base_class:

    def __init__(self) -> None:
        pass

    def get_value(self, input_dict: dict, key: str) -> str:
        if not self.is_dict(input_dict):
            raise TypeError("Only accepts dictionary as arguments")
        if key not in input_dict:
            return "N/A"
        if self.is_dict(input_dict[key]):
            return input_dict[key]
        else:
            return str(input_dict[key])

    # function to remove duplicates in a dictionary list
    def remove_duplicate_in_dict_list(self, input: list) -> dict:
        if not self.is_list(input):
            raise TypeError("Only accepts LIST as arguments")
        return [dict(t) for t in {tuple(d.items()) for d in input}]

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

    def str_to_int(self, input: str) -> int:
        return int(input)

    def str_strip(self, input: str) -> str:
        return input.strip()

    def str_lower(self, input: str) -> str:
        return input.lower()

    def str_capitalize(self, input: str) -> str:
        return input.capitalize()

    # function to join the target list with "," and merge into a string
    def list_to_str(self, input: list) -> str:
        return ",".join(input)

    # function to convert timestamp to utc time format
    def timestamp_to_utc(self, timestamp: str) -> str:
        try:
            return str(
                datetime.datetime.utcfromtimestamp(
                    int(timestamp)).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return "N/A"


class NFT_scraper_validation_class(NFT_scraper_base_class):

    def __init__(self) -> None:
        self.__LIMIT_PER_PAGE = 20
        self.__LIMIT = 50

    # check and validate the action list is valid
    def validate_action_list(self, input: list) -> bool:

        action_list = ["buy", "sell", "mint", "receive", "send"]

        input = [super().str_strip(element) for element in input]
        input = [super().str_capitalize(element) for element in input]

        if not set(input).issubset(set(action_list)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return True

    # validate the "limit" input parameter
    def validate_limit(self, limit: int) -> int:
        if super().is_none(limit):
            return self.__LIMIT
        if not super().is_int(limit):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    # validate the "limit_per_page" input paramter
    def validate_limit_per_page(self, limit_per_page: int) -> int:
        if super().is_none(limit_per_page):
            return self.__LIMIT_PER_PAGE
        if not super().is_int(limit_per_page):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page