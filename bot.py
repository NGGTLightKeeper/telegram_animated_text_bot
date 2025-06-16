import time
import telebot
import os
import random
import mysql.connector
import django
from django.utils import timezone
from pathlib import Path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_bot_django.settings')
django.setup()
BASE_DIR = Path(__file__).resolve().parent
from telegram_bot_db.models import MessagesModel, PendingMessagesModel
from settings.settings import *
from telebot.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import util
import re

bot = telebot.TeleBot(BOT_TOKEN)

# Working with MySQL database
class DataBase:
    # Save message to the database
    def save_message(message, mid):
        MessagesModel.objects.create(
                    user = message.chat.id,
                    mid = mid,
                    message = message.text,
                    timestamp = timezone.now(),
                )

# Animation types
ANIMATION_TYPES = [
    ('1', 'Message by MID'),
    ('2', 'Message by MID (Hidden after animation)'),
    ('3', 'Message by Text (For short messages)'),
    ('4', 'Message by Text (For short messages and Hidden after animation)'),
    ('5', 'Message with Frames (By MID)'),
    ('6', 'Message with Frames (By MID and Hidden after animation)'),
    ('7', 'Message with CF (By MID)'),
    ('8', 'Message with CF (By MID and Hidden after animation)'),

    ('101', 'Pending Message by MID'),
    ('102', 'Pending Message by MID (Hidden after animation)'),
    ('103', 'Pending Message by Text (For short messages)'),
    ('104', 'Pending Message by Text (For short messages and Hidden after animation)'),
    ('105', 'Pending Message with Frames (By MID)'),
    ('106', 'Pending Message with Frames (By MID and Hidden after animation)'),
    ('107', 'Pending Message with CF (By MID)'),
    ('108', 'Pending Message with CF (By MID and Hidden after animation)'),
]

# Escape Markdown v2 characters
def escape_md_v2(text: str) -> str:
    return re.sub(r'([\_\*\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\!])', r'\\\1', text)

# Function to split the message into an array of texts based on the specified rules
def split_frame_message_into_array(mess):
    result = []
    
    # If message doesn't start with '[', return whole message as single item
    if not mess.startswith('['):
        return [mess]
    
    try:
        current_pos = 1  # Skip initial '['
        while current_pos < len(mess):
            # Skip whitespace
            while current_pos < len(mess) and mess[current_pos].isspace():
                current_pos += 1
            
            # Check for chunk start
            if current_pos < len(mess) and mess[current_pos] == '{':
                chunk_start = current_pos + 1
                current_pos += 1
                # Find closing '}'
                brace_count = 1
                while current_pos < len(mess) and brace_count > 0:
                    if mess[current_pos] == '{':
                        brace_count += 1
                    elif mess[current_pos] == '}':
                        brace_count -= 1
                    current_pos += 1
                
                if brace_count == 0:
                    chunk = mess[chunk_start:current_pos-1]
                    result.append(chunk)
                    
                    # Look for comma or closing bracket
                    while current_pos < len(mess) and mess[current_pos] not in ',]':
                        current_pos += 1
                    
                    if current_pos < len(mess) and mess[current_pos] == ']':
                        break
                    elif current_pos < len(mess) and mess[current_pos] == ',':
                        current_pos += 1
                        continue
            else:
                break
                
        # If we didn't find proper formatting, return original message
        if not result:
            return [mess]
            
        return result
        
    except Exception:
        # If any error occurs, return original message
        return [mess]

# Function to split the message into an array of texts based on the specified rules
def split_cf_message_into_array(mess):
    result = []
    
    # If message doesn't start with '[', return whole message as single item
    if not mess.startswith('['):
        return [mess]
    
    try:
        current_pos = 1  # Skip initial '['
        while current_pos < len(mess):
            # Skip whitespace
            while current_pos < len(mess) and mess[current_pos].isspace():
                current_pos += 1
            
            # Check for chunk start
            if current_pos < len(mess) and mess[current_pos] == '{':
                chunk_start = current_pos + 1
                current_pos += 1
                # Find closing '}'
                brace_count = 1
                while current_pos < len(mess) and brace_count > 0:
                    if mess[current_pos] == '{':
                        brace_count += 1
                    elif mess[current_pos] == '}':
                        brace_count -= 1
                    current_pos += 1
                
                if brace_count == 0:
                    chunk = mess[chunk_start:current_pos-1]
                    result.append(chunk)
                    
                    # Look for comma or closing bracket
                    while current_pos < len(mess) and mess[current_pos] not in ',]':
                        current_pos += 1
                    
                    if current_pos < len(mess) and mess[current_pos] == ']':
                        break
                    elif current_pos < len(mess) and mess[current_pos] == ',':
                        current_pos += 1
                        continue
            else:
                break
                
        # If we didn't find proper formatting, return original message
        if not result:
            return [mess]
            
        return result
        
    except Exception:
        # If any error occurs, return original message
        return [mess]



