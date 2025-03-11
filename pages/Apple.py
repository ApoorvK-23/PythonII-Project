import streamlit as st 
import joblib
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from util import PySimFin  # Import PySimFin class
from sklearn.preprocessing import StandardScaler
from trading_strategy import execute_trading_strategy

# Load the trained model
model_path = "saved_models/AAPL_model.joblib"  # Path to your trained model
model = joblib.load(model_path)  # Load model using joblib

scaler_path = "saved_models/AAPL_scaler.joblib"  
scaler = joblib.load(scaler_path)

# Initialize SimFin API
API_KEY = "79f8076c-cdc4-4ffe-9827-a82f92215739"  # Replace with your actual API key
simfin = PySimFin(API_KEY)

# Streamlit UI for User Input
st.set_page_config(page_title="Apple Stock Prediction", layout="wide")

# Apple Logo & Title
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Apple_Store_logo.svg/1024px-Apple_Store_logo.svg.png", width=150)
st.title("Apple Stock Prediction")
st.write("Analyze and predict Apple's stock price movements with AI-powered insights.")

# Company Background Section
st.subheader("📌 About Apple Inc.")
st.write(
    "Apple Inc. is a multinational technology company that specializes in consumer electronics, software, and online services."
    " It is one of the world's most valuable companies and is known for its innovative products such as the iPhone, MacBook, iPad, and Apple Watch."
    " Apple is also a leader in financial performance, consistently showing strong stock growth and market dominance."
)

# Get share prices & financials
st.sidebar.header("📅 Select Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"), format="YYYY-MM-DD")
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"), format="YYYY-MM-DD")

# Convert dates to string format
ticker = "AAPL"
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

# Separate price df

separate_prices = clean_df['Close']


# Select relevant features
selected_features = ['Open', 'Close', 'Dividend', 'Long Term Debt', 'Non-Cash Items', 'Change in Working Capital', 'Net Cash from Operating Activities', 'Net Change in Long Term Investment', 'Net Cash from Acquisitions & Divestitures', 'Net Cash from Financing Activities']

filtered_df = simfin.filter_selected_features(clean_df, selected_features)

# Scaling
df_scaled = pd.DataFrame(scaler.fit_transform(filtered_df), columns=filtered_df.columns)

# Validate filtered data
if df_scaled is None or filtered_df.empty:
    st.error("❌ No valid data available after filtering selected features.")
    st.stop()

# Display candlestick
fig = go.Figure(data=[go.Candlestick(x=merged_df.index, open=clean_df['Open'], high=clean_df['High'], low=clean_df['Low'], close=clean_df['Close'])])
fig.update_layout(title="📊 Apple Stock Candlestick Chart", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)



# Display Scaled Data
with st.container():
    st.subheader("🔍 Processed Data Before Prediction")
    st.dataframe(df_scaled)



# Make Predictions
predictions = model.predict(df_scaled)




# Convert Predictions into Human-Readable Labels
prediction_labels = ["📉 Price will go DOWN" if pred == 0 else "📈 Price will go UP" for pred in predictions]

# Create DataFrame for Display
prediction_results = pd.DataFrame({
    "Date": merged_df.index,
    "Predicted Movement": prediction_labels
})


#price +prediction

pred1 = pd.concat([prediction_results,separate_prices], axis=1)
pred1 = pred1.rename(columns={'Close':'Current Price'})

# Display Prediction Results
with st.container():
    st.subheader("🔮 AI Predictions for Selected Date Range")
    st.dataframe(pred1)


st.write("🔍 AI-powered stock movement prediction based on fundamental & technical analysis.")

if "initial_balance" not in st.session_state:
    st.session_state["initial_balance"] = 10000  # Default value


initial_balance = st.session_state["initial_balance"]




# Run Trading Strategy with an initial balance of $10,000

final_results = execute_trading_strategy(pred1, initial_balance)

# Display Results in Streamlit
st.subheader("📊 Trading Strategy Results")
st.write(f"**Final Account Balance:** ${final_results['Final Balance']:.2f}")
st.write(f"**Shares Held:** {final_results['Shares Held']}")
st.write(f"**Total Portfolio Value:** ${final_results['Total Portfolio Value']:.2f}")

# Simple Time Series Line Chart for Total Portfolio Value
# trading_df = pd.DataFrame(final_results["Trading History"], columns=["Date", "Portfolio Value"])
# fig, ax = plt.subplots()
# ax.plot(trading_df["Date"], trading_df["Portfolio Value"], marker='o', linestyle='-')
# ax.set_title("📈 Total Portfolio Value Over Time")
# ax.set_xlabel("Date")
# ax.set_ylabel("Portfolio Value")
# plt.xticks(rotation=45)
# st.pyplot(fig)


# Display Trading History as a DataFrame
trading_history_df = pd.DataFrame(final_results["Trading History"], columns=["Action", "Price"])
st.subheader("📜 Trading History")
st.dataframe(trading_history_df)
