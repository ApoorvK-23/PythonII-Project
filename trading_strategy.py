import pandas as pd

class TradingAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.shares = 0
        self.trading_history = []

    def buy(self, price):
        if self.balance >= price:
            self.shares += 1
            self.balance -= price
            self.trading_history.append(("BUY", price))
    
    def sell(self, price):
        if self.shares > 0:
            self.shares -= 1
            self.balance += price
            self.trading_history.append(("SELL", price))
    

    
    def get_summary(self, final_price):
        total_value = self.balance + (self.shares * final_price)
        return {
            "Final Balance": self.balance,
            "Shares Held": self.shares,
            "Total Portfolio Value": total_value,
            "Trading History": self.trading_history
        }

def execute_trading_strategy(predictions_df, initial_balance=10000):
    account = TradingAccount(initial_balance)
    
    for index, row in predictions_df.iterrows():
        prediction = row["Predicted Movement"]
        price = row["Current Price"]
        
        if prediction == "📈 Price will go UP":
            account.buy(price)
        elif prediction == "📉 Price will go DOWN":
            account.sell(price)

    
    final_summary = account.get_summary(predictions_df["Current Price"].iloc[-1])
    return final_summary

# Example Usage (Replace 'pred1' with actual DataFrame containing predictions)
# final_results = execute_trading_strategy(pred1)
# print(final_results)
