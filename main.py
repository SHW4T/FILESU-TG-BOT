import telebot  # pip install pyTelegramBotAPI
import os
import json
import uuid
from keep_alive import keep_alive

keep_alive()

TOKEN = ""  # replace with your bot token
CHANNEL_ID = "-1002022252775"  # replace with your channel ID
UPDATE_CHANNEL_ID = ""  # replace with your update channel ID
AUTHORIZED_USER_ID =   # replace with your authorized user ID
bot = telebot.TeleBot(TOKEN)

# File to store user data
USER_DATA_FILE = 'user_data.json'
BATCH_DATA_FILE = 'batch_data.json'

# Load user data from JSON file
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as file:
        user_data = json.load(file)
else:
    user_data = {}

# Load batch data from JSON file
if os.path.exists(BATCH_DATA_FILE):
    with open(BATCH_DATA_FILE, 'r') as file:
        batch_data = json.load(file)
else:
    batch_data = {}

def save_user_data():
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

def save_batch_data():
    with open(BATCH_DATA_FILE, 'w') as file:
        json.dump(batch_data, file)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
        save_user_data()
    bot.send_message(message.chat.id, "Hello, I'm SHWAT's Personal Assistant. You can receive files shared by SHWAT.")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Please send the message you want to broadcast.")
        bot.register_next_step_handler(message, handle_broadcast)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

def handle_broadcast(message):
    for user_id in user_data.keys():
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text)
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id)
            elif message.content_type == 'audio':
                bot.send_audio(user_id, message.audio.file_id)
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id)
            elif message.content_type == 'animation':
                bot.send_animation(user_id, message.animation.file_id)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

