import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    """
    Generates professional financial charts and regime analyses.
    """

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        sns.set_theme(style="whitegrid")

    def plot_inflation_regime(self, df: pd.DataFrame, threshold: float = 0.03):
        """
        Splits data into 'High' vs 'Low' inflation regimes and plots sector performance.
        Now dynamically handles any tickers present in the dataframe.
        """
        print(f"Generating Regime Analysis (Threshold: {threshold*100}% Inflation)...")

        plot_df = df.copy()
        plot_df['Regime'] = plot_df['Inflation_YoY'].apply(
            lambda x: 'High Inflation (>3%)' if x > threshold else 'Low/Normal Inflation (<3%)'
        )

        sector_cols = [col for col in plot_df.columns if col.endswith('_Ret')]
        
        if not sector_cols:
            print("Error: No sector return columns (ending in '_Ret') found in dataframe.")
            print("Columns available:", plot_df.columns.tolist())
            return

        target_cols = ['Regime'] + sector_cols
        melted_df = plot_df[target_cols].melt(
            id_vars='Regime', 
            var_name='Sector', 
            value_name='Monthly_Return'
        )

        plt.figure(figsize=(12, 6))
        
        ax = sns.barplot(
            data=melted_df, 
            x='Sector', 
            y='Monthly_Return', 
            hue='Regime', 
            palette={'High Inflation (>3%)': '#d62728', 'Low/Normal Inflation (<3%)': '#1f77b4'},
            errorbar=None 
        )
        ax.tick_params(axis='x', labelrotation=45)
        
        plt.title('Sector Performance: High vs. Low Inflation Regimes', fontsize=16, fontweight='bold')
        plt.ylabel('Avg Monthly Return', fontsize=12)
        plt.xlabel('Sector', fontsize=12)
        plt.axhline(0, color='black', linewidth=1)
        plt.legend(title='Economic Regime')

        output_path = f"{self.output_dir}/inflation_regime_analysis.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        print(f"Chart saved to: {output_path}")
        plt.close()