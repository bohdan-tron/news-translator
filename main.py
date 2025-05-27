from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import os
from dotenv import load_dotenv
from telethon.tl.types import MessageEntityTextUrl
load_dotenv(dotenv_path='envs/.env')

api_id = int(os.environ.get('API_ID', 0))  # your api_id
api_hash = os.environ.get('API_HASH', 'hash')
session_name = 'news_translator'
source_channel = os.environ.get('SOURCE_CHANNEL', 'source_channel')
target_channel = os.environ.get('TARGET_CHANNEL', 'target_channel')
bot_token = os.environ.get('BOT_TOKEN', 'bot_token')

def insert_links(msg, entities):
    for entity in sorted(entities, key=lambda e: e.offset, reverse=True):
        if isinstance(entity, MessageEntityTextUrl):
            start = entity.offset
            end = start + entity.length
            text = msg[start:end]
            url = entity.url
            
            print(f"Found link: {text} ({url})")
                
            msg = msg[:start] + f'[{text}]({url})' + msg[end:]
    return msg

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message_text = event.message.message or ""
    
    # Translate to Ukrainian
    translated = GoogleTranslator(source='ru', target='uk').translate(text=message_text)
    translated = insert_links(translated, event.message.entities)
    
    # Send text with media if available
    if event.message.media:
        file = await event.message.download_media()
        await client.send_file(target_channel, file, caption=translated)
        os.remove(file)  # clean up local file
    else:
        await client.send_message(target_channel, translated)

client.start()
client.run_until_disconnected()