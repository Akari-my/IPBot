import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 'YOUR_TOKNE'
bot = telebot.TeleBot(TOKEN)


def get_ip_info(ip):
    url = f'http://ip-api.com/json/{ip}'
    response = requests.get(url)
    return response.json()


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    start_message = f"""
👋| Welcome @{username}

🤖| To use this bot, send the /ip command followed by a numeric IP address.

📉| Example: `/ip 8.8.8.8`
"""

    keyboard = InlineKeyboardMarkup()
    developer_button = InlineKeyboardButton("👨‍💻 Developer 👨‍💻", url="https://t.me/akari_my")
    keyboard.add(developer_button)

    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


@bot.message_handler(commands=['ip'])
def ip_info(message):
    ip_address = message.text.split(' ')[1]

    try:
        ip_info = get_ip_info(ip_address)
        if ip_info['status'] == 'fail':
            bot.reply_to(message, 'Invalid or not found IP address.')
        else:
            info = f"""
*IP*: {ip_info['query']}
*Village*: {ip_info['country']} ({ip_info['countryCode']})
*Region*: {ip_info['regionName']} ({ip_info['region']})
*City*: {ip_info['city']}
*Latitude*: {ip_info['lat']}
*Longitude*: {ip_info['lon']}
*ISP*: {ip_info['isp']}
*Organization*: {ip_info['org']}
*AS*: {ip_info['as']}
"""
            bot.reply_to(message, info, parse_mode='Markdown')
    except Exception as e:
        print(e)
        bot.reply_to(message, 'An error has occurred. Try later.')


if __name__ == '__main__':
    bot.polling()