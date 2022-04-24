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
... for token_detail in (my_dextools_scraper.get_tokens(search_string)):
...     # print all token's address with "APE" as symbol or similar
...     print(token_detail["network"] + ", " + token_detail["address"])

arbitrum, 0x4d221c3a5c10a74c377a5909658e2a639b6edb5c
avalanche, 0x0802d66f029c46e042b74d543fc43b6705ccb4ba
bsc, 0x0b079b33b6e72311c6be245f9f660cc385029fc3
ethereum, 0x14dd7ebe6cb084cb73ef377e115554d47dc9d61e
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