# **Introduction**
- This project aims to scrape crypto token's information from some of the most popular exchanges or cryptocurrency data aggregator

# **Setup**
- Run the following command to install the necessary dependencies
```python
pipenv install
```

# **1. Token Info Generator**
- Retrieve token's information based on either **SYMBOL**, **NAME** or **ADDRESS**
- Chains and Netorks covered currently:
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
- The following information can be generated
1. **Token details**, eg: token's name, address, symbol, decimals, holders count, total supply
2. **Pricing detials**, eg: price, Volume, Liquidity
3. **Gas details**, eg: gas price, cumulative gas used
4. **Pairing details**, eg: pairing address, exchange, pair type, base and target token's info
```python
import dextools_scraper

my_dextools_scraper = dextools_scraper()
for index, token_detail in enumerate(my_dextools_scraper.get_tokens("APE")):
    # eg: print the address of all tokens with "APE" as symbol
    print(token_detail["address"])
```

# **2. Honeypot Validator**
