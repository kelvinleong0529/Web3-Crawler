import datetime
import requests


class NFT_scraper_utility_class:

    def __init__(self) -> None:
        pass

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        if not self.is_dict(input_dict):
            raise TypeError("Only accepts dictionary as arguments")
        if key not in input_dict:
            return "N/A"
        if self.is_dict(input_dict[key]):
            return input_dict[key]
        else:
            return str(input_dict[key])

    # function to remove duplicates in a dictionary list
    def remove_duplicate_in_dict_list(self, input: list) -> list:
        if not self.is_list(input):
            raise TypeError("Only accepts LIST as arguments")
        return [dict(t) for t in {tuple(d.items()) for d in input}]

    def get_url_response(self, url: str, proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
        """
        if not self.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (self.is_dict(proxy_dict) or self.is_none(proxy_dict)):
            raise TypeError("proxy_dict must be DICTIONARY type")

        # is_sucess TRUE means successful GET request
        is_success, response = None, None
        try:
            response = requests.get(url=url, proxies=proxy_dict)
            is_success = True
            response = response.json()
        except requests.ConnectionError as e:
            print(
                "Connection Error, make sure you are connected to the Internet!"
            )
            print(str(e))
            is_success = False
        except requests.Timeout as e:
            print("Timeout Error!")
            print(str(e))
            is_success = False
        except requests.RequestException as e:
            print("General Error, something unexpected happen!")
            print(str(e))
        except KeyboardInterrupt:
            print("Program was forced to close externally")
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

    def timestamp_to_utc(self, timestamp: str | None) -> str:
        """convert timestamp to utc time format
        """
        if self.is_none(timestamp):
            return "N/A"
        if not self.is_str(timestamp):
            raise TypeError("Timestamp must be STRING format")
        try:
            return str(
                datetime.datetime.utcfromtimestamp(
                    int(timestamp)).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return "N/A"


class NFT_scraper_validation_class(NFT_scraper_utility_class):

    def __init__(self) -> None:
        pass

    def validate_action_list(self, input: list | None) -> bool:
        """ validate the acion list to see if it's valid
        """

        if super().is_none(input):
            return True

        if not super().is_list(input):
            raise TypeError("action_list must be LIST type")

        ACTION_LIST = ["buy", "sell", "mint", "receive", "send"]

        # remove any trailing whitespace and convert the elements to lower case
        input = [super().str_strip(element) for element in input]
        input = [super().str_lower(element) for element in input]

        if not set(input).issubset(set(ACTION_LIST)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return True

    def validate_limit(self, limit: int | None) -> int:
        """ validate the "limit" parameter, and return default value if it's None
        """
        LIMIT = 20
        if super().is_none(limit):
            return LIMIT
        if not super().is_int(limit):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    def validate_limit_per_page(self, limit_per_page: int | None) -> int:
        """ validate the "limit_par_page" parameter, and return default value if it's None
        """
        LIMIT_PER_PAGE = 50
        if super().is_none(limit_per_page):
            return LIMIT_PER_PAGE
        if not super().is_int(limit_per_page):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page

    def validate_price_range(self, price_range: int | None) -> str:
        """ validate the "price_range" parameter, and convert it from int to string type
        """
        if super().is_none(price_range):
            return ""
        if not super().is_int(price_range):
            raise TypeError("price_range argument must be a INTEGER type")
        return super().int_to_str(price_range)

    def get_sort_option(self, sort_option: str) -> int:
        """ return sorting parameter based on sorting option input
        """
        if not super().is_str(sort_option):
            raise TypeError("sort_option must be STRING type argument")

        # sort option list
        # market cap = 1, latest = 2, etc ...
        SORT_OPTION_LIST = ["market cap", "latest", "oldest"]

        # remove any trailing whitespaces and convert the string to lower case
        sort_option = super().str_strip(sort_option)
        sort_option = super().str_lower(sort_option)

        # check and see if the sort option is valid
        if sort_option not in SORT_OPTION_LIST:
            raise ValueError(
                "Sort option must be either one of these: [Market Cap, Latest, Oldest]"
            )

        # return the corresponding sort parameter
        return SORT_OPTION_LIST.index(sort_option) + 1
