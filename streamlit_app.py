import streamlit as st
import pandas as pd

# Load the combined data
st.title("Food Search for Linoleic Acid Data")

# Load the dataset with caching
@st.cache_data
def load_data():
    return pd.read_csv("linoleic_acid_data_combined.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

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

# Search input
query = st.text_input("Enter food name or keyword to search:")

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

# Display results
if not filtered_df.empty:
    st.write(f"Showing {len(filtered_df)} result(s):")
    st.dataframe(filtered_df[['food', 'la_cal', 'cal', 'percent', 'category']])
    
    # Download option for filtered results
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Results as CSV",
        data=csv,
        file_name="filtered_results.csv",
        mime="text/csv",
    )
else:
    st.write("No results found. Adjust your filters and try again.")

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
