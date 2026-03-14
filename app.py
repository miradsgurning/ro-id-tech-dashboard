import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration (UI Setup)
# Setting up the page title and wide layout
st.set_page_config(page_title="RO-ID Tech Data Insight", layout="wide")

# Data Loading Function with Optimization
@st.cache_data # Performance optimation by caching the processed data
def load_data():
    # Load dataset (CSV Format)
    # skiprows=4 is for bypassing the metadata header rows in the original file
    df = pd.read_csv('tech_data.csv', skiprows=4)

    #Filter specific countries (Romania and Indonesia)
    countries = ['Romania', 'Indonesia']
    df_filtered = df[df['Country Name'].isin(countries)]

    # Data Transformation ( Wide to Long format)
    df_melted = df_filtered.melt(id_vars=['Country Name'], 
                                 value_vars=[str(year) for year in range(2010, 2025)],
                                 var_name='Year', value_name='Tech_Export_Value')
    
    # Ensure 'Year' column is treated as numeric for continuous axis plotting
    df_melted['Year'] = pd.to_numeric(df_melted['Year'])
    return df_melted

# Main Application Logic
try:
    # Execute data Loading and transformation
    df_final = load_data()

    # UI Header
    st.title("🇷🇴 Romania & 🇮🇩 Indonesia: High-Tech Export Analysis")
    st.markdown("**High-Technology Exports** Data Analysis. Developed as part of a **Computer Science** Scholarship Portfolio")
    
    # Data Visualization
    # Craeting an interactive Line chart to visualize the growth trends
    fig = px.line(df_final, x='Year', y='Tech_Export_Value', color='Country Name',
                  title="Trend of High-Technology Exports (Current US$)",
                  labels={'Tech_Export_Value': 'Value in USD', 'Year': 'Year'},
                  markers=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # Interactive Filter
    # Slider for user interaction
    year_range = st.slider("Select Year Range:", 2010, 2024, (2015, 2024))
    
    # Filtering the dataframe based on the slider input
    df_selection = df_final[(df_final['Year'] >= year_range[0]) & (df_final['Year'] <= year_range[1])]
    
    # Displaying the filtered raw data for transparency
    st.dataframe(df_selection, use_container_width=True)

except FileNotFoundError:
    st.error("Critical Error: 'tech_data.csv' not found. Please ensure the dataset is in the root directory.")