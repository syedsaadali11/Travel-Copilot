import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Weather | Travel Copilot",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS – Sleek, compact, modern
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
        color: rgba(255, 255, 255, 0.8);
        font-size: 15px;
        text-align: center;
        margin-bottom: 24px;
    }

    /* Input Box – Compact */
    .stTextArea > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        line-height: 1.5;
        height: 80px !important;  /* Smaller height */
        resize: none;              /* Disable resize */
    }

    .stTextArea > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        font-size: 15px !important;
    }

    .stForm label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500;
        font-size: 14px;
    }

    /* Submit Button – Compact */
    .stButton>button {
        background: linear-gradient(90deg, #0d9dbb, #00c2d6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        width: 160px;
        margin: 16px auto;
        display: block;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 194, 214, 0.3);
    }

    /* Compact Weather Card */
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 20px auto;
        max-width: 500px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        color: white;
        text-align: center;
        font-size: 14px;
        line-height: 1.5;
    }

    .weather-card h3 {
        color: #60DAFB;
        font-size: 18px;
        margin: 0 0 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
    }

    .weather-temp {
        font-size: 32px;
        font-weight: 700;
        color: #60DAFB;
        margin: 8px 0;
    }

    .weather-condition {
        font-size: 16px;
        color: #60DAFB;
        margin-bottom: 12px;
    }

    .weather-details {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 12px 0;
        font-size: 13px;
    }

    .detail-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 6px 10px;
        min-width: 80px;
    }

    .detail-box strong {
        color: #60DAFB;
    }

    .weather-summary p {
        margin: 10px 0 0;
        font-size: 13px;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.5;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 20px 10px;
        margin-top: 40px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Back to Home
st.markdown('<a href="/" class="back-btn">← Back</a>', unsafe_allow_html=True)

# Page Title
st.markdown("<h1>🌤️ Ask About the Weather</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Just type your question — we’ll find the forecast.</p>", unsafe_allow_html=True)

# Compact Query Form
with st.form("weather_query_form"):
    query = st.text_area(
        "Your Question",
        value="What's the weather in Paris today?",
        placeholder="e.g., Will it rain in Tokyo tomorrow?",
        height=80
    )
    submit = st.form_submit_button("Get Forecast")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a question.")
    else:
        with st.spinner("🌤️ Fetching forecast..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if not response:
            st.markdown("<div style='text-align:center; color: #ff7675; font-size:14px;'>❌ No response. Try again.</div>", unsafe_allow_html=True)
        else:
            # Clean response
            cleaned = re.sub(r'^🌤️\s*', '', response).strip()

            # Extract key data
            location = "Unknown"
            temp = "N/A"
            condition = "Weather"
            precipitation = "N/A"

            loc_match = re.search(r"in\s+([A-Za-z\s]+?)(?:\s+on|$)", cleaned)
            if loc_match:
                location = loc_match.group(1).strip()

            temp_match = re.search(r"(\d+(?:\.\d+)?–\d+(?:\.\d+)?)°C", cleaned)
            if temp_match:
                temp = temp_match.group(1) + "°C"

            condition_match = re.search(r":\s*([^,]+),", cleaned)
            if condition_match:
                condition = condition_match.group(1).strip()

            precip_match = re.search(r"Precipitation:\s*([\d.]+ mm)", cleaned)
            if precip_match:
                precipitation = precip_match.group(1)

            # Build compact result
            result_html = f"""
            <div class="weather-card">
                <h3>📍 {location}</h3>
                <div class="weather-temp">{temp}</div>
                <div class="weather-condition">{condition}</div>
                <div class="weather-details">
                    <div class="detail-box"><strong>Rain</strong><br>{precipitation}</div>
                </div>
                <div class="weather-summary">
                    <p>{cleaned}</p>
                </div>
            </div>
            """
            st.markdown(result_html, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • <a href="#" style="color: #60DAFB;">How it works</a>
</div>
""", unsafe_allow_html=True)