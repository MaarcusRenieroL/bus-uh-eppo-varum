import requests
from bs4 import BeautifulSoup
import time
import telebot
from telebot import types

# Set up your Telegram bot by obtaining a bot token
bot_token = '6005017668:AAEWpFFyvGHt_fty6zGccT1IHvyu1RwOAW0'
bot = telebot.TeleBot(bot_token)

# Define the URL of the static website you want to fetch content from
website_url = 'http://localhost:3000'

# Define a global variable to keep track of the checking status
checking_enabled = False

# Define a function to fetch the specific content from the website
def fetch_website_content():
    # Fetch the website content
    website_content = requests.get(website_url).text
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(website_content, 'html.parser')
    # Extract the specific contents you want
    content1 = soup.find('span', {'class': 'morning-timing'}).text.strip()
    content2 = soup.find('span', {'class': 'return-students-timing'}).text.strip()
    content3 = soup.find('span', {'class': 'return-admin-timing'}).text.strip()
    # Return the specific contents as a tuple
    return (content1, content2, content3)

# Send a message to start checking for updates
@bot.message_handler(commands=['start'])
def start_checking(message):
    handle_message(message)
    global checking_enabled
    if not checking_enabled:
        checking_enabled = True
        bot.send_message(chat_id=message.chat.id, text='Checking for updates...')
        check_for_updates(message.chat.id)
    else:
        bot.send_message(chat_id=message.chat.id, text='Updates are already being checked.')

# Send a message to stop checking for updates
@bot.message_handler(commands=['stop'])
def stop_checking(message):
    global checking_enabled
    checking_enabled = False
    bot.send_message(chat_id=message.chat.id, text='Updates checking stopped.')

# Define a function to check for updates and send messages
def check_for_updates(chat_id):
    # Fetch the initial website content
    website_content_old = fetch_website_content()

    # Set up a loop to check for updates and send messages
    while checking_enabled:
        # Wait for 5 minutes
        time.sleep(5)

        # Fetch the current website content
        website_content_new = fetch_website_content()

        # Compare the new website content with the previous one
        if website_content_new != website_content_old:
            # If the content has changed, send a new message with the changed content
            if website_content_new[0] != website_content_old[0]:
                bot.send_message(chat_id=chat_id, text="Morning Bus Count has been changed \nNew Bus Count : " + website_content_new[0])
            if website_content_new[1] != website_content_old[1]:
                bot.send_message(chat_id=chat_id, text="Return after 3:15pm Bus Count has been changed \nNew Bus Count : " + website_content_new[1])
            if website_content_new[2] != website_content_old[2]:
                bot.send_message(chat_id=chat_id, text="Return after 5:00pm Bus Count has been changed \nNew Bus Count : " + website_content_new[2])
            # Update the previous website content with the new one
            website_content_old = website_content_new

    # Send a message to indicate that checking has stopped
    bot.send_message(chat_id=chat_id, text='Updates checking stopped.')

# Handle menu options for specific contents
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message is a menu option
    if message.text == 'Morning Bus Count':
        content = fetch_website_content()[0]
        bot.send_message(chat_id=message.chat.id, text=content)
    elif message.text == 'Return at 3:15 pm Bus Count':
        content = fetch_website_content()[1]
        bot.send_message(chat_id=message.chat.id, text=content)
    elif message.text == 'Return at 5:00 pm Bus Count':
        content = fetch_website_content()[2]
        bot.send_message(chat_id=message.chat.id, text=content)
    # Check if the message is the stop command
    elif message.text == '/stop':
        global checking_enabled
        checking_enabled = False
        bot.send_message(chat_id=message.chat.id, text='Updates checking stopped.')
    # Check if the message is anything else
    else:
        # Send the menu options as a reply keyboard
        menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        content1_button = types.KeyboardButton('Morning Bus Count')
        content2_button = types.KeyboardButton('Return at 3:15 pm Bus Count')
        content3_button = types.KeyboardButton('Return at 5:00 pm Bus Count')
        stop_button = types.KeyboardButton('/stop')
        menu_keyboard.add(content1_button, content2_button, content3_button, stop_button)
        bot.send_message(chat_id=message.chat.id, text='Please select an option:', reply_markup=menu_keyboard)

bot.polling()