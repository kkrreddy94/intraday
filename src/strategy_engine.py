import pandas as pd
from src.indicators import IntradayIndicators

class IntradayStrategyEngine:
    """
    Combines indicator signals based on institutional guidelines:
    - Trend + Momentum: VWAP + RSI
    - Trend + Confirmation: EMA + MACD
    """
    
    @staticmethod
    def evaluate_signals(df: pd.DataFrame) -> dict:
        if df.empty or len(df) < 26:
            return {"signal": "NEUTRAL", "reason": "Insufficient data"}

        # Calculate indicators
        vwap = IntradayIndicators.calculate_vwap(df)
        rsi = IntradayIndicators.calculate_rsi(df)
        ema_9 = IntradayIndicators.calculate_ema(df, 9)
        ema_21 = IntradayIndicators.calculate_ema(df, 21)
        macd, signal_line, _ = IntradayIndicators.calculate_macd(df)

        latest_close = df['Close'].iloc[-1]
        latest_vwap = vwap.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        latest_ema9 = ema_9.iloc[-1]
        latest_ema21 = ema_21.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = signal_line.iloc[-1]

        # Strategy Logic: VWAP + RSI setup (Trend + Momentum)
        bullish_vwap_rsi = (latest_close > latest_vwap) and (latest_rsi > 50)
        bearish_vwap_rsi = (latest_close < latest_vwap) and (latest_rsi < 50)

        # Strategy Logic: EMA Crossover + MACD Confirmation (Trend + Confirmation)
        bullish_ema_macd = (latest_ema9 > latest_ema21) and (latest_macd > latest_signal)
        bearish_ema_macd = (latest_ema9 < latest_ema21) and (latest_macd < latest_signal)

        if bullish_vwap_rsi and bullish_ema_macd:
            return {
                "signal": "STRONG BUY",
                "reason": "Price above VWAP, RSI > 50, 9 EMA > 21 EMA, and bullish MACD crossover."
            }
        elif bearish_vwap_rsi and bearish_ema_macd:
            return {
                "signal": "STRONG SELL",
                "reason": "Price below VWAP, RSI < 50, 9 EMA < 21 EMA, and bearish MACD crossover."
            }
        
        return {
            "signal": "NEUTRAL / HOLD",
            "reason": "Conflicting signals or sideways market conditions."
        }
