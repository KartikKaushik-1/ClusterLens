import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ================================
# ---- SESSION STATE INIT ----
# ================================
defaults = {
    "df_temp": None,
    "df": None,
    "features": [],
    "features_temp": [],
    "kmeans": None,
    "X": None,
    "downloads": []
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ================================
# ---- CUSTOM STYLES ----
# ================================
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 10rem; }
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid red !important;
        border-radius: 100px !important;
        margin-right: 5px !important;
        padding: 5px 5px !important;
    }
    .stFileUploader { width: 50% !important; margin: 0 auto; }
    div[data-testid="stButton"] {
        display: flex; justify-content: center; margin-top: 20px;
    }
    h1 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ================================
# ---- HELPER FUNCTIONS ----
# ================================
@st.cache_data
def cluster_data(df, features):
    """Perform clustering and return clusters, fitted model, and scaled features."""
    X = df[features].copy()
    
    st.session_state.df = st.session_state.df_temp.copy()
    st.session_state.features = st.session_state.features_temp.copy()

    # Encode categorical features
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le

    # Fill missing values and scale
    X.fillna(X.mean(), inplace=True)
    X_scaled = StandardScaler().fit_transform(X)

    X = X.loc[:, X.nunique() > 1]
    max_k = min(10, len(X))
    # Find optimal clusters
    wcss = [KMeans(n_clusters=k, random_state=42).fit(X_scaled).inertia_ for k in range(1, max_k+1)]
    kl = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')

    # Final clustering
    kmeans = KMeans(n_clusters=kl.elbow, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    return clusters, kmeans, X_scaled

def show_clusters():
    """Display clustered data by cluster in separate tabs."""
    st.title("📊 Segmentation by Clusters")
    clusters = sorted(st.session_state.df['Cluster'].unique())
    tabs = st.tabs([f"Cluster {c+1}" for c in clusters])

    for tab, cluster in zip(tabs, clusters):
        with tab:
            cluster_df = st.session_state.df[st.session_state.df["Cluster"] == cluster]
            st.dataframe(cluster_df.drop(columns=["Cluster"]))

def decode_cluster_means(cluster_summary, label_encoders):
    """Decode encoded categorical feature means back to labels."""
    decoded = cluster_summary.copy()
    for col in decoded.columns:
        if col in label_encoders:
            le = label_encoders[col]
            mapping = dict(zip(le.transform(le.classes_), le.classes_))
            decoded[col] = decoded[col].apply(
                lambda val: mapping[min(mapping, key=lambda x: abs(x - val))]
            )
    return decoded

# ================================
# ---- TABS ----
# ================================
segment, profiling, analyzing, download, about = st.tabs(
    ["🗂️ Segment", "📝 Profiling", "📊 Analyzing", "📥 Download", "ℹ️ About"]
)

# ---- SEGMENT TAB ----
with segment:
    st.info("Upload your CSV to see real clustering insights")
    uploaded_file = st.file_uploader(" ", type=".csv", help="Upload a .CSV dataset")
    st.session_state.df_temp = None

    if uploaded_file:
        df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
        # Remove duplicate rows 
        df = df.drop_duplicates()
        
        st.session_state.df_temp = df.copy()
        features = st.multiselect("Select Features for Clustering", options=df.columns)
        st.session_state.features_temp = features.copy()

        if st.button("Cluster"):
            if not features:
                st.warning("Please select at least one feature.")
            else:
                clusters, kmeans, X_scaled = cluster_data(df, features)
                st.session_state.df["Cluster"] = clusters
                st.session_state.kmeans = kmeans
                st.session_state.X_scaled = X_scaled
                show_clusters()
                st.success("Clustering complete!")

# ---- PROFILING TAB ----
with profiling:
    if st.session_state.df_temp is not None and st.session_state.df is not None:
        if "Cluster" in st.session_state.df and st.session_state.features == st.session_state.features_temp:
            X = st.session_state.df.copy()
            X_encoded = X.copy()

            # Encode all categorical for profiling
            label_encoders = {}
            for col in X_encoded.columns:
                if X_encoded[col].dtype == 'object':
                    le = LabelEncoder()
                    X_encoded[col] = le.fit_transform(X_encoded[col])
                    label_encoders[col] = le

            cluster_summary = X_encoded.groupby("Cluster")[st.session_state.features].mean().round(2)
            decoded_summary = decode_cluster_means(cluster_summary, label_encoders)

            st.markdown("📊 Cluster Profiles (Mean Feature Values)")
            st.dataframe(decoded_summary)

            clusters = sorted(X['Cluster'].unique())
            tabs = st.tabs([f"Cluster {c+1}" for c in clusters])
            for tab, cluster in zip(tabs, clusters):
                with tab:
                    cluster_df = X_encoded[X_encoded["Cluster"] == cluster]
                    st.markdown("📈 Cluster Summary Statistics")
                    st.dataframe(cluster_df.drop(columns=["Cluster"]).describe())

            # Feature importance
            feature_importance = cluster_summary.var().sort_values(ascending=False)
            st.markdown("### 🌟 Features Separating Clusters the Most")
            st.dataframe(feature_importance.to_frame("Variance"))

            # Natural-language insights
            st.markdown("### 📝 Summary of Differences")
            top_features = feature_importance.head(3).index
            summary_text = "The clusters differ most based on: " + ", ".join(top_features) + ".\n\n"
            for feature in top_features:
                vals = cluster_summary[feature].to_dict()
                diff = max(vals.values()) - min(vals.values())
                summary_text += f"- **{feature}** varies by ~{diff:.2f} across clusters.\n"
            st.markdown(summary_text)
        else:
            st.warning("No clusters found yet. Please run clustering first.")
    else:
        st.warning("Please upload and process a dataset first.")

# ---- ANALYZING TAB ----
with analyzing:
    if st.session_state.df_temp is not None and st.session_state.df is not None:
        if "Cluster" in st.session_state.df and st.session_state.features == st.session_state.features_temp:
            st.markdown("## 🔍 Cluster Comparison Visualization")
            X = st.session_state.df.copy()
            
            clusters = sorted(X["Cluster"].unique())
            colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))

            for feature in st.session_state.features:
                st.markdown(f"### Feature: **{feature}**")
                cols = st.columns(len(clusters))

                for col, cluster, color in zip(cols, clusters, colors):
                    with col:
                        cluster_data = X[X["Cluster"] == cluster][feature].dropna()
                        fig, ax = plt.subplots(figsize=(3.5, 3))
                        if np.issubdtype(cluster_data.dtype, np.number):
                            ax.hist(cluster_data, bins=15, color=color, edgecolor='black')
                            ax.set_ylabel("Count")
                        else:
                            counts = cluster_data.value_counts()
                            ax.bar(counts.index.astype(str), counts.values, color=color)
                            ax.set_xticks(range(len(counts.index))) 
                            ax.set_xticklabels(counts.index.astype(str), rotation=45, ha='right')
                        ax.set_title(f"Cluster {cluster+1}", fontsize=10)
                        ax.set_xlabel(feature)
                        plt.tight_layout()
                        st.pyplot(fig)
        else:
            st.warning("No clusters found yet. Please run clustering first.")
    else:
        st.warning("Please upload and process a dataset first.")

