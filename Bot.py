import telebot
import pandas as pd
import yfinance as yf

TOKEN = "9124335377:AAGoZJazt2qIGTPryo86lJ0zZ5C-zchOxEE"
bot = telebot.TeleBot(TOKEN)

SYMBOL = "EURUSD=X"

def analyze_market():
    try:
        data = yf.download(tickers=SYMBOL, period="1d", interval="1m")
        if data.empty:
            return "Market data nahi mil saka, dobara koshish karein."
        
        prices = data['Close']
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        ema_fast = prices.ewm(span=9, adjust=False).mean()
        ema_slow = prices.ewm(span=21, adjust=False).mean()
        
        current_rsi = rsi.iloc[-1]
        current_fast = ema_fast.iloc[-1]
        current_slow = ema_slow.iloc[-1]
        
        if current_rsi < 35 and current_fast > current_slow:
            signal = "📈 BUY (Call) Signal"
        elif current_rsi > 65 and current_fast < current_slow:
            signal = "📉 SELL (Put) Signal"
        else:
            signal = "⏳ **WAIT / Sideways Market**"
            
        msg = (
            f"**Live Chart Analysis**\n"
            f"Current Price: `{prices.iloc[-1]:.5f}`\n"
            f"RSI (14): `{current_rsi:.2f}`\n"
            f"Direction: **{signal}**"
        )
        return msg
    except Exception as e:
        return f"Error aa gaya: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Salam! Main aap ka Quotex Style Trading Signal Bot hoon.\n"
        "Live signal lene ke liye command bhejein: /signal"
    )

@bot.message_handler(commands=['signal'])
def send_signal(message):
    bot.reply_to(message, "📊 Live chart analyze kiya ja raha hai...")
    result = analyze_market()
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()

