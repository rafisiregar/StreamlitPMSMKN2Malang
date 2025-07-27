import streamlit as st  # type: ignore

def render_sidebar():
    st.sidebar.title("PKL Placement at SMK Negeri 2 Malang")
    st.sidebar.markdown(
        """
        This application aims to **determine the most suitable PKL placement**
        for students based on their academic performance and skills.
        The decision-making process uses a **Profile Matching Algorithm** 
        trained on student data to provide personalized recommendations.
        Upload student data to get real-time PKL placement predictions.
        """
    )
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### 🧭 Navigation")
    selected = st.sidebar.radio("Select page:", ["Home", "PKL Placement"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made by Rafi Arya Siregar")

    return selected
