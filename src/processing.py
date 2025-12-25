import pandas as pd

class DataProcessor:
    """
    Handles cleaning, resampling, and merging of Economic and Market data.
    """

    # src/processing.py

import pandas as pd

class DataProcessor:
    """
    Handles cleaning, resampling, and merging of Economic and Market data.
    """

    def process_data(self, macro_df: pd.DataFrame, sector_df: pd.DataFrame) -> pd.DataFrame:
        """
        Merges macro data (Monthly) with sector data (Daily) by resampling sectors.
        """
        print("Processing data...")

        if isinstance(sector_df.columns, pd.MultiIndex):
            if 'Adj Close' in sector_df.columns.get_level_values(0):
                sector_df = sector_df['Adj Close']
            elif 'Close' in sector_df.columns.get_level_values(0):
                sector_df = sector_df['Close']
            else:
                sector_df = sector_df.xs(sector_df.columns.get_level_values(0)[0], axis=1, level=0)

        ticker_map = {
            'XLK': 'Technology',
            'XLE': 'Energy',
            'XLU': 'Utilities',
            'SPY': 'S&P 500'
        }
        sector_df = sector_df.rename(columns=ticker_map)

        # Resample Sector Data to Month-End
        sector_monthly = sector_df.resample('ME').last()

        # Calculate Monthly Returns (%)
        sector_returns = sector_monthly.pct_change()
        
        # Add suffix so the plotting script can find them
        sector_returns.columns = [f"{col}_Ret" for col in sector_returns.columns]

        # Process Macro Data
        if macro_df.index.tz is not None:
            macro_df.index = macro_df.index.tz_localize(None)

        macro_df.index = macro_df.index + pd.offsets.MonthEnd(0)

        # Feature Engineering
        processed_macro = pd.DataFrame()
        
        if 'CPIAUCSL' in macro_df.columns:
            processed_macro['Inflation_YoY'] = macro_df['CPIAUCSL'].pct_change(periods=12)
        
        if 'FEDFUNDS' in macro_df.columns:
            processed_macro['FedFunds_Level'] = macro_df['FEDFUNDS']
            processed_macro['FedFunds_Delta'] = macro_df['FEDFUNDS'].diff()

        # Merge Everything
        final_df = pd.concat([processed_macro, sector_returns], axis=1).dropna()

        return final_df

if __name__ == "__main__":
    print("Processor module ready.")