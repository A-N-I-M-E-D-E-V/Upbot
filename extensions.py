from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import GROUP_ID, RECEIVER
from aiogram.utils import markdown

import json

def send_hello(name: str) -> str:
    return f"""
Assalomu alaykum {name}!
Bu gif konkurslar o'tkazishga yordamlashuvchi bot
Ko'proq malumot olish uchun /help
"""
def send_help() -> str:
    return f"""
Ishni boshlashi uchun avval botni guruhingizga qo'shing
Keyin guruhda /start_count buyrug'ini yuboring
siz har safar /top buyrug'i yordamida top g'oliblarni ko'rib borishingiz mumkin."""

def send_top_list() -> str:

    with open('users_data.json', 'r', encoding='utf-8') as file:
        group = json.load(file)
    
    if group != {}:
        users = {}
        
        res = ""    

        for user in list(group.keys()):
            users.update({user: len(group[user]["added_users"])})

        sorted_users = sorted(users.items(), reverse=True,key = lambda kv: kv[1])

        nagrad = ["🥇", "🥈", "🥉"]
        nagrad.extend(list(range(4, len(sorted_users))))

        count = -1

        for user in sorted_users:
            id, num_addeds = user
            if num_addeds>0:
                name = group[id]["name"]
                count += 1
                res += f"{nagrad[count]} {markdown.hlink(name, url=f'tg://user?id={id}') } \n{ num_addeds } ta odam qo'shgan \n------------------------------------------------\n"
       
        if res != "":
            return res
        else:
            return "Barcha qo'shilgan odamlar guruhni tark etishdi"
    else: 
        return "Guruhga hali hech kim odam qo'shmadi"

def send_start_con() -> str:
    return f"""
Yaxshi, Konkurs boshlandi!
Avvalgi naijalar o'chirib yuborildi."""

def add_user(message: dict):
    with open('users_data.json', 'r', encoding='utf-8') as file:
        group = json.load(file)

    from_id =str(message['from']['id']).strip()
    add_user_id = str(message["new_chat_member"]["id"]).strip()
    from_is_bot = bool(message["from"]["is_bot"])
    add_user_is_bot = bool(message["new_chat_member"]["is_bot"])

    if from_id != add_user_id:
        if not from_is_bot:
            if not add_user_is_bot:
                if group.get(from_id) != None:
                    if add_user_id not in group[from_id]["added_users"]:
                        group[from_id]["added_users"].append(add_user_id)

                else:
                    new_data = {from_id: {"name": message['from']["first_name"],"added_users": [add_user_id]}}
                    group.update(new_data)
            else:
                return 'added_bot'
        else:
            return 'bot_added'

    with open('users_data.json', 'w', encoding='utf-8') as f:
        json.dump(group, f, ensure_ascii=False, indent=4)

def delete_user( user_id ):
    with open('users_data.json', 'r', encoding='utf-8') as file:
        group = json.load(file)
    
    for key_user in group.keys():
        if str(user_id) in group[key_user]["added_users"]:
            group[key_user]["added_users"].remove(str(user_id))
            break
    
    with open('users_data.json', 'w', encoding='utf-8') as f:
        json.dump(group, f, ensure_ascii=False, indent=4)
        

help_reply_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='/help')]
    ]
    )
