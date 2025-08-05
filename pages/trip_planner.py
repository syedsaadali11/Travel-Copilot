import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Trip Planner | Travel Copilot",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .main {
        background: linear-gradient(135deg, #0f1b3a 0%, #1e3a8a 50%, #0d9dbb 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: white;
    }

    /* Back Button */
    .back-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #60DAFB;
        font-size: 14px;
        font-weight: 500;
        margin: 16px 0;
        text-decoration: none;
        transition: all 0.2s ease;
        padding: 8px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    .back-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(-2px);
    }

    /* Page Title */
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

    /* Input Box */
    .stTextArea > div > textarea {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        line-height: 1.5;
        height: 80px !important;
        resize: none;
    }

    .stTextArea > div > textarea::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }

    .stForm label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500;
        font-size: 14px;
    }

    /* Submit Button */
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

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 194, 214, 0.3);
    }

    /* Itinerary Card */
    .itinerary-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 16px;
        margin: 20px auto;
        max-width: 700px;
        color: white;
        font-size: 14px;
        line-height: 1.6;
    }

    .itinerary-card strong {
        color: #60DAFB;
    }

    .itinerary-card h3 {
        color: #60DAFB;
        font-size: 16px;
        margin: 10px 0;
    }

    /* Price & Budget Highlight */
    .budget-good {
        color: #4BB543;
        font-weight: 600;
    }

    .budget-over {
        color: #FF4444;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        padding: 20px 10px;
        margin-top: 40px;
        color: rgba(255,255,255,0.5);
        font-size: 12px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Back to Home
st.page_link("main.py", label="← Back to Home", icon="🏠", use_container_width=True)

# Page Title
st.markdown("<h1>🗺️ Trip Planner</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Get a complete travel plan with hotels, places, and budget insights.</p>", unsafe_allow_html=True)

# Query Form
with st.form("itinerary_query_form"):
    query = st.text_area(
        "Your Trip Request",
        value="Plan a trip to Paris next Friday with $1500",
        placeholder="Examples:\n• Plan a trip to Tokyo with $2000\n• I want to visit Dammam next week\n• Trip to Lahore with focus on food and sightseeing",
        height=80
    )
    submit = st.form_submit_button("Generate Itinerary")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a trip request.")
    else:
        with st.spinner("🗺️ Planning your trip..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if response:
            # ✅ Clean only once — no double processing
            formatted_response = response  
            st.markdown("<div class='itinerary-card'>", unsafe_allow_html=True)
            st.markdown(formatted_response, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='itinerary-card'>❌ No itinerary generated.</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • Your AI travel planner • <a href='#' style='color: #60DAFB;'>Learn more</a>
</div>
""", unsafe_allow_html=True)