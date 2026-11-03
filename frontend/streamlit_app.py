import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from frontend.views import analyzer, results
from frontend.components.footer import render_feedback_and_footer

st.set_page_config(
    page_title="Adhii ATS Resume",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Theme state
if 'app_theme' not in st.session_state:
    st.session_state['app_theme'] = 'Dark'

def get_theme_css(theme: str) -> str:
    if theme == "Light":
        return """
        :root, .stApp {
            --bg-main: #F8FAFC !important;
            --bg-gradient: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 50%, #E2E8F0 100%) !important;
            --bg-card: #FFFFFF !important;
            --border-glass: #CBD5E1 !important;
            --text-primary: #0F172A !important;
            --text-secondary: #334155 !important;
            --text-muted: #64748B !important;
            --input-bg: #FFFFFF !important;
            --input-text: #0F172A !important;
            --sidebar-bg: #F1F5F9 !important;
            --uploader-bg: #F8FAFC !important;
            --file-data-bg: #E2E8F0 !important;
            --accent-blue: #2563EB !important;
            --accent-purple: #7C3AED !important;
            --heading-gradient: linear-gradient(135deg, #1D4ED8 0%, #6D28D9 100%) !important;
            --card-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.08) !important;
        }
        """
    elif theme == "Semi":
        return """
        :root, .stApp {
            --bg-main: #1E293B !important;
            --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #273549 100%) !important;
            --bg-card: rgba(30, 41, 59, 0.9) !important;
            --border-glass: rgba(148, 163, 184, 0.25) !important;
            --text-primary: #F8FAFC !important;
            --text-secondary: #CBD5E1 !important;
            --text-muted: #94A3B8 !important;
            --input-bg: #0F172A !important;
            --input-text: #F8FAFC !important;
            --sidebar-bg: #0F172A !important;
            --uploader-bg: rgba(15, 23, 42, 0.7) !important;
            --file-data-bg: #334155 !important;
            --accent-blue: #0284C7 !important;
            --accent-purple: #6366F1 !important;
            --heading-gradient: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
            --card-shadow: 0 8px 28px 0 rgba(0, 0, 0, 0.25) !important;
        }
        """
    else: # Dark (Default)
        return """
        :root, .stApp {
            --bg-main: #0B0F19 !important;
            --bg-gradient: radial-gradient(circle at top left, #1a1c2c 0%, #0B0F19 45%, #0B0F19 100%) !important;
            --bg-card: rgba(20, 26, 40, 0.8) !important;
            --border-glass: rgba(255, 255, 255, 0.1) !important;
            --text-primary: #F3F4F6 !important;
            --text-secondary: #9CA3AF !important;
            --text-muted: #6B7280 !important;
            --input-bg: #151D2E !important;
            --input-text: #FFFFFF !important;
            --sidebar-bg: #0D121F !important;
            --uploader-bg: rgba(21, 29, 46, 0.6) !important;
            --file-data-bg: #1A2337 !important;
            --accent-blue: #3B82F6 !important;
            --accent-purple: #8B5CF6 !important;
            --heading-gradient: linear-gradient(135deg, #60A5FA 0%, #C084FC 100%) !important;
            --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35) !important;
        }
        """

# Load base CSS
try:
    with open("frontend/assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Inject active theme dynamic CSS variables
active_theme = st.session_state.get('app_theme', 'Dark')
st.markdown(f"<style>{get_theme_css(active_theme)}</style>", unsafe_allow_html=True)


def main():
    st.sidebar.markdown("## 📄 Adhii ATS Resume")
    st.sidebar.divider()
    
    # Navigation
    pages = {
        "Analyzer": analyzer.show,
        "Results": results.show,
    }
    default_page = "Results" if 'analysis_result' in st.session_state else "Analyzer"
    selection = st.sidebar.radio("Navigation", list(pages.keys()), index=list(pages.keys()).index(default_page))
    
    st.sidebar.divider()
    
    # Theme Toggle Section (Dark, Semi-Dark, Light)
    st.sidebar.markdown("### 🎨 Theme Mode")
    theme_options = ["🌙 Dark", "🌓 Semi-Dark", "☀️ Light"]
    theme_map = {"🌙 Dark": "Dark", "🌓 Semi-Dark": "Semi", "☀️ Light": "Light"}
    inv_map = {"Dark": 0, "Semi": 1, "Light": 2}
    
    current_choice = inv_map.get(st.session_state.get('app_theme', 'Dark'), 0)
    selected_option = st.sidebar.radio(
        "Appearance",
        options=theme_options,
        index=current_choice,
        label_visibility="collapsed"
    )
    
    chosen_theme = theme_map[selected_option]
    if chosen_theme != st.session_state.get('app_theme'):
        st.session_state['app_theme'] = chosen_theme
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Adhii ATS Resume Intelligence • v1.2")
        
    pages[selection]()
    render_feedback_and_footer()

if __name__ == "__main__":
    main()
