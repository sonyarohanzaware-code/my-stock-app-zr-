import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz

# 1. PREMIUM STANDARD TERMINAL CONFIGURATION
st.set_page_config(
    page_title="Institutional Algo-Intelligence Terminal", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS for Premium Terminal Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #2b6cb0; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #3182ce; }
    div[data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Institutional Algo-Intelligence & Precision Predictive Terminal")
st.markdown("Advanced Quantitative Forecasting Model with Custom Lot Size (0.1, 0.01) Risk Assessment in Dollars ($).")

# LIVE INDIAN TIME DISPLAYER
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
st.sidebar.markdown("### 🎛️ Terminal Control Center")
st.sidebar.info(f"📅 **Terminal Time (IST):** {current_time.strftime('%Y-%m-%d %I:%M:%S %p')}")

# --- INPUT CORE SELECTION PANEL ---
st.markdown("### ⚙️ 1. Quantitative Input & Risk Matrix")
col_ui1, col_ui2, col_ui3, col_ui4 = st.columns(4)

with col_ui1:
    assets_dict = {
        "Bitcoin (BTC-USD) ⚡": "BTC-USD",
        "Gold (XAUUSD=X) 🪙": "GC=F",
        "Silver (XAGUSD=X) 🥈": "SI=F",
        "Crude Oil 🛢️": "CL=F",
        "Ethereum (ETH-USD) 💎": "ETH-USD",
        "NIFTY 50 🇮🇳": "^NSEI",
        "BANK NIFTY 🇮🇳": "^NSEBANK",
        "SENSEX 🇮🇳": "^BSESN",
        "SBI (SBIN.NS) 🏦": "SBIN.NS",
        "RELIANCE INDUSTRIES 🏭": "RELIANCE.NS",
        "TATA MOTORS 🚗": "TATAMOTORS.NS"
    }
    selected_display = st.selectbox("Asset Class Structure:", list(assets_dict.keys()))
    ticker_symbol = assets_dict[selected_display]

with col_ui2:
    trading_style = st.selectbox("Trading Modality Frame:", ["Scalping", "Intraday", "Swing", "Position"])

with col_ui3:
    target_date = st.date_input("Fix Analytics Date:", current_time.date())
    target_time = st.time_input("Fix Analytics Time Point:", time(9, 15))

with col_ui4:
    # --- NEW: LOT SIZE INPUT FIELD ---
    lot_size = st.number_input("Enter Lot Size (e.g., 0.01, 0.1, 1.0):", min_value=0.001, max_value=100.0, value=0.01, step=0.01, format="%.3f")

st.markdown("---")

# ADVANCED MATHEMATICAL MATRIX QUANT MATHS
def calculate_advanced_signals(df, style):
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    latest_candle_body = df['Close'].iloc[-1] - df['Open'].iloc[-1]
    avg_candle_body = (df['Close'] - df['Open']).abs().rolling(window=10).mean().iloc[-1]
    
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    atr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1).rolling(window=14).mean().iloc[-1]
    
    if pd.isna(atr):
        atr = df['Close'].iloc[-1] * 0.01

    tech_score = 0
    if df['Close'].iloc[-1] > df['EMA_20'].iloc[-1]: tech_score += 1.5
    if df['RSI'].iloc[-1] > 52: tech_score += 1.0
    if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1]: tech_score += 1.5
    if latest_candle_body > 0 and abs(latest_candle_body) > avg_candle_body: tech_score += 1.0
    
    max_tech_score = 5.0
    algo_bull_prob = (tech_score / max_tech_score) * 100
    
    if style == "Scalping":
        horizon_desc = "Next 5 to 15 Minutes window."
        sl_factor, tgt_factor = 0.15, 0.45
    elif style == "Intraday":
        horizon_desc = "Valid till standard session close today."
        sl_factor, tgt_factor = 0.50, 1.25
    elif style == "Swing":
        horizon_desc = "3 Trading Days to 2 Weeks maximum."
        sl_factor, tgt_factor = 1.30, 3.20
    else:
        horizon_desc = "1 Month to Quarter Target Projection."
        sl_factor, tgt_factor = 2.50, 6.50
        
    return algo_bull_prob, atr, horizon_desc, sl_factor, tgt_factor

