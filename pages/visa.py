import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Visa Requirements | Travel Copilot",
    page_icon="🛂",
    layout="wide"
)

# Custom CSS – Sleek, compact, modern (aligned with weather/hotels)
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

    /* Visa Card */
    .visa-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 16px;
        margin: 20px auto;
        max-width: 600px;
        color: white;
        font-size: 14px;
        line-height: 1.6;
    }

    .visa-card h3 {
        color: #60DAFB;
        font-size: 18px;
        margin: 0 0 12px;
        text-align: center;
    }

    .visa-card ul {
        list-style: none;
        padding: 0;
        margin: 10px 0;
    }

    .visa-card li {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 6px 0;
        font-size: 14px;
    }

    .visa-card .highlight {
        color: #60DAFB;
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
st.markdown("<h1>🛂 Visa Requirements</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Just type your question — we’ll check entry rules and visa needs.</p>", unsafe_allow_html=True)

# Query Form
with st.form("visa_query_form"):
    query = st.text_area(
        "Your Visa Question",
        value="Do I need a visa for India if I'm from the USA?",
        placeholder="Examples:\n• Visa requirements for Canadian citizens in Japan\n• Do Australians need a visa for Turkey?\n• Entry rules for Germany from Brazil",
        height=80
    )
    submit = st.form_submit_button("Check Requirements")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a question.")
    else:
        with st.spinner("🛂 Checking entry requirements..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if response:
            cleaned = re.sub(r'^🛂\s*', '', response).strip()

            # Parse bullet points
            lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
            points = []
            for line in lines:
                if line.startswith("- ") or line.startswith("•") or "**" in line:
                    clean_line = line.strip("-• ")
                    clean_line = clean_line.replace("**", "").replace("##", "").strip()
                    points.append(clean_line)

            # Build result
            st.markdown("<div class='visa-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3>🛂 Visa Info</h3>", unsafe_allow_html=True)

            if points:
                st.markdown("<ul>", unsafe_allow_html=True)
                for point in points:
                    st.markdown(f"<li>{point}</li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p>{cleaned}</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='visa-card'>❌ No visa information found.</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • Always verify with official embassies • <a href='#' style='color: #60DAFB;'>Report outdated info</a>
</div>
""", unsafe_allow_html=True)