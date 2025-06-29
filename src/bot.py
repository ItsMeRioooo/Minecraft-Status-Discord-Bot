# MIT License
# 
# Copyright (c) 2025 ItsMeRiooooPH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Color codes for console output
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

def print_bootup():
    print(GREEN + r"""
███╗░░░███╗██╗███╗░░██╗███████╗░█████╗░██████╗░░█████╗░███████╗████████╗
████╗░████║██║████╗░██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██╔████╔██║██║██╔██╗██║█████╗░░██║░░╚═╝██████╔╝███████║█████╗░░░░░██║░░░
██║╚██╔╝██║██║██║╚████║██╔══╝░░██║░░██╗██╔══██╗██╔══██║██╔══╝░░░░░██║░░░
██║░╚═╝░██║██║██║░╚███║███████╗╚█████╔╝██║░░██║██║░░██║██║░░░░░░░░██║░░░
╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░░░░╚═╝░░░
""" + GREEN + r"""
          ░██████╗████████╗░█████╗░████████╗██╗░░░██╗░██████╗
          ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║░░░██║██╔════╝
          ╚█████╗░░░░██║░░░███████║░░░██║░░░██║░░░██║╚█████╗░
          ░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██║░░░██║░╚═══██╗
          ██████╔╝░░░██║░░░██║░░██║░░░██║░░░╚██████╔╝██████╔╝
          ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░╚═════╝░
""" + BLUE + r"""
                     Minecraft Status Discord Bot
        https://github.com/ItsMeRioooo/Minecraft-Status-Discord-Bot
""" + RESET)

import discord
import os
import asyncio
from dotenv import load_dotenv
from mc_status import get_server_status
from mcstatus import JavaServer
import datetime

load_dotenv()
print_bootup()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
SERVER_IP = os.getenv('MINECRAFT_SERVER_IP')
SERVER_PORT = os.getenv('MINECRAFT_SERVER_PORT')
SERVER_NAME = os.getenv('SERVER_NAME', 'Minecraft Server')
SERVER_IMAGE = os.getenv('SERVER_IMAGE', None)
SERVER_COLOR = os.getenv('SERVER_COLOR', '#00ff00')

# 🔧 Modified to replace "\n" with actual line breaks
SERVER_VERSION = os.getenv('SERVER_VERSION', 'Unknown').replace("\\n", "\n")

MESSAGE_ID_FILE = "status_message_id.txt"

missing = []
if not TOKEN:
    missing.append("DISCORD_TOKEN")
if not CHANNEL_ID:
    missing.append("CHANNEL_ID")
if not SERVER_IP:
    missing.append("MINECRAFT_SERVER_IP")
if not SERVER_PORT:
    missing.append("MINECRAFT_SERVER_PORT")

if missing:
    print(f"[ERROR] Missing required environment variables: {', '.join(missing)}")
    print("Please check your .env file and set the required values.")
    exit(1)

CHANNEL_ID = int(CHANNEL_ID)
SERVER_PORT = int(SERVER_PORT)

def parse_color(color_str):
    color_str = color_str.lstrip('#')
    return int(color_str, 16)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_status_update():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    message = None

    if os.path.exists(MESSAGE_ID_FILE):
        with open(MESSAGE_ID_FILE, "r") as f:
            try:
                msg_id = int(f.read().strip())
                message = await channel.fetch_message(msg_id)
            except Exception:
                message = None

    while not client.is_closed():
        status, player_count, player_names = get_server_status(SERVER_IP, SERVER_PORT)
        max_players = 0
        if status:
            server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
            try:
                max_players = server.status().players.max
            except Exception:
                max_players = "?"

            embed = discord.Embed(
                title=f"{SERVER_NAME} Status",
                description="🟢 **ONLINE**",
                color=parse_color(SERVER_COLOR)
            )
            embed.add_field(
                name="PLAYERS",
                value=f"{player_count}/{max_players}",
                inline=False
            )
            embed.add_field(
                name="SERVER ADDRESS",
                value=f"**IP:** `{SERVER_IP}`\n**Port:** `{SERVER_PORT}`",
                inline=True
            )
            embed.add_field(
                name="VERSION",
                value=SERVER_VERSION,
                inline=False  # Changed to False for better newline support
            )
            embed.add_field(
                name="",
                value=f"```\n{chr(10).join(player_names) if player_names else 'None'}\n```",
                inline=False
            )
        else:
            embed = discord.Embed(
                title=f"{SERVER_NAME} Status",
                description="🔴 **OFFLINE**",
                color=0xff0000
            )

        if SERVER_IMAGE:
            embed.set_thumbnail(url=SERVER_IMAGE)

        now = datetime.datetime.now().strftime("%I:%M %p").lower()
        embed.set_footer(text=f"Minecraft Server Status • Today at {now}")

        if message is None:
            message = await channel.send(embed=embed)
            with open(MESSAGE_ID_FILE, "w") as f:
                f.write(str(message.id))
            print(f"[INFO] Sent new status message at {now}")
        else:
            await message.edit(embed=embed)
            print(f"[INFO] Updated status message at {now}")

        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{player_count} players online"
            )
        )
        await asyncio.sleep(30)

print(GREEN + f"[INFO] Server Name: {SERVER_NAME}" + RESET)
print(GREEN + f"[INFO] Server IP: {SERVER_IP}:{SERVER_PORT}" + RESET)
print(GREEN + f"[INFO] Discord Channel ID: {CHANNEL_ID}" + RESET)
print(GREEN + f"[INFO] Embed Color: {SERVER_COLOR}" + RESET)
print(BLUE + "[INFO] Bot is starting up...\n" + RESET)

async def print_server_status():
    status, player_count, _ = get_server_status(SERVER_IP, SERVER_PORT)
    if status:
        print(GREEN + f"[INFO] Server is ONLINE | Players: {player_count}" + RESET)
    else:
        print(RED + f"[INFO] Server is OFFLINE" + RESET)

@client.event
async def on_ready():
    print(BLUE + f'Logged in as {client.user}' + RESET)
    client.loop.create_task(send_status_update())
    await print_server_status()

client.run(TOKEN)
