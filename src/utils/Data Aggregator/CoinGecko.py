import requests


class CoinGecko_scraper:

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_str(input: str) -> bool:
        return True if isinstance(input, str) else False

    def get_token_details(self,
                          coingecko_id: str,
                          proxy_dict: dict = None) -> None:
        if not self.is_str(coingecko_id):
            raise TypeError("coingecko_id must be STRING type")
        api = "https://api.coingecko.com/api/v3/coins/{id}?tickers=false&market_data=false".format(
            id=coingecko_id)
        while True:
            response = requests.get(api)
            if str(response.status_code) == "200":
                response = response.json()

                # Basic information
                self.symbol = response["symbol"]
                self.name = response["name"]
                self.hashing_algorithm = response["hashing_algorithm"]

                # Platforms & Blockchain Site URL
                platforms = response["platforms"]
                # 1. Ethereum
                self.ethereum_address = platforms[
                    "ethereum"] if "ethereum" in platforms else None
                self.ethereum_site_url = "https://etherscan.io/token/{address}".format(
                    address=self.ethereum_address
                ) if self.ethereum_address else None
                # 2. Binance Smart Chain
                self.bsc_address = platforms[
                    "binance-smart-chain"] if "binance-smart-chain" in platforms else None
                self.bsc_ite_url = "https://bscscan.com/token/{address}".format(
                    address=self.bsc_address) if self.bsc_address else None
                # 3. Polygon
                self.polygon_address = platforms[
                    "polygon-pos"] if "polygon-pos" in platforms else None
                self.polygon_site_url = "https://polygonscan.com/token/{address}".format(
                    address=self.polygon_address
                ) if self.polygon_address else None
                # 4. Fantom
                self.fantom_address = platforms[
                    "fantom"] if "fantom" in platforms else None
                self.fantom_site_url = "https://ftmscan.com/token/{address}".format(
                    address=self.fantom_address
                ) if self.fantom_address else None
                # 5. Solana
                self.solana_address = platforms[
                    "solana"] if "solana" in platforms else None
                self.solana_site_url = "https://solscan.io//token/{address}".format(
                    address=self.solana_address
                ) if self.solana_address else None

                # Description
                self.description = response["description"]["en"]

                # Categories
                self.categories = [
                    category for category in response["categories"] if category
                ]

                # Links
                links = response["links"]
                self.homepages = [link for link in links["homepage"] if link]
                self.official_forum_url = [
                    link for link in links["official_forum_url"] if link
                ]
                self.chat_url = [link for link in links["chat_url"] if link]
                self.announcement_url = [
                    link for link in links["announcement_url"] if link
                ]

                # Community
                community = response["community_data"]
                # 1. Twitter
                twitter_screen_name = links["twitter_screen_name"]
                self.twitterUrl = "https://twitter.com/{twitter_screen_name}".format(
                    twitter_screen_name=twitter_screen_name
                ) if twitter_screen_name != "" else None
                self.twitter_followers = community["twitter_followers"]
                # 2. Telegram
                telegram_channel_identifier = links[
                    "telegram_channel_identifier"]
                self.telegramUrl = "https://t.me/{telegramChannelIdentifier}".format(
                    telegramChannelIdentifier=telegram_channel_identifier
                ) if telegram_channel_identifier != "" else None
                self.telegram_channel_user_count = community[
                    "telegram_channel_user_count"]
                # 3. Reddit
                self.reddit_url = community["subreddit_url"]

                # Scoring
                self.coingecko_rank = response["coingecko_rank"]
                self.coingecko_score = response["coingecko_score"]
                self.community_score = response["community_score"]
                self.liquidity_score = response["liquidity_score"]

                # Image
                self.image = requests.get(response["image"]["large"])

                # Last updated time
                self.last_updated = response["last_updated"]

            break