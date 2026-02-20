import streamlit as st
import pandas as pd
import random

# --- 1. KONFIGURÁCIÓ & STÍLUS ---
st.set_page_config(page_title="HagglerBot Pro v5.1", layout="centered", page_icon="🤝")

# Custom CSS a jobb megjelenésért
st.markdown("""
    <style>
    .stMetric { background-color: rgba(240, 242, 246, 0.5); padding: 15px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

PERSONAS = {
    "SELLER": {
        "🛡️ The Wall": {"floor": 0.92, "round": "UP", "quote": "Nem zsibvásár, az ár fix. 🧱"},
        "⚖️ The Stoic": {"floor": 0.80, "round": "MID", "quote": "A matek nem hazudik. ⏳"},
        "🤝 The Merchant": {"floor": 0.70, "round": "DOWN", "quote": "Találjuk meg a közös utat! ✨"},
        "✨ Gen-Z Slay": {"floor": 0.75, "round": "TREND", "quote": "Ez az ajánlat nem slay, tesó. 💅"}
    },
    "BUYER": {
        "🔨 The Lowballer": {"bid": 0.60, "round": "DOWN", "quote": "Ennyim van rá, vagy hagyjuk. 📉"},
        "📊 Value Hunter": {"bid": 0.75, "round": "MID", "quote": "Piaci ár alatt keresek. 🧐"},
        "✨ Fair Player": {"bid": 0.85, "round": "UP", "quote": "Gyorsan fizetnék, ha engedsz kicsit. 🤝"},
        "🔥 Hype Beast": {"bid": 0.70, "round": "TREND", "quote": "Nagyon élem a fitet, de szűkös a budget. 🔥"}
    }
}

# --- 2. LOGIKA FINOMÍTÁSA ---
def zeno_round(price, mode, round_type):
    base = int(price)
    if mode == "SELLER":
        if round_type == "UP": return float(base) + 0.95
        if round_type == "TREND": return float(base) + 0.00 # Kerek számok "tisztábbak"
        return float(base) + 0.50
    else: # BUYER
        if round_type == "DOWN": return float(base) # Alacsony, kerek ajánlat
        if round_type == "MID": return float(base) + 0.45
        return float(base) + 0.95

# Session State inicializálás az analitikához
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. UI LAYOUT ---
mode_toggle = st.sidebar.radio("Üzemmód Kiválasztása:", ["💰 Eladó vagyok", "🛒 Vevő vagyok"])
current_mode = "SELLER" if "Eladó" in mode_toggle else "BUYER"

tab1, tab2, tab3 = st.tabs(["🎮 Dashboard", "📈 Analitika", "📖 Segédlet"])

with tab1:
    st.title(f"{'🛡️' if current_mode == 'SELLER' else '🛒'} HagglerBot v5.1")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        persona = st.selectbox("Karakterstílus:", list(PERSONAS[current_mode].keys()))
    with col2:
        label = "Eredeti eladási ár (£):" if current_mode == "SELLER" else "Kikiáltási ár (£):"
        price_input = st.number_input(label, value=20.0, step=1.0)

    if st.button(f"🚀 {'Ellenajánlat' if current_mode == 'SELLER' else 'Első ajánlat'} számítása"):
        config = PERSONAS[current_mode][persona]
        
        # Logika: Eladónál a floor alá nem megyünk, vevőnél a bid-ről indulunk
        factor = config['floor'] if current_mode == "SELLER" else config['bid']
        raw_price = price_input * factor
        final_price = zeno_round(raw_price, current_mode, config['round'])
        
        # Eredmény megjelenítése
        st.divider()
        diff_pct = int((final_price / price_input - 1) * 100)
        
        c1, c2 = st.columns(2)
        c1.metric("Javasolt ár", f"£{final_price:.2f}", f"{diff_pct}%")
        c2.info(f"**Stílus:** {persona}\n\n*\"{config['quote']}\"*")
        
        # Copy-paste kész szöveg
        copy_text = f"Legyen £{final_price:.2f}, {config['quote']}"
        st.text_area("Másolható üzenet:", value=copy_text, height=70)
        
        # Mentés az analitikához
        st.session_state.history.append({
            "Idő": pd.Timestamp.now().strftime("%H:%M:%S"),
            "Mód": current_mode,
            "Ár": final_price,
            "Eredeti": price_input
        })

with tab2:
    st.subheader("Munkamenet statisztika")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        
        # Kis vizualizáció az árak alakulásáról
        st.line_chart(df['Ár'])
        
        if st.button("Analitika törlése"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("Még nincs mentett kalkuláció.")

with tab3:
    st.markdown("""
    ### 💡 Tippek a profi alkudozáshoz
    - **Pszichológiai árazás:** A `.95` végződés professzionális eladót sugall, a `.00` pedig határozottságot.
    - **A Lowballer stratégia:** Mindig 60%-ról indulj, de számíts rá, hogy 75-80%-nál fogtok találkozni.
    - **Vinted algoritmus:** A gyors válaszidő és a konkrét ajánlat gomb használata növeli az eladási esélyeket.
    """)

# --- LÁBLÉC ---
st.sidebar.divider()
st.sidebar.caption(f"Verzió: 5.1 | Mode: {current_mode}")
