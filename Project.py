# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:39:59 2024

@author: Colby Jaskowiak
"""

#Project FM

import pandas as pd
import yfinance as yf

import plotly.graph_objects as go
import streamlit as st
import plotly.express as px

import requests
#%%

tickers = ['XOM', 'CVX', 'NEE', 'DUK', 'RSG', 'CLH', 'VEOEY', 'WCN']
start_date = '2014-11-01'
end_date = '2024-11-01'
stock_price_data = yf.download(tickers, start=start_date, end=end_date).dropna()
sp500_data = yf.download('^GSPC', start=start_date, end=end_date).dropna()
energy_sector_data = yf.download('XLE', start=start_date, end=end_date).dropna()
print(stock_price_data.head())

api_key = 'HA3CDG8kslZcE0QlmBeldiDQEqkRsIpI'
#%%
def fetch_financial_ratios(ticker):
    url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?limit=20&apikey={api_key}"
    response = requests.get(url)
    ratios = response.json()
    
    if isinstance(ratios, list) and len(ratios) > 0:
        return pd.DataFrame([{
            'Company': ticker,
            'Quarter': entry['date'],
            'P/E Ratio': entry.get('priceEarningsRatio', None),
            'D/E Ratio': entry.get('debtEquityRatio', None),
            'Current Ratio': entry.get('currentRatio', None),
            'Price-to-Sales Ratio': entry.get('priceToSalesRatio', None),
            'Price-to-Book (PB) Ratio': entry.get('priceToBookRatio', None),
            'Receivables Turnover': entry.get('receivablesTurnover', None),
            'Quick Ratio': entry.get('quickRatio', None),
            'Cash Ratio': entry.get('cashRatio', None),
            'Return on Assets (ROA)': entry.get('returnOnAssets', None),
            'Return on Equity (ROE)': entry.get('returnOnEquity', None),
            'Return on Capital Employed (ROCE)': entry.get('returnOnCapitalEmployed', None),
            'Long-Term Debt to Capitalization': entry.get('longTermDebtToCapitalization', None),
            'Total Debt to Capitalization': entry.get('totalDebtToCapitalization', None),
            'Fixed Asset Turnover': entry.get('fixedAssetTurnover', None),
            'Operating Cash Flow Sales Ratio': entry.get('operatingCashFlowSalesRatio', None),
            'Capital Expenditure Coverage Ratio': entry.get('capitalExpenditureCoverageRatio', None),
            'Operating Cycle': entry.get('operatingCycle', None),
            'Cash Conversion Cycle (CCC)': entry.get('cashConversionCycle', None),
            'Operating Profit Margin': entry.get('operatingProfitMargin', None),
            'Pretax Profit Margin': entry.get('pretaxProfitMargin', None),
            'Net Profit Margin': entry.get('netProfitMargin', None),
            'Effective Tax Rate': entry.get('effectiveTaxRate', None),
            'EBITperRevenue': entry.get('ebitPerRevenue', None),
            'Debt Ratio': entry.get('debtRatio', None),
            'Cash Flow to Debt Ratio': entry.get('cashFlowToDebtRatio', None),
            'Asset Turnover': entry.get('assetTurnover', None),
            'Inventory Turnover': entry.get('inventoryTurnover', None)            
            } for entry in ratios])
    else:
        return pd.DataFrame()

#%%

df_1 = fetch_financial_ratios('XOM')
df_2 = fetch_financial_ratios('CVX')
df_3 = fetch_financial_ratios('NEE')
df_4 = fetch_financial_ratios('DUK')
df_5 = fetch_financial_ratios('RSG')
df_6 = fetch_financial_ratios('CLH')
df_7 = fetch_financial_ratios('VEOEY')
df_8 = fetch_financial_ratios('WCN')

#%%
st.title("Environmental Sector Financial & M&A Analytics Dashboard")
st.write("Comprehensive Valuation and Industry Analysis")
st.write("Analyze financial data interactively.")

dfs = []

for ticker in tickers:
    df = fetch_financial_ratios(ticker)
    if not df.empty:
        dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)
final_df
#%%

selected_company = st.sidebar.selectbox("Select a Company", options=final_df["Company"].unique())
selected_metric = st.sidebar.selectbox("Select a Metric", options=[
    "P/E Ratio", "D/E Ratio", "Current Ratio", "Return on Assets (ROA)", "Return on Equity (ROE)",
    "Operating Profit Margin", "Net Profit Margin", "Cash Conversion Cycle (CCC)", "Asset Turnover"
])

company_data = final_df[final_df["Company"] == selected_company]

metric_data = company_data[["Quarter", selected_metric]]

metric_data = metric_data.copy()

metric_data["Quarter"] = pd.to_datetime(metric_data["Quarter"])

metric_data = metric_data.sort_values(by="Quarter")

st.header(f"{selected_company} - {selected_metric} Over Time")

st.line_chart(metric_data.set_index("Quarter")[selected_metric])

st.write("Raw Data:", metric_data)

#%%
st.header("Stock Price Trend")

selected_stock = st.selectbox("Select a stock:", options=tickers, key="stock_selectbox")

adj_close_data = stock_price_data["Adj Close"][selected_stock]

fig = px.line(adj_close_data, x=adj_close_data.index, y=adj_close_data, 
              labels={'x': 'Date', 'y': 'Price (USD)'}, 
              title=f"Stock Price Trend for {selected_stock}")

st.plotly_chart(fig)

#%%
st.header("Raw Data Table")
st.dataframe(data=stock_price_data)  # Placeholder for your dataframe

st.write("Data Source: [Yahoo Finance](https://www.yahoo.com/)")

#%%

#automatic stock analysis
#normalized growth rate model for inflation/other metrics with forecast
#forecasting dashboard that includes the various strategic perspectives, competitive advantage, financial forecasts, etc.

#polars
#streamlit

#cd C:\Users\Colby Jaskowiak\FM HW

#%%
#DCF model
api_key = 'HA3CDG8kslZcE0QlmBeldiDQEqkRsIpI'

ticker = 'RSG'
url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?limit=10&apikey={api_key}"
response = requests.get(url)
cash_flows = response.json()
#%%
st.title("Discounted Cash Flow (DCF) Valuation")
st.markdown(f"**Company:** {ticker}")
st.markdown("---")

st.header("Step 1: Free Cash Flows (FCFs)")

fcf_data = []

for entry in cash_flows[:5]:
    fcf_data.append({
        'date': entry['date'],
        'FCF': entry['freeCashFlow']
        })
df_fcf = pd.DataFrame(fcf_data)

st.table(df_fcf)

#%%

st.header("Step 2: Estimate Growth Rate")
df_fcf = df_fcf.sort_values(by = 'date')
df_fcf['FCF Growth'] = df_fcf['FCF'].pct_change()

growth_rate = df_fcf['FCF Growth'].mean()

st.write(f"Estimated Growth Rate: {growth_rate:.2%}")
#%%
st.header("Step 3: Project Future FCFs")
years = 5
projected_fcf = []

last_fcf = df_fcf.iloc[0]['FCF']
for i in range(1,years + 1):
    projected_fcf.append(last_fcf * (1 + growth_rate) **i)

df_projected_fcf = pd.DataFrame({
    'Year': [f"Year {i}" for i in range(1, years + 1)],
    'Projected FCF': projected_fcf
})
st.table(df_projected_fcf)

#%%
st.header("Step 4: Compute Terminal Value")
terminal_growth_rate = .06 #6% growth rate
terminal_value = projected_fcf[-1]*(1+terminal_growth_rate)/(.08 - terminal_growth_rate)

st.write(f"Terminal Value: ${terminal_value:,.2f}")
#%%
st.header("Step 5: Discount Future FCFs")
wacc = .07
discounted_fcf = [cf / (1+wacc)**i for i, cf in enumerate(projected_fcf, start = 1)]
discounted_terminal_value = terminal_value / (1 + wacc) ** years

df_discounted_fcf = pd.DataFrame({
    'Year': [f"Year {i}" for i in range(1, years + 1)] + ['Terminal Value'],
    'Discounted FCF': discounted_fcf + [discounted_terminal_value]
})
st.table(df_discounted_fcf)

#%%
enterprise_value = sum(discounted_fcf) + discounted_terminal_value

st.write(f"Enterprise Value: ${enterprise_value:,.2f}")

#%%
st.header("Step 6: Get Net Debt")

balance_sheet_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=1&apikey={api_key}"
balance_sheet_response = requests.get(balance_sheet_url)
balance_sheet = balance_sheet_response.json()[0]

net_debt = balance_sheet['totalDebt'] - balance_sheet['cashAndCashEquivalents']

st.write(f"Net Debt: ${net_debt:,.2f}")

#%%
st.header("Step 7: Compute Price per Share")

equity_value = enterprise_value - net_debt
shares_outstanding = 314000000

price_per_share = equity_value / shares_outstanding
st.write(f"Price per Share: ${price_per_share:,.2f}")

#%%
st.markdown("---")
st.subheader("Final Results")
st.write(f"**Projected FCFs:** {', '.join(f'${cf:,.2f}' for cf in projected_fcf)}")
st.write(f"**Discounted FCFs:** {', '.join(f'${cf:,.2f}' for cf in discounted_fcf)}")
st.write(f"**Discounted Terminal Value:** ${discounted_terminal_value:,.2f}")
st.write(f"**Enterprise Value:** ${enterprise_value:,.2f}")
st.write(f"**Net Debt:** ${net_debt:,.2f}")
st.write(f"**Price per Share:** ${price_per_share:,.2f}")

#%%
recommendations = {
    'Buy': 12,
    'Hold': 5,
    'Sell': 2
}

fig = go.Figure(data=[
    go.Bar(name='Buy', x=list(recommendations.keys()), y=[recommendations['Buy']]),
    go.Bar(name='Hold', x=list(recommendations.keys()), y=[recommendations['Hold']]),
    go.Bar(name='Sell', x=list(recommendations.keys()), y=[recommendations['Sell']])
])

fig.update_layout(
    title="Analyst Recommendations",
    xaxis_title="Recommendation",
    yaxis_title="Number of Analysts",
    barmode='group'
)

st.plotly_chart(fig)

st.write("Data Source: [Yahoo Finance](https://www.yahoo.com/)")
#%%
# Print the results
#print(f"Projected FCFs: {projected_fcf}")
#print(f"Discounted FCFs: {discounted_fcf}")
#print(f"Terminal Value: {terminal_value}")
#print(f"Discounted Terminal Value: {discounted_terminal_value}")
#print(f"Enterprise Value: {enterprise_value}")
#print(f"Price per share: {price_per_share}")

#%%
#cd C:\Users\Colby Jaskowiak\FM HW

#%%

mna_data = [
    {
        "Acquirer": "WM (Waste Management)",
        "Target": "Stericycle",
        "Deal Value (USD)": 7.2e9,
        "Year": 2024,
        "Details": "Enhanced regulated waste and compliance solutions."
    },
    {
        "Acquirer": "Republic Services",
        "Target": "US Ecology",
        "Deal Value (USD)": 2.2e9,
        "Year": 2022,
        "Details": "Expanded hazardous waste management capabilities."
    },
    {
        "Acquirer": "Casella Waste Systems",
        "Target": "Various (e.g., Whitetail Disposal, Royal Carting)",
        "Deal Value (USD)": 200e6,  # Approximation for multiple deals
        "Year": 2024,
        "Details": "Strengthened regional operations through tuck-in acquisitions."
    }
]
#%%
mna_df = pd.DataFrame(mna_data)

st.title("Environmental and Waste Management Mergers & Acquisitions")
st.write("Below are some notable M&A activities in the sector:")
#%%
st.dataframe(mna_df)

st.subheader("M&A Deal Value Comparison")
st.bar_chart(mna_df.set_index("Acquirer")["Deal Value (USD)"])

st.write("Data Source: [Yahoo Finance](https://www.yahoo.com/)")

#%%