@bot.message_handler(commands=['get_user'])
def get_user(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        response = "User Info:\n"
        for user_id, user_info in user_data.items():
            user_link = f"https://t.me/{user_info['username']}" if user_info['username'] else "Mention"
            response += (f"ID: {user_id}\n"
                         f"Username: {user_info['username']}\n"
                         f"First Name: {user_info['first_name']}\n"
                         f"Last Name: {user_info['last_name']}\n"
                         f"Profile Link: {user_link}\n\n")
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

@bot.message_handler(commands=['batch'])
def batch(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "How many files do you want to batch?")
        bot.register_next_step_handler(message, get_batch_file_count)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

def get_batch_file_count(message):
    try:
        file_count = int(message.text)
        unique_code = str(uuid.uuid4())
        batch_data[unique_code] = []
        save_batch_data()
        bot.send_message(message.chat.id, f"Batch code generated: {unique_code}\nPlease send {file_count} files to include in this batch.")
        bot.register_next_step_handler(message, handle_batch_files, unique_code, file_count)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number.")

def handle_batch_files(message, unique_code, file_count):
    if message.content_type in ['document', 'photo', 'audio', 'video']:
        file_id = None
        caption = message.caption if message.caption else ""
        if message.content_type == 'document':
            file_id = message.document.file_id
        elif message.content_type == 'photo':
            file_id = message.photo[-1].file_id
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
        elif message.content_type == 'video':
            file_id = message.video.file_id

        if file_id:
            batch_data[unique_code].append({
                'file_id': file_id,
                'content_type': message.content_type,
                'caption': caption
            })
            save_batch_data()
            bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
            if len(batch_data[unique_code]) < file_count:
                bot.send_message(message.chat.id, f"File added to batch. {file_count - len(batch_data[unique_code])} more files to go.")
                bot.register_next_step_handler(message, handle_batch_files, unique_code, file_count)
            else:
                bot.send_message(message.chat.id, f"Batch complete. Use the code `{unique_code}` to share the files.", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Unsupported file type. Please send a document, photo, audio, or video.")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def handle_files(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        # Forward the file to the channel
        forwarded_message = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)

        # Get the file ID of the file in the channel
        if message.content_type == 'document':
            channel_file_id = forwarded_message.document.file_id
        elif message.content_type == 'photo':
            # Telegram sends photos in different sizes, we'll use the largest one
            channel_file_id = forwarded_message.photo[-1].file_id
        elif message.content_type == 'audio':
            channel_file_id = forwarded_message.audio.file_id
        elif message.content_type == 'video':
            channel_file_id = forwarded_message.video.file_id

        # Generate a unique code for the file
        unique_code = str(uuid.uuid4())
        batch_data[unique_code] = [{
            'file_id': channel_file_id,
            'content_type': message.content_type,
            'caption': message.caption if message.caption else ""
        }]
        save_batch_data()

        bot.send_message(message.chat.id, f"File forwarded to channel. Use the code `{unique_code}` to share the file.", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Don't send me files.")

@bot.message_handler(commands=['delete'])
def delete_code(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Please send the unique code you want to delete.")
        bot.register_next_step_handler(message, handle_delete_code)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

def handle_delete_code(message):
    unique_code = message.text
    if unique_code in batch_data:
        del batch_data[unique_code]
        save_batch_data()
        bot.send_message(message.chat.id, f"Unique code {unique_code} has been deleted successfully.")
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't find a batch with that code.")

@bot.message_handler(commands=['load_user'])
def load_user(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Please send the user info in the following format:\n\n"
                                          "User Info:\n"
                                          "ID: \n"
                                          "Username: \n"
                                          "First Name: \n"
                                          "Last Name: \n"
                                          "Profile Link:\n\n"
                                          "ID: \n"
                                          "Username: \n"
                                          "First Name: \n"
                                          "Last Name: \n"
                                          "Profile Link: \n")
        bot.register_next_step_handler(message, handle_load_user)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

def handle_load_user(message):
    user_info_text = message.text.split('\n')[1:]  # Skip the "User Info:" line
    for i in range(0, len(user_info_text), 6):  # Adjusted to 6 to account for 'Profile Link' line
        user_id = user_info_text[i].split(': ')[1]
        username = user_info_text[i + 1].split(': ')[1]
        first_name = user_info_text[i + 2].split(': ')[1]
        last_name = user_info_text[i + 3].split(': ')[1]
        # Skip the 'Profile Link' line
        user_data[user_id] = {
            'username': username if username != 'None' else None,
            'first_name': first_name if first_name != 'None' else None,
            'last_name': last_name if last_name != 'None' else None
        }
    save_user_data()
    bot.send_message(message.chat.id, "User data loaded successfully.")

@bot.message_handler(commands=['get_batch'])
def get_batch(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        response = "Batch Codes\n"
        for code, files in batch_data.items():
            response += f"Code: {code}\nTotal documents: {len(files)}\nDocument file id: {', '.join([file['file_id'] for file in files])}\n\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

@bot.message_handler(commands=['load_batch'])
def load_batch(message):
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Please send the batch info in the following format:\n\n"
                                          "Batch Codes\n"
                                          "Code: \n"
                                          "Total documents: \n"
                                          "Document file id: {id 1}, {id 2}\n\n"
                                          "Code: \n"
                                          "Total documents: \n"
                                          "Document file id: {id 1}, {id 2}\n")
        bot.register_next_step_handler(message, handle_load_batch)
    else:
        bot.send_message(message.chat.id, "You are not SHWAT & you can never be😏.")

def handle_load_batch(message):
    batch_info_text = message.text.split('\n')[1:]  # Skip the "Batch Codes" line
    for i in range(0, len(batch_info_text), 4):  # Adjusted to 4 to account for the format
        code = batch_info_text[i].split(': ')[1]
        # Skip the 'Total documents' line
        file_ids = batch_info_text[i + 2].split(': ')[1].split(', ')
        batch_data[code] = [{'file_id': file_id, 'content_type': 'document'} for file_id in file_ids]
    save_batch_data()
    bot.send_message(message.chat.id, "Batch data loaded successfully.")

@bot.message_handler(func=lambda message: True)
def track_users_and_send_file(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name
        }
        save_user_data()

    # Ignore commands
    if message.text.startswith('/'):
        return

    try:
        # Check if the user is a member of the update channel
        user_status = bot.get_chat_member(UPDATE_CHANNEL_ID, message.from_user.id)
        if user_status.status not in ["creator", "administrator", "member"]:
            bot.send_message(message.chat.id, "Please join the Update Channel to get your file. https://t.me/+lKjcWcpSK8AzYzQ1")
            return

        # Check if the message text is a batch code
        if message.text in batch_data:
            for file_info in batch_data[message.text]:
                if file_info['content_type'] == 'document':
                    bot.send_document(message.chat.id, file_info['file_id'])
                elif file_info['content_type'] == 'photo':
                    bot.send_photo(message.chat.id, file_info['file_id'], caption=file_info.get('caption', ''))
                elif file_info['content_type'] == 'audio':
                    bot.send_audio(message.chat.id, file_info['file_id'])
                elif file_info['content_type'] == 'video':
                    bot.send_video(message.chat.id, file_info['file_id'])
        else:
            # Check if the message text is a file ID
            found = False
            for files in batch_data.values():
                for file_info in files:
                    if file_info['file_id'] == message.text:
                        found = True
                        if file_info['content_type'] == 'document':
                            bot.send_document(message.chat.id, file_info['file_id'])
                        elif file_info['content_type'] == 'photo':
                            bot.send_photo(message.chat.id, file_info['file_id'], caption=file_info.get('caption', ''))
                        elif file_info['content_type'] == 'audio':
                            bot.send_audio(message.chat.id, file_info['file_id'])
                        elif file_info['content_type'] == 'video':
                            bot.send_video(message.chat.id, file_info['file_id'])
                        break
                if found:
                    break
            if not found:
                bot.send_message(message.chat.id, "Sorry, I couldn't find a batch or file with that ID.")
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, I couldn't find a file with that ID.")
        print(f"Error: {e}")

bot.polling()
