import streamlit as st 
import joblib
import pandas as pd
from util import PySimFin  # Import PySimFin class
from sklearn.preprocessing import StandardScaler

# Load the trained model
model_path = "saved_models/NFLX_model.joblib"  # Path to your trained model
model = joblib.load(model_path)  # Load model using joblib

scaler_path = "saved_models/NFLX_scaler.joblib"  
scaler = joblib.load(scaler_path)

# Initialize SimFin API
API_KEY = "79f8076c-cdc4-4ffe-9827-a82f92215739"  # Replace with your actual API key
simfin = PySimFin(API_KEY)

# Streamlit UI for User Input
st.set_page_config(page_title="Netflix Stock Prediction", layout="wide")

# Apple Logo & Title
st.image("https://seeklogo.com/images/N/netflix-n-logo-0F1ED3EBEB-seeklogo.com.png", width=150)
st.title("Google's Stock Prediction")
st.write("Analyze and predict Netflix's stock price movements with AI-powered insights.")

# Company Background Section
st.subheader("📌 About Netflix")
st.write(
    "Apple Inc. is a multinational technology company that specializes in consumer electronics, software, and online services."
    " It is one of the world's most valuable companies and is known for its innovative products such as the iPhone, MacBook, iPad, and Apple Watch."
    " Apple is also a leader in financial performance, consistently showing strong stock growth and market dominance."
)

# Date Input
st.subheader("📆 Select Date Range")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"), format="YYYY-MM-DD")
end_date = st.date_input("End Date", pd.to_datetime("2024-01-01"), format="YYYY-MM-DD")

# Convert dates to string format
ticker = "NFLX"
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

# Get share prices & financials
prices_df = simfin.get_share_prices(ticker, start_date, end_date)
financials_df = simfin.get_financial_statement(ticker, start_date, end_date)

# Validate retrieved data
if prices_df is None or financials_df is None or prices_df.empty or financials_df.empty:
    st.error("❌ Unable to fetch stock prices or financial data. Please try again later.")
    st.stop()

# Merge and Clean Data
merged_df = simfin.merge_data(prices_df, financials_df)
if merged_df is None or merged_df.empty:
    st.error("❌ Merging data failed, resulting in an empty DataFrame.")
    st.stop()

# Adding additional columns
add_df = simfin.add_technical_indicators(merged_df)
renamed_df = simfin.rename_columns(add_df)
renamed_df["Dividend"].fillna(0, inplace=True)
clean_df = renamed_df.ffill().bfill()

st.write(clean_df.isna().sum())

# Select relevant features
selected_features = ['Volume', 'Other Long Term Assets', 'Cash from (Repurchase of) Equity', 'Operating Expenses', 'Operating Income (Loss)', 'Income Tax (Expense) Benefit, Net', 'SMA_5', 'RSI_14']

filtered_df = simfin.filter_selected_features(clean_df, selected_features)

# Scaling
df_scaled = pd.DataFrame(scaler.fit_transform(filtered_df), columns=filtered_df.columns)

st.write(df_scaled.isna().sum())

# Validate filtered data
if df_scaled is None or filtered_df.empty:
    st.error("❌ No valid data available after filtering selected features.")
    st.stop()

# Display Scaled Data
with st.container():
    st.subheader("🔍 Processed Data Before Prediction")
    st.dataframe(df_scaled)

# Ensure correct input shape
if len(df_scaled.shape) == 1:
    df_scaled = df_scaled.values.reshape(1, -1)
latest_data = df_scaled.to_numpy()[-1].reshape(1, -1)

# Make Predictions
predictions = model.predict(latest_data)[0]
prediction_labels = "📉 Price will go DOWN" if predictions == 0 else "📈 Price will go UP"

# Display Prediction Results
with st.container():
    st.subheader("🔮 AI Prediction for Next Trading Day")
    if predictions == 0:
        st.markdown("<h3 style='color: red;'>📉 Price will go DOWN</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: lime;'>📈 Price will go UP</h3>", unsafe_allow_html=True)

st.write("🔍 AI-powered stock movement prediction based on fundamental & technical analysis.")
