import nest_asyncio
import asyncio
from telethon import TelegramClient
from telethon import events
import tools
import re

nest_asyncio.apply()
memory = []
API_ID = ''
API_HASH = ''
sender = -1002306843892
reciever = -1002462696731


client = TelegramClient('my_new', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):

    if event.sender_id == sender:
        is_reply = handle_reply(event)
        if (is_reply):
            await client.send_message(reciever, f"Сделка по {is_reply} была отменена. Ордер закрыт")
            return

        if tools.Tools.isValidMessage(remove_formatting(event.text)):
            await event.forward_to(reciever)

            
def add_to_memmory(id, symbol):
    data = {"id": id, 
            "symbol": symbol,
            }
    memory.append(data)



def remove_formatting(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  
    text = re.sub(r'__(.*?)__', r'\1', text)      
    text = re.sub(r'\*(.*?)\*', r'\1', text)     
    text = re.sub(r'_(.*?)_', r'\1', text)        
    text = re.sub(r'~~(.*?)~~', r'\1', text)     
    text = re.sub(r'`(.*?)`', r'\1', text)       
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  

    text = re.sub(r'<.*?>', '', text)  

    return text

def handle_reply(event):
    if event.is_reply:
        for i in range(len(memory)):
            if memory[i]["id"] == event.reply_to_msg_id:
                symbol = memory[i]["symbol"]
                memory.remove(memory[i])
                return symbol
    return None

    
async def main():
    await client.start()  
    await client.send_message(reciever, "Bot запущен")
    await client.run_until_disconnected()  

asyncio.run(main())
