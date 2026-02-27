import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(page_title="Uber Mobility Dashboard", layout="wide")

st.title("🚖 Uber Urban Mobility Analytics Dashboard")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Admin\Desktop\Uber\Datasets\uber-raw-data-janjune-15.csv")   # 🔥 CHANGE this to your exact file name
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Convert Pickup_date to datetime
    df['Pickup_date'] = pd.to_datetime(df['Pickup_date'])
    
    # Create hour column
    df['hour'] = df['Pickup_date'].dt.hour
    
    # Create weekday
    df['weekday'] = df['Pickup_date'].dt.day_name()
    
    # Weekend flag
    df['is_weekend'] = df['weekday'].isin(['Saturday', 'Sunday'])
    
    return df

df = load_data()

# ----------------------------------
# Dataset Preview
# ----------------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ----------------------------------
# Hourly Demand
# ----------------------------------
st.subheader("📊 Ride Demand by Hour")

hourly_demand = df.groupby('hour').size().reset_index(name='rides')

fig1 = px.bar(
    hourly_demand,
    x='hour',
    y='rides',
    title="Hourly Ride Demand"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------
# Peak & Lowest Hour
# ----------------------------------
peak_row = hourly_demand.loc[hourly_demand['rides'].idxmax()]
low_row = hourly_demand.loc[hourly_demand['rides'].idxmin()]

total_rides = hourly_demand['rides'].sum()

peak_percentage = (peak_row['rides'] / total_rides) * 100
low_percentage = (low_row['rides'] / total_rides) * 100

col1, col2 = st.columns(2)

with col1:
    st.metric("🔥 Peak Hour", f"{int(peak_row['hour'])}:00")
    st.metric("Peak % of Total Rides", f"{peak_percentage:.2f}%")

with col2:
    st.metric("💤 Lowest Hour", f"{int(low_row['hour'])}:00")
    st.metric("Lowest % of Total Rides", f"{low_percentage:.2f}%")

# ----------------------------------
# Weekend vs Weekday
# ----------------------------------
st.subheader("📈 Weekend vs Weekday Demand")

comparison = df.groupby(['is_weekend', 'hour']).size().reset_index(name='rides')

fig2 = px.line(
    comparison,
    x='hour',
    y='rides',
    color='is_weekend',
    labels={'is_weekend': 'Weekend'},
    title="Weekend vs Weekday Hourly Demand"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# Heatmap
# ----------------------------------
st.subheader("🌡 Ride Demand Heatmap")

pivot = df.pivot_table(index='weekday', columns='hour', aggfunc='size')

fig3 = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Ride Demand Heatmap (Weekday vs Hour)"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------
# Business Insights
# ----------------------------------
st.subheader("📌 Business Insights")

st.write(f"""
- Peak demand occurs at **{int(peak_row['hour'])}:00**, accounting for **{peak_percentage:.2f}%** of total rides.
- Lowest demand occurs at **{int(low_row['hour'])}:00**, accounting for **{low_percentage:.2f}%** of total rides.
- Evening hours indicate strong commuter-driven demand.
- Early morning demand is minimal, suggesting potential driver reallocation.
- Weekend patterns differ from weekday commuting structure.
""")