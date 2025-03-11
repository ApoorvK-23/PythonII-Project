# **Automated Daily Trading System**

## **Project Overview**

This project implements an **Automated Daily Trading System** that integrates **machine learning (ML)** for predicting stock market movements with a **Streamlit-based web application**. The system provides real-time stock analysis, forecasts price movements, and simulates trading strategies.

## **Project Features**

- **Machine Learning Model:** Predicts daily stock price movements.
- **Real-Time Stock Data Integration:** Fetches live data using the **SimFin API**.
- **Automated Trading Strategy:** Simulates buy/sell decisions based on ML predictions.
- **User-Friendly Web Application:** Interactive dashboard built with **Streamlit**.
- **Cloud Deployment:** Accessible without local installations.

## **Setup and Installation**

### **Requirements**

Ensure you have the following installed:

- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### **Installation Steps**

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd automated-trading-system
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   streamlit run Homepage.py
   ```

## **Usage Guide**

1. Open the **web application**.
2. Enter the initial balance for trading simulation.
3. Select a stock from the provided list.
4. View real-time **market trends, ML predictions, and trading strategy results**.
5. Monitor the **portfolio performance and trading history**.

## **Project Structure**

```
.
├── Homepage.py             # Main entry point for Streamlit web application
├── trading_strategy.py     # Trading logic and simulation
├── util.py                 # API wrapper for SimFin data fetching
├── v2python.py             # ML model training and evaluation
├── Apple.py                # Stock analysis for Apple
├── Ford.py                 # Stock analysis for Ford
├── Google.py               # Stock analysis for Google
├── Meta.py                 # Stock analysis for Meta
├── Netflix.py              # Stock analysis for Netflix
├── requirements.txt        # Dependencies
└── README.txt              # Project documentation
```

## **Challenges & Future Improvements**

- **Challenges:**
  - Handling data imbalance (solved using **SMOTE**).
  - API rate limits (optimized request frequency).
  - Performance variability across stocks.
- **Future Enhancements:**
  - Expand stock selection.
  - Improve model accuracy with advanced ML techniques.
  - Enhance trading strategy with risk management techniques.

## **Contributors**

- APOORV KULSHRESTHA
- MARTIN GUTIERREZ OLARTE
- MOAYAD SALEM BARAYAN
- TARA TEYLOUNI
- MARTIN ROBINSON




