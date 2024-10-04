import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Load data
day_df = pd.read_csv('https://raw.githubusercontent.com/Muzhoffar/bike-sharing/refs/heads/main/dashboard/day_clean.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/Muzhoffar/bike-sharing/refs/heads/main/dashboard/hour_clean.csv')

# Convert 'date_time' column to datetime type
day_df['date_time'] = pd.to_datetime(day_df['date_time'])

# Sidebar
st.sidebar.title('Bike Rental Analysis')

# Date range filter
min_date = day_df['date_time'].min().date()
max_date = day_df['date_time'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Ensure end_date is not before start_date
if start_date > end_date:
    st.sidebar.error("Error: End date must be after start date.")
    st.stop()

# Filter data based on date range
mask = (day_df['date_time'].dt.date >= start_date) & (day_df['date_time'].dt.date <= end_date)
filtered_df = day_df.loc[mask]

analysis_type = st.sidebar.selectbox(
    'Select Analysis Type',
    ['Weather Impact', 'User Type Comparison', 'Time-based Analysis']
)

# Mapping for season
season_mapping = {1: 'Fall', 2: 'Spring', 3: 'Summer', 4: 'Winter'}
filtered_df['season'] = filtered_df['season'].map(season_mapping)

# Main content
st.title('Bike Rental Dashboard')

if analysis_type == 'Weather Impact':
    st.header('Weather Impact on Bike Rentals')
    
    weather_var = st.selectbox('Select Weather Variable', ['temperature', 'humidity', 'windspeed'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=weather_var, y='count', data=filtered_df, hue='season', ax=ax)
    plt.title(f'Impact of {weather_var.capitalize()} on Bike Rentals')
    plt.xlabel(weather_var.capitalize())
    plt.ylabel('Number of Rentals')
    plt.xticks(rotation=0)
    st.pyplot(fig)
    
    st.subheader('Weather Impact Insights')
    st.write("""
    - Temperature has a strong positive correlation with bike rentals.
    - Humidity shows a slight negative correlation with rentals.
    - Wind speed has a weak negative correlation with rentals.
    - Optimal conditions for high rentals seem to be warm temperatures with moderate humidity and low wind speed.
    """)

elif analysis_type == 'User Type Comparison':
    st.header('Comparison of Casual vs Registered Users')
    
    season_group = filtered_df.groupby('season')[['casual', 'registered']].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    season_group.plot(x='season', y=['casual', 'registered'], kind='bar', ax=ax, color=['#D3D3D3', '#72BCD4'])
    plt.title('Average Rentals by User Type Across Seasons')
    plt.xlabel('Season')
    plt.ylabel('Average Number of Rentals')
    plt.legend(['Casual', 'Registered'])
    plt.xticks(rotation=0)
    st.pyplot(fig)
    
    st.subheader('User Type Comparison Insights')
    st.write("""
    - Registered users consistently rent more bikes across all seasons.
    - Casual users show more seasonal variation, with peaks in summer and fall.
    - The gap between casual and registered users is smallest in summer and largest in winter.
    - Both user types show reduced activity in winter.
    """)

else:  # Time-based Analysis
    st.header('Time-based Analysis of Bike Rentals')
    
    time_var = st.selectbox('Select Time Variable', ['week', 'month', 'season'])
    
    if time_var == 'week':
        day_type = filtered_df['weekday'].apply(lambda x: 'Weekdays' if x in [1, 2, 3, 4, 5] else 'Weekends')
        day_type_group = filtered_df.groupby(day_type)['count'].mean()
        
        holiday_group = filtered_df.groupby('holiday')['count'].mean()
        holiday_names = ['Weekdays', 'Holidays']
        holiday_group.index = holiday_names

        fig, ax = plt.subplots(figsize=(10, 6))
        day_type_group.plot(kind='bar', ax=ax, color=['#D3D3D3', '#72BCD4'])
        plt.title('Average Bike Rentals by Weekdays vs Weekends')
        plt.xlabel('Day Type')
        plt.ylabel('Average Number of Rentals')
        plt.xticks(rotation=0)
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 6))
        holiday_group.plot(kind='bar', ax=ax, color=['#72BCD4', '#D3D3D3'])
        plt.title('Average Bike Rentals by Holidays vs Weekdays')
        plt.xlabel('Day Status')
        plt.ylabel('Average Number of Rentals')
        plt.xticks(rotation=0)
        st.pyplot(fig)
        
    elif time_var == 'month':
        month_group = filtered_df.groupby('month')['count'].mean()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_group.index = month_names
        
        fig, ax = plt.subplots(figsize=(10, 6))
        month_group.plot(kind='bar', ax=ax, color='#72BCD4')
        plt.title('Average Bike Rentals by Month')
        plt.xlabel('Month')
        plt.ylabel('Average Number of Rentals')
        plt.xticks(rotation=0)
        st.pyplot(fig)
        
    else:  # season
        season_group = filtered_df.groupby('season')['count'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        season_group.plot(kind='bar', ax=ax, color='#72BCD4')
        plt.title('Average Bike Rentals by Season')
        plt.xlabel('Season')
        plt.ylabel('Average Number of Rentals')
        plt.xticks(rotation=0)
        st.pyplot(fig)
    
    st.subheader('Time-based Analysis Insights')
    st.write("""
    - Weekdays vs. Weekends: Bike rentals are higher on weekdays, indicating commuting usage.
    - Holidays vs. Weekdays: Rentals are lower on holidays, indicating reduced commuter activity.
    - Month: Summer months (June-August) show the highest rental numbers.
    - Season: Fall has the highest average rentals, followed closely by summer.
    - There's a clear seasonal pattern with lower rentals in winter and spring.
    """)

# Footer
st.sidebar.info('Data source: Bike Sharing Dataset')
st.sidebar.text('Created by Rifqi Sirojul Muzhoffar')
