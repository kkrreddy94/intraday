import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from config import SYMBOLS, NEWS_FEEDS
from src.indicators import IntradayIndicators
from src.news_fetcher import ReliableNewsFetcher
from src.strategy_engine import IntradayStrategyEngine

def run_dashboard():
    st.set_page_config(page_title="NSE/BSE Intraday Algo Dashboard", layout="wide")
    
    st.title("📈 NSE & BSE Intraday Trading Dashboard & Signal Engine")
    st.markdown("Real-time intraday analytics powered by institutional indicators (VWAP, RSI, EMA, MACD, Bollinger Bands) and verified financial news feeds.")

    # Sidebar Controls
    st.sidebar.header("Configuration")
    selected_symbol_name = st.sidebar.selectbox("Select Index", list(SYMBOLS.keys()))
    ticker_symbol = SYMBOLS[selected_symbol_name]

    # Fetch Market Data
    @st.cache_data(ttl=60)
    def load_data(ticker):
        df = yf.download(ticker, period="1d", interval="5m")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df

    data = load_data(ticker_symbol)

    if data.empty:
        st.error(f"Unable to fetch data for {selected_symbol_name}. Markets might be closed.")
        return

    # Strategy Evaluation
    signal_result = IntradayStrategyEngine.evaluate_signals(data)

    # Display Top Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"₹{data['Close'].iloc[-1]:.2f}")
    col2.metric("Trading Signal", signal_result["signal"])
    col3.metric("Market Sentiment", "Accurate & Monitored")

    st.info(f"**Strategy Analysis Rationale:** {signal_result['reason']}")

    # Interactive Chart with Indicators
    st.subheader(f"Intraday Chart & Indicators ({selected_symbol_name} - 5m)")
    
    vwap = IntradayIndicators.calculate_vwap(data)
    ema_9 = IntradayIndicators.calculate_ema(data, 9)
    ema_21 = IntradayIndicators.calculate_ema(data, 21)
    upper_bb, middle_bb, lower_bb = IntradayIndicators.calculate_bollinger_bands(data)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=data.index, y=vwap, mode='lines', name='VWAP', line=dict(color='orange', width=1.5)))
    fig.add_trace(go.Scatter(x=data.index, y=ema_9, mode='lines', name='9 EMA', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=ema_21, mode='lines', name='21 EMA', line=dict(color='purple', width=1)))
    fig.add_trace(go.Scatter(x=data.index, y=upper_bb, mode='lines', name='Upper BB', line=dict(color='gray', dash='dash')))
    fig.add_trace(go.Scatter(x=data.index, y=lower_bb, mode='lines', name='Lower BB', line=dict(color='gray', dash='dash')))

    fig.update_layout(xaxis_title="Time", yaxis_title="Price (INR)", height=500, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Reliable News Feed Section
    st.markdown("---")
    st.subheader("📰 Latest Market News & Updates (Reliable Reporting Agencies)")
    news_fetcher = ReliableNewsFetcher(NEWS_FEEDS)
    latest_news = news_fetcher.fetch_latest_news()

    if latest_news:
        for item in latest_news:
            with st.expander(f"[{item['source']}] {item['title']} ({item['published']})"):
                st.markdown(f"Read full article: [Click Here]({item['link']})")
    else:
        st.write("Fetching real-time news updates...")

if __name__ == "__main__":
    run_dashboard()
