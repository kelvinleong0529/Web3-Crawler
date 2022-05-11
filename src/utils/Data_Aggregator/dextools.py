import requests


class DexToolsScraper:

    __api = "https://www.dextools.io/chain-{network}/api/pair/search?s={search_string}"
    __HEADERS = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
    }
    __NETWORKS = [
        "arbitrum", "astar", "aurora", "avalanche", "bsc", "celo", "cronos",
        "dfk", "ethereum", "fantom", "fuse", "harmony", "heco", "iotex",
        "kucoin", "metis", "milkomeda", "moonbeam", "moonriver", "oasis",
        "oec", "optimism", "polygon", "telos", "velas"
    ]

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def is_none(input: None) -> bool:
        return True if input is None else False

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
    # function to remove duplicates in a dictionary list
    def remove_duplicate_in_dict_list(cls, input: list) -> list:
        if not cls.is_list(input):
            raise TypeError("Only accepts LIST as arguments")
        return [dict(t) for t in {tuple(d.items()) for d in input}]

    @classmethod
    def get_tokens(cls, search_string: str, proxy_dict: dict = None) -> list:

        # validate the input parameters
        if not cls.is_str(search_string):
            raise TypeError("search_string must be STRING type")

        # create a list to store the scraped results
        token_detail_list = []
        for index, network in enumerate(cls.__NETWORKS):
            token_detail_list.append(
                cls._search_network(network=network,
                                    search_string=search_string,
                                    proxy_dict=proxy_dict))
        token_detail_list = cls.remove_duplicate_in_dict_list(
            token_detail_list)
        return token_detail_list

    @classmethod
    def get_url_response(cls, url: str, headers: dict,
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
    def _search_network(cls, network: str, search_string: str,
                        proxy_dict: int | None) -> list:

        # create a list to store the scraped results
        token_detail_list = []

        api = cls.__api.format(network=network, search_string=search_string)
        is_success, response = cls.get_url_response(url=api,
                                                    headers=cls.__HEADERS,
                                                    proxy_dict=proxy_dict)

        if is_success:
            for index, value in enumerate(response):
                # create a dict to store the details
                token = {}

                # token info
                info = cls.get_value(value, "info")
                token["name"] = cls.get_value(info, "name")
                token["network"] = network
                token["address"] = cls.get_value(info, "address")
                token["symbol"] = cls.get_value(info, "symbol")
                token["decimals"] = cls.get_value(info, "decimals")
                token["holders_count"] = cls.get_value(info, "holders")
                token["total_supply"] = cls.get_value(info, "totalSupply")

                # token pricing info
                token["price"] = cls.get_value(value, "price")
                token["price_24h"] = cls.get_value(value, "price24h")
                token["volume_24h"] = cls.get_value(value, "volume24h")
                token["liquidity"] = cls.get_value(value, "liquidity")
                token["diluted_market_cap"] = cls.get_value(
                    value, "diluted_market_cap")

                # token gas info
                creation = cls.get_value(value, "creation")
                token["gas"] = cls.get_value(creation, "gas")
                token["gas_price"] = cls.get_value(creation, "gasPrice")
                token["gas_used"] = cls.get_value(creation,
                                                  "cumulativeGasUsed")

                # pair basic info
                token["pair_exchange"] = cls.get_value(value, "exchange")
                token["pair_address"] = cls.get_value(value, "id")
                token["pair_type"] = cls.get_value(value, "pair")

                # pair base token info
                base_token = cls.get_value(value, "token0")
                token["pair_base_token_name"] = cls.get_value(
                    base_token, "name")
                token["pair_base_token_symbol"] = cls.get_value(
                    base_token, "symbol")
                token["pair_base_token_address"] = cls.get_value(
                    base_token, "id")
                token["pair_base_token_decimals"] = cls.get_value(
                    base_token, "decimals")

                # pair target token info
                target_token = cls.get_value(value, "token1")
                token["pair_target_token_name"] = cls.get_value(
                    target_token, "name")
                token["pair_target_token_symbol"] = cls.get_value(
                    target_token, "symbol")
                token["pair_target_token_address"] = cls.get_value(
                    target_token, "id")
                token["pair_target_token_decimals"] = cls.get_value(
                    target_token, "decimals")

                token_detail_list.append(token)

        return token_detail_list