import os
import json
import subprocess
from pprint import pprint

pool_list = []
pool_item = {"pool_address" : "", "wallet_address" : "", "pool_password" : "x", "use_nicehash" : False, "use_tls" : False, "tls_fingerprint" : "", "pool_weight" : 10 }
coin = input("Add coin or start mining? ['add','mine']: ")

data = json.loads("{"+open("config.base").read()+"}")


if coin.upper() == "ADD":
    coin = input("Enter the name of the coin: ")
    more = "Y"
    while (more not in ["N", "n", "no"]):
        pool_item["pool_address"] = input("Enter pool URL with port: ").strip()
        pool_item["wallet_address"] = input("Enter your address: ").strip()
        pool_item["pool_weight"] = int(input("Weight: "))
        pool_list.append(pool_item)
        more = input("Add another pool? ")
    data["pool_list"] = pool_list

    with open('config.{}'.format(coin), 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    with open('config.{}'.format(coin), 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[1:-1]
        lines[-1] = lines[-1]+","
        f.seek(0)
        f.truncate()
        print(lines)
        f.writelines(lines)
else:
    coin = input("Enter the name of the coin: ")

print("\n\n\nNow mining {}!".format(coin))
filepath = "C:\\Users\\krruz\\Desktop\\CRYPTONOTE-COINS\\MINING\\XMR-STAK-RUNNER.bat"
print(filepath + " config.{}".format(coin))
p = subprocess.Popen([filepath, "config.{}".format(coin)], shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()
