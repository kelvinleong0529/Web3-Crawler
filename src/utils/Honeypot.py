import requests


class honeypot_scraper:

    # all the honeypot validator function returns TRUE if detect honeypot and vice-versa

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

    def check_honeypot(self, network: str, address: str) -> dict:
        network = network.lower().strip()
        network_pool = self.__NETWORK_POOL
        if network in network_pool:
            network_target = network_pool[network]
            is_honeypot, non_honeypot, source_checked = 0, 0, 0
            for network in network_target.items():
                honeypot_function = network[-1]["function"]
                honeypot_network = network[-1]["network"]
                if honeypot_function(honeypot_network, address):
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

    # function to check honeypot on "rugdoc", reference website: https://rugdoc.io/honeypot/
    def __check_rugdoc(self, network: str, address: str) -> bool:
        api = "https://api.{network}.com/api?module=contract&action=getsourcecode&address={address}".format(
            network=network, address=address)
        honeypot_result = None
        response = requests.get(api)
        if str(response.status_code) == "200":
            response = response.json()
            return True if response["result"][0]["ABI"] in [
                "Contract source code not verified"
            ] else False
        return honeypot_result

    # function to check honeypot on "honeypot.is", reference website: https://honeypot.is/
    def __check_honeypot_is(self, network: str, address: str) -> bool:
        api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}".format(
            address=address, network=network)
        honeypot_result = None
        response = requests.get(api)
        if str(response.status_code) == "200":
            return response.json()["IsHoneypot"]
        return honeypot_result
