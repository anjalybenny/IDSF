import streamlit as st
import numpy as np
from idsf import compute_inclusivity
from fuzzy_system_clarity import compute_clarity
from fuzzy_system_accessibility import compute_accessibility
from fuzzy_system_navigation import compute_navigation
from fuzzy_system_fairness import compute_fairness

st.set_page_config(page_title="Digital Service Inclusivity Evaluator", layout="wide")

st.title("Digital Public Service Inclusivity Evaluator")
st.markdown("""
This tool uses **Fuzzy Logic** to calculate the inclusivity of a digital service based on 
user experience metrics. Adjust the sliders below to see the result.
""")

# Sidebar for high-level summary
st.sidebar.header("How it works")
st.sidebar.info("""
Each category (Clarity, Accessibility, etc.) is calculated using its own fuzzy control system. 
These are then fed into a master system to determine the overall **Inclusivity Score**.
""")

# Organized Layout using Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Clarity")
    c_read = st.slider("Readability of text", 0.0, 5.0, 2.5, help="Is the text easy to read?")
    c_guid = st.slider("Step-by-step guidance", 0.0, 5.0, 2.5)
    c_term = st.slider("Terminology explained", 0.0, 5.0, 2.5)
    c_tone = st.slider("Tone consistency", 0.0, 5.0, 2.5)

    st.subheader("Navigation")
    n_search = st.slider("Search effectiveness", 0.0, 5.0, 2.5)
    n_error = st.slider("Error feedback", 0.0, 5.0, 2.5)
    n_menu = st.slider("Menu consistency", 0.0, 5.0, 2.5)
    n_task = st.slider("Task completion", 0.0, 5.0, 2.5)

with col2:
    st.subheader("Accessibility")
    a_lang = st.slider("Language availability", 0.0, 5.0, 2.5)
    a_screen = st.slider("Screen-reader compliance", 0.0, 5.0, 2.5)
    a_mobile = st.slider("Mobile responsiveness", 0.0, 5.0, 2.5)
    a_form = st.slider("Form accessibility", 0.0, 5.0, 2.5)

    st.subheader("Fairness")
    f_parity = st.slider("Parity across languages", 0.0, 5.0, 2.5)
    f_transp = st.slider("Transparency of contact", 0.0, 5.0, 2.5)
    f_equal = st.slider("Equal service access", 0.0, 5.0, 2.5)
    f_inc = st.slider("Inclusive imagery and tone", 0.0, 5.0, 2.5)

st.divider()

# Calculation Trigger
if st.button("Calculate Inclusivity Score", type="primary"):
    # Calculate Sub-scores
    score_clarity = compute_clarity(c_read, c_guid, c_term, c_tone)
    score_access = compute_accessibility(a_lang, a_screen, a_mobile, a_form)
    score_nav = compute_navigation(n_search, n_error, n_menu, n_task)
    score_fair = compute_fairness(f_parity, f_transp, f_equal, f_inc)

    # Calculate Final Score
    final_result = compute_inclusivity(score_clarity, score_access, score_nav, score_fair)

    # Display Results
    st.balloons()
    
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        st.metric(label="Overall Inclusivity Score", value=f"{final_result:.2f}%")
        
        if final_result >= 80:
            st.success("Verdict: Really Inclusive!")
        elif final_result >= 50:
            st.warning("Verdict: Inclusive Enough.")
        else:
            st.error("Verdict: Not Inclusive Enough. Needs Improvement.")

    with res_col2:
        # Mini dashboard for sub-scores
        st.write("**Sub-Category Performance:**")
        st.progress(score_clarity/100, text=f"Clarity: {score_clarity:.1f}")
        st.progress(score_access/100, text=f"Accessibility: {score_access:.1f}")
        st.progress(score_nav/100, text=f"Navigation: {score_nav:.1f}")
        st.progress(score_fair/100, text=f"Fairness: {score_fair:.1f}")