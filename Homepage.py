import streamlit as st
import yfinance as yf
import requests
import pandas as pd
import datetime

# def fetch_financial_news():
# API_KEY = "1Sz45lN5jp4HrVJeS07bZ6KQv84GlrNw21jc77WX"  # Replace with your valid API key
# url = f"https://api.marketaux.com/v1/news/all?language=en&api_token={API_KEY}"
# response = requests.get(url)
# if response.status_code == 200:
#     articles = response.json().get("articles", [])
#     return articles[:5]  # Return top 5 news articles
# else:
#     st.warning("⚠️ Unable to fetch news. API response:", response.json())
#     return []

# def fetch_market_indices():
# indices = {
#     "S&P 500": "https://finance.yahoo.com/quote/^GSPC/",
#     "NASDAQ": "https://finance.yahoo.com/quote/^IXIC/",
#     "Dow Jones": "https://finance.yahoo.com/quote/^DJI/"
# }
# return indices

# def fetch_stock_data():
# stocks = ['GOOGL', 'META', 'F', 'AAPL', 'NFLX']
# stock_data = {}
# for stock in stocks:
#     ticker = yf.Ticker(stock)
#     hist = ticker.history(period="1mo")  # Get last month's data
#     if not hist.empty:
#         stock_data[stock] = hist['Close']
# return pd.DataFrame(stock_data)

def main():
    st.set_page_config(page_title="Stock Prediction App", layout="wide")
    
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
            html, body, [class*="st"] {
                background-color: #0a0f1c;
                font-family: 'Orbitron', sans-serif;
                color: #00ffea;
                overflow: auto;
                background-image: url('https://i.gifer.com/4NB4.gif'); /* External Matrix GIF */
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

        # User input for initial balance and shares
    initial_balance = st.number_input("Enter Initial Balance ($):", min_value=1000, value=10000, step=500)
    

    # Store values in session state
    st.session_state["initial_balance"] = initial_balance


    st.success(f"✅ Initial balance set to: ${initial_balance}")
    
    
    with st.container():
        st.markdown('<p class="title-text">💹 Welcome to the Future of FinTech</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">AI-Powered Stock Market Predictions at Your Fingertips</p>', unsafe_allow_html=True)
    
    st.subheader("🌎 Live Market Overview")
    
    Market Indices Links
    with st.container():
        st.subheader("📊 Global Market Indices")
        indices = fetch_market_indices()
        for name, link in indices.items():
            st.markdown(f"🔗 [{name}]({link})")
    
    # Live Financial News
    with st.container():
        st.subheader("📰 Latest Financial News")
        news_articles = fetch_financial_news()
        if news_articles:
            for article in news_articles:
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.write(f"🗞 {article['source']['name']} - {article['publishedAt'][:10]}")
                st.write(f"{article['description']}")
                st.write("---")
        else:
            st.warning("⚠️ Unable to fetch news at the moment. Try again later.")
    
    # Stock Trends Graph
    with st.container():
        st.subheader("📈 Stock Trends")
        stock_df = fetch_stock_data()
        if not stock_df.empty:
            st.line_chart(stock_df)
        else:
            st.warning("⚠️ Unable to fetch stock data.")
    

    

    
if __name__ == "__main__":
    main()
