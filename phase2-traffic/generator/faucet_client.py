import json, requests
from eth_account import Account

FAUCET_URL = "http://faucet.astria.127.0.0.1.nip.io/api/fund"
OUT_FILE = "../config/wallets.json"

def create_accounts(n=5):
    accs = [Account.create() for _ in range(n)]
    data = [{"address": a.address, "private_key": a.key.hex()} for a in accs]
    with open(OUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return data

def fund_accounts(accounts):
    for a in accounts:
        payload = {"address": a["address"], "amount": "1000000000000000000"}  # 1 RIA
        r = requests.post(FAUCET_URL, json=payload, timeout=10)
        if r.status_code == 200:
            print(f"[ok] funded {a['address']}")
        else:
            print(f"[fail] {a['address']} → {r.text}")

if __name__ == "__main__":
    accounts = create_accounts(5)
    fund_accounts(accounts)