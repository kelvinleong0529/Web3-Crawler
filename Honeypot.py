class honeypot:

    def __init__(self) -> None:
        self.__api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}"

    def check_honeypot(self, network: str, address: str) -> bool:
        api = self.__api.format(network=network, address=address)
