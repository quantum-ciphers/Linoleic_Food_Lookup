import streamlit as st
import pandas as pd

# Set page configuration and Open Graph metadata
st.set_page_config(
    page_title="Linoleic Acid Food Lookup",  # Updated title
    page_icon="🍴",  # Optional: Set a custom favicon
    layout="wide",  # Options: "wide" or "centered"
    initial_sidebar_state="collapsed"  # Sidebar is expanded by default
)

# Add Open Graph metadata for the custom thumbnail
st.markdown(
    """
    <meta property="og:title" content="Linoleic Acid Food Lookup">
    <meta property="og:description" content="Explore foods with high and low linoleic acid content. Filter and search foods to learn more about their omega-6 fatty acid levels.">
    <meta property="og:image" content="https://raw.githubusercontent.com/quantum-ciphers/Linoleic_Food_Lookup/main/seedoils.png">
    <meta property="og:url" content="https://seedoilcontent.streamlit.app">
    <meta property="og:type" content="website">
    """,
    unsafe_allow_html=True
)

# Add title
st.title("Food Search for Linoleic Acid Data")

# Add note about the sidebar
st.markdown("### Use the sidebar to apply filters and customize your search.")

# Add Column Definitions
st.markdown(
    """
    ### Column Definitions
    - **la_cal**: Number of calories from linoleic acid per 100 grams of food.
    - **cal**: Total calories per 100 grams of food.
    - **percent**: Percentage of calories from linoleic acid.
    """
)

# Load the dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("linoleic_acid_data_combined.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")  # Kept only the filters header

# Dropdown filter for High/Low LA
category_filter = st.sidebar.selectbox("Select Category", options=["All", "High LA", "Low LA"])

# Sliders for numeric filters
min_la_cal = st.sidebar.slider(
    "Minimum LA Calories",
    float(df['la_cal'].min()), float(df['la_cal'].max()), float(df['la_cal'].min())
)
max_la_cal = st.sidebar.slider(
    "Maximum LA Calories",
    float(df['la_cal'].min()), float(df['la_cal'].max()), float(df['la_cal'].max())
)

min_cal = st.sidebar.slider(
    "Minimum Total Calories",
    float(df['cal'].min()), float(df['cal'].max()), float(df['cal'].min())
)
max_cal = st.sidebar.slider(
    "Maximum Total Calories",
    float(df['cal'].min()), float(df['cal'].max()), float(df['cal'].max())
)

min_percent = st.sidebar.slider(
    "Minimum Percent LA",
    float(df['percent'].min()), float(df['percent'].max()), float(df['percent'].min())
)
max_percent = st.sidebar.slider(
    "Maximum Percent LA",
    float(df['percent'].min()), float(df['percent'].max()), float(df['percent'].max())
)

# Add search bar and results table with matching widths
col1, col2, col3 = st.columns([3, 5, 3])  # Adjust column widths for smaller search bar
with col2:
    query = st.text_input("Enter food name or keyword to search:", key="search_input")

    # Filter data based on inputs
    filtered_df = df.copy()

    # Apply category filter
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]

    # Apply numeric filters
    filtered_df = filtered_df[
        (filtered_df['la_cal'] >= min_la_cal) &
        (filtered_df['la_cal'] <= max_la_cal) &
        (filtered_df['cal'] >= min_cal) &
        (filtered_df['cal'] <= max_cal) &
        (filtered_df['percent'] >= min_percent) &
        (filtered_df['percent'] <= max_percent)
    ]

    # Apply text search filter
    if query:
        filtered_df = filtered_df[filtered_df['food'].str.contains(query, case=False, na=False)]

    # Display results below the search bar
    st.write(f"Showing {len(filtered_df)} result(s):")
    st.dataframe(filtered_df[['food', 'la_cal', 'cal', 'percent', 'category']], use_container_width=True)

# Download option for filtered results
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Results as CSV",
    data=csv,
    file_name="filtered_results.csv",
    mime="text/csv",
)

# Add a data source section in the sidebar
st.sidebar.markdown(
    """
    ### Data Source
    This data is obtained from the **[FoodData Central](https://fdc.nal.usda.gov/)** database, 
    specifically filtered for linoleic acid, the omega-6 polyunsaturated fat.
    """
)

# Add a footer with the same data source information
st.markdown(
    """
    ---
    ### Data Source
    This data is obtained from the **[FoodData Central](https://fdc.nal.usda.gov/)** database, 
    specifically filtered for linoleic acid, the omega-6 polyunsaturated fat.
    """
)
