import requests


class honeypot:

    def __init__(self) -> None:
        self.__api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}"

    def check_honeypot(self, network: str, address: str) -> dict:
        api = self.__api.format(network=network, address=address)
        response = requests.get(api)
        honeypot_result = {}
        if str(response.status_code) == "200":
            response = response.json()
            honeypot_result["is_honeypot"] = response["IsHoneypot"]
            honeypot_result["max_tax_amount"] = response["MaxTxAmount"]
            honeypot_result["buy_tax"] = response["BuyTax"]
            honeypot_result["sell_tax"] = response["SellTax"]
            honeypot_result["buy_gas"] = response["BuyGas"]
            honeypot_result["sell_gas"] = response["SellGas"]

        return honeypot_result