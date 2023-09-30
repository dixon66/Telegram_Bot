import telebot
from telebot import types
from constantss import API_KEY

bot = telebot.TeleBot(API_KEY)

# Function to handle /start command
@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton('/start')
    item_help = types.KeyboardButton('/help')
    item_contact = types.KeyboardButton('/contact')
    markup.row(item_start, item_help, item_contact)
    bot.send_message(message.chat.id, "Hello! Welcome to Simplilearn.", reply_markup=markup)

# Function to handle /help command
@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.reply_to(message, """
    The following commands are available:
    
    /start -> Welcome to the channel
    /help -> This message
    /SQL -> The first video from SQL Playlist
    /DownloadCV -> The first video from Java Playlist
    /Skillup -> Free platform for certification by Simplilearn
    /contact -> contact information 
    """)

# Function to handle /contact command
@bot.message_handler(commands=['contact'])
def send_contact_link(message):
    bot.reply_to(message, "LinkedIn: https://www.linkedin.com/in/your-profile")

# Function to handle /SQL command (and other commands)
@bot.message_handler(commands=['SQL'])
def send_sql_link(message):
    bot.reply_to(message, "Tutorial link for SQL: https://youtu.be/pFq1pgli0OQ")

# Function to handle /Python command (and other commands)
@bot.message_handler(commands=['Python'])
def send_python_link(message):
    bot.reply_to(message, "Tutorial link for Python: https://youtu.be/Tm5u97I7OrM")


@bot.message_handler(commands=['DownloadCV'])
def send_cv_link(message):
    # Assuming you have a direct link to the CV
    bot.reply_to(message, "Download CV: https://example.com/cv.pdf")

@bot.message_handler(commands=['Skillup'])
def send_skillup_link(message):
    bot.reply_to(message, "Skillup platform: https://www.simplilearn.com/skillup-free-online-courses-for-college-students-rar2852")

@bot.message_handler(commands=['contact'])
def send_contact_link(message):
    bot.reply_to(message, "LinkedIn: https://www.linkedin.com/in/your-profile")

# Handle inline keyboard presses
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_keyboard(callback_query):
    if callback_query.data == 'menu':
        markup = types.InlineKeyboardMarkup()
        item_help = types.InlineKeyboardButton('Help', callback_data='help')
        item_contact = types.InlineKeyboardButton('Contact', callback_data='contact')
        markup.row(item_help, item_contact)
        bot.send_message(callback_query.from_user.id, 'Menu:', reply_markup=markup)

    elif callback_query.data == 'help':
        send_help_message(callback_query.message)
    
    elif callback_query.data == 'contact':
        send_contact_link(callback_query.message)

# Start the bot
bot.polling()
