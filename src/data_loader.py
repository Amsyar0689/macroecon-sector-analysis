import os
import pandas as pd
import yfinance as yf
from fredapi import Fred
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DataLoader:
    """
    A robust data fetcher for the Macro-Sector Analysis project.
    Connects to Federal Reserve (FRED) and Yahoo Finance APIs.
    """

    def __init__(self):
        self.fred_api_key = os.getenv("FRED_API_KEY")
        
        if not self.fred_api_key:
            raise ValueError("FRED_API_KEY not found. Please check your .env file.")
        
        self.fred = Fred(api_key=self.fred_api_key)

    def fetch_macro_data(self, series_ids: list, start_date: str) -> pd.DataFrame:
        """
        Fetches economic indicators from FRED.
        
        Args:
            series_ids (list): List of FRED codes (e.g., ['FEDFUNDS', 'CPIAUCSL']).
            start_date (str): Start date in 'YYYY-MM-DD' format.
            
        Returns:
            pd.DataFrame: Merged dataframe of economic indicators.
        """
        print(f"Fetching macro data for: {series_ids}...")
        data_frames = []
        
        for series in series_ids:
            try:
                series_data = self.fred.get_series(series, observation_start=start_date)
                df = series_data.to_frame(name=series)
                data_frames.append(df)
            except Exception as e:
                print(f"Error fetching {series}: {e}")

        if not data_frames:
            return pd.DataFrame()

        macro_df = pd.concat(data_frames, axis=1)
        macro_df.index.name = 'Date'
        return macro_df

    def fetch_sector_data(self, tickers: list, start_date: str) -> pd.DataFrame:
        """
        Fetches historical price data (Adj Close) for Sector ETFs via Yahoo Finance.
        
        Args:
            tickers (list): List of ticker symbols (e.g., ['XLK', 'XLE']).
            start_date (str): Start date in 'YYYY-MM-DD' format.
            
        Returns:
            pd.DataFrame: DataFrame containing Adjusted Close prices.
        """
        print(f"Fetching sector data for: {tickers}...")
        
        try:
            data = yf.download(tickers, start=start_date, progress=False, threads=False)
            
            if 'Adj Close' in data:
                return data['Adj Close']
            else:
                return data
        
        except Exception as e:
            print(f"Error fetching sector data: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    loader = DataLoader()
    
    START_DATE = "2010-01-01"
    MACRO_CODES = ['FEDFUNDS', 'CPIAUCSL'] # Interest Rates, CPI
    SECTOR_TICKERS = ['XLK', 'XLE', 'XLU', 'SPY'] # Tech, Energy, Utilities, S&P500

    macro_df = loader.fetch_macro_data(MACRO_CODES, start_date=START_DATE)
    sector_df = loader.fetch_sector_data(SECTOR_TICKERS, start_date=START_DATE)

    print("\n--- Macro Data Head ---")
    print(macro_df.head())
    
    print("\n--- Sector Data Head ---")
    print(sector_df.head())