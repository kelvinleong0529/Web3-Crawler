import datetime
from typing import Type
import requests


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

    def get_url_response(self, url: str, proxy_dict: dict) -> tuple:
        if not self.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (self.is_dict(proxy_dict) or self.is_none(proxy_dict)):
            raise TypeError("proxy_dict must be DICTIONARY type")

        # is_sucess TRUE means successful GET request
        is_success = None
        response = requests.get(url=url, proxies=proxy_dict)
        if str(response.status_code) == "200":
            is_success = True
            response = response.json()
        else:
            is_success = False
        return (is_success, response)

    @staticmethod
    def is_int(input: int) -> bool:
        return True if isinstance(input, int) else False

    @staticmethod
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_none(input: None) -> bool:
        return True if input is None else False

    @staticmethod
    def int_to_str(input: int) -> str:
        return str(input)

    @staticmethod
    def str_to_int(input: str) -> int:
        return int(input)

    @staticmethod
    def str_strip(input: str) -> str:
        return input.strip()

    @staticmethod
    def str_lower(input: str) -> str:
        return input.lower()

    @staticmethod
    def str_capitalize(input: str) -> str:
        return input.capitalize()

    @staticmethod
    # function to join the target list with "," and merge into a string
    def list_to_str(input: list) -> str:
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

    def get_sort_option(self, sort_option: str) -> int:
        if not super().is_str(sort_option):
            raise TypeError("sort_option must be STRING type argument")

        # sort option list
        # market cap = 1, latest = 2, etc ...
        sort_option_list = ["market cap", "latest", "oldest"]

        # remove any trailing whitespaces and convert the string to lower case
        sort_option = super().str_strip(sort_option)
        sort_option = super().str_lower(sort_option)

        # check and see if the sort option is valid
        if sort_option not in sort_option_list:
            raise ValueError(
                "Sort option must be either one of these: [Market Cap, Latest, Oldest]"
            )

        # return the corresponding sort parameter
        return sort_option_list.index(sort_option) + 1