import requests


class dextools_scraper:

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

    def __get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    def get_tokens(self, search_string: str) -> list:
        token_detail_list = []
        for index, network in enumerate(self.__networks):
            token_detail_list += self.__search(network, search_string)
        return [dict(token) for token in {tuple(tokens.items()) for tokens in token_detail_list}]

    def __search(self, network: str, search_string: str) -> list:
        api = "https://www.dextools.io/chain-{network}/api/pair/search?s={search_string}".format(
            network=network, search_string=search_string)
        response = requests.get(api, headers=self.__headers)
        token_detail_list = []
        if str(response.status_code) == "200":
            response = response.json()
            for index, value in enumerate(response):
                # initialize a dict to store the details
                token = {}

                # token info
                info = self.__get_value(value, "info")
                token["name"] = self.__get_value(info, "name")
                token["network"] = network
                token["address"] = self.__get_value(info, "address")
                token["symbol"] = self.__get_value(info, "symbol")
                token["decimals"] = self.__get_value(info, "decimals")
                token["holders_count"] = self.__get_value(info, "holders")
                token["total_supply"] = self.__get_value(info, "totalSupply")

                # token pricing info
                token["price"] = self.__get_value(value, "price")
                token["price_24h"] = self.__get_value(value, "price24h")
                token["volume_24h"] = self.__get_value(value, "volume24h")
                token["liquidity"] = self.__get_value(value, "liquidity")
                token["diluted_market_cap"] = self.__get_value(
                    value, "diluted_market_cap")

                # token gas info
                creation = self.__get_value(value, "creation")
                token["gas"] = self.__get_value(creation, "gas")
                token["gas_price"] = self.__get_value(creation, "gasPrice")
                token["gas_used"] = self.__get_value(creation,
                                                     "cumulativeGasUsed")

                # pair basic info
                token["pair_exchange"] = self.__get_value(value, "exchange")
                token["pair_address"] = self.__get_value(value, "id")
                token["pair_type"] = self.__get_value(value, "pair")

                # pair base token info
                base_token = self.__get_value(value, "token0")
                token["pair_base_token_name"] = self.__get_value(
                    base_token, "name")
                token["pair_base_token_symbol"] = self.__get_value(
                    base_token, "symbol")
                token["pair_base_token_address"] = self.__get_value(
                    base_token, "id")
                token["pair_base_token_decimals"] = self.__get_value(
                    base_token, "decimals")

                # pair target token info
                target_token = self.__get_value(value, "token1")
                token["pair_target_token_name"] = self.__get_value(
                    target_token, "name")
                token["pair_target_token_symbol"] = self.__get_value(
                    target_token, "symbol")
                token["pair_target_token_address"] = self.__get_value(
                    target_token, "id")
                token["pair_target_token_decimals"] = self.__get_value(
                    target_token, "decimals")

                token_detail_list.append(token)

        return token_detail_list