# 2. LIVE ANALYSIS STREAM PIPELINE
if st.button("🚀 EXECUTE MATHEMATICAL PREDICTION MATRIX"):
    with st.spinner('Synchronizing server matrices and performing risk diagnostics...'):
        try:
            stock = yf.Ticker(ticker_symbol)
            df = stock.history(period="90d")
            
            if df.empty or len(df) < 30:
                st.error("Matrix Calibration Failed: Insufficient price history found.")
            else:
                bull_prob, atr_val, validity_horizon, sl_mult, tgt_mult = calculate_advanced_signals(df, trading_style)
                
                # --- LIVE INTELLIGENCE NEWS FEED ---
                news_list = stock.news
                news_score = 0
                latest_headline = "No critical data transmission found."
                news_impact_statement = "Neutral sentiment flows detected."
                
                bull_keys = ['growth', 'rally', 'surge', 'boom', 'breakout', 'profit', 'gain', 'support', 'high', 'rise', 'positive', 'upgrade']
                bear_keys = ['drop', 'crash', 'slump', 'dump', 'inflation', 'fear', 'risk', 'low', 'fall', 'loss', 'negative', 'downgrade']

                if news_list:
                    latest_headline = news_list[0].get('title', 'Headline format non-readable')
                    for article in news_list[:5]:
                        title = article.get('title', '').lower()
                        for w in bull_keys:
                            if w in title: news_score += 1
                        for w in bear_keys:
                            if w in title: news_score -= 1

                if news_score > 0:
                    news_bull_p = min(90.0, 50.0 + (news_score * 12))
                    news_impact_statement = "⚠️ STIMULUS IMPACT: Buying volume acceleration expected."
                elif news_score < 0:
                    news_bull_p = max(10.0, 50.0 + (news_score * 12))
                    news_impact_statement = "⚠️ BEARS IMPACT: Volatility downside risk is active."
                else:
                    news_bull_p = 50.0

                final_bullish_pct = (bull_prob * 0.70) + (news_bull_p * 0.30)
                final_bearish_pct = 100.0 - final_bullish_pct
                direction_bias = "BULLISH" if final_bullish_pct >= final_bearish_pct else "BEARISH"

                # LEVEL SELECTION
                latest_close = df['Close'].iloc[-1]
                
                if direction_bias == "BULLISH":
                    sl_level = latest_close - (atr_val * sl_mult)
                    tgt_level = latest_close + (atr_val * tgt_mult)
                    trend_flag = "📈 UPWARD MOMENTUM (Bullish Structuring)"
                else:
                    sl_level = latest_close + (atr_val * sl_mult)
                    tgt_level = latest_close - (atr_val * tgt_mult)
                    trend_flag = "📉 DOWNWARD MOMENTUM (Bearish Liquidating)"

                # --- NEW: DOLLAR RISK & REWARD ENGINE BASED ON LOT SIZE ---
                price_diff_sl = abs(latest_close - sl_level)
                price_diff_tgt = abs(latest_close - tgt_level)
                
                # Contract sizes details according to standard asset classes
                if "BTC-USD" in ticker_symbol:
                    # 1 Lot Bitcoin = 1 BTC. So Profit/Loss = Price Change * Lot Size
                    dollar_risk = price_diff_sl * lot_size
                    dollar_reward = price_diff_tgt * lot_size
                elif "ETH-USD" in ticker_symbol:
                    dollar_risk = price_diff_sl * lot_size
                    dollar_reward = price_diff_tgt * lot_size
                elif "GC=F" in ticker_symbol: # Gold
                    # Standard Gold Contract: 1 Lot = 100 Ounces
                    dollar_risk = price_diff_sl * 100 * lot_size
                    dollar_reward = price_diff_tgt * 100 * lot_size
                elif "SI=F" in ticker_symbol: # Silver
                    # Standard Silver Contract: 1 Lot = 5000 Ounces
                    dollar_risk = price_diff_sl * 5000 * lot_size
                    dollar_reward = price_diff_tgt * 5000 * lot_size
                elif "CL=F" in ticker_symbol: # Crude Oil
                    # Standard Crude Contract: 1 Lot = 1000 Barrels
                    dollar_risk = price_diff_sl * 1000 * lot_size
                    dollar_reward = price_diff_tgt * 1000 * lot_size
                else:
                    # For Indian Stocks / Indices (Approx USD value calculation based on average USDINR exchange rate)
                    usdinr_rate = 83.5
                    dollar_risk = (price_diff_sl * lot_size * 100) / usdinr_rate # Assuming standard lot multi
                    dollar_reward = (price_diff_tgt * lot_size * 100) / usdinr_rate

                is_crypto_or_global = "-" in ticker_symbol or "GC=" in ticker_symbol or "CL=" in ticker_symbol or "SI=" in ticker_symbol
                currency = "$" if is_crypto_or_global else "₹"

                # PANEL DISPLAY
                st.markdown("### 📊 2. Algorithmic Vector Probability Statistics")
                col_met1, col_met2 = st.columns(2)
                with col_met1:
                    st.write(f"🟢 **Bullish Probability:** {final_bullish_pct:.2f}%")
                    st.progress(int(final_bullish_pct))
                with col_met2:
                    st.write(f"🔴 **Bearish Probability:** {final_bearish_pct:.2f}%")
                    st.progress(int(final_bearish_pct))

                st.markdown("---")

                # PRECISION TRADING EXECUTION BLOCK
                st.markdown(f"### ⚡ 3. Institutional Execution Setup [{trading_style.upper()} MODE | LOT: {lot_size}]")
                
                col_p1, col_p2, col_p3 = st.columns(3)
                col_p1.metric(label="Current Spot Execution Price", value=f"{currency}{latest_close:.2f}")
                col_p2.metric(label="System Forecast Matrix", value=trend_flag)
                col_p3.metric(label="Volatility Index Spread (ATR)", value=f"{atr_val:.2f}")

                # THE PRECISION RISK-REWARD LAYOUT WITH DYNAMIC DOLLAR CALCULATIONS
                st.markdown("#### 🛠️ Precision Risk-Managed Entry Channels")
                col_box1, col_box2, col_box3 = st.columns(3)
                
                with col_box1:
                    st.markdown(f"""
                    <div style='border-left: 5px solid orange; background-color:#1e2430; padding:15px; border-radius:5px;'>
                        <b>🛒 Standard Entry Zone</b><br>
                        <h2 style='color:orange;'>{currency}{latest_close:.2f}</h2>
                        <small style='color:#a0aec0;'>Volume Lot Size Allocated: {lot_size}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_box2:
                    st.markdown(f"""
                    <div style='border-left: 5px solid #ff4b4b; background-color:#1e2430; padding:15px; border-radius:5px;'>
                        <b>🛑 Narrow Stop Loss (SL)</b><br>
                        <h2 style='color:#ff4b4b;'>{currency}{sl_level:.2f}</h2>
                        <h4 style='color:#ff8b8b; margin: 5px 0 0 0;'>💵 Risk: ${dollar_risk:.2f}</h4>
                        <small style='color:#a0aec0;'>Maximum expected dollar drawdown for this lot.</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_box3:
                    st.markdown(f"""
                    <div style='border-left: 5px solid #28a745; background-color:#1e2430; padding:15px; border-radius:5px;'>
                        <b>🎯 Profit Target (TGT)</b><br>
                        <h2 style='color:#28a745;'>{currency}{tgt_level:.2f}</h2>
                        <h4 style='color:#8bff8b; margin: 5px 0 0 0;'>💵 Profit: ${dollar_reward:.2f}</h4>
                        <small style='color:#a0aec0;'>Highly achievable estimated mathematical returns.</small>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Processing Error Interrupted: {e}")
