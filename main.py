import streamlit as st

# Set page config
st.set_page_config(
    page_title="Travel Copilot",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with modern design: glassmorphism, gradients, smooth fonts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@400;500&display=swap');

    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #0f1b3a 0%, #1e3a8a 50%, #20C4B4 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: white;
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }

    /* Header with glassmorphism */
    .header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        padding: 16px 40px;
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    .header h2 {
        margin: 0;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 24px;
        letter-spacing: -0.5px;
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .logo-icon {
        font-size: 28px;
        color: #20C4B4;
    }

    /* Hero Section */
    .hero {
        height: 70vh;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-bg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center/cover;
        opacity: 0.6;
        z-index: -1;
    }

    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(15, 27, 58, 0.8), rgba(32, 196, 180, 0.6));
        z-index: -1;
    }

    .hero-content {
        max-width: 800px;
        padding: 20px;
        z-index: 1;
    }

    .hero-content h1 {
        font-family: 'Montserrat', sans-serif;
        font-size: 56px;
        font-weight: 700;
        color: white;
        margin: 0 0 16px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .hero-content p {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.9);
        margin: 0 auto 32px;
        line-height: 1.6;
        max-width: 600px;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #0d9dbb, #20C4B4);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 28px;
        font-family: 'Montserrat', sans-serif;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        width: 220px;
        margin: 10px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(32, 196, 180, 0.4);
        background: linear-gradient(90deg, #20C4B4, #33e5f5);
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.8s, height 0.8s;
    }

    .stButton>button:hover::after {
        width: 300px;
        height: 300px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="logo">
        <div class="logo-icon">✈️</div>
        <h2>Travel Copilot</h2>
    </div>
    <div style="color: rgba(255,255,255,0.8); font-size: 14px;">Your AI Travel Assistant</div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-bg"></div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1>Plan Smarter. Travel Better.</h1>
        <p>Let Travel Copilot handle the details — from flights and hotels to visas and weather. Your perfect journey starts here.</p>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;">
            <button class="stButton">Explore Tools</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Use session state for tool cards (optional)
if "page" not in st.session_state:
    st.session_state.page = "main.py"

# Restored Section
st.markdown("""
<h2 style="text-align: center; font-family: 'Montserrat'; color: white; margin-top: 40px;">
    Everything You Need to Travel
</h2>
<p style="text-align: center; color: rgba(255,255,255,0.8); max-width: 700px; margin: 20px auto;">
    One platform. Infinite possibilities. Access all your travel tools in one place.
</p>
""", unsafe_allow_html=True)

# ✅ REMOVED: st.switch_page logic
# Sidebar handles navigation — no need to interfere