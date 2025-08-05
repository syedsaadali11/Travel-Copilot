import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Hotel Search | Travel Copilot",
    page_icon="🏨",
    layout="wide"
)

# Custom CSS – Sleek, modern, compact
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

    /* Result Card */
    .hotel-card {
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

    .hotel-card h3 {
        color: #60DAFB;
        font-size: 18px;
        margin: 0 0 12px;
        text-align: center;
    }

    .hotel-list {
        text-align: left;
        margin: 10px 0;
    }

    .hotel-list ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .hotel-list li {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px 12px;
        margin: 6px 0;
        font-size: 14px;
        line-height: 1.5;
    }

    .hotel-name {
        font-weight: 600;
        color: white;
        display: block;
    }

    .hotel-details {
        color: rgba(255,255,255,0.8);
        margin: 4px 0;
        font-size: 13px;
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
st.markdown("<h1>🏨 Find Your Perfect Stay</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Just type where and when — we’ll find the best hotels.</p>", unsafe_allow_html=True)

# Query Form
with st.form("hotel_query_form"):
    query = st.text_area(
        "Your Hotel Request",
        value="Find hotels in Lahore next Friday",
        placeholder="Examples:\n• Hotels in Tokyo for tomorrow\n• Where can I stay in Rome?\n• Best hotel in Islamabad on 2025-08-10",
        height=80
    )
    submit = st.form_submit_button("Search Hotels")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a request.")
    else:
        with st.spinner("🏨 Searching for the best stays..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if response:
            # Clean response
            cleaned = response.replace("<br>", "\n").replace("<b>", "").replace("</b>", "")

            # Split into lines
            lines = [line.strip() for line in cleaned.split("\n") if line.strip()]

            st.markdown("<div class='hotel-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3>🏨 Hotels Found</h3>", unsafe_allow_html=True)

            hotel_items = []
            in_hotel_section = False

            for line in lines:
                # Detect hotel section
                if "🏨" in line and ("Top hotels" in line or "Hotels in" in line):
                    in_hotel_section = True
                    continue
                if not in_hotel_section:
                    continue
                if line.startswith("- "):
                    content = line[2:].strip()
                    if "\n" in content:
                        parts = content.split("\n", 1)
                        name = parts[0].strip()
                        details = parts[1].strip()
                    else:
                        name = content
                        details = "📍 Location details available"
                    # Skip low-quality entries
                    bad_names = ["unknown hotel", "sunset", "regal internet inn", "king edward's medical university hostel"]
                    if name.lower() in bad_names:
                        continue
                    hotel_items.append((name, details))

            if hotel_items:
                st.markdown("<div class='hotel-list'><ul>", unsafe_allow_html=True)
                for name, details in hotel_items:
                    st.markdown(f"""
                    <li>
                        <span class='hotel-name'>{name}</span>
                        <div class='hotel-details'>{details}</div>
                    </li>
                    """, unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)
            else:
                st.markdown("<p>No quality hotels found. Try another city or date.</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='hotel-card'>❌ No response from hotel engine.</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • Real-time data • <a href='#' style='color: #60DAFB;'>How we find deals</a>
</div>
""", unsafe_allow_html=True)