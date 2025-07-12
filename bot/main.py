# Version: 0.1
import discord
import aiohttp

API_URL = 'http://llama:8000/v1/chat/completions'
try:
    with open("tokens.txt", "r") as tokens:
        DISCORD_TOKEN = tokens.readline().strip()
except OSError:
    exit("Error: tokens.txt file not found.\nPlease create the file and add your discord bot token in the first line.")

try:
    with open("system_input.txt", "r") as system_input:
        SYSTEM_INPUT = system_input.readline().strip()
except OSError:
    print("Warning: system_input.txt file not found.\nSetting empty system input.")
    SYSTEM_INPUT = ""

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online and running as >> {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bot_name = bot.user.name.lower()
    is_mentioned = bot.user.mentioned_in(message)
    is_name_in_message = bot_name in message.content.lower()

    if is_mentioned or is_name_in_message:
        print(f"Message from {message.author} >> {message.clean_content}")

        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama",
            "messages": [
                {"role": "system", "content": SYSTEM_INPUT},
                {"role": "user", "content": message.clean_content}
            ]
        }

        try:
            async with message.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.post(API_URL, json=payload, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            reply = data['choices'][0]['message']['content'].strip()
                            print(f"Reply from bot >> {reply}")
                            await message.channel.send(
                                reply,
                                reference=message.to_reference(),
                                mention_author=False
                            )
                        else:
                            print(f"Error, bot returned >> {resp.status}")
        except Exception as e:
            print(f"Failed to connect to bot >> {e}")


# Run bot
bot.run(DISCORD_TOKEN)
