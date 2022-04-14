import requests

class CoinGecko:

    def __init__(self,coinGeckoId:str) -> None:
        self.__api = "https://api.coingecko.com/api/v3/coins/{Id}?tickers=false&market_data=false".format(Id=coinGeckoId)
        self.__getAllDetails()

    def __getAllDetails(self) -> None:
        while True:
            response = requests.get(self.__api)
            if str(response.status_code) == "200":
                response = response.json()

                # Basic information
                self.symbol = response["symbol"]
                self.name = response["name"]
                self.hashingAlgorithm = response["hashing_algorithm"]

                # Platforms & Blockchain Site URL
                platforms = response["platforms"]
                # 1. Ethereum
                self.ethereumAddress = platforms["ethereum"] if "ethereum" in platforms else None
                self.ethereumSiteUrl = "https://etherscan.io/token/{address}".format(address=self.ethereumAddress) if self.ethereumAddress else None
                # 2. Binance Smart Chain
                self.bscAddress = platforms["binance-smart-chain"] if "binance-smart-chain" in platforms else None
                self.bscSiteUrl = "https://bscscan.com/token/{address}".format(address=self.bscAddress) if self.bscAddress else None
                # 3. Polygon
                self.polygonAddress = platforms["polygon-pos"] if "polygon-pos" in platforms else None
                self.polygonSiteUrl = "https://polygonscan.com/token/{address}".format(address=self.polygonAddress) if self.polygonAddress else None
                # 4. Fantom
                self.fantomAddress = platforms["fantom"] if "fantom" in platforms else None
                self.fantomSiteUrl = "https://ftmscan.com/token/{address}".format(address=self.fantomAddress) if self.fantomAddress else None
                # 5. Solana
                self.solanaAddress = platforms["solana"] if "solana" in platforms else None
                self.solanaSiteUrl = "https://solscan.io//token/{address}".format(address=self.solanaAddress) if self.solanaAddress else None

                # Description
                self.description = response["description"]["en"]

                # Categories
                self.categories = [category for category in response["categories"] if category]

                # Links
                links = response["links"]
                self.homepages = [link for link in links["homepage"] if link]
                self.officialForumUrl = [link for link in links["official_forum_url"] if link]
                self.chatUrl = [link for link in links["chat_url"] if link]
                self.announcementUrl = [link for link in links["announcement_url"] if link]

                # Community
                community = response["community_data"]
                # 1. Twitter
                twitterScreenName = links["twitter_screen_name"]
                self.twitterUrl = "https://twitter.com/{twitterScreenName}".format(twitterScreenName=twitterScreenName) if twitterScreenName != "" else None
                self.twitterFollowers = community["twitter_followers"]
                # 2. Telegram
                telegramChannelIdentifier = links["telegram_channel_identifier"]
                self.telegramUrl = "https://t.me/{telegramChannelIdentifier}".format(telegramChannelIdentifier=telegramChannelIdentifier) if telegramChannelIdentifier != "" else None
                self.telegramChannelUserCount = community["telegram_channel_user_count"]
                # 3. Reddit
                self.redditUrl = community["subreddit_url"]

                # Scoring
                self.coinGeckoRank = response["coingecko_rank"]
                self.coinGeckoScore = response["coingecko_score"]
                self.communityScore = response["community_score"]
                self.liquidityScore = response["liquidity_score"]

                # Image
                self.image = requests.get(response["image"]["large"])

                # Last updated time
                self.lastUpdated = response["last_updated"]

            break