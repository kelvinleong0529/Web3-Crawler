import requests


class HoneypotScraper:

    # all honeypot validator functions return TRUE if detects any honeypot and vice-versa
    def __init__(self) -> None:
        self.__NETWORK_POOL = {
            "binance smart chain": {
                0: {
                    "function": self.__check_honeypot_is,
                    "network": "bsc2"
                },
                1: {
                    "function": self.__check_rugdoc,
                    "network": "bscscan"
                }
            },
            "ethereum": {
                0: {
                    "function": self.__check_honeypot_is,
                    "network": "eth"
                }
            },
            "fantom": {
                0: {
                    "function": self.__check_rugdoc,
                    "network": "ftmscan"
                }
            },
            "polygon": {
                0: {
                    "function": self.__check_rugdoc,
                    "network": "polygonscan"
                }
            }
        }

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def str_lower(input: str) -> str:
        return input.lower()

    @staticmethod
    def str_strip(input: str) -> str:
        return input.strip()

    @classmethod
    def get_url_response(cls, url: str, proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
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

    def check_honeypot(self,
                       network: str,
                       address: str,
                       proxy_dict: dict = None) -> dict:
        """ function that checks whether the token is a honeypot
        """
        # validate the input parameters
        if not self.is_str(network):
            raise TypeError("Network argument must be string type")

        if not self.is_str(address):
            raise TypeError("Address argument must be string type")

        # convert the network to lower case
        network = self.str_lower(network)

        network_pool = self.__NETWORK_POOL
        if network in network_pool:
            network_target = network_pool[network]
            is_honeypot, non_honeypot, source_checked = 0, 0, 0
            for network in network_target.items():
                honeypot_function = network[-1]["function"]
                honeypot_network = network[-1]["network"]
                honeypot_result = honeypot_function(honeypot_network, address,
                                                    proxy_dict)
                if honeypot_result is None:
                    continue
                if honeypot_result:
                    is_honeypot += 1
                else:
                    non_honeypot += 1
                source_checked += 1
            return {
                "message":
                "Checked {source_checked} honeypot source(s)".format(
                    source_checked=source_checked),
                "non_honeypot":
                non_honeypot,
                "is_honeypot":
                is_honeypot
            }
        return {"message": "Target Network not supported!"}

    @classmethod
    def __check_rugdoc(cls, network: str, address: str,
                       proxy_dict: dict | None) -> bool | None:
        """ function to check honeypot on "rugdoc", reference website: https://rugdoc.io/honeypot/
        """
        api = "https://api.{network}.com/api?module=contract&action=getsourcecode&address={address}".format(
            network=network, address=address)
        is_success, response = cls.get_url_response(url=api,
                                                    proxy_dict=proxy_dict)
        if is_success:
            return True if response["result"][0]["ABI"] in [
                "Contract source code not verified"
            ] else False
        return None

    @classmethod
    def __check_honeypot_is(self, network: str, address: str,
                            proxy_dict: dict | None) -> bool | None:
        """ function to check honeypot on "honeypot.is", reference website: https://honeypot.is/
        """
        api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}".format(
            address=address, network=network)
        is_success, response = self.get_url_response(url=api,
                                                     proxy_dict=proxy_dict)
        if is_success:
            return response["IsHoneypot"]
        return None
