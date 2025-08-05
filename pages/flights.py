import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Flight Search | Travel Copilot",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS – Sleek & compact
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .main {
        background: linear-gradient(135deg, #0f1b3a 0%, #1e3a8a 50%, #0d9dbb 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: white;
    }

    h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 24px;
        text-align: center;
        margin-bottom: 12px;
    }

    p.subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 15px;
        text-align: center;
        margin-bottom: 24px;
    }

    .stTextArea > div > textarea {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        height: 80px !important;
        resize: none;
    }

    .stButton>button {
        background: linear-gradient(90deg, #0d9dbb, #00c2d6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        width: 160px;
        margin: 16px auto;
        display: block;
    }

    .result-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 16px;
        margin: 20px auto;
        max-width: 600px;
        color: white;
        font-size: 14px;
        line-height: 1.6;
    }

    .result-card strong {
        color: #60DAFB;
    }
</style>
""", unsafe_allow_html=True)

# Back to Home
st.markdown('<a href="/" class="back-btn">← Back</a>', unsafe_allow_html=True)

# Page Title
st.markdown("<h1>✈️ Find Your Flight</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Just type your request — we’ll find the best flights.</p>", unsafe_allow_html=True)

# Query Form
with st.form("flight_query_form"):
    query = st.text_area(
        "Your Flight Request",
        value="Find a flight from Paris to Tokyo next Friday",
        placeholder="Examples:\n• Book a flight from Rome to Athens tomorrow\n• Flights from Sydney to Singapore on 2025-09-10",
        height=80
    )
    submit = st.form_submit_button("Search Flights")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a flight request.")
    else:
        with st.spinner("🛫 Searching for flights..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if response:
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown(f"**Query:** {query.strip()}")
            # ✅ Fixed: Use \n\n for line breaks, no HTML, no replace()
            st.markdown(f"**Result:**\n\n{response}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-card'>❌ No response from flight engine.</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • Real-time data • <a href='#' style='color: #60DAFB;'>How we source data</a>
</div>
""", unsafe_allow_html=True)