import streamlit as st
import random

st.set_page_config(page_title="HagglerBot v5.5 | Professional UK", page_icon="🎩")

# --- INITIALIZE MEMORY (The 'Brain' of the Bot) ---
if 'history' not in st.session_state:
    st.session_state.history = []

def reset_haggling():
    st.session_state.history = []

# --- PERSONA DATASETS ---
PERSONAS = {
    "SELLER": {
        "🛡️ The Wall": {"floor": 0.90, "style": "Unyielding. Firm. Professional.", "round": "UP"},
        "⚖️ The Stoic": {"floor": 0.80, "style": "Logical. Sarcastic. Detached.", "round": "MID"},
        "🤝 The Merchant": {"floor": 0.70, "style": "Friendly. Flexible. Fair.", "round": "DOWN"},
        "🎭 The Absurdist": {"floor": 0.85, "style": "Surreal. Bizarre. Philosophical.", "round": "MID"},
        "✨ Gen-Z Slay": {"floor": 0.75, "style": "Sassy. Trendy. Honest.", "round": "TREND"}
    },
    "BUYER": {
        "🧐 The Aristocrat": {"bid": 0.85, "style": "Polite. Prudent. High-end."},
        "📉 The Analyst": {"bid": 0.75, "style": "Data-driven. Cold. Precise."},
        "🔥 The Hype Beast": {"bid": 0.80, "style": "Direct. Cool. Budget-conscious."},
        "🔨 The Lowballer": {"bid": 0.60, "style": "Aggressive. Audacious. Persistent."},
        "🧘 The Zen Seeker": {"bid": 0.70, "style": "Patient. Minimalist. Calm."}
    }
}

# --- TEXT ENGINE ---
def generate_response(mode, persona, current_price, is_improvement, category):
    # Context-based phrases
    if is_improvement:
        feedback = ["It's taking shape, even if slowly.", "We're getting on the right track.", "I see we're starting to hit the ground running with reality."]
    else:
        feedback = ["Your offer is a fascinating exercise in optimism.", "My patience is a finite resource.", "Entropy increases, your offer does not."]

    # Persona-specific flavor
    quotes = {
        "⚖️ The Stoic": f"{random.choice(feedback)} Logic dictates £{current_price:.2f} for this {category}.",
        "🎭 The Absurdist": f"My pet lobster says that {category} is worth at least £{current_price:.2f}. Don't upset him.",
        "🛡️ The Wall": f"Quality is worth the value. £{current_price:.2f} is the rock bottom for this {category}.",
        "🤝 The Merchant": f"I appreciate the offer! How about we meet at £{current_price:.2f}?",
        "✨ Gen-Z Slay": f"This {category} is literally main character energy. £{current_price:.2f} or it's a pass, bestie."
    }
    return quotes.get(persona, f"Let's aim for £{current_price:.2f}.")

# --- UI ---
st.title("🎩 HagglerBot v5.5")
st.sidebar.button("🔄 Reset Negotiation", on_click=reset_haggling)

with st.sidebar:
    mode = st.radio("Choose Role:", ["Selling", "Buying"])
    category = st.selectbox("Category:", ["Clothes", "Electronics", "Books", "Other"])
    persona_type = st.selectbox("Your Persona:", list(PERSONAS[mode.upper()].keys()))
    base_price = st.number_input("Original Price (£):", min_value=1.0, value=50.0)

# --- NEGOTIATION LOGIC ---
st.subheader(f"{mode} Dashboard: {category}")

if mode == "Selling":
    current_offer = st.number_input("Enter Buyer's Offer (£):", min_value=1.0, key="offer_input")
    
    if st.button("Analyze & Respond"):
        # Check for improvement
        is_imp = False
        if st.session_state.history and current_offer > st.session_state.history[-1]:
            is_imp = True
        
        st.session_state.history.append(current_offer)
        
        # Zeno/Floor Logic
        target_price = base_price * PERSONAS["SELLER"][persona_type]["floor"]
        
        # Adjust target based on Zeno-style approach
        if is_imp:
            target_price = (target_price + current_offer) / 2 # Closing the gap
        
        reply = generate_response("SELLER", persona_type, target_price, is_imp, category)
        
        st.divider()
        st.info(f"**{persona_type} Response:**\n\n{reply}")
        st.code(f"Look, {reply}", language=None)

else: # BUYING MODE
    if st.button("Generate Opening Offer"):
        config = PERSONAS["BUYER"][persona_type]
        bid_price = base_price * config["bid"]
        
        # Unique Buyer Quotes
        buyer_quotes = {
            "🧐 The Aristocrat": f"In this economy, one must be prudent. Would you consider £{bid_price:.2f} for this {category}?",
            "📉 The Analyst": f"Market data for {category} suggests £{bid_price:.2f} is the optimal value.",
            "🔨 The Lowballer": f"I've seen this {category} cheaper elsewhere. £{bid_price:.2f}, take it or leave it."
        }
        
        res = buyer_quotes.get(persona_type, f"How about £{bid_price:.2f} for the {category}?")
        st.success(f"**Suggested Message:**\n\n{res}")
        st.code(res, language=None)

# --- HISTORY VISUAL ---
if st.session_state.history:
    st.write("---")
    st.write("📈 **Negotiation Trend:**")
    st.line_chart(st.session_state.history)
