# Macro-Economic Impact on Sector Performance

### 📊 Project Overview
This project quantifies the relationship between Federal Reserve monetary policy (Interest Rates, Inflation) and the performance of key S&P 500 sectors (Technology, Energy, Utilities). 

Using a custom ETL pipeline, it processes 20+ years of economic data to identify **"Regime Shifts"**—specific economic environments where asset correlations break down. It includes a trading strategy backtest that rotates into Energy stocks during high-inflation regimes, significantly outperforming the S&P 500 during the 2022 inflationary spike.

### 🚀 Key Features
* **Automated ETL Pipeline:** Securely fetches data from **FRED (Federal Reserve)** and **Yahoo Finance** APIs.
* **Regime Analysis:** Classifies market environments into "High Inflation" vs. "Low Inflation" to visualize sector behavior changes.
* **Strategy Backtest:** Simulates a "Macro-Rotation" portfolio that switches between Growth and Commodities based on CPI prints.
* **Forecasting:** Uses a **SARIMA** model to forecast future Inflation (CPI) trends.

### 🛠️ Tech Stack
* **Python 3.10+**
* **Data Engineering:** `pandas`, `yfinance`, `fredapi`
* **Analysis & Viz:** `matplotlib`, `seaborn`, `statsmodels` (SARIMA)
* **Environment:** `python-dotenv` for secure API key management

### 📂 Repository Structure
```text
├── data/               # Processed data cached
├── notebooks/          # Jupyter Notebooks for interactive analysis & storytelling
├── output/             # Generated charts and reports
├── src/                # Modular source code
│   ├── data_loader.py  # API connections (FRED/Yahoo)
│   ├── processing.py   # Data cleaning & time-series alignment
│   └── plotting.py     # Visualization modules
├── main.py             # Orchestrator script to run the full pipeline
├── requirements.txt    # Project dependencies
└── README.md
```

### 📈 Key Insights

1.  **Tech is Regime-Dependent:** Technology stocks are not inherently rate-sensitive. The negative correlation with interest rates only becomes significant (<-0.6) during extreme stress events (2008 Financial Crisis, 2022 Inflation Spike). During stable bull markets, the correlation is often negligible.
    
2.  **Market Efficiency:** The S&P 500 prices in inflation data immediately. Lag analysis shows the strongest negative correlation occurs at **Lag 0** (the month of the data release), with the impact decaying significantly by months 3 and 6.
    
3.  **The Energy Hedge:** A dynamic rotation strategy that switches into **Energy (XLE)** when Inflation > 3% successfully protected capital during the 2022 crisis. However, the strategy underperforms during deflationary oil crashes (e.g., 2015), confirming it is a specialized hedge rather than an "All-Weather" solution.

### 💻 How to Run

1.  **Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/macro-sector-analysis.git](https://github.com/YOUR_USERNAME/macro-sector-analysis.git)
cd macro-sector-analysis
```

2.  **Install Dependencies**
```bash
pip install -r requirements.txt
```

3.  **Set Up API Keys**  This project requires a free API Key from [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/docs/api/api_key.html). Create a file named .env in the root directory and add your key:
```bash
FRED_API_KEY=your_actual_api_key_here
```

4.  **Run the Pipeline**  To execute the ETL process and generate the summary charts:
```bash
python main.py
```

5.  **Explore the Analysis**  Open the Jupyter Notebook for the deep-dive analysis, lag correlations, and SARIMA forecasting:
```bash
jupyter notebook notebooks/analysis.ipynb
```
### Next Step
Once you save this file, you are ready to initialize git and push your project!

```bash
git init
git add .
git commit -m "Initial commit: Macro-Economic Sector Analysis Pipeline"