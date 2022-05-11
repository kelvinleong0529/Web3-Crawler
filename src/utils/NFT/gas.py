from validation import Validation


class Gas(Validation):

    api = "https://api.nftbase.com/web/api/v1/gas"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_current_gas(cls, proxy_dict: dict = None) -> str | None:
        """ returns current gas price
        """
        is_success, response = super().get_url_response(url=cls.api,
                                                        proxy_dict=proxy_dict)
        if is_success:
            return response["data"]
        return None