import requests
import sys

sys.stdout.reconfigure(encoding="utf-8")


def get_token_data(token_address):
    response = requests.post(
        "https://mainnet.helius-rpc.com/?api-key=2c24f9c1-c106-4648-a766-6493fadd9590",
        headers={"Content-Type": "application/json"},
        json={
            "jsonrpc": "2.0",
            "id": "test",
            "method": "getAsset",
            "params": {"id": token_address},
        },
    )
    data = response.json()
    result = data["result"]
    price_per_token = result["token_info"]["price_info"]["price_per_token"]
    image_url = result["content"]["links"]["image"]

    token_data = {}
    token_data["price"] = float(price_per_token)
    token_data["image"] = image_url
    return token_data


token_data = get_token_data("9psiRdn9cXYVps4F1kFuoNjd2EtmqNJXrCPmRppJpump")
token_image = token_data["image"]
print(token_image, token_data["price"])
