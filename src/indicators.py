import pandas as pd
import numpy as np

class IntradayIndicators:
    """
    Implements technical indicators for intraday trading based on institutional standards.
    References: VWAP, RSI, EMA, MACD, Bollinger Bands.
    """
    
    @staticmethod
    def calculate_vwap(df: pd.DataFrame) -> pd.Series:
        """VWAP tracks average price weighted by volume, resetting daily."""
        typical_price = (df['High'] + df['Low'] + df['Close']) / 2
        return (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()

    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """RSI measures momentum on a scale of 0 to 100."""
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_ema(df: pd.DataFrame, span: int = 9) -> pd.Series:
        """Exponential Moving Average gives higher weight to recent price data."""
        return df['Close'].ewm(span=span, adjust=False).mean()

    @staticmethod
    def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9):
        """MACD measures momentum shifts using moving average convergence divergence."""
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: int = 2):
        """Bollinger Bands measure volatility using moving averages and standard deviation."""
        middle_band = df['Close'].rolling(window=period).mean()
        std = df['Close'].rolling(window=period).std()
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)
        return upper_band, middle_band, lower_band
