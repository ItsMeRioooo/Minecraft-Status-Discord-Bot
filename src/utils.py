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

def load_env_variables():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    
    return token, channel_id

def format_status_message(server_status, player_count, player_names):
    status = "Online" if server_status else "Offline"
    player_list = ", ".join(player_names) if player_names else "No players online"
    
    message = f"Server Status: {status}\nPlayer Count: {player_count}\nPlayers: {player_list}"
    return message