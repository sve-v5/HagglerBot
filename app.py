import streamlit as st
import random

st.set_page_config(page_title="HagglerBot v5.8 | Deal Maker", page_icon="🤝")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'deal_closed' not in st.session_state:
    st.session_state.deal_closed = False

def reset_bot():
    st.session_state.history = []
    st.session_state.deal_closed = False

# --- PERSONA ENGINE ---
PERSONAS = {
    "Seller": {
        "🛡️ The Wall": {"floor": 0.95, "style": "Unyielding"},
        "⚖️ The Stoic": {"floor": 0.80, "style": "Logical"},
        "🤝 The Merchant": {"floor": 0.70, "style": "Flexible"},
        "🎭 The Absurdist": {"floor": 0.85, "style": "Surreal"},
        "✨ Gen-Z Slay": {"floor": 0.75, "style": "Trendy"}
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("Vinted UK Settings")
    mode = st.radio("Mode:", ["Selling", "Buying"])
    category = st.selectbox("Category:", ["Clothes", "Electronics", "Books", "Other"])
    persona = st.selectbox("Style:", list(PERSONAS["Seller"].keys()))
    list_price = st.number_input("Listed Price (£):", min_value=1.0, value=50.0)
    st.button("🔄 New Negotiation", on_click=reset_bot)

# --- MAIN ---
st.title(f"🤝 HagglerBot - {category}")

if mode == "Selling":
    buyer_offer = st.number_input("Buyer's Offer (£):", min_value=1.0, step=1.0)
    
    if st.button("Respond to Offer") and not st.session_state.deal_closed:
        config = PERSONAS["Seller"][persona]
        absolute_floor = list_price * config["floor"]
        
        # 1. CHECK FOR DEAL
        if buyer_offer >= absolute_floor:
            st.session_state.deal_closed = True
            res = f"Acceptable. We have a deal at £{buyer_offer:.2f}! Send the offer on Vinted, and I'll ship your {category.lower()} ASAP. ✅"
            st.balloons()
        
        # 2. GENERATE COUNTER-OFFER (Haggle)
        else:
            is_improving = len(st.session_state.history) > 0 and buyer_offer > st.session_state.history[-1]
            st.session_state.history.append(buyer_offer)
            
            # Zeno Method: meeting halfway
            target = max(absolute_floor, (list_price + buyer_offer) / 2)
            if persona == "🛡️ The Wall": target = max(absolute_floor, list_price * 0.98) # Wall barely moves
            
            final_p = round(target) - 0.05
            
            # Witty Responses
            if is_improving:
                msg = f"We are getting on the right track with this {category.lower()}."
            else:
                msg = f"Your offer for this {category.lower()} is an exercise in optimism."
            
            quotes = {
                "🛡️ The Wall": f"I'm firm on quality. My best is £{final_p:.2f}.",
                "⚖️ The Stoic": f"{msg} Logic dictates £{final_p:.2f}.",
                "🎭 The Absurdist": f"My pet lobster is offended. He demands £{final_p:.2f}.",
                "🤝 The Merchant": f"I appreciate the bump! Can we meet at £{final_p:.2f}?",
                "✨ Gen-Z Slay": f"This {category.lower()} is too iconic for that. Best I can do is £{final_p:.2f}."
            }
            res = quotes[persona]

        st.session_state.last_res = res

    if 'last_res' in st.session_state:
        st.divider()
        st.info(f"**{persona}:** {st.session_state.last_res}")
        st.code(f"Look, {st.session_state.last_res}", language=None)
        
        if st.session_state.history:
            st.write("📈 **Haggling Progress:**")
            st.line_chart(st.session_state.history)

else:
    st.write("Buyer mode under construction for v5.9 - Focus on Seller Deal-Making now.")
