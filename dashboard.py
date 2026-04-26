import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io

st.set_page_config(page_title="Social Media Strategy Dashboard", layout="wide")
st.title("Live Engagement Analytics")

def fetch_live_data():
    types = ['Video', 'Photo', 'Reel']
    times = ['Morning', 'Evening']
    new_data = {
        'Content_Type': [np.random.choice(types) for _ in range(50)],
        'Post_Time': [np.random.choice(times) for _ in range(50)],
        'Likes': [np.random.randint(100, 6000) for _ in range(50)],
        'Shares': [np.random.randint(10, 1000) for _ in range(50)]
    }
    return pd.DataFrame(new_data)


st.sidebar.header("Data Controls")
if st.sidebar.button("Reload to fetch new live data"):
    st.session_state['data'] = fetch_live_data()
    st.sidebar.success("Data updated!")


if 'data' not in st.session_state:
    st.session_state['data'] = fetch_live_data()

df = st.session_state['data']


report = df.groupby(['Content_Type', 'Post_Time']).agg({
    'Likes': 'mean',
    'Shares': 'sum'
}).reset_index()


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Real-Time Aggregation")
    st.dataframe(report, hide_index=True, use_container_width=True)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report.to_excel(writer, index=False)
    
    st.download_button(
        label="Download the aggregated report",
        data=output.getvalue(),
        file_name='Social_Media_Report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

with col2:
    st.subheader("Performance Chart")
    metric = st.segmented_control("Metric:", ["Likes", "Shares"], default="Likes")
    
    fig = px.bar(report, x="Content_Type", y=metric, color="Post_Time", 
                 barmode="group", text_auto='.0f',
                 color_discrete_map={'Morning': '#3498db', 'Evening': '#e74c3c'})
    st.plotly_chart(fig, use_container_width=True)