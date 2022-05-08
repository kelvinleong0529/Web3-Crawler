import datetime


class NFT_scraper_base_class:

    def __init__(self) -> None:
        self.LIMIT_PER_PAGE = 20
        self.LIMIT = 50

    def get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    def remove_duplicate(self, target_list: list):
        return [dict(t) for t in {tuple(d.items()) for d in target_list}]

    def utc_from_timestamp(self, timestamp: str) -> str:
        try:
            return str(
                datetime.datetime.utcfromtimestamp(
                    int(timestamp)).strftime("%Y-%m-%d %H:%M:%S"))
        except:
            return "N/A"