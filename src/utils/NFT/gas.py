from validation import Validation


class Gas(Validation):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_gas(proxy_dict: dict = None) -> str | None:
        api = "https://api.nftbase.com/web/api/v1/gas"
        is_success, response = super().get_url_response(url=api,
                                                        proxy_dict=proxy_dict)
        if is_success:
            return response["data"]
        return None