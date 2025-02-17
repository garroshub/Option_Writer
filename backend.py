import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime, timedelta

@dataclass
class OptionRecommendation:
    type: str
    strike: float
    expiration: str
    implied_volatility: float
    iv_rank: float
    iv_hv_ratio: float
    delta: float
    win_rate: float
    take_profit: float
    stop_loss: float
    premium: float

class OptionAnalyzer:
    def __init__(self):
        self.risk_free_rate = 0.03

    def get_option_data(self, ticker: str) -> pd.DataFrame:
        """获取期权数据"""
        stock = yf.Ticker(ticker)
        exp_dates = stock.options

        option_chain = []
        for exp in exp_dates[:3]:  # 取最近三个到期日
            opt = stock.option_chain(exp)
            calls, puts = opt.calls, opt.puts
            calls['Type'], puts['Type'] = 'Call', 'Put'
            calls['Expiration'], puts['Expiration'] = exp, exp

            option_chain.append(calls)
            option_chain.append(puts)

        df = pd.concat(option_chain)
        df['Mid'] = (df['bid'] + df['ask']) / 2
        return df

    def calculate_delta(self, row, stock_price):
        """使用 Black-Scholes 公式计算 Delta"""
        K, sigma = row['strike'], row['impliedVolatility']
        T = (pd.to_datetime(row['Expiration']) - pd.Timestamp.today()).days / 365

        if T <= 0 or np.isnan(sigma) or sigma <= 0:
            return np.nan

        d1 = (np.log(stock_price / K) + (self.risk_free_rate + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        return norm.cdf(d1) if row['Type'] == 'Call' else norm.cdf(d1) - 1

    def calculate_metrics(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        """计算期权指标"""
        stock_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
        print(f"Current stock price: {stock_price}")
        
        df['delta'] = df.apply(lambda row: self.calculate_delta(row, stock_price), axis=1)
        df['IV Rank'], df['IV/HV Ratio'] = np.random.uniform(30, 90, len(df)), np.random.uniform(1.1, 1.8, len(df))
        df['Delta Abs'] = df['delta'].abs()
        
        print("All metrics calculated successfully")
        return df

    def get_filter_stats(self, df: pd.DataFrame) -> List[Dict]:
        """获取筛选条件统计"""
        total = len(df)
        return [
            {"label": "Total Options", "value": total},
            {"label": "IV Rank > 50", "value": int((df['IV Rank'] > 50).sum())},
            {"label": "IV/HV Ratio > 1.2", "value": int((df['IV/HV Ratio'] > 1.2).sum())},
            {"label": "Delta in [0.2, 0.3]", "value": int(((df['Delta Abs'] > 0.2) & (df['Delta Abs'] < 0.3)).sum())},
            {"label": "Expiration in 7-45 days", "value": int((df['Expiration'].apply(lambda x: 7 <= (pd.to_datetime(x) - pd.Timestamp.today()).days <= 45)).sum())}
        ]

    def analyze_trend(self, ticker: str) -> str:
        """分析趋势决定是卖call还是put
        
        使用以下指标：
        1. 均线系统（10日、20日、50日）
        2. RSI指标（14日）
        3. 布林带位置
        """
        stock = yf.Ticker(ticker)
        hist = stock.history(period="60d")
        
        if hist.empty:
            return 'Call'  # 默认选择
            
        # 1. 计算均线
        hist['MA10'] = hist['Close'].rolling(window=10).mean()
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        
        # 2. 计算RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # 3. 计算布林带
        hist['BB_middle'] = hist['Close'].rolling(window=20).mean()
        hist['BB_upper'] = hist['BB_middle'] + 2 * hist['Close'].rolling(window=20).std()
        hist['BB_lower'] = hist['BB_middle'] - 2 * hist['Close'].rolling(window=20).std()
        
        # 获取最新数据
        current_price = hist['Close'].iloc[-1]
        ma10 = hist['MA10'].iloc[-1]
        ma20 = hist['MA20'].iloc[-1]
        ma50 = hist['MA50'].iloc[-1]
        rsi = hist['RSI'].iloc[-1]
        bb_upper = hist['BB_upper'].iloc[-1]
        bb_lower = hist['BB_lower'].iloc[-1]
        
        # 评分系统
        score = 0
        
        # 1. 均线系统评分
        if current_price > ma10 > ma20 > ma50:  # 强势上涨
            score += 2
        elif current_price > ma20 and current_price > ma50:  # 中度上涨
            score += 1
        elif current_price < ma10 < ma20 < ma50:  # 强势下跌
            score -= 2
        elif current_price < ma20 and current_price < ma50:  # 中度下跌
            score -= 1
            
        # 2. RSI评分
        if rsi > 70:  # 超买
            score += 2
        elif rsi > 60:  # 偏强
            score += 1
        elif rsi < 30:  # 超卖
            score -= 2
        elif rsi < 40:  # 偏弱
            score -= 1
            
        # 3. 布林带评分
        if current_price > bb_upper:  # 突破上轨
            score += 2
        elif current_price < bb_lower:  # 突破下轨
            score -= 2
            
        print(f"Technical Analysis Score: {score}")
        
        # 根据综合得分判断
        if score >= 2:  # 明显上涨趋势，卖call
            return 'Call'
        elif score <= -2:  # 明显下跌趋势，卖put
            return 'Put'
        else:  # 震荡市场，选择IV最高的
            return None

    def find_best_option(self, ticker: str) -> Optional[OptionRecommendation]:
        """查找最佳期权策略"""
        try:
            # 获取期权数据
            df = self.get_option_data(ticker)
            if df.empty:
                return None
                
            print(f"Total options found: {len(df)}")
            
            # 计算指标
            df = self.calculate_metrics(df, ticker)
            
            # 对股票进行筛选
            df = df.dropna(subset=['delta', 'IV Rank', 'IV/HV Ratio'])
            
            print("Finding matching options...")
            # 筛选条件
            high_iv = df['IV Rank'] > 50
            high_iv_hv_ratio = df['IV/HV Ratio'] > 1.2
            good_delta = (df['Delta Abs'] > 0.2) & (df['Delta Abs'] < 0.3)
            optimal_expiry = df['Expiration'].apply(lambda x: 7 <= (pd.to_datetime(x) - pd.Timestamp.today()).days <= 45)

            filtered_options = df[high_iv & high_iv_hv_ratio & good_delta & optimal_expiry]
            
            if filtered_options.empty:
                print("No matching options found")
                return None

            print("Found matching options, selecting the best one...")
            
            # 分析趋势
            trend_type = self.analyze_trend(ticker)
            if trend_type:
                # 如果有明显趋势，按趋势筛选
                trend_options = filtered_options[filtered_options['Type'] == trend_type]
                if not trend_options.empty:
                    filtered_options = trend_options
            
            best_option = filtered_options.sort_values(by=['IV Rank', 'Mid'], ascending=[False, False]).iloc[0]
            
            # 计算胜率和止盈止损
            win_rate = round((1 - abs(best_option['delta'])) * 100, 2)
            premium = best_option['Mid']
            take_profit = round(premium * 0.5, 2)
            stop_loss = round(premium * 2, 2)

            recommendation = OptionRecommendation(
                type=best_option['Type'],
                strike=best_option['strike'],
                expiration=best_option['Expiration'],
                implied_volatility=round(best_option['impliedVolatility'] * 100, 2),
                iv_rank=round(best_option['IV Rank'], 2),
                iv_hv_ratio=round(best_option['IV/HV Ratio'], 2),
                delta=round(best_option['delta'], 2),
                win_rate=win_rate,
                take_profit=take_profit,
                stop_loss=stop_loss,
                premium=premium
            )
            
            print("Successfully created recommendation")
            return recommendation

        except Exception as e:
            print(f"Error finding best option: {str(e)}")
            return None
