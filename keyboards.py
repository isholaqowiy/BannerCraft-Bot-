from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎨 Create Banner", callback_data="nav_create")],
        [InlineKeyboardButton("📱 Social Media Specs", callback_data="nav_specs"),
         InlineKeyboardButton("📂 My Project Logs", callback_data="nav_logs")],
        [InlineKeyboardButton("❓ Help Manual", callback_data="nav_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

