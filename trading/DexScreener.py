import requests


class DexScanner:

    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex/tokens/"

    def fetchTokensData(self, tokens):
        response = requests.get(f"{self.base_url}{','.join(tokens)}")
        data = response.json()["pairs"][0]

        token_data = {
            "name": data["baseToken"]["name"],
            "symbol": data["baseToken"]["symbol"],
            "marketCap": data["marketCap"],
            "imageUrl": data["info"]["imageUrl"],
            "priceUsd": data["priceUsd"],
        }

        return token_data


dexScreener = DexScanner()

token_data = dexScreener.fetchTokensData(
    ["9psiRdn9cXYVps4F1kFuoNjd2EtmqNJXrCPmRppJpump"]
)
print(token_data)
