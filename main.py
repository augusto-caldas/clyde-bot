# Version: 0.1
import discord
import aiohttp

DISCORD_TOKEN = ""
API_URL = 'http://localhost:8000/v1/chat/completions'
with open("tokens.txt", "r") as tokens:
    DISCORD_TOKEN = tokens.readline().strip()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot is online and running as >> {client.user}")


@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    bot_name = client.user.name.lower()

    # Check if the bot is mentioned or its name is in the message content
    mentioned = client.user.mentioned_in(message)
    name_in_message = bot_name in message.content.lower()

    if mentioned or name_in_message:
        await message.channel.typing()
        user_prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "llama",
                "messages": [
                    {"role": "user", "content": user_prompt}
                ]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, json=payload, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        reply = data['choices'][0]['message']['content'].strip()
                    else:
                        reply = f"Error: LLaMA API returned {resp.status}"
        except Exception as e:
            reply = f"Failed to connect to LLaMA: {e}"

        await message.channel.send(reply)


# Run bot
client.run(DISCORD_TOKEN)
