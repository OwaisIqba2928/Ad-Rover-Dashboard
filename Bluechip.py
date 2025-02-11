import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Load Data
file_path = r"cleaned_data.csv"
data = pd.read_csv(file_path)

# Data Preparation
data['time'] = pd.to_datetime(data['time'])
data['hour'] = data['time'].dt.hour
data['day'] = data['time'].dt.day_name()
data['month'] = data['time'].dt.month_name()

# Streamlit Page Configuration
st.set_page_config(page_title="📊 Ad Rover Analytics Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Enhanced Styling and Background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background: #1a1a2e;
        color: #e3e3e3;
    }

    /* Add a beautiful gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    .title-bar {
        background: linear-gradient(90deg, #ff8c00, #ff0080);
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 36px;
        font-weight: bold;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
        animation: glow 2s infinite alternate;
    }

    @keyframes glow {
        0% {
            box-shadow: 0px 0px 20px rgba(255, 140, 0, 0.7);
        }
        100% {
            box-shadow: 0px 0px 40px rgba(255, 0, 128, 0.7);
        }
    }
    
    .kpi-container {
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
    }
    
    .kpi-card {
        flex: 1;
        background: #22264b;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15);
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        margin: 10px;
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, rgba(255, 140, 0, 0.3), rgba(255, 0, 128, 0.3));
        transform: rotate(45deg);
        transition: all 0.5s ease;
        z-index: 1;
    }

    .kpi-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(255, 140, 0, 0.5), 0px 0px 30px rgba(255, 0, 128, 0.5);
    }

    .kpi-card:hover::before {
        top: 0;
        left: 0;
    }

    .kpi-card span {
        position: relative;
        z-index: 2;
    }
    
    .chart-title {
        font-size: 22px;
        font-weight: bold;
        color: white;
        text-align: center;
        padding: 12px;
        background: #22264b;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
        margin-bottom: 24px;
        animation: glow 2s infinite alternate;
    }

    .sidebar-box {
        background: linear-gradient(135deg, #8a2be2, #ff1493);
        padding: 20px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .sidebar-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar Background */
    .css-1d391kg {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    .css-1d391kg .st-bb {
        color: white;
    }

    .css-1d391kg .st-cb {
        color: white;
    }

    .css-1d391kg .st-db {
        color: white;
    }

    /* Modern Navbar */
    .navbar {
        background: linear-gradient(90deg, #ff8c00, #ff0080);
        padding: 16px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        width: 60%;
        margin: 25px auto;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease-in-out;
        animation: glow 2s infinite alternate;
    }
    
    .navbar:hover {
        transform: scale(1.03);
        box-shadow: 0px 8px 22px rgba(0, 0, 0, 0.4);
    }
    
    .navbar img {
        width: 30px;
        height: 30px;
        margin-right: 10px;
        filter: drop-shadow(2px 2px 5px rgba(0, 0, 0, 0.2));
    }

    /* Glowing Animation */
    @keyframes glow {
        0% {
            box-shadow: 0px 0px 20px rgba(255, 140, 0, 0.7);
        }
        100% {
            box-shadow: 0px 0px 40px rgba(255, 0, 128, 0.7);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dashboard Title
st.markdown("<div class='title-bar'>📊 Ad Rover Analytics Dashboard</div>", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    min_date = data['time'].min().date()
    max_date = data['time'].max().date()
    default_start_date = max_date - timedelta(days=7)
    
    st.markdown("<div class='sidebar-box'>📅 Select Date Range</div>", unsafe_allow_html=True)
    date_range = st.date_input("", [default_start_date, max_date], min_value=min_date, max_value=max_date)
    start_date, end_date = date_range
    
    st.markdown("<div class='sidebar-box'>📺 Filter by Ad ID</div>", unsafe_allow_html=True)
    ad_filter = st.multiselect("", options=data['ad_id'].unique(), default=data['ad_id'].unique())
    
    st.markdown("<div class='sidebar-box'>🎂 Filter by Age</div>", unsafe_allow_html=True)
    age_filter = st.slider("", min_value=int(data['age'].min()), max_value=int(data['age'].max()), value=(int(data['age'].min()), int(data['age'].max())))

# Filter Data
filtered_data = data[
    (data['time'].dt.date >= start_date) & 
    (data['time'].dt.date <= end_date) & 
    (data['ad_id'].isin(ad_filter)) & 
    (data['age'].between(age_filter[0], age_filter[1]))
]

# KPI Metrics
total_users = len(filtered_data)
unique_ads = filtered_data['ad_id'].nunique()
most_common_gender = filtered_data['gender'].mode()[0] if not filtered_data.empty else "N/A"
average_age = round(filtered_data['age'].mean()) if not filtered_data.empty else 0

# KPI Cards
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card"><span>👥 Total Users <br> {total_users}</span></div>
        <div class="kpi-card"><span>📢 Unique Ads <br> {unique_ads}</span></div>
        <div class="kpi-card"><span>📌 Most Gender <br> {most_common_gender}</span></div>
        <div class="kpi-card"><span>📊 Average Age <br> {average_age}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

# ✨ Beautiful & Modern Navbar
st.markdown(
    """
    <div class="navbar">
        <img src="https://cdn-icons-png.flaticon.com/512/747/747376.png">
        Gender Distribution of Users
    </div>
    """,
    unsafe_allow_html=True
)

import plotly.express as px
import streamlit as st

import plotly.express as px
import streamlit as st

import pandas as pd
import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit as st
import plotly.express as px

import pandas as pd
import streamlit as st
import plotly.express as px

# 📊 Gender Distribution Pie Chart (Mesmerizing & Professional)
gender_icons = {"Male": "👨", "Female": "👩", "Other": "⚧"}  # Icons for clarity
gender_count = filtered_data['gender'].value_counts().reset_index()
gender_count.columns = ['Gender', 'Count']
gender_count['Count'] = gender_count['Count'].astype(int)  # Ensure integer values
gender_count['Label'] = gender_count.apply(lambda row: f"{gender_icons.get(row['Gender'], '❓')} {row['Gender']} ({row['Count']})", axis=1)

fig_gender_pie = px.pie(
    gender_count, names="Label", values="Count", color="Gender",
    color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFD700'],  # Modern & premium colors
    hole=0.25  # Elegant donut effect
)

fig_gender_pie.update_traces(
    textinfo='label+percent',
    texttemplate="%{label}: %{percent:.0%}",  # Displays absolute values & percentage
    pull=[0.1 if i == gender_count['Count'].idxmax() else 0.05 for i in range(len(gender_count))],  # Highlight the highest value
    marker=dict(line=dict(color='black', width=2)),  # Improved contrast
    hoverinfo="label+percent+value",  # Show absolute values on hover
)

# 🎨 Polished Chart Design
fig_gender_pie.update_layout(
    font=dict(size=18, color="white"),  # Improved readability
    showlegend=True,
    height=500,
    paper_bgcolor="#1A2B4C",  # Consistent background
    plot_bgcolor="#1A2B4C",  
    margin=dict(t=10, b=10, l=10, r=10),  # Optimal spacing
    legend=dict(title="🧑‍🤝‍🧑 Gender", font=dict(size=16, color="white"))  # Professional legend design
)

# ✨ Stylish Chart Container
st.markdown(
    """
    <style>
    .chart-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease-in-out;
        border: 2px solid #FFD700;
    }
    .chart-container:hover {
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🖼️ Display the Chart
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_gender_pie, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)




# 🌟 Attractive Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        padding: 16px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.02);
    }
    </style>
    <div class="navbar">📊 Age Distribution of Users</div>
    """,
    unsafe_allow_html=True
)

import pandas as pd
import streamlit as st
import plotly.express as px

# Define Age Groups for Clear Segmentation
age_bins = [10, 20, 30, 40, 50, 60, 70, 80, 100]
age_labels = ['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+']
filtered_data['age_group'] = pd.cut(filtered_data['age'], bins=age_bins, labels=age_labels, right=False)
age_count = filtered_data['age_group'].value_counts().reset_index()
age_count.columns = ['Age Group', 'Count']

# 📊 Stunning Age Distribution Bar Chart
fig_age_bar = px.bar(
    age_count, x='Age Group', y='Count', text='Count',
    color='Age Group', color_discrete_sequence=px.colors.qualitative.Vivid  # Vibrant colors
)

fig_age_bar.update_traces(
    textposition='outside',
    marker=dict(line=dict(color='black', width=1))  # Enhanced contrast
)

# 🎨 Beautiful Background & Professional Styling
fig_age_bar.update_layout(
    title="📈 Age Group Distribution",
    xaxis=dict(
        title="👶 Age Group 🧓",
        tickmode="linear",
        tickfont=dict(size=16, color="white")
    ),
    yaxis=dict(
        title="📊 Number of People",
        tickfont=dict(size=16, color="white")
    ),
    font=dict(size=18, color="white"),
    showlegend=False,
    height=500,
    paper_bgcolor="#1A2B4C",  # Attractive dark blue gradient background
    plot_bgcolor="#1A2B4C",  # Same background for seamless look
    margin=dict(t=10, b=10, l=10, r=10)
)

# 🖼️ Elegant Chart Container with Matching Theme
st.markdown("<div class='chart-container' style='background: linear-gradient(135deg, #1A2B4C, #2C3E50); padding: 15px; border-radius: 15px;'>", unsafe_allow_html=True)
st.plotly_chart(fig_age_bar, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)




# 🌟 Attractive Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        padding: 16px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.02);
    }
    </style>
    <div class="navbar">📊 Number Of Users Over Time</div>
    """,
    unsafe_allow_html=True
)

import plotly.express as px

import plotly.express as px

import plotly.express as px

# 📊 Persons Over Time
time_series = filtered_data.groupby('time')['total_persons'].sum().reset_index()

# 🎨 Define background color (Deep Navy Blue)
bg_color = '#1A2B4C'

fig_time = px.line(
    time_series, x="time", y="total_persons", markers=True,
    color_discrete_sequence=["#FF4C4C"],  # 🔥 Bold Red Line
    labels={"time": "⏳ Time", "total_persons": "👥 Users"}
)

# 🎨 Theme Styling
fig_time.update_traces(
    line=dict(width=4),
    marker=dict(size=10, symbol="circle", color="#FF4C4C")
)

fig_time.update_layout(
    xaxis=dict(
        title="⏳ Time",
        title_font=dict(size=18, color="#FFFFFF"),
        tickfont=dict(size=14, color="#FFFFFF"),
        showgrid=True, gridcolor="rgba(255, 255, 255, 0.3)"
    ),
    yaxis=dict(
        title="👥 Users",
        title_font=dict(size=18, color="#FFFFFF"),
        tickfont=dict(size=14, color="#FFFFFF"),
        showgrid=True, gridcolor="rgba(255, 255, 255, 0.3)"
    ),
    font=dict(size=16, color="#FFFFFF"),
    template="plotly_white",
    plot_bgcolor=bg_color,  # 📉 Chart Background
    paper_bgcolor=bg_color,  # 🔥 Fully Match Background (Fix White Bar)
    margin=dict(t=5, b=40, l=40, r=20)  # 🔥 Reduce Top Margin
)

# 🖼️ Stylish Chart Container
st.markdown(
    """
    <style>
    .chart-container {
        background: rgba(255, 255, 255, 0.98);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_time, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
# 🌟 Attractive Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        padding: 16px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.02);
    }
    </style>
    <div class="navbar">📊 Number Of Users Per Ad</div>
    """,
    unsafe_allow_html=True
)


import pandas as pd
import streamlit as st
import plotly.express as px

# 📊 Total Persons Per Ad (Stylish & Modern)
persons_per_ad = filtered_data.groupby('ad_id')['total_persons'].sum().reset_index()

# 🌟 Create a Bar Chart with Enhanced Styling
fig_persons = px.bar(
    persons_per_ad, x="ad_id", y="total_persons", 
    color="total_persons", color_continuous_scale="Viridis",  # Attractive Color Gradient for Better Appeal
    labels={"ad_id": "Ad ID", "total_persons": "Users"}
)

# 🎨 Enhance Styling for Visual Appeal
fig_persons.update_traces(
    marker=dict(line=dict(color="black", width=2)),  # Sleek Black Border for Better Contrast
    hoverinfo="x+y",  # Hover Information for Interaction
    opacity=0.9  # Slight Transparency for a Modern Look
)

# 🌟 Perfect Background & Axis Styling
fig_persons.update_layout(
    xaxis=dict(
        title="📢 Ad ID",  # Title with Icons for Context
        title_font=dict(size=18, color="#FFFFFF", family="Arial, sans-serif"),
        tickfont=dict(size=14, color="#FFFFFF"),
        showgrid=False,  # Clean Grid for Better Focus
        zeroline=False
    ),
    yaxis=dict(
        title="👥 Users",  # Title with Icons to Enhance Readability
        title_font=dict(size=18, color="#FFFFFF", family="Arial, sans-serif"),
        tickfont=dict(size=14, color="#FFFFFF"),
        showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)",  # Subtle Gridlines for Clean Look
        zeroline=False
    ),
    font=dict(size=16, color="#FFFFFF", family="Arial, sans-serif"),
    template="plotly_dark",  # Dark Background Template for Modern Design
    plot_bgcolor='rgba(26, 43, 76, 1)',  # Dark Blue Background for a Professional Look
    paper_bgcolor='rgba(26, 43, 76, 1)',  # Dark Blue Paper Background
    margin=dict(t=20, b=40, l=40, r=20),  # Adjusted Margins for Better Spacing
    hovermode="closest"  # Ensure the hover interaction works smoothly
)

# 🖼️ Stylish Chart Container with Hover Effect
st.markdown(
    """
    <style>
    .chart-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        text-align: center;
    }
    .chart-container:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the chart in a stylish container
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_persons, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# 🌟 Attractive Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        padding: 16px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .chart-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.02);
    }
    </style>
    <div class="navbar">📊 Number Of Users By Hour And Day</div>
    """,
    unsafe_allow_html=True
)
import pandas as pd
import streamlit as st
import plotly.express as px

# 📊 Group Data for Clarity
bar_data = filtered_data.groupby(['hour', 'day']).size().reset_index(name='Count')

# 🌈 Attractive & Intuitive Stacked Area Chart
fig_area = px.area(
    bar_data, x="hour", y="Count", color="day",
    labels={"hour": "🕒 Hour of the Day", "Count": "👥 Number of Users", "day": "📅 Day"},
    line_group="day",
    color_discrete_sequence=["#FFD700", "#FF4500", "#32CD32", "#1E90FF", "#FF69B4", "#8A2BE2"],  # Bright & appealing colors
)

# ✨ Enhanced Chart Design
fig_area.update_layout(
    xaxis=dict(
        title="🕒 Hour of the Day",
        title_font=dict(size=20, color="#FFFFFF", family="Arial, sans-serif"),
        tickfont=dict(size=16, color="#FFFFFF"),
        showgrid=False  
    ),
    yaxis=dict(
        title="👥 Number of Users",
        title_font=dict(size=20, color="#FFFFFF", family="Arial, sans-serif"),
        tickfont=dict(size=16, color="#FFFFFF"),
        showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)",
    ),
    font=dict(size=18, color="#FFFFFF", family="Arial, sans-serif"),
    template="plotly_dark",  
    plot_bgcolor='rgba(26, 43, 76, 1)',  
    paper_bgcolor='rgba(26, 43, 76, 1)',  
    margin=dict(t=20, b=40, l=40, r=20),  
    legend=dict(title="📅 Day", font=dict(size=16, color="#FFFFFF"))  
)

# 🖼️ Stylish Chart Container
st.markdown(
    """
    <style>
    .chart-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease-in-out;
    }
    .chart-container:hover {
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the Stacked Area Chart
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_area, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


import pandas as pd
import streamlit as st

# 📋 --- STYLISH DATA SUMMARY TABLE ---
summary_data = filtered_data.copy()
summary_data['date'] = summary_data['time'].dt.date
summary_data['time_only'] = summary_data['time'].dt.time
summary_data = summary_data[['date', 'time_only', 'ad_id', 'total_persons', 'gender', 'age']]
summary_data.columns = ['📅 Date', '⏰ Time', '📢 Ad ID', '👥 Total Persons', '⚧ Gender', '🎂 Age']

# 📜 Beautiful Table Styling
st.markdown(
    """
    <style>
    /* Table Container */
    .summary-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 8px 18px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease-in-out;
        border: 2px solid #FFD700;
    }
    .summary-container:hover {
        transform: scale(1.02);
    }

    /* Table */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden;
        background: white;
        color: black;
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    
    /* Header Styling */
    thead {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: black;
        font-weight: bold;
        font-size: 18px;
        text-transform: uppercase;
    }

    /* Alternate Row Colors */
    tbody tr:nth-child(odd) {
        background-color: #F8F9FA;
    }

    tbody tr:nth-child(even) {
        background-color: #E9ECEF;
    }

    /* Hover Effect */
    tbody tr:hover {
        background-color: #FFD700;
        color: black;
        font-weight: bold;
    }

    /* Borders */
    th, td {
        padding: 12px;
        border-bottom: 2px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Elegant Navigation Bar
st.markdown(
    """
    <style>
    .navbar {
        background: linear-gradient(90deg, #ff5733, #ff8d1a);
        padding: 18px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    </style>
    <div class="navbar">📊 Beautiful Data Table</div>
    """,
    unsafe_allow_html=True
)

# Display the Data Table
st.markdown("<div class='summary-container'>", unsafe_allow_html=True)
st.dataframe(
    summary_data.tail(10),  # Show last 10 records
    use_container_width=True,  
    height=320
)
st.markdown("</div>", unsafe_allow_html=True)
