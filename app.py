import streamlit as st
import random

# Alapbeállítások
st.set_page_config(page_title="HagglerBot v5.7 | UK Vinted", page_icon="🎩")

# --- MEMÓRIA KEZELÉSE (Session State) ---
# Ez tárolja az alku történetét, hogy ne kelljen "Previous offer" mező
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_reply' not in st.session_state:
    st.session_state.last_reply = ""

def reset_negotiation():
    st.session_state.history = []
    st.session_state.last_reply = ""

# --- ADATBÁZIS (Personas & Logic) ---
PERSONAS = {
    "Seller": {
        "🛡️ The Wall": {"floor": 0.90, "quote": "Quality is worth the value. Price is firm for this {cat}."},
        "⚖️ The Stoic": {"floor": 0.80, "quote": "Logic dictates the value of this {cat}. £{p} is the floor."},
        "🤝 The Merchant": {"floor": 0.70, "quote": "Let's find a middle ground for this {cat}. How about £{p}?"},
        "🎭 The Absurdist": {"floor": 0.85, "quote": "My pet lobster says this {cat} is worth at least £{p}."},
        "✨ Gen-Z Slay": {"floor": 0.75, "quote": "This {cat} is literally main character energy. £{p} or skip, bestie."}
    },
    "Buyer": {
        "🧐 The Aristocrat": {"bid": 0.85},
        "📉 The Analyst": {"bid": 0.75},
        "🔨 The Lowballer": {"bid": 0.60},
        "🔥 The Hype Beast": {"bid": 0.80},
        "🧘 The Zen Seeker": {"bid": 0.70}
    }
}

# --- OLDALSÁV (Sidebar) ---
with st.sidebar:
    st.header("Settings")
    mode = st.radio("Are you Buying or Selling?", ["Selling", "Buying"])
    category = st.selectbox("Category:", ["Clothes", "Electronics", "Books", "Other"])
    
    # Karakter választó a mód alapján
    current_persona_list = list(PERSONAS["Seller"].keys()) if mode == "Selling" else list(PERSONAS["Buyer"].keys())
    persona = st.selectbox("Your Style:", current_persona_list)
    
    original_price = st.number_input("Original Price (£):", min_value=1.0, value=50.0)
    
    if st.button("🔄 Reset Negotiation"):
        reset_negotiation()

# --- FŐ INTERFÉSZ (Main UI) ---
st.title(f"🎩 HagglerBot - {mode} Mode")

if mode == "Selling":
    st.subheader(f"Negotiating your {category}")
    buyer_offer = st.number_input("Enter Buyer's Offer (£):", min_value=1.0, key="offer_input")
    
    if st.button("Generate Counter-Offer"):
        # Ellenőrizzük, hogy javult-e az ajánlat az előzőhöz képest
        is_improving = False
        if st.session_state.history and buyer_offer > st.session_state.history[-1]:
            is_improving = True
        
        # Elmentjük az aktuális ajánlatot a történetbe
        st.session_state.history.append(buyer_offer)
        
        # LOGIKA: Zeno-módszer (az eladó enged kicsit, ha a vevő javít)
        config = PERSONAS["Seller"][persona]
        absolute_floor = original_price * config["floor"]
        
        # Ha javul az ajánlat, az eladó is közelít (átlagolás), de nem megy a floor alá
        if is_improving:
            target_price = max(absolute_floor, (absolute_floor + buyer_offer) / 2)
            feedback = random.choice([
                "We are getting on the right track.",
                "It's taking shape, even if slowly.",
                "I see we are starting to hit the ground running with reality."
            ])
        else:
            target_price = absolute_floor
            feedback = random.choice([
                "Your offer is a fascinating exercise in optimism.",
                "Entropy increases, but my patience does not.",
                "Logic dictates we stay closer to the value."
            ])
            
        final_p = round(target_price) - 0.05
        base_quote = config["quote"].format(cat=category.lower(), p=f"{final_p:.2f}")
        
        st.session_state.last_reply = f"{feedback} {base_quote}"

    # Válasz megjelenítése
    if st.session_state.last_reply:
        st.divider()
        st.info(f"**{persona} says:**\n\n{st.session_state.last_reply}")
        st.code(f"Look, {st.session_state.last_reply}", language=None)
        
        # Grafikon az alku menetéről
        st.write("📈 **Price Trend:**")
        st.line_chart(st.session_state.history)

else: # BUYING MODE
    st.subheader(f"Bidding for {category}")
    if st.button("Generate Opening Bid"):
        config = PERSONAS["Buyer"][persona]
        bid_value = (original_price * config["bid"]) - 0.05
        
        st.success(f"**Suggested Offer:** £{bid_value:.2f}")
        st.code(f"Hi! Would you consider £{bid_value:.2f} for this {category.lower()}? I can pay immediately.", language=None)

st.caption("v5.7 | Progressive Negotiation Logic | UK Market")
