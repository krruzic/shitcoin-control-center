import os
import json
import subprocess
import discord
from discord.ext.commands import Bot, Context
import glob
import asyncio

pool_item = {"pool_address" : "", "wallet_address" : "", "pool_password" : "x", "use_nicehash" : False, "use_tls" : False, "tls_fingerprint" : "", "pool_weight" : 1 }
stakrunnerpath = os.path.dirname(os.path.realpath(__file__))+"\XMR-STAK-RUNNER.bat"
basejson = json.loads("{"+open("config.base").read()+"}")
coins = [c.split(".")[1] for c in glob.glob('config*')]
config = json.load(open('bot.json'))

intensity = ["--noNVIDIA", "--noCPU"]

client = Bot(
        description="C&C for remote shitcoin mining",
        command_prefix='!',
        pm_help=False)

def reset_pool():
    global pool_item
    pool_item = {"pool_address" : "", "wallet_address" : "", "pool_password" : "x", "use_nicehash" : False, "use_tls" : False, "tls_fingerprint" : "", "pool_weight" : 1 }


# reads the fake shitty json xmr-stak uses and returns real json
def from_shitty_json(coin):
    with open('config.{}'.format(coin), 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        lines.insert(0, "{")
        lines[-1] = lines[-1].split(",")[0]+"}"
        f.seek(0)
        f.truncate()
        f.writelines(lines)


    return json.loads(open("config.{}".format(coin)).read())


# writes the fake shitty json xmr-stak wants and returns lines written
def to_shitty_json(coin, data):
    with open('config.{}'.format(coin), 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    with open('config.{}'.format(coin), 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[1:-1]
        lines[-1] = lines[-1]+","
        f.seek(0)
        f.truncate()
        f.writelines(lines)

    return lines



@client.command()
async def addcoin(coin_name, pool_addr, address):
    global pool_item, basejson, existing_coins

    if coin_name in coins:
        await client.say("Coin exists! Now mining {}!".format(coin_name))
        await start_mining(coin_name)
        return


    pool_item["pool_address"] = pool_addr
    pool_item["wallet_address"] = address

    writejson = basejson
    writejson["pool_list"] = [pool_item]
    to_shitty_json(coin_name, writejson)

    await client.say("Success. Run `!startmining {}` to mine.".format(coin_name))
    reset_pool()
    coins.append(coin_name)


@client.command()
async def getcoins():
    global coins
    await client.say("Coins available: {}".format(coins))


@client.command()
async def addpool(coin_name, pool_addr, address, weight):
    global pool_item, basejson, coins

    if not weight:
        weight = 1

    if coin_name not in coins:
        await client.say("Coin does not exist, cannot add a pool!")
        return

    current_pools = from_shitty_json(coin_name)

    pool_item["pool_address"] = pool_addr
    pool_item["wallet_address"] = address
    pool_item["pool_weight"] = weight
    current_pools.append(pool_item)

    to_shitty_json(coin_name, current_pools)  

    await client.say("Pool successfully added to: {}!".format(coin_name))
    reset_pool()


@client.command()
async def getpools(coin_name): 
    data = from_shitty_json(coin_name)
    em = discord.Embed(title="Pools for {}".format(coin_name),colour=discord.Colour(0xD4AF37))
    em.description = "```json\n{}```".format(json.dumps(data["pool_list"]))

    to_shitty_json(coin_name, data)
    await client.say(embed = em)

@client.command()
async def m(coin_name):
    global intensity

    if coin_name not in coins:
        await client.say("Coin doesn't exist!")
        return

    os.system("taskkill /im xmr-stak.exe")
    p = subprocess.Popen([stakrunnerpath, intensity[0], intensity[1], "config.{}".format(coin_name)], shell=True, stdout = subprocess.PIPE)

    await client.say("Now mining {}!".format(coin_name))
    await client.say("{} was called.".format(p.args))


@client.command()
async def ci(intense):
    global intensity

    if intense == "high":
        intensity = ["", ""]
        await client.say("Set intensity to high!")

    else:
        intensity = ["--noNVIDIA", "--noCPU"] # change to your liking
        await client.say("Set intensity to low!")


@client.command()
async def i():
    global intensity

    await client.say("Intensity is: **{}**".format(intensity))


client.run(config['token'])
