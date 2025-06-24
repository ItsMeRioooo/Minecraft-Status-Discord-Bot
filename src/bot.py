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

import discord
import os
import asyncio
from dotenv import load_dotenv
from mc_status import get_server_status
import datetime

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
SERVER_IP = os.getenv('MINECRAFT_SERVER_IP')
SERVER_PORT = int(os.getenv('MINECRAFT_SERVER_PORT'))
SERVER_NAME = os.getenv('SERVER_NAME', 'Minecraft Server')
SERVER_IMAGE = os.getenv('SERVER_IMAGE', None)
SERVER_COLOR = os.getenv('SERVER_COLOR', '#00ff00')
MESSAGE_ID_FILE = "status_message_id.txt"

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
        player_names = [
            name.replace('§', '') for name in player_names
            if name.lower() != "anonymous player"
        ]

        if status:
            embed = discord.Embed(
                title=f"{SERVER_NAME} Status",
                description="🟢 **Server is online!**",
                color=parse_color(SERVER_COLOR)
            )
            embed.add_field(name="Player Count", value=str(player_count), inline=False)
            embed.add_field(
                name="Players",
                value=f"```\n{chr(10).join(player_names) if player_names else 'None'}\n```",
                inline=False
            )
        if SERVER_IMAGE:
            embed.set_thumbnail(url=SERVER_IMAGE)

        now = datetime.datetime.now().strftime("%I:%M %p").lower()
        embed.set_footer(text=f"Last update: {now} • Updates every 30s")

        if message is None:
            message = await channel.send(embed=embed)
            with open(MESSAGE_ID_FILE, "w") as f:
                f.write(str(message.id))
        else:
            await message.edit(embed=embed)

        await asyncio.sleep(30)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(send_status_update())

client.run(TOKEN)