import requests
import json


class CoinGeckoScraper:

    __api = "https://api.coingecko.com/api/v3/coins/{id}?tickers=false&market_data=false"

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    @staticmethod
    def is_dict(input: dict) -> bool:
        return True if isinstance(input, dict) else False

    @staticmethod
    def is_list(input: list) -> bool:
        return True if isinstance(input, list) else False

    @staticmethod
    def is_none(input: None) -> bool:
        return True if input is None else False

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
    def get_url_response(cls, url: str,
                         proxy_dict: dict | None) -> tuple[bool, str]:
        """
        Make a GET request to url endpoint and return the result in JSON format

        Args:
            url (str): API / URL endpoint
            proxy_dict (dict | None): Proxy Settings Parameter

        Raises:
            TypeError: when 'url' passed is not STR
            TypeError: when 'proxy_dict' is not DICT

        Returns:
            tuple[bool, str]: 1st value -> true indicates successful request and vice versa, 2nd value -> GET response in JSON format
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
                          coingecko_id: str,
                          proxy_dict: dict = None) -> dict:
        """
        Get the token's following details based on Coin Gecko token ID:
        1. Basic information -> token name, symbol, hashing algorithm
        2. Links -> Official forum URL, homepages, chat URL, announcement URL
        3. Community -> Twitter, Telegram, Reddit
        4. Scoring -> Coin Gecko rank & score, community score, liquidity score
        5. Image

        Args:
            coingecko_id (str): Coin Gecko Token ID
            proxy_dict (dict, optional): Proxy Settings Parameter. Defaults to None.

        Raises:
            TypeError: when 'coingecko_id' is not STR

        Returns:
            dict: token's details
        """

        # validate the input parameters
        if not cls.is_str(coingecko_id):
            raise TypeError("coingecko_id must be STRING type")

        # make GET request to the API endpoint
        api = cls.__api.format(id=coingecko_id)
        is_success, response = cls.get_url_response(url=api,
                                                    proxy_dict=proxy_dict)

        # create a dict to store the scrape results
        token_details = {}

        if is_success:

            # Basic information
            token_details["symbol"] = cls.get_value(response, "symbol")
            token_details["name"] = cls.get_value(response, "name")
            token_details["hashing_algorithm"] = cls.get_value(
                response, "hashing_algorithm")
            token_details["public_notice"] = cls.get_value(
                response, "public_notice")
            token_details["additional_notice"] = cls.get_value(
                response, "additional_notice")

            # Description
            description = cls.get_value(response, "description")
            token_details["description"] = cls.get_value(description, "en")

            # Categories
            token_details["categories"] = [
                category for category in response["categories"] if category
            ]

            # Links
            links = response["links"]
            token_details["homepages"] = [
                link for link in links["homepage"] if link
            ]
            token_details["official_forum_url"] = [
                link for link in links["official_forum_url"] if link
            ]
            token_details["chat_url"] = [
                link for link in links["chat_url"] if link
            ]
            token_details["announcement_url"] = [
                link for link in links["announcement_url"] if link
            ]

            # Community
            community = cls.get_value(response, "community_data")
            # 1. Twitter
            twitter_screen_name = cls.get_value(links, "twitter_screen_name")
            if twitter_screen_name != "N/A":
                token_details[
                    "twitter_url"] = "https://twitter.com/{twitter_screen_name}".format(
                        twitter_screen_name=twitter_screen_name)
            token_details["twitter_followers"] = cls.get_value(
                community, "twitter_followers")
            # 2. Telegram
            telegram_channel_identifier = cls.get_value(
                links, "telegram_channel_identifier")
            if telegram_channel_identifier != "N/A":
                token_details[
                    "telegram_url"] = "https://t.me/{telegramChannelIdentifier}".format(
                        telegramChannelIdentifier=telegram_channel_identifier)
            token_details["telegram_channel_user_count"] = cls.get_value(
                community, "telegram_channel_user_count")
            # 3. Reddit
            token_details["reddit_url"] = cls.get_value(links, "subreddit_url")

            # Scoring
            token_details["coingecko_rank"] = cls.get_value(
                links, "coingecko_rank")
            token_details["coingecko_score"] = cls.get_value(
                links, "coingecko_score")
            token_details["community_score"] = cls.get_value(
                links, "community_score")
            token_details["liquidity_score"] = cls.get_value(
                links, "liquidity_score")

            # Image
            image = cls.get_value(response, "image")
            token_details["image"] = cls.get_value(response, "large")

            # Last updated time
            token_details["last_updated"] = cls.get_value(
                response, "last_updated")

        return token_details