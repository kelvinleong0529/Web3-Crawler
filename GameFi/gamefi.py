import requests


class gamefi_scraper:

    def __init__(self) -> None:
        pass

    def __get_value(self, input_dict: dict, key: str) -> str:
        if isinstance(input_dict, dict):
            return input_dict[key] if key in input_dict else "N/A"
        return "N/A"

    def __search_by_category(self, category: str) -> list:
        page_index = 1
        token_detail_list = []
        while True:
            api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}&page={page_index}".format(category=category, page_index=page_index)
            response = requests.get(api)
            if str(response.status_code) == "200":
                data = response.json()["pageProps"]["data"]
                if page_index == data["lastPage"]:
                    break
                data = data["data"]
                for index,token_iterator in enumerate(data):
                    # initialize a dict to store the details
                    token = {}

                    # gamefi token details
                    token["game_name"] = self.__get_value(token_iterator,"game_name")
                    token["category"] = self.__get_value(token_iterator,"category")
                    token["developer"] = self.__get_value(token_iterator,"developer")
                    token["language"] = self.__get_value(token_iterator,"language")
                    token["description"] = self.__get_value(token_iterator,"short_description")

                    # gamefi token pricing info



api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}".format(
    category="Metaverse")
response = requests.get(api)
print(response.json()["pageProps"]["data"]["page"],
      response.json()["pageProps"]["data"]["lastPage"])
