import pandas as pd
import numpy as np

def analyze_investment_strategy(data, sell_threshold):
    # Convert the string data to DataFrame
    df = pd.read_csv(pd.StringIO(data))
    
    # Convert date to datetime and sort
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # Convert Change % to numeric
    df['Change %'] = df['Change %'].str.rstrip('%').astype(float)
    
    portfolio = {'cash': 0, 'shares': 0}
    transactions = []
    
    # Analyze each day
    for i in range(len(df)):
        current_day = df.iloc[i]
        price = current_day['Price']
        change = current_day['Change %']
        
        # Buy on negative days
        if change < 0:
            shares_bought = 300 / price
            portfolio['shares'] += shares_bought
            transactions.append({
                'date': current_day['Date'],
                'action': 'buy',
                'amount': 300,
                'shares': shares_bought
            })
        
        # Sell when previous day's gain exceeds threshold
        if i > 0 and df.iloc[i-1]['Change %'] > sell_threshold:
            shares_sold = min(1000 / price, portfolio['shares'])
            portfolio['shares'] -= shares_sold
            cash_obtained = shares_sold * price
            portfolio['cash'] += cash_obtained
            transactions.append({
                'date': current_day['Date'],
                'action': 'sell',
                'amount': cash_obtained,
                'shares': shares_sold
            })
    
    # Calculate final values
    final_price = df.iloc[-1]['Price']
    final_portfolio_value = (portfolio['shares'] * final_price) + portfolio['cash']
    total_investment = sum([t['amount'] for t in transactions if t['action'] == 'buy'])
    roi = ((final_portfolio_value - total_investment) / total_investment) * 100 if total_investment > 0 else 0
    
    return {
        'threshold': sell_threshold,
        'total_investment': total_investment,
        'final_value': final_portfolio_value,
        'roi': roi,
        'final_shares': portfolio['shares'],
        'cash_withdrawn': portfolio['cash'],
        'num_buys': len([t for t in transactions if t['action'] == 'buy']),
        'num_sells': len([t for t in transactions if t['action'] == 'sell'])
    }

# Test different thresholds
thresholds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
results = []

# Sample of the data (using the first few rows as example)
data = """Date,Price,Open,High,Low,Vol.,Change %
11/12/2024,364.58,364.51,365.18,362.37,213.56K,0.09%
11/11/2024,364.25,365.62,365.71,362.50,253.29K,-0.18%
[... rest of the data ...]"""

# Test each threshold
for threshold in thresholds:
    result = analyze_investment_strategy(data, threshold)
    results.append(result)

# Convert results to DataFrame for better visualization
results_df = pd.DataFrame(results)

# Sort by ROI to find optimal threshold
results_df = results_df.sort_values('roi', ascending=False)

# Print results
print("\nResults sorted by ROI (best to worst):")
print("\nThreshold  |  ROI     | Total Investment | Final Value  | # Buys | # Sells | Cash Withdrawn")
print("-" * 85)
for _, row in results_df.iterrows():
    print(f"{row['threshold']:8.1f}% | {row['roi']:7.2f}% | ${row['total_investment']:13,.2f} | ${row['final_value']:10,.2f} | {row['num_buys']:6d} | {row['num_sells']:7d} | ${row['cash_withdrawn']:11,.2f}")

# Get optimal threshold
optimal = results_df.iloc[0]
print(f"\nOptimal Selling Threshold: {optimal['threshold']}%")
print(f"Maximum ROI: {optimal['roi']:.2f}%")
print(f"At this threshold:")
print(f"- Number of buy transactions: {optimal['num_buys']}")
print(f"- Number of sell transactions: {optimal['num_sells']}")
print(f"- Total cash withdrawn: ${optimal['cash_withdrawn']:,.2f}")
print(f"- Final shares held: {optimal['final_shares']:.2f}")