# Hanfler start message
@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        text = open(str(BASE_DIR) + MESS_GREETING, 'r', encoding='utf-8').read()

        markup = telebot.types.InlineKeyboardMarkup()
        btn_help = telebot.types.InlineKeyboardButton(text=NAME_BTN_HELP, callback_data="btn_help")
        btn_support = telebot.types.InlineKeyboardButton(text=NAME_BTN_SUPPORT, url=URL_SUPPORT)
        markup.add(btn_help, btn_support)

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

        mid = random.randint(1000000000, 9999999999)
        DataBase.save_message(message, mid)
    except Exception as e:
        print(f"ERROR (command_start):\n{e}")

# Hanfler help message
@bot.message_handler(commands=['help'])
def command_help(message):
    try:
        text = open(str(BASE_DIR) + MESS_HELP, 'r', encoding='utf-8').read()

        markup = telebot.types.InlineKeyboardMarkup()
        btn_support = telebot.types.InlineKeyboardButton(text=NAME_BTN_SUPPORT, url=URL_SUPPORT)
        markup.add(btn_support)

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

        mid = random.randint(1000000000, 9999999999)
        DataBase.save_message(message, mid)
    except Exception as e:
        print(f"ERROR (command_help):\n{e}")


# Hanfler other messages
@bot.message_handler(func=lambda message: True)
def message(message):
    try:
        mid = random.randint(1000000000, 9999999999)
        text = "Message ID: " + str(mid) + "\n" + "\n" + "Message:" + "\n" + message.text
        bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)
        DataBase.save_message(message, mid)
    except Exception as e:
        print(f"ERROR (message):\n{e}")


# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        markup = telebot.types.InlineKeyboardMarkup()
        is_done = False
        
        if 'startanimation' in call.data:
            # Get PMID
            parts = call.data.split('_')
            if len(parts) == 2:
                pmid = parts[1]

                # Get message from database
                try:
                    mess_queryset = PendingMessagesModel.objects.filter(lmid=pmid)[0]
                    chosen_id = mess_queryset.chosen_id
                    inline_message_id = mess_queryset.inline_message_id
                    mess = mess_queryset.message

                    # Animation
                    # Create a mock chosen object as a dictionary
                    chosen_data = {
                        'result_id': chosen_id,
                        'from_user': {
                            'id': call.from_user.id,
                            'is_bot': call.from_user.is_bot,
                            'first_name': call.from_user.first_name,
                            'username': call.from_user.username,
                            'last_name': call.from_user.last_name
                        },
                        'location': None,
                        'inline_message_id': inline_message_id,
                        'query': mess
                    }
                    
                    # Convert to object-like structure for compatibility
                    class ChosenInlineResult:
                        def __init__(self, data):
                            self.result_id = data['result_id']
                            self.from_user = type('User', (), data['from_user'])
                            self.inline_message_id = data['inline_message_id']
                            self.query = data['query']
                    
                    chosen = ChosenInlineResult(chosen_data)
                    chosen_inline_result(chosen)

                except Exception:
                    return
            return
        
        elif call.data == 'btn_back_to_start':
            text = open(str(BASE_DIR) + MESS_GREETING, 'r', encoding='utf-8').read()

            btn_help = telebot.types.InlineKeyboardButton(text=NAME_BTN_HELP, callback_data="btn_help")
            btn_support = telebot.types.InlineKeyboardButton(text=NAME_BTN_SUPPORT, url=URL_SUPPORT)
            markup.add(btn_help, btn_support)

            is_done = True
        elif call.data == 'btn_help':
            text = open(str(BASE_DIR) + MESS_HELP, 'r', encoding='utf-8').read()

            btn_start_back = telebot.types.InlineKeyboardButton(text=NAME_BTN_BACK, callback_data="btn_back_to_start")
            btn_support = telebot.types.InlineKeyboardButton(text=NAME_BTN_SUPPORT, url=URL_SUPPORT)
            markup.add(btn_support)
            markup.add(btn_start_back)

            is_done = True

        if is_done:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

    except Exception as e:
        print(f"ERROR (callback):\n{e}")

