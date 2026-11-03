import streamlit as st
import json
import os
from datetime import datetime
from frontend.services.feedback_notifier import submit_feedback

def render_feedback_and_footer():
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # 1. Feedback Form Section (Rendered as normal open card content)
    st.markdown("""
    <div style='margin-bottom: 16px;'>
        <h3 style='margin-bottom: 4px;'>💬 Feedback & Suggestions</h3>
        <p style='color: var(--text-secondary); font-size: 14px;'>
            Your thoughts and experience help make Adhii ATS Resume more powerful and accurate for everyone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_name, col_email = st.columns(2)
    with col_name:
        fb_name = st.text_input("Your Name (Optional)", placeholder="e.g. Alex Doe", key="fb_name_input")
    with col_email:
        fb_email = st.text_input("Your Email (Optional)", placeholder="e.g. alex@example.com", key="fb_email_input")
        
    fb_rating = st.select_slider(
        "Overall Experience Rating",
        options=["⭐ Poor", "⭐⭐ Fair", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Very Good", "⭐⭐⭐⭐⭐ Excellent"],
        value="⭐⭐⭐⭐⭐ Excellent",
        key="fb_rating_slider"
    )
    
    fb_comments = st.text_area(
        "Suggestions, Thoughts, or Bug Reports",
        placeholder="Tell us what you liked, what could be improved, or features you'd love to see next...",
        height=100,
        key="fb_comments_area"
    )
    
    if st.button("🚀 Submit Feedback", type="primary", key="fb_submit_btn"):
        if not fb_comments.strip():
            st.warning("Please enter a short message or comment before submitting.")
        else:
            with st.spinner("Submitting your feedback..."):
                res = submit_feedback(
                    rating=fb_rating,
                    comments=fb_comments,
                    name=fb_name,
                    email=fb_email
                )
                if res.get("email_sent"):
                    st.success("🎉 Thank you! Your feedback has been sent directly to the creator's inbox.")
                    st.balloons()
                elif res.get("success"):
                    st.success("🎉 Thank you so much! Your feedback has been recorded.")
                    st.balloons()
                else:
                    st.info("Thank you! Your feedback has been received.")

    # 2. Creator Connect & Social Links Footer
    linkedin_url = "https://www.linkedin.com/in/adieshwar-reddy-mogili-3b4b11332/"
    github_url = "https://github.com/AdieshwarReddy"
    youtube_url = "https://www.youtube.com/@theconfident_circle"
    instagram_url = "https://www.instagram.com/theconfident_circle?stkn=MWFlbnd5YmprbGhtNw%3D%3D"
    email_addr = "mogiliadieshwarreddy5919@gmail.com"

    footer_content = f"""<div class='footer-container'>
<div style='font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;'>
🚀 Adhii ATS Resume Intelligence Platform
</div>
<div style='font-size: 13.5px; color: var(--text-secondary); margin-bottom: 12px;'>
Built with ❤️ by <b>Adieshwar Reddy Mogili</b>
</div>
<div class='social-links-container'>
<a href='{linkedin_url}' target='_blank' rel='noopener noreferrer' class='social-link-badge'>💼 LinkedIn</a>
<a href='{github_url}' target='_blank' rel='noopener noreferrer' class='social-link-badge'>💻 GitHub</a>
<a href='{youtube_url}' target='_blank' rel='noopener noreferrer' class='social-link-badge'>📺 YouTube</a>
<a href='{instagram_url}' target='_blank' rel='noopener noreferrer' class='social-link-badge'>📸 Instagram</a>
<a href='mailto:{email_addr}' class='social-link-badge'>✉️ Email Me</a>
</div>
<div style='font-size: 12px; color: var(--text-muted); margin-top: 18px;'>
&copy; 2026 Adhii ATS Resume • Designed for Interview Success
</div>
</div>"""
    st.markdown(footer_content, unsafe_allow_html=True)
