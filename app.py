import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page config
st.set_page_config(page_title="CaptionChef 🍳", page_icon="🍳", layout="centered")

# Header
st.title("🍳 CaptionChef")
st.subheader("AI-powered social media captions for your food business")
st.markdown("---")

# API Key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- FORM ---
st.markdown("### Tell us about your product")

product_name = st.text_input("Product Name", placeholder="e.g. Chocolate Truffle Cake")
description = st.text_area("Describe it", placeholder="e.g. Rich dark chocolate cake with ganache frosting, perfect for birthdays")
price = st.text_input("Price (optional)", placeholder="e.g. ₹850")
offer = st.text_input("Any offer or occasion? (optional)", placeholder="e.g. 10% off this weekend / Diwali special")
tone = st.selectbox("Tone of caption", ["Warm & Friendly", "Fun & Playful", "Professional & Elegant", "Exciting & Urgent"])

st.markdown("### Choose platforms")
platforms = st.multiselect(
    "Select platforms to generate captions for",
    ["Instagram", "WhatsApp", "LinkedIn", "Facebook"],
    default=["Instagram", "WhatsApp"]
)

st.markdown("### Upload a photo (optional)")
photo = st.file_uploader("Upload your food photo", type=["jpg", "jpeg", "png"])

if photo:
    st.image(photo, caption="Your uploaded photo", use_column_width=True)

st.markdown("---")

# --- GENERATE ---
if st.button("🍳 Generate Captions"):
    if not product_name or not description:
        st.warning("Please enter at least the product name and description.")
    elif not platforms:
        st.warning("Please select at least one platform.")
    else:
        with st.spinner("CaptionChef is cooking... 🍳"):

            # Build prompt
            prompt = f"""
You are CaptionChef, an expert social media copywriter for small food businesses and home bakers in India.

Generate social media captions for the following product:

Product: {product_name}
Description: {description}
Price: {price if price else "Not specified"}
Offer/Occasion: {offer if offer else "None"}
Tone: {tone}

Generate a separate caption for each of these platforms: {", ".join(platforms)}

Rules:
- Instagram: engaging, emojis, 3-5 relevant hashtags at the end
- WhatsApp: conversational, warm, short, no hashtags
- LinkedIn: professional, brand story angle, minimal emojis
- Facebook: friendly, community feel, 1-2 hashtags max
- Keep all captions under 150 words
- Make it feel local, relatable, and authentic for an Indian small business
- Do not add any intro text, just output the captions with platform name as heading

Format:
**Platform Name**
[caption here]
"""

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                if photo:
                    image = Image.open(photo)
                    response = model.generate_content([prompt, image])
                else:
                    response = model.generate_content(prompt)

                st.markdown("## ✨ Your Captions Are Ready!")
                st.markdown(response.text)

                # Copy hint
                st.info("💡 Tip: Click on any caption, select all and copy to use it directly!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
