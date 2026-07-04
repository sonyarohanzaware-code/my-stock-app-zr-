import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

# 1. PAGE SETUP
st.set_page_config(page_title="Advanced Smart Market Predictor", page_icon="🔮", layout="centered")

st.title("🔮 AI Smart Market & Forex Predictor")
st.markdown("Apni marzi ki **Date aur Time** chunin, aur system apne smart algorithm se us time frame ka analysis karega.")

# LIVE INDIAN TIME DISPLAY
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
st.sidebar.info(f"📅 **Live Time (IST):** {current_time.strftime('%Y-%m-%d %I:%M %p')}")

# --- NEW: DATE & TIME FIXING SELECTION INTERFACE ---
st.subheader("⚙️ Analysis Settings (Time & Date Fix Karein)")

# Kal ki date tak ka data select karne ke liye default values
default_start_date = current_time.date() - timedelta(days=30)
default_end_date = current_time.date()

col_date1, col_date2 = st.columns(2)
with col_date1:
    start_date = st.date_input("Kab se start karna hai? (Start Date)", default_start_date)
with col_date2:
    end_date = st.date_input("Kab tak ka check karna hai? (End Date)", default_end_date)

# Error validation agar user galat date chunta hai
if start_date > end_date:
    st.error("❌ Error: Start Date, End Date se pehle ki honi chahiye!")

st.markdown("---")

# TECHNICAL INDICATORS FUNCTIONS
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def calculate_macd(series):
    exp1 = series.ewm(span=12, adjust=False).mean()
    exp2 = series.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# 2. GLOBAL & INDIAN ASSETS DICTIONARY
global_assets = {
    "Nifty 50 Index 🇮🇳": "^NSEI",
    "Bank Nifty Index 🇮🇳": "^NSEBANK",
    "Gold (Sona) 🪙": "GC=F",
    "Silver (Chandi) 🥈": "SI=F",
    "Crude Oil (Kacha Tel) 🛢️": "CL=F",
    "Bitcoin (BTC-USD) ⚡": "BTC-USD",
    "Ethereum (ETH-USD) 💎": "ETH-USD",
    "Reliance Industries 🇮🇳": "RELIANCE.NS",
    "Tata Motors 🇮🇳": "TATAMOTORS.NS"
}

selected_asset = st.selectbox("Apna Asset/Stock Select Karein:", list(global_assets.keys()))
ticker_symbol = global_assets[selected_asset]

# Custom Ticker Input Box
custom_ticker = st.text_input("Ya koi dusra custom ticker daalein (e.g., SBIN.NS ya EURUSD=X):", "")
if custom_ticker:
    ticker_symbol = custom_ticker.upper()

# 3. LIVE SMART ANALYSIS LOGIC
if st.button("🔍 Run Smart Intelligence Analysis"):
    if start_date >= end_date:
        st.warning("Kripya sahi date range select karein.")
    else:
        with st.spinner('Fix kiye gaye time frame ka data calculate ho raha hai...'):
            try:
                stock = yf.Ticker(ticker_symbol)
                
                # User ki select ki hui date range ke mutabik data fetch karna
                df = stock.history(start=start_date, end=end_date)
                
                if df.empty or len(df) < 15:
                    st.error(f"❌ Selected Date Range ({start_date} se {end_date}) ke beech ka paryapt (enough) data nahi mila. Kripya date range badhayein.")
                else:
                    # 4. ALGORITHM ENGINE CALCULATIONS
                    df['SMA_20'] = df['Close'].rolling(window=min(20, len(df))).mean()
                    df['RSI'] = calculate_rsi(df['Close'], period=min(14, len(df)-1))
                    df['MACD'], df['MACD_Signal'] = calculate_macd(df['Close'])
                    
                    latest_close = df['Close'].iloc[-1]
                    rsi = df['RSI'].iloc[-1]
                    macd = df['MACD'].iloc[-1]
                    macd_signal = df['MACD_Signal'].iloc[-1]
                    sma_20 = df['SMA_20'].iloc[-1] if not pd.isna(df['SMA_20'].iloc[-1]) else latest_close
                    
                    # Smart Intelligence Signals Scoring
                    bullish_signals = 0
                    total_signals = 3
                    
                    if latest_close > sma_20: bullish_signals += 1
                    if rsi > 50: bullish_signals += 1
                    if macd > macd_signal: bullish_signals += 1
                    
                    algo_bullish_pct = (bullish_signals / total_signals) * 100
                    algo_bearish_pct = 100 - algo_bullish_pct

                    # 5. NEWS INTELLIGENCE BIAS
                    news_list = stock.news
                    news_bullish_pct, news_bearish_pct = 50.0, 50.0
                    
                    bullish_keywords = ['growth', 'rally', 'surge', 'boom', 'breakout', 'profit', 'gain', 'support', 'high', 'rise']
                    bearish_keywords = ['drop', 'crash', 'slump', 'dump', 'inflation', 'fear', 'risk', 'low', 'fall', 'loss']

                    if news_list:
                        news_score = 0
                        for article in news_list[:5]:
                            title = article.get('title', '').lower()
                            for word in bullish_keywords:
                                if word in title: news_score += 1
                            for word in bearish_keywords:
                                if word in title: news_score -= 1
                                
                        if news_score > 0:
                            news_bullish_pct, news_bearish_pct = 75.0, 25.0
                        elif news_score < 0:
                            news_bullish_pct, news_bearish_pct = 25.0, 75.0

                    # FINAL WEIGHTED PERCENTAGE (60% Tech Algo + 40% Intelligence News)
                    final_bullish = (algo_bullish_pct * 0.60) + (news_bullish_pct * 0.40)
                    final_bearish = (algo_bearish_pct * 0.60) + (news_bearish_pct * 0.40)

                    # INTERFACE DISPLAY
                    st.success(f"✅ Data processed successfully for range: {start_date} to {end_date}")
                    
                    col1, col2, col3 = st.columns(3)
                    if "$" in ticker_symbol or "=" in ticker_symbol or "GC" in ticker_symbol or "CL" in ticker_symbol:
                        col1.metric("Closing Price", f"${latest_close:.2f}")
                    else:
                        col1.metric("Closing Price", f"₹{latest_close:.2f}")
                        
                    col2.metric("RSI (Strength)", f"{rsi:.2f}")
                    col3.metric("Trend Status", "🟢 Bullish" if macd > macd_signal else "🔴 Bearish")

                    st.markdown("---")
                    
                    # PERCENTAGE OUTPUT BARS
                    st.subheader("📊 Smart AI Intelligence Results")
                    
                    st.write(f"🟢 **BULLISH Percentage: {final_bullish:.2f}%**")
                    st.progress(int(final_bullish))
                    
                    st.write(f"🔴 **BEARISH Percentage: {final_bearish:.2f}%**")
                    st.progress(int(final_bearish))
                    
                    st.markdown("---")
                    
                    # FINAL CONCLUSION BOX
                    if abs(final_bullish - final_bearish) < 5:
                        st.warning("⚖️ **INTELLIGENCE CONCLUSION: NEUTRAL** (Market rangebound ya sideways trend mein hai)")
                    elif final_bullish > final_bearish:
                        st.success("📈 **INTELLIGENCE CONCLUSION: STRONG BULLISH** (Aapke chune gaye samay ke hisab se market tezi ki taraf jhuka hai)")
                    else:
                        st.error("📉 **INTELLIGENCE CONCLUSION: STRONG BEARISH** (Aapke chune gaye samay ke hisab se market mandi ki taraf jhuka hai)")

            except Exception as e:
                st.error(f"Analysis karne mein dikkat aayi: {e}")
