import requests


class SolanaScraper:

    __API = "https://api.solscan.io/token/meta?token={token_address}"
    __HEADERS = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
    }

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
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

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
    def get_url_response(cls, url: str, headers: dict | None,
                         proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
        """
        if not cls.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (cls.is_dict(proxy_dict) or cls.is_none(proxy_dict)):
            raise TypeError("proxy_dict must be DICTIONARY type")

        # is_sucess TRUE means successful GET request
        is_success, response = None, None
        try:
            response = requests.get(url=url,
                                    headers=headers,
                                    proxies=proxy_dict)
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
    # function to get all the details of the token
    def get_token_details(cls,
                          token_address: str,
                          proxy_dict: dict = None) -> dict:

        if not cls.is_str(token_address):
            raise TypeError("token_address must be STRING type")

        is_success, response = cls.get_url_response(url=cls.__API,
                                                    headers=cls.__HEADERS,
                                                    proxy_dict=proxy_dict)

        # create a dict to store the details
        token_details = {}

        if is_success:

            data = response["data"]

            # Basic information
            token_details["symbol"] = cls.get_value(data, "symbol")
            token_details["name"] = cls.get_value(data, "name")
            token_details["decimals"] = cls.get_value(data, "decimals")
            token_details["holder"] = cls.get_value(data, "holder")

            # Image
            token_details["image"] = cls.get_value(data, "icon")

            # Tags
            tags = cls.get_value(data, "tags")
            if cls.is_list(tags):
                token_details["tags"] = [tag["name"] for tag in tags if tag]

            # website and social media links
            token_details["website"] = cls.get_value(data, "website")
            token_details["twitter"] = cls.get_value(data, "twitter")
            token_details["coingecko_id"] = cls.get_value(data, "coingeckoId")

        return token_details
