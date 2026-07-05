import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# PAGE CONFIGURATION
st.set_page_config(page_title="Pro Algo-Intelligence Predictor", page_icon="📈", layout="wide")

st.title("🚀 Pro Algo-Intelligence & Trading Strategy Predictor")
st.markdown("Yeh system fixed-time news aur dynamic calculation ke basis par exact trading levels provide karta hai.")

# LIVE INDIAN TIME DISPLAY
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
st.sidebar.info(f"📅 **System Time (IST):** {current_time.strftime('%Y-%m-%d %I:%M %p')}")

# --- DYNAMIC ASSETS MAPPING ---
assets_dict = {
    "1. Bitcoin (BTC-USD) ⚡": "BTC-USD",
    "2. Gold (XAUUSD=X) 🪙": "GC=F",
    "3. Silver (XAGUSD=X) 🥈": "SI=F",
    "4. Crude Oil 🛢️": "CL=F",
    "5. Ethereum (ETH-USD) 💎": "ETH-USD",
    "6. NIFTY 50 🇮🇳": "^NSEI",
    "7. BANK NIFTY 🇮🇳": "^NSEBANK",
    "8. SENSEX 🇮🇳": "^BSESN",
    "9. SBI (SBIN.NS) 🏦": "SBIN.NS",
    "10. RELIANCE INDUSTRIES 🏭": "RELIANCE.NS",
    "11. TATA MOTORS 🚗": "TATAMOTORS.NS"
}

# USER INTERFACE - MAIN SETTINGS
st.subheader("⚙️ 1. Asset & Target Configuration")
col_ui1, col_ui2, col_ui3 = st.columns(3)

with col_ui1:
    selected_display = st.selectbox("Select Stock / Index / Forex:", list(assets_dict.keys()))
    ticker_symbol = assets_dict[selected_display]

with col_ui2:
    target_date = st.date_input("Fix Prediction Date:", current_time.date())

with col_ui3:
    trading_style = st.selectbox("Choose Trading Style:", ["Scalping (Minutes)", "Intraday (1 Day)", "Swing (Days-Weeks)", "Position (Weeks-Months)"])

st.markdown("---")

# TECHNICAL MATHEMATICAL ENGINES
def calculate_atr(df, period=14):
    """Volatility tracking for accurate Stop Loss and Target calculations"""
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    df_tr = pd.concat([high_low, high_cp, low_cp], axis=1)
    true_range = np.max(df_tr, axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr.iloc[-1] if not pd.isna(atr.iloc[-1]) else (df['Close'].iloc[-1] * 0.01)

# CORE INTELLIGENCE BUTTON
if st.button("🔥 Run Professional Strategy Engine"):
    with st.spinner('Calculating target levels and parsing news intelligence...'):
        try:
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period="30d")
            
            if df.empty:
                st.error("Data load nahi ho saka. Ticker verification check karein.")
            else:
                latest_close = df['Close'].iloc[-1]
                atr_value = calculate_atr(df)
                
                # --- PURE CURRENT NEWS IMPACT INTELLIGENCE ---
                news_list = stock.news
                news_score = 0
                scanned_count = 0
                
                bullish_keywords = ['growth', 'rally', 'surge', 'boom', 'breakout', 'profit', 'gain', 'support', 'high', 'rise', 'positive', 'upgrade']
                bearish_keywords = ['drop', 'crash', 'slump', 'dump', 'inflation', 'fear', 'risk', 'low', 'fall', 'loss', 'negative', 'downgrade']

                if news_list:
                    for article in news_list[:5]:
                        title = article.get('title', '').lower()
                        scanned_count += 1
                        for word in bullish_keywords:
                            if word in title: news_score += 1
                        for word in bearish_keywords:
                            if word in title: news_score -= 1

                # Exact Percentage distribution based strictly on latest news analysis
                if news_score > 0:
                    bullish_pct = min(85.0, 50.0 + (news_score * 10))
                elif news_score < 0:
                    bullish_pct = max(15.0, 50.0 + (news_score * 10))
                else:
                    bullish_pct = 50.0
                    
                bearish_pct = 100.0 - bullish_pct
                
                # --- TRADING HORIZON PREDICTION TIME ---
                if trading_style == "Scalping (Minutes)":
                    time_horizon = "5 Mins to 15 Mins maximum."
                    sl_multiplier, tgt_multiplier = 0.2, 0.4
                elif trading_style == "Intraday (1 Day)":
                    time_horizon = "Till Market Closing Today."
                    sl_multiplier, tgt_multiplier = 0.6, 1.2
                elif trading_style == "Swing (Days-Weeks)":
                    time_horizon = "3 Days to 2 Weeks."
                    sl_multiplier, tgt_multiplier = 1.5, 3.0
                else:
                    time_horizon = "1 Month to 3 Months."
                    sl_multiplier, tgt_multiplier = 3.0, 6.0

                # MATHEMATICAL POSITION ARCHITECTURE (Target & Stop Loss Engine)
                is_bullish = bullish_pct > bearish_pct
                currency_symbol = "$" if ("-" in ticker_symbol or "GC=" in ticker_symbol or "CL=" in ticker_symbol) else "₹"
                
                if is_bullish:
                    trade_direction = "BUY (Long Position)"
                    stop_loss = latest_close - (atr_value * sl_multiplier)
                    target_level = latest_close + (atr_value * tgt_multiplier)
                else:
                    trade_direction = "SELL (Short Position)"
                    stop_loss = latest_close + (atr_value * sl_multiplier)
                    target_level = latest_close - (atr_value * tgt_multiplier)

                # DISPLAY DASHBOARD PANELS
                st.markdown("### 📊 2. News Intelligence Analysis Engine")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.write(f"🟢 **Bullish Probability:** {bullish_pct:.1f}%")
                    st.progress(int(bullish_pct))
                with col_res2:
                    st.write(f"🔴 **Bearish Probability:** {bearish_pct:.1f}%")
                    st.progress(int(bearish_pct))
                    
                st.info(f"⏳ **Prediction Validity Horizon:** Yeh trend **{time_horizon}** tak active reh sakta hai.")
                st.markdown("---")
                
                # PROFESSIONAL TRADING SIGNALS FRAMEWORK
                st.markdown(f"### ⚡ 3. Professional Execution Setup ({trading_style})")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric(label="Current Execution Price", value=f"{currency_symbol}{latest_close:.2f}")
                
                if is_bullish:
                    col_m2.metric(label="Recommended Action", value=trade_direction, delta="📈 BULLISH BIAS")
                else:
                    col_m2.metric(label="Recommended Action", value=trade_direction, delta="-📉 BEARISH BIAS", delta_color="inverse")
                    
                col_m3.metric(label="Calculated Volatility (ATR)", value=f"{atr_value:.2f}")
                
                # TARGET AND STOP LOSS BOXES
                st.markdown("#### 🛠️ Entry Levels Layout")
                col_box1, col_box2 = st.columns(2)
                
                with col_box1:
                    st.error(f"🚫 **Strict Stop Loss (SL):** {currency_symbol}{stop_loss:.2f}")
                with col_box2:
                    st.success(f"🎯 **Expected Profit Target (TGT):** {currency_symbol}{target_level:.2f}")
                    
                st.caption("💡 Tip: Yeh targets mathematically Volatility Indicator (ATR) ke data par calculated hain, jo risk-to-reward ratio ko maintain karte hain.")
                
        except Exception as e:
            st.error(f"Calculation Error: {e}")
