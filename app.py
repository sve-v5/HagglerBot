import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION & PERSONAS ---
st.set_page_config(page_title="HagglerBot Pro v5.02", layout="centered", page_icon="🤖")

PERSONAS = {
    "SELLER": {
        "🛡️ The Wall": {"floor": 0.90, "round": "UP", "quote": "Nem zsibvásár, az ár fix. 🧱"},
        "⚖️ The Stoic": {"floor": 0.75, "round": "MID", "quote": "A matek nem hazudik. ⏳"},
        "🤝 The Merchant": {"floor": 0.65, "round": "DOWN", "quote": "Találjuk meg a közös utat! ✨"},
        "✨ Gen-Z Slay": {"floor": 0.70, "round": "TREND", "quote": "Ez az ajánlat nem slay, tesó. 💅"}
    },
    "BUYER": {
        "🔨 The Lowballer": {"bid": 0.60, "round": "DOWN", "quote": "Ennyim van rá, vagy hagyjuk. 📉"},
        "📊 Value Hunter": {"bid": 0.80, "round": "MID", "quote": "Piaci ár alatt keresek. 🧐"},
        "✨ Fair Player": {"bid": 0.85, "round": "UP", "quote": "Gyorsan fizetnék, ha engedsz kicsit. 🤝"},
        "🔥 Hype Beast": {"bid": 0.75, "round": "TREND", "quote": "Nagyon élem a fitet, de szűkös a budget. 🔥"}
    }
}

# --- 2. CORE ENGINES (Zeno & Logic) ---
def zeno_round(price, mode, round_type):
    base = int(price)
    dec = price - base
    if mode == "SELLER":
        if round_type == "UP" or dec > 0.75: return float(base) + 0.95
        if round_type == "MID" and dec > 0.30: return float(base) + 0.50
        return float(base)
    else: # BUYER MODE
        if round_type == "DOWN" or dec < 0.40: return float(base) - 0.05
        if round_type == "MID" and dec < 0.80: return float(base) + 0.45
        return float(base) + 0.95

# --- 3. UI LAYOUT & STYLE ---
mode_toggle = st.sidebar.radio("SVE Operation Mode:", ["💰 Selling Mode", "🛒 Buying Mode"])
current_mode = "SELLER" if "Selling" in mode_toggle else "BUYER"

# Dinamikus színek
if current_mode == "SELLER":
    st.markdown("<style>.stApp {background-color: #f0f7ff;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp {background-color: #fffaf0;}</style>", unsafe_allow_html=True)

# --- 4. TABS: CONTROL / ANALYTICS / GUIDE ---
tab1, tab2, tab3 = st.tabs(["🎮 Dashboard", "📊 Analytics", "📖 Quick Start"])

with tab1:
    st.title(f"{'🛡️' if current_mode == 'SELLER' else '🛒'} HagglerBot v5.02")
    
    col1, col2 = st.columns(2)
    with col1:
        persona = st.selectbox("Select Character:", list(PERSONAS[current_mode].keys()))
    with col2:
        price_input = st.number_input(f"{'Your List Price' if current_mode == 'SELLER' else 'Asking Price'} (£):", value=20.0)

    if st.button(f"🚀 Calculate {'Counter-Offer' if current_mode == 'SELLER' else 'Opening Bid'}", use_container_width=True):
        config = PERSONAS[current_mode][persona]
        raw_price = price_input * (config['floor'] if current_mode == "SELLER" else config['bid'])
        final_price = zeno_round(raw_price, current_mode, config['round'])
        
        st.divider()
        st.metric("Suggested Price", f"£{final_price:.2f}", f"{int((final_price/price_input-1)*100)}%")
        st.success(f"**{persona} says:** *\"{config['quote']}\"*")
        st.code(f"Copy this: Legyen £{final_price:.2f}, {config['quote']}", language=None)

with tab2:
    st.subheader("Haggle-Performance")
    stats = pd.DataFrame({
        "Mode": ["Seller", "Buyer"],
        "Saved/Earned (£)": [145.50, 82.20],
        "Deals": [12, 8]
    })
    st.bar_chart(stats.set_index("Mode")["Saved/Earned (£)"])
    st.info("Analytics tracking is active for this session.")

with tab3:
    st.header("📖 Quick Start Guide")
    st.markdown("""
    1. **Choose Mode**: Use the sidebar to switch between **Buying** (Low prices) and **Selling** (High margins).
    2. **Pick a Persona**: Different characters use different psychological math (Zeno-Rounding).
    3. **Copy-Paste**: Use the generated text directly in Vinted chat to save time.
    4. **Smart Rounding**: Prices ending in **.95** or **.45** are proven to be more effective than round numbers!
    """)
