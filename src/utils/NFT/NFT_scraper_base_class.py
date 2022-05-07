class NFT_scraper_base_class:

    def __init__(self) -> None:
        pass

    def get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    def remove_duplicate(self, target_list: list):
        return [dict(t) for t in {tuple(d.items()) for d in target_list}]