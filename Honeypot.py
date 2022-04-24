import requests


class honeypot_scraper:

    # all the honeypot validate function returns True if detect honeypot and vice-versa

    def __init__(self) -> None:
        self.__network_pool = {
            "binance smart chain": {
                0: {
                    "function": self.__honeypot_is,
                    "network": "bsc2"
                },
                1: {
                    "function": self.__rugdoc,
                    "network": "bscscan"
                }
            },
            "ethereum": {
                0: {
                    "function": self.__honeypot_is,
                    "network": "eth"
                }
            },
            "fantom": {
                0: {
                    "function": self.__rugdoc,
                    "network": "ftmscan"
                }
            },
            "polygon": {
                0: {
                    "function": self.__rugdoc,
                    "network": "polygonscan"
                }
            }
        }

    def check_honeypot(self, network: str, address: str) -> dict:
        network = network.lower().strip()
        network_pool = self.__network_pool
        if network in network_pool:
            network_target = network_pool[network]
            is_honeypot = 0
            non_honeypot = 0
            source_checked = 0
            for network in network_target.items():
                honeypot_function = network[-1]["function"]
                honeypot_network = network[-1]["network"]
                # if function returns True means it's a HONEYPOT
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
    def __rugdoc(self, network: str, address: str) -> bool:
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
    def __honeypot_is(self, network: str, address: str) -> bool:
        api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}".format(
            address=address, network=network)
        honeypot_result = None
        response = requests.get(api)
        if str(response.status_code) == "200":
            return response.json()["IsHoneypot"]
        return honeypot_result
