import streamlit as st
import random

st.set_page_config(page_title="HagglerBot v5.3 | Negotiation Engine", page_icon="🎩")

# --- CONTEXT-AWARE RESPONSE ENGINE ---
def get_seller_response(persona, current_offer, prev_offer, target_price):
    # Dynamic logic for price improvement
    is_improving = prev_offer is not None and current_offer > prev_offer
    
    responses = {
        "⚖️ The Stoic": {
            "standard": f"Logic dictates £{target_price:.2f}. Your offer is merely a suggestion.",
            "improving": "I see we are starting to hit the ground running with reality. Still, we need to reach £{p}.",
            "insult": "Entropy increases, but my patience for lowballs does not."
        },
        "🎭 The Absurdist": {
            "standard": f"My pet lobster is unimpressed. He demands £{target_price:.2f}.",
            "improving": "It's taking shape, even if slowly—like a glacier with a bank account. Let's aim for £{p}.",
            "insult": "I would rather trade this for a single, very high-quality cloud."
        },
        "✨ Gen-Z Slay": {
            "standard": f"Main character energy requires a main character price. £{target_price:.2f}?",
            "improving": "Wait, this offer is actually starting to slay. We're getting on the right track! £{p}?",
            "insult": "This offer is giving 'delusional era'. Major L."
        }
    }
    
    char = responses[persona]
    if is_improving:
        return char["improving"].format(p=f"{target_price:.2f}")
    elif current_offer < (target_price * 0.7):
        return char["insult"]
    else:
        return char["standard"]

# --- UI ---
st.title("🎩 HagglerBot v5.3")

tab1, tab2 = st.tabs(["Selling Mode", "Buying Mode"])

with tab1:
    st.header("Counter-Offer Engine")
    col1, col2 = st.columns(2)
    with col1:
        listed_p = st.number_input("Listed Price (£):", value=50.0, key="s_listed")
        prev_o = st.number_input("Previous Offer (£) (Optional):", value=0.0, key="s_prev")
    with col2:
        current_o = st.number_input("Current Offer (£):", value=30.0, key="s_curr")
        s_persona = st.selectbox("Your Style:", ["⚖️ The Stoic", "🎭 The Absurdist", "✨ Gen-Z Slay"])

    # Seller Logic: Floor is Listed - 20%
    target = listed_p * 0.8
    if st.button("Generate Response", key="s_btn"):
        prev_val = prev_o if prev_o > 0 else None
        reply = get_seller_response(s_persona, current_o, prev_val, target)
        st.info(f"**Response:** {reply}")
        st.code(f"Look, {reply}", language=None)

with tab2:
    st.header("Strategic Buyer")
    colA, colB = st.columns(2)
    with colA:
        item_p = st.number_input("Item Price (£):", value=100.0, key="b_price")
        b_persona = st.selectbox("Buyer Persona:", ["🧐 The Reluctant Aristocrat", "📉 The Cold Analyst", "🔥 The Hype Beast"])
    with colB:
        category = st.selectbox("Category:", ["Luxury", "Tech", "Vintage", "Books"])

    if st.button("Generate Opening Bid"):
        # Buyer Logic: Bid starts at 70-80%
        bid_map = {"🧐 The Reluctant Aristocrat": 0.85, "📉 The Cold Analyst": 0.75, "🔥 The Hype Beast": 0.80}
        bid = item_p * bid_map[b_persona]
        
        quotes = {
            "🧐 The Reluctant Aristocrat": "In this economy, one must be prudent. Would you consider £{p} for this charming piece?",
            "📉 The Cold Analyst": "Market data suggests an overvaluation. My algorithmic offer is £{p}.",
            "🔥 The Hype Beast": "Love the fit, but the bank account is screaming. Can we do £{p} and call it a day?"
        }
        
        final_bid = round(bid) - 0.05
        res = quotes[b_persona].format(p=f"{final_bid:.2f}")
        st.success(f"**Your Move:** {res}")
        st.code(res, language=None)

st.divider()
st.caption("v5.3 | Context-Aware Negotiation | No 'bruv' zone.")
