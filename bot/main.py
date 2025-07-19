# Version: 0.3
import discord
import aiohttp

USER_CHAT_HISTORY_QUEUE = []
BOT_CHAT_HISTORY_QUEUE = []

API_URL = 'http://llama:8000/v1/chat/completions'

# Get discord token from the file
try:
    with open("discord_token.txt", "r") as tokens:
        DISCORD_TOKEN = tokens.readline().strip()
except OSError:
    exit("Error: tokens.txt file not found.\nPlease create the file and add your discord bot token in the first line.")
# Get system input from the file
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


# Format chat history in one string
def format_chat_history():
    chat_history = "Previous messages: "
    for i in range(len(USER_CHAT_HISTORY_QUEUE)):
        chat_history += f"User message: {USER_CHAT_HISTORY_QUEUE[i]}"
        chat_history += f"Bot response: {BOT_CHAT_HISTORY_QUEUE[i]}"
    return chat_history


# Update chat queues to keep track of the last 6 messages
def update_chat_history(user_prompt, reply):
    if len(USER_CHAT_HISTORY_QUEUE) > 6:
        USER_CHAT_HISTORY_QUEUE.pop(0)
        BOT_CHAT_HISTORY_QUEUE.pop(0)
    USER_CHAT_HISTORY_QUEUE.append(user_prompt)
    BOT_CHAT_HISTORY_QUEUE.append(reply)
    print(f"Updated chat history >> {format_chat_history()}")


# Remove bot id/name from the message
def clean_message(message):
    user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()
    user_message = user_message.replace(f"<{bot.user.name}>", "").strip()
    return user_message


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
        # Create payload
        chat_history = format_chat_history()
        user_message = clean_message(message)
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama",
            "messages": [
                {"role": "system", "content": SYSTEM_INPUT},
                {"role": "assistant", "content": chat_history},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            async with message.channel.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.post(API_URL, json=payload, headers=headers) as response:
                        if response.status == 200:
                            # Get bot response and send to discord
                            data = await response.json()
                            bot_reply = data['choices'][0]['message']['content'].strip()
                            await message.channel.send(
                                bot_reply,
                                reference=message.to_reference(),
                                mention_author=False
                            )

                            print(f"Message from {message.author} >> {user_message}")
                            print(f"Reply from bot >> {bot_reply}")
                            update_chat_history(user_message, bot_reply)
                        else:
                            print(f"Error: bot returned >> {response.status}")
        except Exception as e:
            print(f"Error: failed to connect to bot >> {e}")


# Run bot
bot.run(DISCORD_TOKEN)
