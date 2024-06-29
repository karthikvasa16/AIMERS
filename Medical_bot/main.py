import telebot
import requests
import json

# Telegram bot token
BOT_TOKEN = '7358499257:AAHBRIBbGZIESCjG7oCn3Zcl943_05LI-eE'
bot = telebot.TeleBot(BOT_TOKEN)

# API details
API_URL = "https://drug-info-and-price-history.p.rapidapi.com/1/druginfo"
HEADERS = {
    "x-rapidapi-key": "e980a51c0dmshfee51235fc71445p1e7438jsnffd9be124e8b",
    "x-rapidapi-host": "drug-info-and-price-history.p.rapidapi.com"
}

# Helper function to send API request
def get_drug_info(drug_name):
    querystring = {"drug": drug_name}
    response = requests.get(API_URL, headers=HEADERS, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Start command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, (
        "Welcome! Use this bot to get drug information.\n"
        "Just send the name of the drug, and I'll fetch the details for you."
    ))

# Command handler for drug info
@bot.message_handler(func=lambda message: True)
def handle_drug_info(message):
    drug_name = message.text.strip()
    bot.reply_to(message, f"Searching for information on '{drug_name}'...")

    drug_info = get_drug_info(drug_name)
    if drug_info:
        response_text = json.dumps(drug_info, indent=2)  # Pretty print JSON for readability
        if len(response_text) > 4096:
            # Truncate the response if it's too long for Telegram
            response_text = response_text[:4093] + '...'
        bot.reply_to(message, f"Drug Information:\n{response_text}")
    else:
        bot.reply_to(message, "Sorry, I couldn't retrieve information for that drug.")

# Start polling
bot.polling()
