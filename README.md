# FILESU-TG-BOT

A powerful Telegram bot built with Python and the `pyTelegramBotAPI` library. This bot allows authorized users to broadcast messages, batch upload files, manage user data, and share files securely with subscribers. It also enforces membership in an update channel before users can access files.

---

## Features

- **User Registration:** Automatically tracks and stores user information.
- **Broadcast Messages:** Authorized user can broadcast text, documents, photos, audio, video, and animations to all users.
- **Batch File Upload:** Upload multiple files as a batch with a unique code for easy sharing.
- **File Forwarding:** Forward files directly to a specified Telegram channel.
- **File & Batch Retrieval:** Users can request files or batches using unique codes.
- **User & Batch Data Management:** Load and delete user and batch data via commands.
- **Update Channel Membership Enforcement:** Users must join a specified update channel to access files.
- **Persistent Storage:** User and batch data are saved in JSON files for persistence.

---

## Prerequisites

- Python 3.7+
- `pyTelegramBotAPI` library
- A Telegram bot token (from [BotFather](https://t.me/BotFather))
- Telegram channel ID for file forwarding
- Update channel ID for membership enforcement

---

## Installation

1. **Clone the repository:**
2. **Create and activate a virtual environment (optional but recommended):**
3. **Install dependencies:** 
4. **Create a `keep_alive.py` file** (if you want to keep your bot running on platforms like Replit).

---

## Configuration

Open the main bot script and update the following variables with your own values:

1. TOKEN = "YOUR_BOT_TOKEN"
2. CHANNEL_ID = "-100xxxxxxxxxx" # Your Telegram channel ID (for forwarding files)
3. UPDATE_CHANNEL_ID = "-100xxxxxxxxxx" # Your update channel ID (for membership check)
4. AUTHORIZED_USER_ID = 123456789 # Your Telegram user ID (integer)

---

## Commands


- Commands available to the authorized user:

- `/start` - Register and greet the user.
- `/broadcast` - Broadcast a message or media to all users.
- `/batch` - Create a batch of files with a unique code.
- `/get_user` - Retrieve stored user information.
- `/delete` - Delete a batch by its unique code.
- `/load_user` - Load user data from formatted text.
- `/get_batch` - Retrieve list of batch codes and their files.
- `/load_batch` - Load batch data from formatted text.

- Users must join the specified channel to receive files.

- Users can send a batch code or file ID to receive the corresponding files.

---












