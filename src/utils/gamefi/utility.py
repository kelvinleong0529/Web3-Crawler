import requests


class Utility:

    LIMIT = 20

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
    def is_none(input: None) -> bool:
        return True if input is None else False

    @staticmethod
    def int_to_str(input: int) -> str:
        return str(input)

    @staticmethod
    def trim_string(input: str) -> str:
        return input.strip()

    @staticmethod
    def lower_string(input: str) -> str:
        return input.lower()

    @staticmethod
    # function to join the target list with "," and merge into a string
    def list_to_str(input: list) -> str:
        return ",".join(input)

    @classmethod
    def get_value(cls, input_dict: dict, key: str) -> dict | list | str:
        if not cls.is_dict(input_dict):
            raise TypeError("Only accepts dictionary as arguments")
        if key not in input_dict:
            return "N/A"
        if cls.is_dict(input_dict[key]) or cls.is_list(input_dict[key]):
            return input_dict[key]
        else:
            return str(input_dict[key])

    @classmethod
    def get_url_response(cls, url: str,
                         proxy_dict: dict | None) -> tuple[bool, str]:
        """
        Make a GET request to url endpoint and return the result in JSON format

        Args:
            url (str): API / URL endpoint
            proxy_dict (dict | None): Proxy Settings Parameter

        Raises:
            TypeError: when 'url' passed is not STR
            TypeError: when 'proxy_dict' is not DICT

        Returns:
            tuple[bool, str]: 1st value -> true indicates successful request and vice versa, 2nd value -> GET response in JSON format
        """
        if not cls.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (cls.is_dict(proxy_dict) or cls.is_none(proxy_dict)):
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

    @classmethod
    # function to validate the "limit" parameter
    def validate_limit(cls, limit: int | None) -> str:
        if limit is None:
            return cls.LIMIT
        if not cls.is_int(limit):
            raise TypeError("limit parameter must be INTEGER type")
        return cls.int_to_str(limit)