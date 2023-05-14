from dotenv import load_dotenv
import requests
import telebot
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

COINMARKETCAP_API = os.getenv('COINMARKETCAP_API')

ETHERSCAN_API = os.getenv('ETHERSCAN_API')

telBot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

CmarketCap_headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COINMARKETCAP_API
}

@telBot.message_handler(commands=['start'])
def send_commands(message):
    telBot.reply_to(message, """Here are some commands you can use to get started:

- /btcfees: Get the recommended fee for Bitcoin transactions
- /ethgas: Get the recommended fee for Ethereum transactions""")
    
@telBot.message_handler(commands=['btcfees'])
def send_btcfee(message):
    requestBtcFees = ""
    requestSATPrice = ""
    
    try:
        requestBtcFees = requests.get("https://mempool.space/api/v1/fees/recommended")
        dataBtcFees = requestBtcFees.json()

        requestSATPrice = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=SATS&convert=USD", headers=CmarketCap_headers)
        SATPrice = requestSATPrice.json()['data']['SATS']['quote']['USD']['price']

        feeDict = ["fastestFee", "halfHourFee", "hourFee", "economyFee"]
        fees = []

        for fee in feeDict:
            fees.append(f"{dataBtcFees[fee]} sat/vB (${'{:,.2f}'.format(SATPrice * (dataBtcFees[fee] * 140))})")

        telBot.reply_to(message,f"""
The recommended fees for Bitcoin transactions:

    ●🚀 High-Priority: <b>{fees[0]}</b>
    ●💨 Mid-Priority (Half-Hour): <b>{fees[1]}</b>
    ●🐢 Low-Priority (Hour): <b>{fees[2]}</b>

    ●💸 Economic: <b>{fees[3]}</b>

The minimum fee for Bitcoin transactions is: <b>{dataBtcFees['minimumFee']} sat/vB</b>""")
        
    except:
        telBot.reply_to(message, "⁉ An error has occurred. Please try again later.")

@telBot.message_handler(commands=['ethgas'])
def send_ethgas(message):
    requestEthFees = ""
    
    try:
        requestEthFees = requests.get(f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API}")
        dataEthFees = requestEthFees.json()['result']

        gasDict = ["FastGasPrice", "ProposeGasPrice", "SafeGasPrice"]
        gas = []

        for fee in gasDict:
            gas.append(f"{dataEthFees[fee]} Gwei (${'{:,.2f}'.format(int(dataEthFees[fee]) * 0.036)})")

        telBot.reply_to(message,f"""
The recommended fees for Ethereum transactions:

    ●🟢 Fast: <b>{gas[0]}</b>
    ●🟡 Standard: <b>{gas[1]}</b>
    ●🔵 Safe: <b>{gas[2]}</b>
""")
        
    except:
        telBot.reply_to(message, "⁉ An error has occurred. Please try again later.")

print(f"@{telBot.get_me().username} is running...")
telBot.infinity_polling()