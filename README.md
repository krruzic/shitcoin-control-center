# shitcoin-control-center
Simple python script to manage what you mine via a discord bot! Requires xmr-stak and Windows.


# Running
This only works on Windows. Make sure you have python3 installed and the `discord` module from pip. 


0. Head over to https://discordapp.com/developers/applications/me and create a new bot user. 
Copy down the Token and then generate an oauth url. Invite the bot to a server with NO OTHER members

1. Clone this repo and create a `bot.json` file with the following contents:
```json
{
  "token": "token_from_step0"
}
```

2. Make sure xmr-stak and all necessary config files (amd.txt, nvidia.txt, cpu.txt) are in the same folder

3. Double click `miner.py` and you're good to go! The default bot prefix is `!`


To run, clone this repo to a directory with xmr-stak inside. 

# Help
Read through the source :) you may want to modify xmr-stak-runner to your needs. I have it set to disable nvidia and cpu
so that I can game while my 2nd card mines.


# Notes
There's literally no error checking. Files are saved as `config.coin_name` and read the same way.
