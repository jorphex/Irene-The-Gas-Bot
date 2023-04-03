# Irene The Gas Bot
Simple gas tracker bot for Discord servers.
### Features
- Irene
- Shows gas price in nickname as often as Discord and your RPC allows
- Changes role to show different name colors when above or below threshold.
- Changes emoji before gas price when above or below threshold
- Changes avatar when above or below thresold
- Updates avatar and role only when threshold is crosssed in either direction to avoid redundant updates, rate limiting, and wasted API calls.

### How to use
- Setup Discord bot in Discord developer portal with permisions to manage roles and change nickname.
- In your Discord server, create roles "Normal Gas Price" and "High Gas Price"
- Set the colors of these two roles to anything you want.
- In `gas_bot.py`, replace `RPC_ENDPOINT` with your or any RPC endpoint.
- Replace `update_interval` to you preferred interval.
- Replace `threshold` to any value you want for your chain and usecase.
- Replace `avatar_urls` with your image URLS. Defaults are the two images below.
- In `Dockefile`, define `SERVER_ID` with your server's ID.
- Define `DISCORD_BOT_TOKEN` with your bot token from Discord developer portal.
- Run gas_bot.py in Docker container: `docker run -d --restart always --name gas-bot gas-bot`

![irene](https://i.imgur.com/ZLI3tKj.jpg) ![irene](https://i.imgur.com/9rkhxVw.png)

### Setup
- Install Docker: `sudo apt-get update` `sudo apt-get install docker.io`
- Clone this repo: `git clone https://github.com/jorphex/Irene-The-Gas-Bot.git`
- Navigate to folder containing relevant files: `cd ~/Irene-The-Gas-Bot/discord-bot`
- Build image: `docker build -t gas-bot .`
- Run: `docker run -d --restart=always --name gas-bot-container gas-bot`

### Other commands for troubleshooting
- Build it: `docker build -t gas-bot .`
- Run it: `docker run -d --restart always --name gas-bot gas-bot`
- Stop it: `docker stop gas-bot`
- Remove it: `docker rm $(docker ps -a -q)`
- Remove it: `docker rmi $(docker ps images -q)`
- Watch it: `docker logs gas-bot`
- Restart it: `docker restart gas-bot`
