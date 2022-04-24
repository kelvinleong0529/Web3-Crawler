import requests


class gamefi_scraper:

    def __init__(self) -> None:
        pass

    def __search_by_category(self, category: str) -> list:
        page_index = 1
        search_result = []
        while True:
            api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}&page={page_index}".format(category=category, page_index=page_index)
            response = requests.get(api)
            if str(response.status_code) == "200":
                data = response.json()["pageProps"]["data"]
                if page_index == data["lastPage"]:
                    break
                


api = "https://v2.gamefi.org/_next/data/05TfXTSF5_7vpLam60k8c/hub.json?category={category}".format(
    category="Metaverse")
response = requests.get(api)
print(response.json()["pageProps"]["data"]["page"],
      response.json()["pageProps"]["data"]["lastPage"])
