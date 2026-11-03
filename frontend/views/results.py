import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
import textwrap

def create_radar_chart(scores: dict, theme: str = 'Dark'):
    is_light = (theme == 'Light')
    categories = ['Formatting', 'Keywords', 'Content', 'Skill Validation', 'ATS Compatibility']
    values = [
        scores.get('formatting', 0),
        scores.get('keywords', 0),
        scores.get('content', 0),
        scores.get('skill_validation', 0),
        scores.get('ats_compatibility', 0)
    ]
    # Close the loop
    cat_loop = categories + [categories[0]]
    val_loop = values + [values[0]]
    bench_loop = [80, 80, 80, 80, 80, 80] # 80+ benchmark

    fig = go.Figure()

    # Benchmark trace
    bench_color = 'rgba(15, 23, 42, 0.4)' if is_light else 'rgba(255, 255, 255, 0.35)'
    fig.add_trace(go.Scatterpolar(
        r=bench_loop,
        theta=cat_loop,
        name='Interview Target (80)',
        line=dict(color=bench_color, dash='dash', width=1.5),
        hoverinfo='skip'
    ))

    # Candidate score trace
    line_color = '#2563EB' if is_light else '#4A90E2'
    fill_color = 'rgba(37, 99, 235, 0.25)' if is_light else 'rgba(74, 144, 226, 0.35)'
    fig.add_trace(go.Scatterpolar(
        r=val_loop,
        theta=cat_loop,
        fill='toself',
        name='Your Resume',
        line=dict(color=line_color, width=2.5),
        fillcolor=fill_color,
        marker=dict(size=6, color=line_color)
    ))

    grid_color = 'rgba(0, 0, 0, 0.12)' if is_light else 'rgba(255, 255, 255, 0.12)'
    tick_color = '#475569' if is_light else '#9DA5B4'
    text_color = '#0F172A' if is_light else '#E0E6ED'

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color=tick_color, size=10),
                gridcolor=grid_color
            ),
            angularaxis=dict(
                tickfont=dict(color=text_color, size=12, family='sans-serif'),
                gridcolor=grid_color
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color)
        ),
        height=320
    )
    return fig

def create_skills_donut(matched_count: int, missing_count: int, theme: str = 'Dark'):
    is_light = (theme == 'Light')
    total = matched_count + missing_count
    if total == 0:
        pct = 0
        values = [1]
        labels = ["No specific skills extracted"]
        colors = ['#94A3B8' if is_light else '#4A5568']
    else:
        pct = int((matched_count / total) * 100)
        values = [matched_count, missing_count]
        labels = ['Matched Skills', 'Missing Skills']
        colors = ['#16A34A' if is_light else '#2ECC71', '#DC2626' if is_light else '#E74C3C']

    donut_line_color = '#FFFFFF' if is_light else '#1E2129'
    center_text_color = '#0F172A' if is_light else '#FFFFFF'
    text_color = '#0F172A' if is_light else '#E0E6ED'

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        marker=dict(colors=colors, line=dict(color=donut_line_color, width=2)),
        textinfo='value',
        hoverinfo='label+value+percent'
    )])

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{pct}%</b><br><span style='font-size:11px;color:{'#64748B' if is_light else '#9DA5B4'};'>Match Rate</span>",
            x=0.5, y=0.5,
            font_size=24,
            font_color=center_text_color,
            showarrow=False
        )],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=30, b=30),
        height=320
    )
    return fig

