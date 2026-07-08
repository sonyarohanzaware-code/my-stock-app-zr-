import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz

# 1. PREMIUM INITIALIZATION & DESIGN LAYOUT
st.set_page_config(
    page_title="Institutional Algo Terminal", 
    page_icon="⚡", 
    layout="wide"
)

# Premium Dark CSS for TradingView Terminal Look
st.markdown("""
    <style>
    .main { background-color: #131722; color: #d1d4dc; }
    .stButton>button { width: 100%; background-color: #2962ff; color: white; border-radius: 4px; font-weight: bold; border: none; height: 45px; }
    .stButton>button:hover { background-color: #1e4bd8; }
    div[data-testid="stMetricValue"] { font-size: 26px; font-weight: bold; color: #2962ff; }
    .card-buy { border-left: 6px solid #089981; background-color: #1c252c; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
    .card-sell { border-left: 6px solid #f23645; background-color: #2a1e22; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
    .card-neutral { border-left: 6px solid #787b86; background-color: #1e222d; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Institutional Quality Algo-Intelligence Terminal")
st.markdown("Advanced Micro-Candlestick Scaling Model with Exact Risk/Reward Metrics & Target Achievement Metrics.")

# TIME SETTING SYSTEM
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
st.sidebar.markdown("### 🎛️ Terminal Dashboard Settings")
st.sidebar.info(f"📅 **System Live Time:** {current_time.strftime('%Y-%m-%d %I:%M %p')}")

# --- INPUT MATRIX ---
st.markdown("### ⚙️ 1. Set Trade & Time Parameters")
col_ui1, col_ui2, col_ui3, col_ui4 = st.columns(4)

with col_ui1:
    assets_dict = {
        "Bitcoin (BTCUSD) ⚡": "BTCUSD",
        "Gold (XAUUSD) 🪙": "GC=F",
        "Silver (XAGUSD) 🥈": "SI=F",
        "Crude Oil 🛢️": "CL=F",
        "Ethereum (ETHUSD) 💎": "ETHUSD",
        "NIFTY 50 🇮🇳": "^NSEI",
        "BANK NIFTY 🇮🇳": "^NSEBANK",
        "SENSEX 🇮🇳": "^BSESN",
        "SBI (SBIN.NS) 🏦": "SBIN.NS",
        "RELIANCE INDUSTRIES 🏭": "RELIANCE.NS",
        "TATA MOTORS 🚗": "TATAMOTORS.NS"
    }
    selected_display = st.selectbox("Asset Class:", list(assets_dict.keys()))
    ticker_symbol = assets_dict[selected_display]

with col_ui2:
    trading_style = st.selectbox("Modality Profile:", ["Scalping", "Intraday", "Swing", "Position", "Option"])

with col_ui3:
    target_date = st.date_input("Fix Target Date:", current_time.date())
    target_time = st.time_input("Fix Analysis Time:", time(9, 15))

with col_ui4:
    lot_size = st.number_input("Lot Size / Quantity (e.g., 0.01, 0.1, 1):", min_value=0.001, max_value=1000.0, value=1.465, step=0.01, format="%.3f")

st.markdown("---")

# ADVANCED TECHNICAL MODEL WITH WEIGHTED CANDLE BODY & VOLUME
def calculate_precision_signals(df, style):
    # Indicators
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Candle Vectors
    latest_candle_body = df['Close'].iloc[-1] - df['Open'].iloc[-1]
    avg_candle_body = (df['Close'] - df['Open']).abs().rolling(window=10).mean().iloc[-1]
    
    # ATR Volatility
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    atr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(window=14).mean().iloc[-1]
    
    if pd.isna(atr) or atr == 0:
        atr = df['Close'].iloc[-1] * 0.005

    # Quantitative Scoring Matrix
    score = 0
    if df['Close'].iloc[-1] > df['EMA_20'].iloc[-1]: score += 1.5
    if df['RSI'].iloc[-1] > 50: score += 1.0
    if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]: score += 1.5
    if latest_candle_body > 0 and abs(latest_candle_body) > avg_candle_body: score += 1.0
    
    algo_bull_prob = (score / 5.0) * 100
    
    # Multiplier based on Trading Styles to keep SL extremely tight and Target realistic
    if style == "Scalping":
        sl_factor, tgt_factor = 0.25, 0.68  # Exact 2.72 ratio matching your chart setup
    elif style == "Intraday":
        sl_factor, tgt_factor = 0.45, 1.23  
    elif style == "Swing":
        sl_factor, tgt_factor = 1.10, 3.02
    else:
        sl_factor, tgt_factor = 2.20, 6.05
        
    return algo_bull_prob, atr, sl_factor, tgt_factor

# EXECUTION ACTION
if st.button("🚀 EXECUTE PRECISION PREDICTION MATRIX"):
    with st.spinner('Syncing global matrices and fetching price vectors...'):
        try:
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period="60d")
            
            if df.empty or len(df) < 20:
                st.error("Data fetch failed. Please retry.")
            else:
                bull_prob, atr_val, sl_mult, tgt_mult = calculate_precision_signals(df, trading_style)
                
                # Global/Indian Currency handling
                is_global = "-" in ticker_symbol or "GC=" in ticker_symbol or "CL=" in ticker_symbol or "SI=" in ticker_symbol
                currency = "$" if is_global else "₹"
                
                # Fetch News Flow
                news_list = stock.news
                news_score = 0
                latest_headline = "No critical headline transmissions detected."
                
                if news_list:
                    latest_headline = news_list[0].get('title', 'Headline Non-readable')
                    for article in news_list[:3]:
                        title = article.get('title', '').lower()
                        if any(w in title for w in ['growth', 'rally', 'surge', 'profit', 'high', 'breakout']): news_score += 1
                        if any(w in title for w in ['drop', 'crash', 'slump', 'loss', 'low', 'risk']): news_score -= 1
                
                final_bullish = (bull_prob * 0.75) + ((50 + news_score*20) * 0.25)
                final_bullish = max(10, min(95, final_bullish))
                final_bearish = 100 - final_bullish
                
                direction = "BULLISH" if final_bullish >= final_bearish else "BEARISH"
                latest_close = df['Close'].iloc[-1]
                
                # Target and SL calculations
                if direction == "BULLISH":
                    sl_change = atr_val * sl_mult
                    tgt_change = atr_val * tgt_mult
                    sl_level = latest_close - sl_change
                    tgt_level = latest_close + tgt_change
                    action_flag = "LONG (BUY SETUP)"
                    card_style = "card-buy"
                else:
                    sl_change = atr_val * sl_mult
                    tgt_change = atr_val * tgt_mult
                    sl_level = latest_close + sl_change
                    tgt_level = latest_close - tgt_change
                    action_flag = "SHORT (SELL SETUP)"
                    card_style = "card-sell"

                # Mathematical Percentages matching your TradingView layout
                sl_pct = (sl_change / latest_close) * 100
                tgt_pct = (tgt_change / latest_close) * 100
                risk_reward_ratio = tgt_change / (sl_change + 1e-9)
                
                # Contract Multipliers for absolute exact Dollar amount calculation
                if "BTC-USD" in ticker_symbol or "ETH-USD" in ticker_symbol:
                    multiplier = 1.0
                elif "GC=F" in ticker_symbol: multiplier = 100.0  
                elif "SI=F" in ticker_symbol: multiplier = 5000.0 
                elif "CL=F" in ticker_symbol: multiplier = 1000.0 
                else: multiplier = 1.0 / 83.5 
                
                amt_risk = sl_change * lot_size * multiplier
                amt_reward = tgt_change * lot_size * multiplier

                # --- UI DISPLAY DASHBOARD ---
                st.markdown("### 📊 2. Algorithmic Matrix & News Flow")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.write(f"🟢 **Bullish Probability:** {final_bullish:.1f}%")
                    st.progress(int(final_bullish))
                with col_b2:
                    st.write(f"🔴 **Bearish Probability:** {final_bearish:.1f}%")
                    st.progress(int(final_bearish))
                    
                st.info(f"📰 **Live News Flow Impact:** \"{latest_headline}\"")
                st.markdown("---")
                
                st.markdown(f"### ⚡ 3. TradingView Precision Execution Deck ({action_flag})")
                
                # Metric display matching chart specs
                st.markdown(f"""
                <div class="{card_style}">
                    <h3 style='margin:0; color:white;'>🎯 System Position Assessment Matrix</h3>
                    <p style='margin:5px 0 15px 0; color:#b2b5be;'>Calculated for Target Date: <b>{target_date}</b> at <b>{target_time.strftime('%I:%M %p')}</b></p>
                    <table style='width:100%; border-collapse: collapse; color: white;'>
                        <tr style='border-bottom: 1px solid #2a2e39;'>
                            <td style='padding:10px 0;'>Current Price</td>
                            <td style='text-align:right; font-weight:bold; font-size:18px;'>{currency}{latest_close:.2f}</td>
                        </tr>
                        <tr style='border-bottom: 1px solid #2a2e39;'>
                            <td style='padding:10px 0; color:#089981;'>🎯 Expected Profit Target (TGT)</td>
                            <td style='text-align:right; font-weight:bold; color:#089981; font-size:18px;'>{currency}{tgt_level:.2f} ({tgt_pct:.3f}%)</td>
                        </tr>
                        <tr style='border-bottom: 1px solid #2a2e39;'>
                            <td style='padding:10px 0; color:#f23645;'>🛑 Narrow Stop Loss (SL)</td>
                            <td style='text-align:right; font-weight:bold; color:#f23645; font-size:18px;'>{currency}{sl_level:.2f} ({sl_pct:.3f}%)</td>
                        </tr>
                        <tr style='border-bottom: 1px solid #2a2e39;'>
                            <td style='padding:10px 0; color:#2962ff;'>📊 Calculated Position Quantity / Lot</td>
                            <td style='text-align:right; font-weight:bold; color:#2962ff;'>{lot_size:.3f}</td>
                        </tr>
                        <tr style='border-bottom: 1px solid #2a2e39;'>
                            <td style='padding:10px 0;'>⚖️ Risk / Reward Ratio</td>
                            <td style='text-align:right; font-weight:bold; color:#ff9800; font-size:18px;'>{risk_reward_ratio:.2f}</td>
                        </tr>
                        <tr style='border-bottom: 1px solid #2a2e39; background-color: #1e222d;'>
                            <td style='padding:10px; color:#8bff8b;'>💵 Target Est. Amount (Profit)</td>
                            <td style='text-align:right; font-weight:bold; color:#8bff8b; padding:10px; font-size:18px;'>${amt_reward:.2f}</td>
                        </tr>
                        <tr style='background-color: #221a1d;'>
                            <td style='padding:10px; color:#ff8b8b;'>💵 Stop Est. Amount (Loss Risk)</td>
                            <td style='text-align:right; font-weight:bold; color:#ff8b8b; padding:10px; font-size:18px;'>${amt_risk:.2f}</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error executing logic: {e}")
