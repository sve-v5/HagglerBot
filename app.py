import streamlit as st
import pandas as pd
import random
import time

# --- 1. CONFIG & PERSONAS ---
st.set_page_config(page_title="HagglerBot Pro v5.4", layout="centered", page_icon="🤖")

PERSONAS = {
    "SELLER": {
        "🛡️ The Wall": {"floor": 0.92, "flex": 0.1, "quote": "Nem zsibvásár, az ár fix. 🧱"},
        "⚖️ The Stoic": {"floor": 0.82, "flex": 0.3, "quote": "A matek nem hazudik. ⏳"},
        "🤝 The Merchant": {"floor": 0.70, "flex": 0.6, "quote": "Találjuk meg a közös utat! ✨"}
    }
}

# --- 2. SESSION STATE INICIALIZÁLÁS (A hiba javítása itt van) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_bot_price" not in st.session_state:
    st.session_state.current_bot_price = 0.0
if "target_p" not in st.session_state:
    st.session_state.target_p = 0.0

# --- 3. UI TABS ---
tab1, tab2, tab3 = st.tabs(["🎮 Dashboard", "💬 Alku-szimulátor", "📊 Analitika"])

with tab1:
    st.title("HagglerBot v5.4")
    price_input = st.number_input("Termék ára (£):", value=20.0)
    persona = st.selectbox("Karakter:", list(PERSONAS["SELLER"].keys()))
    
    if st.button("Kalkuláció"):
        res = price_input * PERSONAS["SELLER"][persona]["floor"]
        st.metric("Javasolt ár", f"£{res:.2f}")
        st.session_state.history.append({"Idő": pd.Timestamp.now(), "Ár": res})

with tab2:
    st.subheader("Alku-szimulátor")
    col_a, col_b = st.columns(2)
    start_p = col_a.number_input("Kezdő ár:", value=100.0, key="sim_p")
    bot_style = col_b.selectbox("Eladó stílusa:", list(PERSONAS["SELLER"].keys()), key="sim_s")
    
    if st.button("Szimuláció Reset"):
        st.session_state.messages = []
        st.session_state.current_bot_price = float(start_p)
        st.session_state.target_p = float(start_p * PERSONAS["SELLER"][bot_style]["floor"])
        st.session_state.messages.append({"role": "assistant", "content": f"Szia! £{start_p} az ára. Érdekel?"})
        st.rerun()

    # Üzenetek megjelenítése
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    # Chat Logika
    if user_offer := st.chat_input("Ajánlatod (pl: 80)..."):
        try:
            offer_val = float(user_offer)
            st.session_state.messages.append({"role": "user", "content": f"Legyen £{offer_val}"})
            
            with st.chat_message("assistant"):
                # 1. Elfogadás
                if offer_val >= st.session_state.current_bot_price:
                    savings = start_p - offer_val
                    # Biztonsági ellenőrzés a nullával osztás ellen
                    div = (start_p - st.session_state.target_p)
                    perf = (savings / div * 100) if div > 0 else 100
                    
                    resp = f"✅ Elfogadom! Üzlet megköttetett.\n\n📊 **ALKU JELENTÉS**\n- Megtakarítás: £{savings:.2f}\n- Hatékonyság: {min(int(perf), 100)}%"
                    st.balloons()
                
                # 2. Túl pofátlan ajánlat
                elif offer_val < st.session_state.target_p * 0.7:
                    resp = f"Ez komolytalan. {PERSONAS['SELLER'][bot_style]['quote']}"
                
                # 3. Ellenajánlat
                else:
                    flex = PERSONAS["SELLER"][bot_style]["flex"]
                    new_p = st.session_state.current_bot_price - (st.session_state.current_bot_price - offer_val) * flex
                    st.session_state.current_bot_price = max(new_p, st.session_state.target_p)
                    resp = f"Annyiért nem, de £{st.session_state.current_bot_price:.2f} és viheted."
                
                st.write(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
        except ValueError:
            st.error("Kérlek, csak számot írj be!")

with tab3:
    st.subheader("Statisztika")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
        if 'Ár' in df.columns:
            st.line_chart(df['Ár'])
    else:
        st.info("Még nincs adat.")
