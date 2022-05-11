class GameFi_scraper_utility_cass:

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

    @staticmethod
    def is_int(input: int) -> bool:
        return True if isinstance(input, int) else False

    @staticmethod
    def int_to_str(input: int) -> str:
        return str(input)

    @staticmethod
    # function to join the target list with "," and merge into a string
    def list_to_str(input: list) -> str:
        return ",".join(input)

    def get_value(self, input_dict: dict, key: str) -> dict | str:
        if not self.is_dict(input_dict):
            raise TypeError("Only accepts dictionary as arguments")
        if key not in input_dict:
            return "N/A"
        if self.is_dict(input_dict[key]):
            return input_dict[key]
        else:
            return str(input_dict[key])

    def get_url_response(self, url: str, proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
        """
        if not self.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (self.is_dict(proxy_dict) or self.is_none(proxy_dict)):
            raise TypeError("proxy_dict must be DICTIONARY type")

    # function to validate the "limit" parameter
    def validate_limit(self, limit: int | None) -> str:
        LIMIT = 20
        if limit is None:
            return LIMIT
        if not self.is_int(limit):
            raise TypeError("limit parameter must be INTEGER type")
        return self.int_to_str(limit)