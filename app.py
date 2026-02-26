import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# App Configuration
# ---------------------------------
st.set_page_config(
    page_title="Traffic Congestion Analysis",
    layout="centered"
)

st.title("🚦 Traffic Congestion Analysis Dashboard")

st.write("""
This dashboard analyzes **raw traffic data** to identify congestion events
based on vehicle count and average speed.
""")

# ---------------------------------
# File Upload
# ---------------------------------
uploaded_file = st.file_uploader(
    "Upload traffic_data_sample.csv",
    type="csv"
)

if uploaded_file is not None:

    # ---------------------------------
    # Load Dataset
    # ---------------------------------
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📊 Dataset Information")
    st.write("Shape (rows, columns):", df.shape)
    st.write("Columns:", list(df.columns))

    # ---------------------------------
    # Data Cleaning (NO duplicate removal)
    # ---------------------------------
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    df = df[df['vehicle_count'] >= 0]
    df = df[(df['avg_speed'] >= 0) & (df['avg_speed'] <= 120)]

    st.write("Total rows after cleaning:", df.shape[0])

    # ---------------------------------
    # Visualization
    # ---------------------------------
    st.subheader("📈 Speed vs Vehicle Count")

    fig, ax = plt.subplots()
    ax.scatter(df['vehicle_count'], df['avg_speed'], alpha=0.6)
    ax.set_xlabel("Vehicle Count")
    ax.set_ylabel("Average Speed (km/h)")
    ax.set_title("Speed vs Vehicle Count")

    st.pyplot(fig)

    # ---------------------------------
    # Congestion Rule Explanation
    # ---------------------------------
    st.subheader("🚨 Congestion Detection Rule")
    st.write("""
    Congestion is detected when:
    - **Vehicle count > 100**
    - **Average speed < 25 km/h**
    """)

    # ---------------------------------
    # Congestion Detection
    # ---------------------------------
    congestion_df = df[
        (df['vehicle_count'] > 100) &
        (df['avg_speed'] < 25)
    ].copy()

    congestion_df['congestion'] = True

    st.subheader("🚦 Congestion Records")
    st.dataframe(congestion_df)

    st.write("Total congestion records:", congestion_df.shape[0])

    # ---------------------------------
    # Download Report
    # ---------------------------------
    csv = congestion_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Congestion Report",
        data=csv,
        file_name="congestion_report.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Please upload a traffic CSV file to begin analysis.")
