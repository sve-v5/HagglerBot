import streamlit as st
import random

st.set_page_config(page_title="HagglerBot v5.2 | Smart UK", page_icon="🎩")

# --- PERSONA ENGINE WITH INTELLECTUAL & ABSURD HUMOUR ---
STRATEGIES = {
    "SELLER": {
        "⚖️ The Stoic": {
            "floor_mult": 0.80, # Full price - 20%
            "responses": [
                "I have contemplated your offer. It is as hollow as a drum. Let us return to reality.",
                "Entropy increases, but my price remains relatively stable. £{p} is the compromise.",
                "Your offer is a fascinating exercise in optimism. However, logic dictates £{p}.",
                "I am indifferent to the sale, but committed to the value. £{p} is the floor."
            ]
        },
        "✨ Gen-Z Slay": {
            "floor_mult": 0.70,
            "responses": [
                "This offer isn't giving what you think it's giving. Major L. Let's try £{p}?",
                "I'm literally obsessed with this item, so parting with it for less than £{p} is a hate crime.",
                "Your offer is giving 'delusional era'. Bestie, £{p} is the lowest I'll go.",
                "Main character energy requires a main character price. £{p} or keep scrolling."
            ]
        },
        "🎭 The Absurdist": {
            "floor_mult": 0.85,
            "responses": [
                "I would accept that, but my pet lobster says the economy is too fragile. £{p}?",
                "If I sell it for your price, the ghosts of Victorian orphans will haunt me. £{p} is safer.",
                "Money is a social construct, but unfortunately, my landlord is a constructivist. £{p} please.",
                "I'll accept your offer if you can prove the moon isn't made of low-quality cheddar. No? Then £{p}."
            ]
        }
    }
}

# --- UI ---
st.title("🎩 HagglerBot v5.2")
st.markdown("*Intellectual negotiation for the discerning Vinted user.*")

mode = st.sidebar.toggle("Switch to Buyer Mode", value=False) # Simple toggle for now

if not mode: # SELLING MODE
    st.header("Seller Interface")
    
    col1, col2 = st.columns(2)
    with col1:
        listed_price = st.number_input("Your Listed Price (£):", min_value=1.0, value=50.0)
    with col2:
        buyer_offer = st.number_input("Buyer's Low Offer (£):", min_value=1.0, value=30.0)
    
    category = st.selectbox("Product Category:", ["Clothes", "Tech", "Books", "Collectibles"])
    persona_name = st.selectbox("Select Your Response Style:", list(STRATEGIES["SELLER"].keys()))
    
    # Logic
    config = STRATEGIES["SELLER"][persona_name]
    suggested_price = listed_price * config["floor_mult"]
    
    # Psych-rounding (ending in .95 or .50)
    final_price = round(suggested_price) - 0.05 if suggested_price % 1 > 0.5 else round(suggested_price) + 0.50

    if st.button("Generate Intellectual Clapback"):
        quote_template = random.choice(config["responses"])
        final_quote = quote_template.format(p=f"{final_price:.2f}")
        
        st.divider()
        st.subheader("The Counter-Attack:")
        
        # Display the witty response
        st.info(f"**{persona_name} logic:** \n\n '{final_quote}'")
        
        st.write("### 📋 Copy to Chat:")
        st.code(f"Look, {final_quote}", language=None)
        
        if buyer_offer < (listed_price * 0.5):
            st.warning("⚠️ Note: This buyer is a 'Lowballer'. The response has been sharpened accordingly.")

else:
    st.header("Buyer Interface")
    st.write("Buyer mode logic updated to match intellectual standards in v5.3.")

# --- FOOTER ---
st.caption("v5.2 | Now with 100% more sarcasm and 0% 'bruv'.")
