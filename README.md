# **Introduction**
- This project aims to scrape crypto token's information from some of the most popular exchanges or cryptocurrency data aggregator

# **Setup**
- Run the following command to install the necessary dependencies
```python
pipenv install
```

# **1. Token Info Generator**
- Retrieve token's information based on either **SYMBOL**, **NAME** or **ADDRESS**
- Chains and Networks covered currently:
```
1. Arbitrum
2. Astar
3. Aurora
4. Avalanche
5. Binance Smart Chain
6. Celo
7. Cronos
8. DeFi Kingdoms
9. Ethereum
10. Fantom
11. Fuse
12. Harmony
13. Heco
14. Iotex
15. Kucoin
16. Metis
17. Milkomeda
18. Moonbeam
19. Moonriver
20. Oasis
21. OEC
22. OPtimisim
23. Polygon
24. Telos
25. Velas
```
# **Information Generated**

| Field | Example          |
|---------|----------------|
| Token details     | name, network, address, symbol, decimals, holders count, total supply |
| Pricing details     | price, volume, liquidity    |
| Gas details   | gas price, cumulative gas used    |
| Pairing details | pairing address, exchange, pair type, base and target token's info |
# **Usage**
```python
>>> import dextools_scraper

>>> my_dextools_scraper = dextools_scraper()
... search_string = "APE"
... for index,token in enumerate(my_dextools_scraper.get_tokens(search_string)):
...     # print all token's address with "APE" as symbol or similar
...     print(token["network"] + "; " + token["address"])

(0) ApeCoin; ethereum; 0x4d224452801aced8b2f0aebe155379bb5d594381
(1) APE MOON; bsc; 0xf5b21a18a510cd315dd9f46d3c117321f1851d51
(2) BORD APE NIKE TOKEN; polygon; 0x9a575498ce240fe43504f53d68eef6440f0cf280
(3) Ape-X; avalanche; 0xd039c9079ca7f2a87d632a9c0d7cea0137bacfb5
...
```
## **Parameteres**
1. **search_string**: str, token's name, symbol, or address that wanted to be searched

# **2. Honeypot Detector**
- Determine if a token is a honeypot (crypto scam)
- Chains and Networks supported currently:
```
1. Binance Smart Chain
2. Ethereum
3. Fantom
4. Polygon
```
# **Usage**
```python
>>> import honeypot_scraper

>>> my_honeypot_scraper = honeypot_scraper()
... network = "Binance Smart Chain"
... address = "0x7ccE94C0B2C8aE7661f02544E62178377Fe8cF92"
... honeypot_result = my_honeypot_scraper.check_honey(network = network,address = address )

# based on 2 honeypot sources, 2 failed to detected honeypot, 0 detected honeypot
{'message': 'Checked 2 honeypot source(s)', 'non_honeypot': 2, 'is_honeypot': 0}
```
## **Parameteres**
1. **network**: str, must be either of one of the 4 networks above
2. **address**: str, token's address that would like to check for honeypot

# **3. GameFi Token Info Generator**
## **By Category**
- Retrieve GameFi token's info based on **CATEGORY**
- Example of GameFi token's category:
```
1. 2D PvP battler
2. 3D
3. Action
4. Adventure
5. Battle
6. Card
7. Collectibles
8. Combat
9. Idle Game
10. Fantasy
11. Metaverse
12. MOBA
13. MMORPG
14. NFTs
15. Party Game
16. Play to Earn
17. Puzzle
18. Racing
19. Real-Time Strategy
20. Role Playing
21. Simulation
22. Strategy
23. Tower Defense
......
and more
```

# **Usage**
```python
>>> import gamefi_scraper

>>> my_gamefi_scraper = gamefi_scraper()
... category_list = ["3D","Card"]
... for index, gamefi_token in enumerate(my_gamefi_scraper.search_by_category(category_list)):
...     print("(" + str(index) + ") " + gamefi_token["game_name"] + "; " +
...         gamefi_token["category"] + "; " + gamefi_token["description"])

(0) Splintershards; Card,Collectibles; Splinterlands is a unique digital trading card game that allows players to truly own their cards and other in-game assets.
(1) Gods Unchained; Card,Collectibles,Metaverse; Gods Unchained is a free-to-play tactical card game that gives players true ownership of their in-game items.
(2) Mytheria - Clash of Pantheons; Card,Turn-Based Strategy,Strategy; Mytheria is the first NFT game offering an exclusive Create to Earn feature for artists all over the world, with the name GodForge
...
```
## **Parameteres**
1. **category**: list, list of GameFi tokens category to filter