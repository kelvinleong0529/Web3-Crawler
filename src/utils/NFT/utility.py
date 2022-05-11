import datetime
import requests

class Utlity:

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