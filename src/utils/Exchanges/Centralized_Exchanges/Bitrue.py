import requests


class BitrueScraper:

    __api = "https://www.bitrue.com/exchange-web/web/tokenInfo/full?coinName={token_symbol}&language=en&appName=Netscape&appCodeName=Mozilla&appVersion=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&userAgent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F100.0.4896.60+Safari%2F537.36&cookieEnabled=true&platform=Win32&userLanguage=en-US&vendor=Google+Inc.&onLine=true&product=Gecko&productSub=20030107&mimeTypesLen=4&pluginsLen=3&javaEnbled=false&windowScreenWidth=1920&windowScreenHeight=1080&windowColorDepth=24&bitrueLanguage=en_US&token="

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_none(input: None) -> bool:
        return True if input is None else False

    @staticmethod
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

    @classmethod
    def get_value(cls, input_dict: dict, key: str) -> dict | list | str:
        if not cls.is_dict(input_dict):
            raise TypeError("Only accepts dictionary as arguments")
        if key not in input_dict:
            return "N/A"
        if cls.is_dict(input_dict[key]) or cls.is_list(input_dict[key]):
            return input_dict[key]
        else:
            return str(input_dict[key])

    @classmethod
    def get_url_response(cls, url: str, proxy_dict: dict | None) -> tuple:
        """ make a GET request to the url end point, and return the response in json format
        """
        if not cls.is_str(url):
            raise TypeError("Invalid URL / API passed!")
        if not (cls.is_dict(proxy_dict) or cls.is_none(proxy_dict)):
            raise TypeError("proxy_dict must be DICTIONARY type")

        # is_sucess TRUE means successful GET request
        is_success, response = None, None
        try:
            response = requests.get(url=url, proxies=proxy_dict)
            is_success = True
            response = response.json()
        except requests.ConnectionError as e:
            print(
                "Connection Error, make sure you are connected to the Internet!"
            )
            print(str(e))
            is_success = False
        except requests.Timeout as e:
            print("Timeout Error!")
            print(str(e))
            is_success = False
        except requests.RequestException as e:
            print("General Error, something unexpected happen!")
            print(str(e))
        except KeyboardInterrupt:
            print("Program was forced to close externally")
        return (is_success, response)

    @classmethod
    def get_token_details(cls,
                          token_symbol: str,
                          proxy_dict: dict = None) -> dict:

        if not cls.is_str(token_symbol):
            raise TypeError("token_symbol should be in STRING format")

        # make GET reqeust to the API endpoint
        api = cls.__api.format(token_symbol=token_symbol)
        is_success, response = cls.get_url_response(url=api,
                                                    proxy_dict=proxy_dict)

        # create a dict to store the scraped results
        token_details = {}

        if is_success:

            data = response["data"]

            # token details
            coin_info = cls.get_value(data, "coinInfo")
            token_details["coin_name"] = cls.get_value(coin_info, "coinName")
            token_details["name_3rd"] = cls.get_value(coin_info, "name3rd")
            token_details["abbreviate"] = cls.get_value(
                coin_info, "abbreviate")

            # token basic details
            base_info = cls.get_value(coin_info, "baseInfo")
            token_details["max_supply"] = cls.get_value(base_info, "maxSupply")
            token_details["total_coin_supply"] = cls.get_value(
                base_info, "totalCoinSupply")
            token_details["available_supply"] = cls.get_value(
                base_info, "availableSupply")
            token_details["consensus_method"] = cls.get_value(
                base_info, "consensusMethod")
            token_details["algorithm"] = cls.get_value(base_info, "algorithm")
            token_details["description"] = cls.get_value(
                base_info, "description")
            token_details["whitepaper"] = cls.get_value(
                base_info, "whitePaper")

            # token website and social media URLs
            token_details["twitter_link"] = cls.get_value(
                base_info, "twitterLink")
            token_details["github_link"] = cls.get_value(
                base_info, "githubLink")
            token_details["algorithm"] = cls.get_value(base_info, "algorithm")
            token_details["one_level_industry"] = cls.get_value(
                base_info, "oneLevelIndustry")
            token_details["two_level_industry"] = cls.get_value(
                base_info, "twoLevelIndustry")
            token_details["cmc_url"] = cls.get_value(coin_info, "cmcUrl")

            # token supply info
            supply_info = cls.get_value(coin_info, "supplyInfo")
            token_details["supply_rate"] = cls.get_value(
                supply_info, "supplyRate")
            token_details["market_cap"] = cls.get_value(
                supply_info, "marketCap")
            token_details["rate"] = cls.get_value(supply_info, "rate")
            token_details["rank"] = cls.get_value(supply_info, "rank")
            token_details["industry"] = cls.get_value(supply_info, "industry")

            # token market info
            market_info = cls.get_value(data, "marketInfo")
            token_details["current_price"] = cls.get_value(
                market_info, "currentPrice")
            token_details["increase"] = cls.get_value(market_info, "increase")

            # token relevant symbols
            symbols = cls.get_value(market_info, "symbols")
            token_details["symbols"] = [symbol for symbol in symbols]

        return token_details