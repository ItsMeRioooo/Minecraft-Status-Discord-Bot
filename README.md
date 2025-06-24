# Minecraft Status Discord Bot

This project is a Discord bot that tracks the status of a Minecraft server. It provides updates on the server's online/offline status, player count, and player names in a specified Discord channel using a rich embed.


![image](https://github.com/user-attachments/assets/cdc4d310-155d-4e01-a718-e8ce89c79c0b)


## Features

- Periodically checks the status of a Minecraft server every 30 seconds.
- Sends updates to a configurable Discord channel.
- Displays the server's online/offline status, player count, and player names.
- Embed color, server name, and image are configurable via `.env`.
- Clean, readable embed and footer.

## Requirements

- Python 3.7 or higher
- [discord.py](https://pypi.org/project/discord.py/)
- [mcstatus](https://pypi.org/project/mcstatus/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd minecraft-status-discord-bot
   ```

2. **Install dependencies:**
   Make sure you have `pip` installed, then run:
   ```bash
   pip install -r requirements.txt
   ```


3. **Create a `.env` file:**
   In the root directory of the project, create a `.env` file and add the following lines:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   CHANNEL_ID=your_discord_channel_id
   SERVER_COLOR=#FF0000
   SERVER_NAME=Your Server Name
   SERVER_IMAGE=https://your-image-url.png
   MINECRAFT_SERVER_IP=your.minecraft.server.ip
   MINECRAFT_SERVER_PORT=25565
   ```

   - **DISCORD_TOKEN**: Your Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications))
   - **CHANNEL_ID**: The ID of the channel where the bot will post
   - **SERVER_COLOR**: Embed color in hex (e.g., `#00ff00`)
   - **SERVER_NAME**: The display name for your server
   - **SERVER_IMAGE**: (Optional) Image URL for the embed thumbnail
   - **MINECRAFT_SERVER_IP**: Your Minecraft server IP or hostname
   - **MINECRAFT_SERVER_PORT**: Your Minecraft server port (default: 25565)

4. **Run the bot:**
   Execute the following command to start the bot:
   ```bash
   python src/bot.py
   ```

## Usage

Once the bot is running, it will automatically send and update status embeds in the specified Discord channel every 30 seconds. You can customize the server address, channel ID, and embed appearance in the `.env` file.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the bot.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