def show():
    if 'analysis_result' not in st.session_state:
        st.warning("⚠️ No analysis results found. Please upload your resume in the Analyzer tab to begin.")
        if st.button("⬅️ Go to Analyzer"):
            st.rerun()
        return

    result = st.session_state['analysis_result']
    
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Resume Intelligence Results</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9DA5B4;'>In-depth ATS compatibility, semantic match, visual graph analytics, and AI coaching.</p>", unsafe_allow_html=True)
    
    # 1. Overall Score Summary
    score = result.get('overall_score', 0)
    sim = int(result.get('semantic_similarity', 0) * 100)
    score_color = "#2ECC71" if score >= 80 else "#F1C40F" if score >= 60 else "#E74C3C"
    
    status_label = "✅ INTERVIEW READY" if score >= 80 else "⚠️ NEEDS KEYWORD ALIGNMENT" if score >= 60 else "❌ CRITICAL REVISIONS NEEDED"
    status_bg = "#1a4231" if score >= 80 else "#42371a" if score >= 60 else "#4a1919"
    status_border = "#2ECC71" if score >= 80 else "#F1C40F" if score >= 60 else "#E74C3C"

    col_score, col_sim = st.columns(2)
    with col_score:
        st.markdown(f"""
        <div class='card' style='text-align: center;'>
            <h3 style='margin-bottom: 0.5rem;'>Overall ATS Score</h3>
            <div style='font-size: 3.8rem; font-weight: 800; color: {score_color}; line-height: 1;'>
                {score}<span style='font-size: 1.8rem; color: #9DA5B4;'>/100</span>
            </div>
            <div style='margin-top: 10px;'>
                <span style='background: {status_bg}; color: {status_border}; border: 1px solid {status_border}; padding: 4px 12px; border-radius: 14px; font-size: 12px; font-weight: 700;'>
                    {status_label}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(score / 100)
        
    with col_sim:
        st.markdown(f"""
        <div class='card' style='text-align: center;'>
            <h3 style='margin-bottom: 0.5rem;'>Semantic Match</h3>
            <div style='font-size: 3.8rem; font-weight: 800; color: #3498DB; line-height: 1;'>
                {sim}<span style='font-size: 1.8rem; color: #9DA5B4;'>%</span>
            </div>
            <div style='margin-top: 10px;'>
                <span style='background: #192a3e; color: #3498DB; border: 1px solid #3498DB; padding: 4px 12px; border-radius: 14px; font-size: 12px; font-weight: 700;'>
                    EMBEDDING SIMILARITY
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(sim / 100)

    # 2. Score Breakdown Cards
    scores = result.get('scores', {})
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, "Formatting", scores.get('formatting', 0), "10%"),
        (c2, "Keywords", scores.get('keywords', 0), "25%"),
        (c3, "Content Relevance", scores.get('content', 0), "30%"),
        (c4, "Skill Validation", scores.get('skill_validation', 0), "25%"),
        (c5, "ATS Compatibility", scores.get('ats_compatibility', 0), "10%")
    ]
    for col, label, val, weight in metrics:
        with col:
            st.metric(label, f"{val}/100", f"Weight: {weight}")

    st.divider()

    # 3. Interactive Graph Analysis Section
    st.markdown("### 📈 Visual Graph Analysis")
    graph_col1, graph_col2 = st.columns([1, 1], gap="medium")
    
    current_theme = st.session_state.get('app_theme', 'Dark')
    
    with graph_col1:
        st.markdown("<div class='card'><b>🕸️ Evaluation Radar (ATS 5 Pillars vs Target 80)</b>", unsafe_allow_html=True)
        fig_radar = create_radar_chart(scores, current_theme)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with graph_col2:
        matched = result.get('matched_skills', [])
        missing = result.get('missing_skills', [])
        st.markdown("<div class='card'><b>🍩 Skills Coverage Ratio</b>", unsafe_allow_html=True)
        fig_donut = create_skills_donut(len(matched), len(missing), current_theme)
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # 4. Skills Analysis
    st.markdown("### 🛠️ Skills & Keyword Breakdown")
    sk_col1, sk_col2 = st.columns(2)
    
    with sk_col1:
        st.success(f"#### ✅ Matched Skills ({len(matched)})")
        if matched:
            st.markdown(" ".join([f"<span style='background-color: #1a4231; padding: 4px 10px; border-radius: 6px; margin: 3px 4px; display: inline-block; border: 1px solid #2ecc71; font-weight: 500;'>{s}</span>" for s in matched]), unsafe_allow_html=True)
        else:
            st.info("No explicit target skills matched yet.")

    with sk_col2:
        st.error(f"#### ❌ Missing Critical Skills ({len(missing)})")
        if missing:
            st.markdown(" ".join([f"<span style='background-color: #4a1919; padding: 4px 10px; border-radius: 6px; margin: 3px 4px; display: inline-block; border: 1px solid #e74c3c; font-weight: 500;'>{s}</span>" for s in missing]), unsafe_allow_html=True)
        else:
            st.success("🎉 All identified required skills are present in your resume!")

    st.divider()

    # 5. Optimization & Improvement Hub
    st.markdown("### 💡 Actionable Insights & Improvement Plan")
    tab_improve, tab_ai, tab_sw, tab_quick = st.tabs([
        "🎯 Where Can I Improve?",
        "🤖 AI Suggestions & Coach",
        "⚖️ Strengths & Weaknesses",
        "📋 Quick Actions & Checklist"
    ])
    
    with tab_improve:
        st.markdown("#### 🎯 Strategic Resume Improvement Plan")
        st.markdown("Follow these targeted steps to elevate your ATS score from **{}** to **85+**.".format(score))
        
        # 1. Missing Skills Placement Guide
        if missing:
            st.markdown("##### 1. Missing Skills Placement Guide")
            st.info(f"Inject these high-priority keywords into your resume: **{', '.join(missing[:5])}**")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown("**Where to place them:**")
                st.markdown("""
                - **Professional Summary**: Include top 2 missing skills that summarize your capability.
                - **Skills Section**: List under categorized subheadings (e.g. *Languages, Frameworks, Cloud & Tools*).
                - **Work Experience**: Pair each skill with an action verb and project context.
                """)
            with p_col2:
                st.markdown("**How to describe them:**")
                st.markdown(f"""
                - *Example*: "Leveraged **{missing[0] if missing else 'Docker'}** to streamline deployment pipelines and enhance environment consistency."
                """)
        
        # 2. Bullet Point Rewriting Guide
        st.markdown("##### 2. Bullet Point Transformation (Google X-Y-Z Formula)")
        st.markdown("Transform passive duty statements into metric-backed accomplishments: *'Accomplished [X] as measured by [Y], by doing [Z]'*")
        
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown(textwrap.dedent("""
            <div style='background: rgba(231, 76, 60, 0.1); border-left: 4px solid #E74C3C; padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <b>❌ Weak / Generic:</b><br>
                <i>"Responsible for developing backend APIs and improving database queries."</i>
            </div>
            """).strip(), unsafe_allow_html=True)
        with b_col2:
            st.markdown(textwrap.dedent("""
            <div style='background: rgba(46, 204, 113, 0.1); border-left: 4px solid #2ECC71; padding: 12px; border-radius: 6px; margin-bottom: 8px;'>
                <b>✅ ATS-Optimized:</b><br>
                <i>"Architected 6+ RESTful microservices, reducing API latency by 35% and supporting 40k+ daily transactions."</i>
            </div>
            """).strip(), unsafe_allow_html=True)
            
        # 3. Formatting & ATS Compliance
        st.markdown("##### 3. ATS Parsing Best Practices")
        st.markdown("""
        - **Standard Section Headers**: Use clear titles (*Work Experience, Education, Technical Skills, Projects*). Avoid non-standard headers like *"My Journey"*.
        - **Single-Column Flow**: Ensure your resume parses sequentially from top to bottom. Multi-column tables often scramble text order in legacy ATS parsers.
        - **Standard Bullet Points**: Use standard circle bullets rather than custom icons or emojis which can fail character encoding.
        """)

    with tab_ai:
        st.markdown("#### 🤖 AI Coach & Tailored Recommendations")
        ai_sugg = result.get('ai_suggestions', '')
        if ai_sugg:
            st.markdown(ai_sugg)
        else:
            st.info("AI suggestions are being generated or are currently unavailable.")

    with tab_sw:
        st_c1, st_c2 = st.columns(2)
        with st_c1:
            st.markdown("#### ✅ Strengths Identified")
            strengths = result.get('strengths', [])
            if strengths:
                for s in strengths:
                    st.success(f"✓ {s}")
            else:
                st.write("Resume provides good fundamental career history.")
        with st_c2:
            st.markdown("#### ⚠️ Areas of Weakness")
            weaknesses = result.get('weaknesses', [])
            if weaknesses:
                for w in weaknesses:
                    st.warning(f"⚠ {w}")
            else:
                st.write("No major formatting weaknesses detected.")

    with tab_quick:
        st.markdown("#### ⚡ Priority Recommendations")
        for rec in result.get('recommendations', []):
            if "HIGH" in rec:
                st.error(rec)
            elif "MEDIUM" in rec:
                st.warning(rec)
            else:
                st.info(rec)
                
        st.markdown("#### 🏃 Quick Actions (Under 5 Minutes)")
        for act in result.get('quick_actions', []):
            st.markdown(f"- **{act}**")

    st.divider()
    
    # 6. Generate Report Section (Clean & Direct)
    st.markdown("### 📄 Generate Report")
    st.markdown("Export a clean executive analysis report with full scoring, skills gap, and improvement steps.")
    
    rep_col1, rep_col2 = st.columns([1, 2])
    
    with rep_col1:
        if st.button("📄 Generate Report", type="primary", use_container_width=True):
            with st.spinner("Compiling full analysis report..."):
                from frontend.services.api_client import api_download_report
                report_bytes = api_download_report(result)
                if report_bytes:
                    st.session_state['generated_report_bytes'] = report_bytes
                    st.success("✅ Report generated successfully!")

    if 'generated_report_bytes' in st.session_state:
        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state['generated_report_bytes'],
            file_name="Adhii_ATS_Analysis_Report.html",
            mime="text/html",
            type="primary"
        )
        
        with st.expander("👁️ Preview Generated Report"):
            try:
                report_html_str = st.session_state['generated_report_bytes'].decode('utf-8', errors='ignore')
                components.html(report_html_str, height=650, scrolling=True)
            except Exception as e:
                st.error(f"Could not render preview: {e}")
