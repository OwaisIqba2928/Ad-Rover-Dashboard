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

# Custom CSS for Enhanced Styling and Responsiveness
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

    /* Responsive Title Bar */
    .title-bar {
        background: linear-gradient(90deg, #ff8c00, #ff0080);
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
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

    /* Responsive KPI Cards */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
        margin: 20px 0;
    }

    .kpi-card {
        flex: 1 1 calc(25% - 20px);
        background: #22264b;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15);
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
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

    /* Responsive Sidebar */
    .sidebar-box {
        background: linear-gradient(135deg, #8a2be2, #ff1493);
        padding: 15px;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .sidebar-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }

    /* Responsive Charts */
    .chart-container {
        background: linear-gradient(135deg, #1A2B4C, #2C3E50);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }

    .chart-container:hover {
        transform: scale(1.02);
    }

    /* Media Queries for Mobile and Tablet */
    @media (max-width: 768px) {
        .title-bar {
            font-size: 24px;
            padding: 15px;
        }

        .kpi-card {
            flex: 1 1 calc(50% - 10px);
            font-size: 16px;
            padding: 15px;
        }

        .sidebar-box {
            padding: 10px;
            font-size: 14px;
        }

        .chart-container {
            padding: 10px;
        }
    }

    @media (max-width: 480px) {
        .title-bar {
            font-size: 20px;
            padding: 10px;
        }

        .kpi-card {
            flex: 1 1 100%;
            font-size: 14px;
            padding: 10px;
        }

        .sidebar-box {
            padding: 8px;
            font-size: 12px;
        }

        .chart-container {
            padding: 8px;
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


import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar">🧑‍🤝‍🧑📊 Gender Distribution Analysis 📈⚖️</div>
    """,
    unsafe_allow_html=True
)

# Gender Distribution Pie Chart
gender_icons = {"Male": "👨", "Female": "👩", "Other": "⚧"}
gender_count = filtered_data['gender'].value_counts().reset_index()
gender_count.columns = ['Gender', 'Count']

# Remove "?" and replace unknown genders with "Other"
gender_count['Gender'] = gender_count['Gender'].replace("?", "Other")

# Create labels with icons
gender_count['Label'] = gender_count.apply(
    lambda row: f"{gender_icons.get(row['Gender'], '⚧')} {row['Gender']} ({row['Count']})", axis=1
)

# Professional and Attractive Color Palette
color_palette = ['#FF6B6B', '#4ECDC4', '#FFD700']

fig_gender_pie = px.pie(
    gender_count, names="Label", values="Count", color="Gender",
    color_discrete_sequence=color_palette,
    hole=0.25
)

fig_gender_pie.update_traces(
    textinfo='label+percent',
    texttemplate="%{label}: %{percent:.0%}",
    pull=[0.1 if i == gender_count['Count'].idxmax() else 0.05 for i in range(len(gender_count))],
    marker=dict(line=dict(color='black', width=2)),
    hoverinfo="label+percent+value",
)

fig_gender_pie.update_layout(
    font=dict(size=16, color="white"),
    showlegend=True,
    height=400,
    paper_bgcolor="#1A2B4C",
    plot_bgcolor="#1A2B4C",
    margin=dict(t=10, b=10, l=10, r=10),
    legend=dict(title="🧑‍🤝‍🧑 Gender", font=dict(size=14, color="white"))
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_gender_pie, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar"> 👴📊 Age Distribution Analysis 📈📊</div>
    """,
    unsafe_allow_html=True
)

# Age Distribution Bar Chart
if 'age' in filtered_data.columns:
    age_bins = [0, 10, 20, 30, 40, 50, 60, 100]  # Added 0-10 and 60+ groups
    age_labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60+']  # Updated labels

    filtered_data['age_group'] = pd.cut(filtered_data['age'], bins=age_bins, labels=age_labels, right=False)
    
    age_count = filtered_data['age_group'].value_counts().reindex(age_labels, fill_value=0).reset_index()
    age_count.columns = ['Age Group', 'Count']

    fig_age_bar = px.bar(
        age_count, x='Age Group', y='Count', text='Count',
        color='Age Group', category_orders={"Age Group": age_labels},
        color_discrete_sequence=px.colors.qualitative.Bold  # Vibrant colors
    )

    fig_age_bar.update_traces(
        textposition='outside',
        marker=dict(line=dict(color='black', width=1.5))  # Stronger border for clarity
    )

    fig_age_bar.update_layout(
        title="📊 Age Distribution Analysis",
        xaxis=dict(title="👶 Age Group 🧓", tickfont=dict(size=14, color="white")),
        yaxis=dict(title="📊 Number of Users", tickfont=dict(size=14, color="white")),
        font=dict(size=16, color="white"),
        showlegend=False,
        height=400,
        paper_bgcolor="#1A2B4C",
        plot_bgcolor="#1A2B4C",
        margin=dict(t=10, b=10, l=10, r=10)
    )

    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig_age_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)









import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar">📅📈 Number of Users Over Time 👥⏳</div>
    """,
    unsafe_allow_html=True
)


# Number of Users Over Time
time_series = filtered_data.groupby('time')['total_persons'].sum().reset_index()

fig_time = px.line(
    time_series, x="time", y="total_persons", markers=True,
    color_discrete_sequence=["#FF4C4C"],
    labels={"time": "⏳ Time", "total_persons": "👥 Users"}
)

fig_time.update_traces(
    line=dict(width=4),
    marker=dict(size=10, symbol="circle", color="#FF4C4C")
)

fig_time.update_layout(
    xaxis=dict(title="⏳ Time", tickfont=dict(size=14, color="white")),
    yaxis=dict(title="👥 Users", tickfont=dict(size=14, color="white")),
    font=dict(size=16, color="white"),
    template="plotly_dark",
    plot_bgcolor='rgba(26, 43, 76, 1)',
    paper_bgcolor='rgba(26, 43, 76, 1)',
    margin=dict(t=5, b=40, l=40, r=20)
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_time, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar">📢📊 Number of Users Per Ad 👥🎯</div>
    """,
    unsafe_allow_html=True
)


# Number of Users Per Ad
persons_per_ad = filtered_data.groupby('ad_id')['total_persons'].sum().reset_index()

fig_persons = px.bar(
    persons_per_ad, x="ad_id", y="total_persons", 
    color="total_persons", color_continuous_scale="Viridis",
    labels={"ad_id": "Ad ID", "total_persons": "Users"}
)

fig_persons.update_traces(
    marker=dict(line=dict(color="black", width=2)),
    hoverinfo="x+y",
    opacity=0.9
)

fig_persons.update_layout(
    xaxis=dict(title="📢 Ad ID", tickfont=dict(size=14, color="white")),
    yaxis=dict(title="👥 Users", tickfont=dict(size=14, color="white")),
    font=dict(size=16, color="white"),
    template="plotly_dark",
    plot_bgcolor='rgba(26, 43, 76, 1)',
    paper_bgcolor='rgba(26, 43, 76, 1)',
    margin=dict(t=20, b=40, l=40, r=20)
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_persons, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar">⏰📅 Number of Users by Hour and Day 👥📊</div>
    """,
    unsafe_allow_html=True
)
# Number of Users By Hour and Day
bar_data = filtered_data.groupby(['hour', 'day']).size().reset_index(name='Count')

fig_area = px.area(
    bar_data, x="hour", y="Count", color="day",
    labels={"hour": "🕒 Hour of the Day", "Count": "👥 Number of Users", "day": "📅 Day"},
    line_group="day",
    color_discrete_sequence=["#FFD700", "#FF4500", "#32CD32", "#1E90FF", "#FF69B4", "#8A2BE2"],
)

fig_area.update_layout(
    xaxis=dict(title="🕒 Hour of the Day", tickfont=dict(size=14, color="white")),
    yaxis=dict(title="👥 Number of Users", tickfont=dict(size=14, color="white")),
    font=dict(size=16, color="white"),
    template="plotly_dark",
    plot_bgcolor='rgba(26, 43, 76, 1)',
    paper_bgcolor='rgba(26, 43, 76, 1)',
    margin=dict(t=20, b=40, l=40, r=20),
    legend=dict(title="📅 Day", font=dict(size=14, color="white"))
)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_area, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st

st.markdown(
    """
    <style>
    /* 🚀 Elegant and Shaded Navigation Bar with Image-Based Colors */
    .navbar {
        background: linear-gradient(45deg, rgb(255, 129, 10), rgb(255, 128, 11)); /* 🎨 Image-Inspired Gradient */
        padding: 12px 25px;
        border-radius: 8px; /* ✅ Slightly Rounded */
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        width: 60%; /* ✅ Slimmer & Compact */
        margin: auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3); /* ✅ Soft Shadow */
        backdrop-filter: blur(10px); /* ✅ Modern Blur Effect */
        border: 4px solid rgb(255, 221, 51); /* ✨ Stylish Yellow Border */
        background-clip: padding-box; /* Ensures border color doesn't get overridden by background */
        transition: all 0.3s ease-in-out;
    }

    /* ✨ Hover Effect */
    .navbar:hover {
        background: linear-gradient(45deg, rgb(240, 110, 5), rgb(220, 100, 5)); /* 🔥 Slightly Darker on Hover */
        transform: scale(1.03);
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.5);
        border-color: rgb(255, 200, 0); /* 🎨 Slightly Darker Yellow on Hover */
    }

    </style>

    <!-- 🔥 Stylish and Image-Based Navigation Bar -->
    <div class="navbar">📊📋 Data Summary 📈✅</div>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import pandas as pd

# Ensure 'filtered_data' exists before using it
if 'filtered_data' in locals():
    # Create a copy to avoid modifying original data
    summary_data = filtered_data.copy()

    # Ensure 'time' column is in datetime format
    if 'time' in summary_data.columns:
        summary_data['date'] = summary_data['time'].dt.date
        summary_data['time_only'] = summary_data['time'].dt.time
    else:
        summary_data['date'] = None
        summary_data['time_only'] = None

    # Select and rename columns for a clean summary table
    summary_data = summary_data[['date', 'time_only', 'ad_id', 'total_persons', 'gender', 'age']]
    summary_data.columns = ['📅 Date', '⏰ Time', '📢 Ad ID', '👥 Total Persons', '⚧ Gender', '🎂 Age']
    # 📋 Display the Data Table
    st.markdown("<div class='summary-container'>", unsafe_allow_html=True)
    st.dataframe(
        summary_data.tail(10),  # Show last 10 records
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("❌ Error: 'filtered_data' is not available. Please check your dataset.")
