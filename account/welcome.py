import streamlit as st

# --- Page Title ---
st.markdown(
        """
        <h1 style="text-align:center;">👋 Welcome to <span style="color:#4CAF50;">ClusterLens</span></h1>
        <h5 style="text-align:center; weight: bold;">Segment • Profile • Visualize • Download</h5>
        """, unsafe_allow_html=True
    )

st.markdown("---")
# --- Two Column Layout ---
col1, col2 = st.columns([1, 1], vertical_alignment = "center")

with col1:
    st.subheader("What is ClusterLens?")
    st.write(
        """
        **ClusterLens** helps you understand your data by:  
        - Segmenting datasets into **clusters** of similar behavior.  
        - Providing **profiling** and summary statistics for each group.  
        - Showing **which features drive clustering the most**.  
        - Offering **visualizations** to make patterns crystal clear.  
        - Letting you **download clustered data as CSV** in one click.  
        """
    )

with col2:
    c1, c2, c3 = st.columns([0.25,2,1], border = False)
    with c2:
        # Add a logo or image
        st.image(
            "images/logo.png",
            caption="Your data, clearly segmented", width = 300
        )
st.markdown("---")     
st.image("images/welcome_cluster_flow.png", caption = "Work flow of ClusterLens", use_container_width = True)

st.markdown("---")
st.header("Why this is useful")
st.write(
    """
    - **Quick Segmentation:** Understand groups of similar data points instantly.  
    - **Decision Making:** Helps businesses, educators, and analysts act on data-driven insights.  
    - **No Coding Required:** All operations are done through a simple, intuitive interface.  
    - **Data Export:** Easily download clustered datasets for reports or further analysis.  
    """
)


