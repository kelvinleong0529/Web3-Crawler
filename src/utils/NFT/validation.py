from utility import Utlity


class Validation(Utlity):

    LIMIT = 50
    LIMIT_PER_PAGE = 20

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def validate_action_list(cls, input_list: list ) -> bool:
        """ validate the acion list to see if it's valid
        """

        if not super().is_list(input_list):
            raise TypeError("action_list must be LIST type")

        ACTION_LIST = ["buy", "sell", "mint", "receive", "send"]

        # remove any trailing whitespace and convert the elements to lower case
        input_list = [super().str_strip(element) for element in input_list]
        input_list = [super().str_lower(element) for element in input_list]

        if not set(input_list).issubset(set(ACTION_LIST)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return True

    @classmethod
    def update_limit(cls, new_limit: int) -> None:
        if not super().is_int(new_limit):
            raise TypeError("Limit to be updated must be INTEGER type")
        cls.LIMIT = new_limit

    @classmethod
    def update_limit_per_page(cls, new_limit_per_page: int) -> None:
        if not super().is_int(new_limit_per_page):
            raise TypeError(
                "Limit_per_page to be updated must be INTEGER type")
        cls.LIMIT_PER_PAGE = new_limit_per_page

    @classmethod
    def validate_limit(cls, limit: int | None) -> int:
        """ validate the "limit" parameter, and return default value if it's None
        """
        if super().is_none(limit):
            return cls.LIMIT
        if not super().is_int(limit):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    @classmethod
    def validate_limit_per_page(cls, limit_per_page: int | None) -> int:
        """ validate the "limit_par_page" parameter, and return default value if it's None
        """
        if super().is_none(limit_per_page):
            return cls.LIMIT_PER_PAGE
        if not super().is_int(limit_per_page):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page

    @classmethod
    def validate_price_range(cls, price_range: int | None) -> str:
        """ validate the "price_range" parameter, and convert it from int to string type
        """
        if super().is_none(price_range):
            return ""
        if not super().is_int(price_range):
            raise TypeError("price_range argument must be a INTEGER type")
        return super().int_to_str(price_range)

    @classmethod
    def get_sort_option(cls, sort_option: str) -> int:
        """ return sorting parameter based on sorting option input
        """
        if not super().is_str(sort_option):
            raise TypeError("sort_option must be STRING type argument")

        # sort option list
        # market cap = 1, latest = 2, etc ...
        SORT_OPTION_LIST = ["market cap", "latest", "oldest"]

        # remove any trailing whitespaces and convert the string to lower case
        sort_option = super().str_strip(sort_option)
        sort_option = super().str_lower(sort_option)

        # check and see if the sort option is valid
        if sort_option not in SORT_OPTION_LIST:
            raise ValueError(
                "Sort option must be either one of these: [Market Cap, Latest, Oldest]"
            )

        # return the corresponding sort parameter
        return SORT_OPTION_LIST.index(sort_option) + 1
