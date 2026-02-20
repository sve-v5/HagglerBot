import streamlit as st
import random

st.set_page_config(page_title="HagglerBot v5.6 | UK Vinted", page_icon="🎩")

# --- SESSION STATE (Memory) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_reply' not in st.session_state:
    st.session_state.last_reply = ""

def reset_game():
    st.session_state.history = []
    st.session_state.last_reply = ""

# --- DATASETS ---
PERSONAS = {
    "SELLER": {
        "🛡️ The Wall": {"floor": 0.95, "desc": "Impenetrable. Minimal movement."},
        "⚖️ The Stoic": {"floor": 0.80, "desc": "Logical. Sarcastic. Firm."},
        "🤝 The Merchant": {"floor": 0.70, "desc": "Flexible. Win-win seeker."},
        "🎭 The Absurdist": {"floor": 0.85, "desc": "Surreal. British weirdness."},
        "✨ Gen-Z Slay": {"floor": 0.75, "desc": "Sassy. Trendy. Honest."}
    },
    "BUYER": {
        "🧐 The Aristocrat": {"bid": 0.85},
        "📉 The Analyst": {"bid": 0.75},
        "🔥 The Hype Beast": {"bid": 0.80},
        "🔨 The Lowballer": {"bid": 0.60},
        "🧘 The Zen Seeker": {"bid": 0.70}
    }
}

# --- APP UI ---
st.title("🎩 HagglerBot v5.6")
st.sidebar.button("🔄 Reset Negotiation", on_click=reset_game)

with st.sidebar:
    # Fix: Mapping the labels to the dictionary keys
    mode_label = st.radio("Role:", ["Seller", "Buyer"])
    mode_key = "SELLER" if mode_label == "Seller" else "BUYER"
    
    category = st.selectbox("Category:", ["Clothes", "Electronics", "Books", "Other"])
    persona_name = st.selectbox("Your Persona:", list(PERSONAS[mode_key].keys()))
    base_price = st.number_input("Original Price (£):", min_value=1.0, value=50.0)

# --- SELLER LOGIC (Multi-step) ---
if mode_key == "SELLER":
    st.subheader(f"Negotiating for: {category}")
    current_o = st.number_input("Enter Buyer's Current Offer (£):", min_value=1.0, key="offer_in")
    
    if st.button("Generate Response"):
        # Improvement check
        is_improving = len(st.session_state.history) > 0 and current_o > st.session_state.history[-1]
        st.session_state.history.append(current_o)
        
        # Zeno Method: target drifts toward the offer but stays above floor
        config = PERSONAS["SELLER"][persona_name]
        absolute_floor = base_price * config["floor"]
        
        # If improving, we meet them halfway between our floor and their offer
        target = max(absolute_floor, (absolute_floor + current_o) / 2)
        final_p = round(target) - 0.05
        
        # Dynamic Text
        if is_improving:
            feedback = random.choice([
                "We are getting on the right track.",
                "It's taking shape, even if slowly.",
                "I see we are starting to hit the ground running with reality."
            ])
        elif current_o < (base_price * 0.5):
            feedback = "Your offer is an insult to the concept of trade. Try harder."
        else:
            feedback = "A fascinating exercise in optimism. However, logic remains."

        # Persona Flavor
        quotes = {
            "⚖️ The Stoic": f"{feedback} For this {category}, £{final_p:.2f} is the only logical conclusion.",
            "🎭 The Absurdist": f"{feedback} My pet lobster is slightly less offended, but still demands £{final_p:.2f}.",
            "🛡️ The Wall": f"Quality dictates the price. £{final_p:.2f} is my final stand for this {category}.",
            "🤝 The Merchant": f"{feedback} We're close! Let's shake hands on £{final_p:.2f}?",
            "✨ Gen-Z Slay": f"{feedback} This {category} is too iconic for that. £{final_p:.2f} or it's a pass, bestie."
        }
        
        st.session_state.last_reply = quotes.get(persona_name, f"Let's settle on £{final_p:.2f}")
        
    if st.session_state.last_reply:
        st.divider()
        st.info(f"**{persona_name}:** {st.session_state.last_reply}")
        st.code(f"Look, {st.session_state.last_reply}", language=None)
        
        # Progress visual
        st.write("📈 **Haggling Progress:**")
        st.line_chart(st.session_state.history)

# --- BUYER LOGIC ---
else:
    st.subheader(f"Bidding for: {category}")
    if st.button("Generate Opening Bid"):
        bid_pct = PERSONAS["BUYER"][persona_name]["bid"]
        bid_val = (base_price * bid_pct) - 0.05
        
        buyer_quotes = {
            "🧐 The Aristocrat": f"In this economy, one must be prudent. Would you consider £{bid_val:.2f} for this {category}?",
            "📉 The Analyst": f"Data suggests this {category} is worth £{bid_val:.2f}. My offer is firm.",
            "🔨 The Lowballer": f"I've seen similar {category} for pennies. £{bid_val:.2f} is my final offer.",
            "🔥 The Hype Beast": f"Love the drip. My budget for this {category} is £{bid_val:.2f}. You down?",
            "🧘 The Zen Seeker": f"Inner peace requires a clean transaction. £{bid_val:.2f} feels right."
        }
        
        res = buyer_quotes.get(persona_name, f"How about £{bid_val:.2f}?")
        st.success(f"**Your Move:** {res}")
        st.code(res, language=None)
