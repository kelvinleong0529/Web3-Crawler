class honeypot:
    def __init__(self) -> None:
        self.__api = "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain={network}&token={address}"

        