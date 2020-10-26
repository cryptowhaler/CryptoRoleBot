import requests
import json


BASE_URL = "https://api.rally.io/v1"


def get_balances(rally_id):
    url = BASE_URL + "/users/rally/" + rally_id + "/balance"
    result = requests.get(url)
    if result.status_code != 200:
        print("Request error!")
        print(url)
        print(result.status_code)
        print(type(result.json()))
        print(result.json())
    return result.json()


def get_balance_of_coin(rally_id, coin_name):
    for coin_balance in get_balances(rally_id):
        if coin_balance["coinKind"] == coin_name:
            return float(coin_balance["coinBalance"])
    return 0.0