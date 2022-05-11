import requests


class DexToolsScraper:

    def __init__(self) -> None:
        self.__headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
        }
        self.__networks = [
            "arbitrum", "astar", "aurora", "avalanche", "bsc", "celo",
            "cronos", "dfk", "ethereum", "fantom", "fuse", "harmony", "heco",
            "iotex", "kucoin", "metis", "milkomeda", "moonbeam", "moonriver",
            "oasis", "oec", "optimism", "polygon", "telos", "velas"
        ]

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def is_none(input: None) -> bool:
        return True if input is None else False

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

    def get_tokens(self, search_string: str, proxy_dict: dict = None) -> list:

        # validate the input parameters
        if not self.is_str(search_string):
            raise TypeError("search_string must be STRING type")

        # create a list to store the scraped results
        token_detail_list = []
        for index, network in enumerate(self.__networks):
            token_detail_list.append(
                self.__search_network(network=network,
                                      search_string=search_string,
                                      proxy_dict=proxy_dict))
        token_detail_list = self.remove_duplicate_in_dict_list(
            token_detail_list)
        return token_detail_list

    def get_url_response(self, url: str, headers: dict,
                         proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
        """
        if not self.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (self.is_dict(proxy_dict) or self.is_none(proxy_dict)):
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

    def __search_network(self, network: str, search_string: str,
                         proxy_dict: int | None) -> list:

        # create a list to store the scraped results
        token_detail_list = []

        api = "https://www.dextools.io/chain-{network}/api/pair/search?s={search_string}".format(
            network=network, search_string=search_string)
        is_success, response = self.get_url_response(url=api,
                                                     headers=self.__headers,
                                                     proxy_dict=proxy_dict)

        if is_success:
            for index, value in enumerate(response):
                # create a dict to store the details
                token = {}

                # token info
                info = self.get_value(value, "info")
                token["name"] = self.get_value(info, "name")
                token["network"] = network
                token["address"] = self.get_value(info, "address")
                token["symbol"] = self.get_value(info, "symbol")
                token["decimals"] = self.get_value(info, "decimals")
                token["holders_count"] = self.get_value(info, "holders")
                token["total_supply"] = self.get_value(info, "totalSupply")

                # token pricing info
                token["price"] = self.get_value(value, "price")
                token["price_24h"] = self.get_value(value, "price24h")
                token["volume_24h"] = self.get_value(value, "volume24h")
                token["liquidity"] = self.get_value(value, "liquidity")
                token["diluted_market_cap"] = self.get_value(
                    value, "diluted_market_cap")

                # token gas info
                creation = self.get_value(value, "creation")
                token["gas"] = self.get_value(creation, "gas")
                token["gas_price"] = self.get_value(creation, "gasPrice")
                token["gas_used"] = self.get_value(creation,
                                                   "cumulativeGasUsed")

                # pair basic info
                token["pair_exchange"] = self.get_value(value, "exchange")
                token["pair_address"] = self.get_value(value, "id")
                token["pair_type"] = self.get_value(value, "pair")

                # pair base token info
                base_token = self.get_value(value, "token0")
                token["pair_base_token_name"] = self.get_value(
                    base_token, "name")
                token["pair_base_token_symbol"] = self.get_value(
                    base_token, "symbol")
                token["pair_base_token_address"] = self.get_value(
                    base_token, "id")
                token["pair_base_token_decimals"] = self.get_value(
                    base_token, "decimals")

                # pair target token info
                target_token = self.get_value(value, "token1")
                token["pair_target_token_name"] = self.get_value(
                    target_token, "name")
                token["pair_target_token_symbol"] = self.get_value(
                    target_token, "symbol")
                token["pair_target_token_address"] = self.get_value(
                    target_token, "id")
                token["pair_target_token_decimals"] = self.get_value(
                    target_token, "decimals")

                token_detail_list.append(token)

        return token_detail_list