# Inline query handler
@bot.inline_handler(lambda query: True)
def inline_query_handler(inline_query):
    text = inline_query.query.strip()
    results = []

    if text:
        for anim_id, anim_title in ANIMATION_TYPES:
            # Add inline query results
            markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="Start", callback_data="startanimation")
            )
            results.append(
                InlineQueryResultArticle(
                    id=anim_id,
                    title=f"{anim_title}",
                    input_message_content=InputTextMessageContent("Please wait..."),
                    reply_markup=markup
                )
            )
    else:
        results.append(
            InlineQueryResultArticle(
                id='empty',
                title="Input text",
                input_message_content=InputTextMessageContent("Input Text or MessageID to send animation"),
            )
        )

    bot.answer_inline_query(inline_query.id, results, cache_time=0)


# Animation handler
@bot.chosen_inline_handler(func=lambda chosen: True)
def chosen_inline_result(chosen):

    # Check inline message ID
    inline_msg_id = getattr(chosen, 'inline_message_id', None)
    text = chosen.query.strip()
    if not inline_msg_id:
        return


    # Check type message ( PENDING or ANIMATION )
    # PENDING
    if len(chosen.result_id) > 2:
        pmid = random.randint(100000000000, 999999999999)
        callback_data = "startanimation_" + str(pmid)

        chosen_result_id = str(int(chosen.result_id) % 100)
        
        # Save message in database
        PendingMessagesModel.objects.create(
                    lmid = pmid,
                    chosen_id = chosen_result_id,
                    inline_message_id = inline_msg_id,
                    message = text,
                    timestamp = timezone.now(),
                )
        
        
        # Message Button
        markup = telebot.types.InlineKeyboardMarkup()
        inline_text = "Click on the button"
        inline_btn = telebot.types.InlineKeyboardButton(text="Start", callback_data=callback_data)
        markup.add(inline_btn)

        # Edit message with button
        bot.edit_message_text(inline_message_id=inline_msg_id, text=inline_text, reply_markup=markup)
        return


    # Check type message ( PENDING or ANIMATION )
    # ANIMATION
    else:
        message_chunks = []

        # Check user selected result
        if chosen.result_id == 'empty':
            # If the user selected the empty result, return
            bot.edit_message_text(inline_message_id=inline_msg_id, text="Please input text or message ID")
            return

        elif chosen.result_id == '1' or chosen.result_id == '2' or chosen.result_id == '5' or chosen.result_id == '6' or chosen.result_id == '7' or chosen.result_id == '8':
            # Check if the first character is a digit
            if text and text[0].isdigit():
                # Try getting the message from the database by ID
                AMID = text
                try:
                    mess_queryset = MessagesModel.objects.filter(mid=text)[0]
                    mess = mess_queryset.message
                # If the message is not found, return an error message
                except Exception:
                    mess = "Error"
            else:
                # If the first character is not a digit, use the text itself
                AMID = None
                mess = "Input correct Message ID"


            # Check structure Message with Frames
            if chosen.result_id == '5' or chosen.result_id == '6':
                # Check if the message starts with "[" and ends with "]"
                message_chunks = split_frame_message_into_array(mess)

            elif chosen.result_id == '7' or chosen.result_id == '8':
                # Check if the message starts with "[" and ends with "]"
                message_chunks = split_cf_message_into_array(mess)

        elif chosen.result_id == '3' or chosen.result_id == '4':
            # Set AMID to None for text messages
            AMID = None
            mess = text


        # Print Animation data
        if PRINT_MESSAGE_DATA:
            print("\n")
            print("User ID: " + str(chosen.from_user.id))
            print("User: " + str(chosen.from_user.username) + ", " + str(chosen.from_user.first_name) + " " + str(chosen.from_user.last_name))
            print("Inline message ID: " + str(inline_msg_id))
            print("Animation Message ID: " + str(AMID))
            print("\nMessage:\n" + str(mess))
            print("\n")


        # Check message
        if mess == "Error":
            bot.edit_message_text(inline_message_id=inline_msg_id, text=mess)
            return


        # Prepare chat message for animation
        full_mess = "ᅠ"
        bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess)
        time.sleep(1)

        # Message animation
        # For message without frames
        if chosen.result_id == '1' or chosen.result_id == '2' or chosen.result_id == '3' or chosen.result_id == '4':
            full_mess = ""
            # For long messages, split into sentences
            if len(mess) > 1024:
                # Split the message into sentences
                sentences = mess.split('.')

                # Animate each sentence
                for sentence in sentences:
                    text = sentence.strip()

                    # Skip empty sentences
                    if not text:
                        continue

                    # Animate each sentence
                    while text:
                        # Check if the message is too long
                        try:
                            randlen = 1
                            if len(text) > 50:
                                randlen = len(text) / 2
                            else:
                                randlen = len(text)
                            chunk_size = random.randint(1, randlen)
                            chunk = text[:chunk_size]
                            text = text[chunk_size:]
                            full_mess += chunk
                            bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                            time.sleep(0.5)
                        except Exception:
                            time.sleep(1)
                        time.sleep(1)
                    # Add a new line after each sentence
                    full_mess += '. '
                    bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                    time.sleep(1)

                # For hidden messages after animation
                if chosen.result_id == '2' or chosen.result_id == '4':
                    raw = full_mess.rstrip()
                    escaped = escape_md_v2(raw)
                    spoiler = f"||{escaped}||"

                    try:
                        bot.edit_message_text(
                            inline_message_id=inline_msg_id,
                            text=spoiler,
                            parse_mode='MarkdownV2',
                            disable_web_page_preview=True
                        )
                        time.sleep(0.3)
                    except Exception:
                        pass

            # For short messages, split into words and animate
            else:
                # Split the message into lines
                lines = mess.split('\n')
                for idx, line in enumerate(lines):
                    # Split the line into words
                    words = line.split()
                    for word in words:
                        # Animate each word
                        while word:
                            chunk_size = random.randint(1, len(word))
                            chunk = word[:chunk_size]
                            word = word[chunk_size:]
                            full_mess += chunk
                            try:
                                bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                                time.sleep(0.05)
                            except Exception:
                                time.sleep(0.5)
                        full_mess += ' '
                        time.sleep(0.1)

                    # Add a new line after each line
                    if idx < len(lines) - 1:
                        full_mess = full_mess.rstrip() + '\n'
                        try:
                            bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                            time.sleep(0.3)
                        except Exception:
                            pass

                # For hidden messages after animation
                if chosen.result_id == '2' or chosen.result_id == '4':
                    raw = full_mess.rstrip()
                    escaped = escape_md_v2(raw)
                    spoiler = f"||{escaped}||"

                    try:
                        bot.edit_message_text(
                            inline_message_id=inline_msg_id,
                            text=spoiler,
                            parse_mode='MarkdownV2',
                            disable_web_page_preview=True
                        )
                        time.sleep(0.3)
                    except Exception:
                        pass
        # For message with frames
        elif chosen.result_id == '5' or chosen.result_id == '6':
            full_mess = ""
            
            for fid, frame in enumerate(message_chunks):
                full_mess = ""
                lines = frame.split('\n')
                for idx, line in enumerate(lines):
                    # Split the line into words
                    words = line.split()
                    for word in words:
                        # Animate each word
                        while word:
                            chunk_size = random.randint(1, len(word))
                            chunk = word[:chunk_size]
                            word = word[chunk_size:]
                            full_mess += chunk
                            try:
                                bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                                time.sleep(0.05)
                            except Exception:
                                time.sleep(0.5)
                        full_mess += ' '
                        time.sleep(0.1)

                    # Add a new line after each line
                    if idx < len(lines) - 1:
                        full_mess = full_mess.rstrip() + '\n'
                        try:
                            bot.edit_message_text(inline_message_id=inline_msg_id, text=full_mess, parse_mode='Markdown', disable_web_page_preview=True)
                            time.sleep(0.3)
                        except Exception:
                            pass
                time.sleep(3)

            # For hidden messages after animation
            if chosen.result_id == '6':
                raw = full_mess.rstrip()
                escaped = escape_md_v2(raw)
                spoiler = f"||{escaped}||"

                try:
                    bot.edit_message_text(
                        inline_message_id=inline_msg_id,
                        text=spoiler,
                        parse_mode='MarkdownV2',
                        disable_web_page_preview=True
                    )
                    time.sleep(0.3)
                except Exception:
                    pass
        elif chosen.result_id == '7' or chosen.result_id == '8':
            for fid, frame in enumerate(message_chunks):
                bot.edit_message_text(inline_message_id=inline_msg_id, text=frame, parse_mode='Markdown', disable_web_page_preview=True)
                time.sleep(0.2)

            # For hidden messages after animation
            if chosen.result_id == '6':
                raw = full_mess.rstrip()
                escaped = escape_md_v2(raw)
                spoiler = f"||{escaped}||"

                try:
                    bot.edit_message_text(
                        inline_message_id=inline_msg_id,
                        text=spoiler,
                        parse_mode='MarkdownV2',
                        disable_web_page_preview=True
                    )
                    time.sleep(0.3)
                except Exception:
                    pass



bot.infinity_polling()
