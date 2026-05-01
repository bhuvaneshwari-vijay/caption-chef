import streamlit as st
from groq import Groq
from PIL import Image

# Page config
st.set_page_config(page_title="CaptionChef 🍳", page_icon="🍳", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .caption-card {
        background-color: #fff8f0;
        border-left: 4px solid #ff6b35;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .platform-title {
        font-size: 18px;
        font-weight: bold;
        color: #ff6b35;
        margin-bottom: 8px;
    }
    .stButton > button {
        background-color: #ff6b35;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5em 1.5em;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #e55a25;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🍳 CaptionChef")
st.subheader("AI-powered social media captions for your food business")
st.markdown("---")

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- FORM ---
st.markdown("### 🏪 Your Business")
business_name = st.text_input("Business Name", placeholder="e.g. Sweeta's Bake Studio")

st.markdown("### 🎂 Tell us about your product")
product_name = st.text_input("Product Name", placeholder="e.g. Chocolate Truffle Cake")
description = st.text_area("Describe it", placeholder="e.g. Rich dark chocolate cake with ganache frosting, perfect for birthdays")
price = st.text_input("Price (optional)", placeholder="e.g. ₹850")
offer = st.text_input("Any offer or occasion? (optional)", placeholder="e.g. 10% off this weekend / Diwali special")
tone = st.selectbox("Tone of caption", ["Warm & Friendly", "Fun & Playful", "Professional & Elegant", "Exciting & Urgent"])

st.markdown("### 📱 Choose platforms")
platforms = st.multiselect(
    "Select platforms to generate captions for",
    ["Instagram", "WhatsApp", "LinkedIn", "Facebook"],
    default=["Instagram", "WhatsApp"]
)

st.markdown("### 📸 Upload a photo (optional)")
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

            prompt = f"""
You are CaptionChef, an expert social media copywriter for small food businesses and home bakers in India.

Generate social media captions for the following:

Business Name: {business_name if business_name else "Not specified"}
Product: {product_name}
Description: {description}
Price: {price if price else "Not specified"}
Offer/Occasion: {offer if offer else "None"}
Tone: {tone}

Generate a separate caption for each of these platforms: {", ".join(platforms)}

Rules:
- Instagram: engaging, emojis, 3-5 relevant hashtags at the end, mention business name if provided
- WhatsApp: conversational, warm, short, no hashtags, mention business name if provided
- LinkedIn: professional, brand story angle, minimal emojis, mention business name if provided
- Facebook: friendly, community feel, 1-2 hashtags max, mention business name if provided
- Keep all captions under 150 words
- Make it feel local, relatable, and authentic for an Indian small business
- Do not add any intro text, just output the captions with platform name as heading

Format your response EXACTLY like this for each platform:
**Platform Name**
[caption text here]

"""

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )

                result = response.choices[0].message.content

                st.markdown("## ✨ Your Captions Are Ready!")
                st.markdown("*Click inside any box, select all (Ctrl+A) and copy!*")
                st.markdown("---")

                # Parse and display each platform caption in a styled card
                sections = result.split("**")
                sections = [s.strip() for s in sections if s.strip()]

                i = 0
                while i < len(sections) - 1:
                    platform = sections[i].strip().rstrip("*").
