import telebot
from telebot import types
from constantss import API_KEY
import yfinance as yf


bot = telebot.TeleBot(API_KEY)

# Function to handle /start command
@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton('/start')
    item_help = types.KeyboardButton('/help')
    item_contact = types.KeyboardButton('/contact')
    markup.row(item_start, item_help, item_contact)
    bot.send_message(message.chat.id, "Hi, I am Dixon Backend Developer", reply_markup=markup)

# Function to handle /help command
@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.reply_to(message, """
    The following commands are available:
    
/start - Welcome to the Portfolio Bot! 🚀

/help - Discover a world of possibilities! 🌟

/price - Unlock real-time stock prices! 💹 Try "price [ticker]" (e.g., price GOOGL). 📊

/wsb - Engage in an epic stock showdown! 📈 Compare GME, AMC, NOK. 🚀

/portfolio - Unveil the detailed portfolio! 💼

/git - Dive into the code ocean! Explore GitHub profile. 🐙

/contact - 🌠 Connect, collaborate, conquer! 🤝 Get in touch. 📲

/leetcode - 🧩 Conquer the code! Glide through the leetcode labyrinth.

/blog - 📚 Explore the latest insights in the boundless world of technology.
    
    """)

# Function to handle /contact command
@bot.message_handler(commands=['contact'])
def send_contact_link(message):
    bot.reply_to(message, "LinkedIn: https://www.linkedin.com/in/dixon055/")

# Function to handle /stock prices command
@bot.message_handler(commands=['price'])
def send_price_link(message):
    bot.reply_to(message, """  try price [stock_name] --> price AAPL, price GOOGL
    
1. Technology    
Apple Inc. (AAPL)
Microsoft Corporation (MSFT)
Amazon.com Inc. (AMZN)
Alphabet Inc. (GOOGL)
Facebook, Inc. (FB)

2. Finance:
JPMorgan Chase & Co. (JPM)
Bank of America Corporation (BAC)
Goldman Sachs Group, Inc. (GS)
Visa Inc. (V)
Mastercard Incorporated (MA)

3. Healthcare:
Johnson & Johnson (JNJ)
Pfizer Inc. (PFE)
Merck & Co., Inc. (MRK)
AbbVie Inc. (ABBV)
Amgen Inc. (AMGN)

4. Automotive:
Tesla, Inc. (TSLA)
General Motors Company (GM)
Ford Motor Company (F)
Toyota Motor Corporation (TM)
Honda Motor Co., Ltd. (HMC)

5. Retail:
Walmart Inc. (WMT)
Amazon.com Inc. (AMZN)
The Home Depot, Inc. (HD)
Alibaba Group Holding Limited (BABA)
Target Corporation (TGT)

6. Entertainment:
Walt Disney Company (DIS)
Netflix, Inc. (NFLX)
Spotify Technology S.A. (SPOT)
Comcast Corporation (CMCSA)
Activision Blizzard, Inc. (ATVI)

more... in real time
    """)

# Function to handle /Git command
@bot.message_handler(commands=['git'])
def send_git_link(message):
    bot.reply_to(message, "GitHub Profile Link: https://github.com/dixon66")

# Function to handle /Blog command
@bot.message_handler(commands=['blog'])
def send_blog_link(message):
    bot.reply_to(message, "Data is the new Gold: https://genesis.hashnode.dev/unveiling-the-power-of-web-scraping-a-comprehensive-guide")


@bot.message_handler(commands=['downloadCV'])
def send_cv(message):
    cv_path = "C:\\Users\\DIXON\\Downloads\\Documents\\Resume 1\\Dixon.pdf"
    with open(cv_path, 'rb') as cv_file:
        bot.send_document(message.chat.id, cv_file)

@bot.message_handler(commands=['leetcode'])
def send_leetcode_link(message):
    bot.reply_to(message, "Leetcode platform: https://leetcode.com/Dixon_N/")

@bot.message_handler(commands=['portfolio'])
def send_portfolio_link(message):
    bot.reply_to(message, "Blog: file:///C:/Users/DIXON/Downloads/Documents/Resume%201/Resume%201/index.html#about")

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


@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  response = ""
  stocks = ['gme', 'amc', 'nok']
  stock_data = []
  for stock in stocks:
    data = yf.download(tickers=stock, period='2d', interval='1d')
    data = data.reset_index()
    response += f"-----{stock}-----\n"
    stock_data.append([stock])
    columns = ['stock']
    for index, row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'], 2)
      format_date = row['Date'].strftime('%m/%d')
      response += f"{format_date}: {price}\n"
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()

  response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
  for row in stock_data:
    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data!?")

bot.polling()
