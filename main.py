import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_loader import DataLoader
from src.processing import DataProcessor
from src.plotting import Visualizer

def run_pipeline():
    START_DATE = "2005-01-01"
    
    # FEDFUNDS = Interest Rate
    # CPIAUCSL = Consumer Price Index (Inflation)
    MACRO_CODES = ['FEDFUNDS', 'CPIAUCSL'] 
    
    # XLK = Tech
    # XLE = Energy
    # XLU = Utilities
    # SPY = S&P 500 Benchmark
    SECTOR_TICKERS = ['XLK', 'XLE', 'XLU', 'SPY']

    print("--- Loading Data ---")
    loader = DataLoader()
    
    try:
        macro_raw = loader.fetch_macro_data(MACRO_CODES, START_DATE)
        sector_raw = loader.fetch_sector_data(SECTOR_TICKERS, START_DATE)
        
        if macro_raw.empty or sector_raw.empty:
            print("Failed to fetch data. Check your API keys and internet connection.")
            return

    except Exception as e:
        print(f"Pipeline crashed during loading: {e}")
        return

    print("\n--- Processing & Aligning ---")
    processor = DataProcessor()
    final_df = processor.process_data(macro_raw, sector_raw)
    
    print("Data aligned successfully!")
    print(final_df.head())

    # Save processed data to analyze in a Notebook later without re-running APIs
    final_df.to_csv("processed_data.csv")
    print(f"\nSaved processed data to 'processed_data.csv' ({len(final_df)} rows)")

    print("\n--- Generating Correlation Matrix ---")

    corr_matrix = final_df.corr()    
    if 'Inflation_YoY' in corr_matrix.columns:
        print("\nCorrelation with Inflation (YoY):")
        print(corr_matrix['Inflation_YoY'].sort_values(ascending=False))

    print("--- Visualizing Results ---")
    viz = Visualizer()
    viz.plot_inflation_regime(final_df, threshold=0.03)

    print("\nPipeline Complete. Check the 'output' folder for your chart!")
     
if __name__ == "__main__":
    run_pipeline()