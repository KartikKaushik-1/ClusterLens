import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None
    
def intro():
    # --- Title Section ---
    st.markdown(
        """
        <h1 style='text-align: center; color: #FF6F61;'> ClusterLens</h1>
        <h4 style='text-align: center; color: gray;'>Segment • Profile • Analyze • Convert</h4>
        <hr>
        """, unsafe_allow_html=True
    )

    # --- Intro Section ---
    st.markdown(
        """
        <p style='text-align: center; font-size:18px;'>
        <b>ClusterLens</b> is an AI-powered tool that helps you 
        <b style="color:#FF6F61;">segment</b> datasets, 
        <b style="color:#1F77B4;">profile</b> patterns, 
        <b style="color:#2CA02C;">analyze</b> groups, 
        and <b style="color:#9467BD;">export</b> insights directly to PDF.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --- Features with Icons ---
    col1, col2, col3, col4 = st.columns(4, border = False)

    with col1:
        c1, c2, c3 = st.columns([1.5,2,1])
        with c2:
            st.image("Images/cluster.png", width=70)
        st.markdown("<h4 style='text-align:center;'>Segmentation</h4>", unsafe_allow_html=True)
        st.markdown("<p style = 'text-align:center;'>Group your data into meaningful clusters.</p>", unsafe_allow_html=True)

    with col2:
        c1, c2, c3 = st.columns([1.5,2,1])
        with c2:
            st.image("Images/profiling.png", width=70)
        st.markdown("<h4 style='text-align:center;'>Profiling</h4>", unsafe_allow_html=True)
        st.markdown("<p style = 'text-align:center;'>Learn group behaviors with statistics.</p>", unsafe_allow_html=True)
        
    with col3:
        c1, c2, c3 = st.columns([1.5,2,1])
        with c2:
            st.image("Images/analyzing.png", width=70)
        st.markdown("<h4 style='text-align:center;'>Analyzing</h4>", unsafe_allow_html=True)
        st.markdown("<p style = 'text-align:center;'>Explore comparison using visual insights.</p>", unsafe_allow_html=True)

    with col4:
        c1, c2, c3 = st.columns([1.5,2,1])
        with c2:
            st.image("Images/pdf.png", width=70)
        st.markdown("<h4 style='text-align:center;'>Download the clusters</h4>", unsafe_allow_html=True)
        st.markdown("<p style = 'text-align:center;'>Generate .csv file of diferent clusters you want.</p>", unsafe_allow_html=True)

    st.markdown("---")
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.role = "Start"
            st.rerun()
    


# ---Define your account pages---#
welcome = st.Page("account/welcome.py", title = "Welcome", icon = "👋")
cluster = st.Page("account/cluster.py", title = "Clustering", icon = ":material/group:")


#--Define your Tools page--#
openai = st.Page("Tools/openAI.py", title = "Ask any thing", icon = "💬")


#--Grouping your pages--#
account_page = [welcome, cluster]
tool_page = [openai]

#--Page Configuration--#
st.set_page_config(
    page_title = "ClusterLens",
    page_icon = "Images/logo.png",
    layout = "wide")
st.logo("Images/logo.png", size = "large", icon_image = "Images/logo.png")


#--Page Dictionary--#
page_dict = {}

#--
page_dict["Account"] = account_page
page_dict["Tool"] = tool_page

#--Define your Navigation--#    
if st.session_state.role == "Start":
    pg = st.navigation(page_dict)
else:
    pg = st.navigation([st.Page(intro)])
    
#--Ececute the Page returned by st.navigation--#
pg.run()





        

