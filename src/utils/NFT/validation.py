from utility import Utlity


class Validation(Utlity):

    def __init__(self) -> None:
        super().__init__()

    def validate_action_list(self, input: list | None) -> bool:
        """ validate the acion list to see if it's valid
        """

        if super().is_none(input):
            return True

        if not super().is_list(input):
            raise TypeError("action_list must be LIST type")

        ACTION_LIST = ["buy", "sell", "mint", "receive", "send"]

        # remove any trailing whitespace and convert the elements to lower case
        input = [super().str_strip(element) for element in input]
        input = [super().str_lower(element) for element in input]

        if not set(input).issubset(set(ACTION_LIST)):
            raise ValueError(
                "action_list values can only be a subset of: [buy, sell, mint, receive, send]"
            )
        return True

    def validate_limit(self, limit: int | None) -> int:
        """ validate the "limit" parameter, and return default value if it's None
        """
        LIMIT = 20
        if super().is_none(limit):
            return LIMIT
        if not super().is_int(limit):
            raise TypeError("limit argument must be INTEGER type")
        return limit

    def validate_limit_per_page(self, limit_per_page: int | None) -> int:
        """ validate the "limit_par_page" parameter, and return default value if it's None
        """
        LIMIT_PER_PAGE = 50
        if super().is_none(limit_per_page):
            return LIMIT_PER_PAGE
        if not super().is_int(limit_per_page):
            raise TypeError("limit_per_page argument must be INTEGER type")
        return limit_per_page

    def validate_price_range(self, price_range: int | None) -> str:
        """ validate the "price_range" parameter, and convert it from int to string type
        """
        if super().is_none(price_range):
            return ""
        if not super().is_int(price_range):
            raise TypeError("price_range argument must be a INTEGER type")
        return super().int_to_str(price_range)

    def get_sort_option(self, sort_option: str) -> int:
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
