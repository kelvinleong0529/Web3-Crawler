api = "https://api.opensea.io/api/v1/asset/0x2302021087377a9e6fced6e478d8714598eb2f2b/2546"
import requests

response = requests.get(api)
print(response.json())