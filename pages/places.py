import streamlit as st
from graph import build_graph
import re

# Set page config
st.set_page_config(
    page_title="Places to Visit | Travel Copilot",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS – Sleek & modern
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
        border: 1px solid rgba(255,255,255,0.15);
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

    /* Places Card */
    .places-card {
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

    .places-card h3 {
        color: #60DAFB;
        font-size: 18px;
        margin: 0 0 12px;
        text-align: center;
    }

    .places-list {
        text-align: left;
        margin: 10px 0;
    }

    .places-list ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .places-list li {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px 12px;
        margin: 6px 0;
        font-size: 14px;
        line-height: 1.5;
    }

    .place-name {
        font-weight: 600;
        color: white;
        display: block;
    }

    .place-type {
        color: #60DAFB;
        font-size: 13px;
        margin: 2px 0;
    }

    .place-location {
        color: rgba(255,255,255,0.8);
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
st.markdown("<h1>🗺️ Places to Visit</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Discover top attractions, parks, museums, and more in your destination.</p>", unsafe_allow_html=True)

# Query Form
with st.form("places_query_form"):
    query = st.text_area(
        "Your Query",
        value="Places to visit in Lahore",
        placeholder="Examples:\n• What should I see in Tokyo?\n• Top attractions in Rome\n• Best parks in Sydney",
        height=80
    )
    submit = st.form_submit_button("Find Places")

# Handle Submission
if submit:
    if not query.strip():
        st.error("⚠️ Please enter a query.")
    else:
        with st.spinner("🗺️ Finding top places..."):
            try:
                graph = build_graph()
                response = graph.invoke({"user_input": query.strip(), "response": "", "next": None})["response"]
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                response = ""

        if response:
            # Clean response
            cleaned = response.replace("<br>", "\n").replace("<b>", "").replace("</b>", "").strip()

            # Extract title
            title_match = re.search(r"🗺️\s*(.+?)(?:\n|$)", cleaned)
            title = title_match.group(1).strip() if title_match else "Top Places"

            # Find all places (lines starting with "- ")
            lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
            place_items = []
            for line in lines:
                if line.startswith("- "):
                    content = line[2:].strip()
                    if "📍" in content:
                        # Split by last "📍" to separate name/type from location
                        parts = content.rsplit("📍", 1)
                        main_part = parts[0].strip()
                        location = parts[1].strip()
                    else:
                        main_part = content
                        location = "Location details available"

                    # Split by last " — " to get name and category
                    if " — " in main_part:
                        name_part, category = main_part.rsplit(" — ", 1)
                    else:
                        name_part = main_part
                        category = "Attraction"

                    name = name_part.strip()
                    place_items.append((name, category, location))

            # Show result
            st.markdown("<div class='places-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3>🎯 {title}</h3>", unsafe_allow_html=True)

            if place_items:
                st.markdown("<div class='places-list'><ul>", unsafe_allow_html=True)
                for name, category, location in place_items:
                    st.markdown(f"""
                    <li>
                        <div class='place-name'>{name}</div>
                        <div class='place-type'>{category}</div>
                        <div class='place-location'>📍 {location}</div>
                    </li>
                    """, unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)
            else:
                # Show raw response if no places parsed
                st.markdown(f"<p>{cleaned}</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='places-card'>❌ No places found.</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Travel Copilot © 2025 • Powered by Geoapify • <a href='#' style='color: #60DAFB;'>Explore more</a>
</div>
""", unsafe_allow_html=True)