# ---- DOWNLOAD TAB ----
with download:
    if st.session_state.df_temp is not None and st.session_state.df is not None:
        if "Cluster" in st.session_state.df and st.session_state.features == st.session_state.features_temp:
            X = st.session_state.df.copy()
            for cluster in sorted(X['Cluster'].unique()):
                csv = X[X["Cluster"] == cluster].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download Cluster {cluster+1} Data as CSV",
                    data=csv,
                    file_name=f'cluster_{cluster+1}.csv',
                    mime='text/csv',
                    key=f"download_{int(cluster)}"
                )
        else:
            st.warning("No clusters found yet. Please run clustering first.")
    else:
        st.warning("Please upload and process a dataset first.")

# ---- ABOUT TAB ----
with about:
    st.header("About this")
    st.write("""
        **ClusterLens** is an interactive tool designed to help you understand and explore datasets 
        by segmenting them into meaningful **clusters**. It identifies patterns of similar behavior, 
        summarizes them, and shows which features contribute most to these groupings.
    """)
    st.header("How it works")
    st.markdown("""
        1. **Upload your dataset** → Import any CSV file containing your data.  
        2. **Automatic Clustering** → The app segments your data into clusters.  
        3. **Profiling and Statistics** → See insights like means, medians, and distributions.  
        4. **Feature Importance** → Identify which features drive clustering.  
        5. **Visualization** → Explore your clusters visually.  
        6. **Download Results** → Export clustered data for offline use.  
    """)
    st.header("Why this is useful")
    st.write("""
        - **Quick Segmentation:** Understand groups of similar data points instantly.  
        - **Decision Making:** Helps businesses, educators, and analysts act on data insights.  
        - **No Coding Required:** Simple interface for all users.  
        - **Data Export:** Download clustered datasets for further analysis.  
    """)
      
