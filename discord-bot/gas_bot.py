import discord
import asyncio
import web3
import aiohttp
import os
from datetime import datetime
import sys

# Redirect stdout to stderr
sys.stdout = sys.stderr
client = discord.Client(intents=discord.Intents.all())
rpc_endpoint = "RPC_ENDPOINT"
update_interval = 15 # update interval in seconds
threshold = 500 # gas price threshold in gwei
avatar_urls = ["https://i.imgur.com/ZLI3tKj.jpg", "https://i.imgur.com/9rkhxVw.png"] # replace with your own image URLs
current_time = datetime.utcnow().strftime("%y/%b/%d %H:%M:%S UTC")

# function to fetch current gas prices
def get_gas_prices():
    w3 = web3.Web3(web3.HTTPProvider(rpc_endpoint))
    try:
        gas_price = w3.eth.gas_price
        gas_price_gwei = gas_price // 10**9 # divide to convert wei to gwei
        return gas_price_gwei
    except Exception as e:
        print(f"[{current_time}] Error fetching gas price: {e}. Retrying...")
        return None

# function to update bot name and avatar on server
async def update_bot():
    prev_role = None
    prev_avatar_url = None
    while True:
        current_time = datetime.utcnow().strftime("%y/%b/%d %H:%M:%S UTC")
        # Get current gas price and check if it's above or below the threshold
        try:
            gas_price = get_gas_prices()
        except Exception as e:
            print(f"[{current_time}] Error fetching gas price: {e}. Retrying...")
            gas_price = None
        if gas_price is not None:
            above_threshold = gas_price > threshold
            
            # Set the bot's nickname, role, and avatar based on the threshold condition
            bot_nickname = "🔥" if above_threshold else "⛽"
            bot_nickname += f" {gas_price} gwei"
            role_name = "High Gas Price" if above_threshold else "Normal Gas Price"
            avatar_url = avatar_urls[1] if above_threshold else avatar_urls[0]
            
            # Update the bot's name, role, and avatar on the server
            guild = client.get_guild(int(os.getenv('SERVER_ID')))
            if guild:
                member = guild.get_member(client.user.id)
                if member:
                    try:
                        # Wait for the member object to be fully loaded before making changes
                        await client.wait_until_ready()
                        
                        # Update nickname
                        if bot_nickname != member.nick:
                            await member.edit(nick=bot_nickname)
                            # Print message indicating the bot's nickname has been updated
                            print(f"[{current_time}] Nickname updated to {bot_nickname}")
                        else:
                            # Print message indicating that the nickname was not updated
                            print(f"[{current_time}] Gas is still {bot_nickname}, no nickname update needed.")

                        # Update role
                        role = discord.utils.get(guild.roles, name=role_name)
                        if role is None:
                            role = await guild.create_role(name=role_name)
                        
                        # Remove previous role if it exists and it's different from the new role
                        if prev_role and prev_role != role:
                            await member.remove_roles(prev_role)
                            # Print message indicating the bot's role has been removed
                            print(f"[{current_time}] Removed role {prev_role.name} from bot.")
                        
                        # Assign new role if it's different from the previous role
                        if role != prev_role:
                            await member.add_roles(role)
                            # Print message indicating the bot's role has been added
                            print(f"[{current_time}] Assigned role {role_name} to bot.")
                        
                        # Update previous role
                        prev_role = role
                        
                        # Update avatar
                        if avatar_url != prev_avatar_url:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(avatar_url) as resp:
                                    avatar_bytes = await resp.read()
                            try:                                
                                await client.user.edit(avatar=avatar_bytes)
                            except discord.errors.HTTPException as e:
                                print(f"[{current_time}] 😠 Error updating avatar: {e}. Retrying in {update_interval} seconds... 🔥")
                                await asyncio.sleep(update_interval)  # wait for update_interval seconds before trying again
                            prev_avatar_url = avatar_url
                            # Print message to show that the avatar has been updated
                            print(f"[{current_time}] ✨ Bot avatar updated to {avatar_url} ✨")
                        else:
                            # Print message indicating that the avatar was not updated
                            print(f"[{current_time}] Gas is still over {threshold}, no avatar update needed.")

                    except discord.Forbidden as e:
                        print(f"[{current_time}] Error: {e}")
        else:
            print(f"[{current_time}] Gas price is None, skipping update.")
        
        # Sleep until the next update
        await asyncio.sleep(update_interval)

# event listener for when the bot is ready
@client.event
async def on_ready():
    print(f"[{current_time}] Logged in as {client.user}")
    asyncio.ensure_future(update_bot())

# run the bot
client.run(os.getenv('DISCORD_BOT_TOKEN'))
