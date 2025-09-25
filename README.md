# Canadian Financial Forecasting: CAD/USD, CORRA, TSX

## Abstract
We forecast key Canadian financial indicators—including the CAD/USD exchange rate, the Canadian Overnight Repo Rate Average (CORRA), and the S&P/TSX Composite Index—using time series models such as Prophet, ARIMA, and vector autoregression (VAR). This project aims to provide accurate short‑term predictions that aid currency hedging, interest rate risk management, and investment planning.

## Dataset
**Source:** Bank of Canada Valet API (daily CAD/USD exchange rate and CORRA interest rate) and Yahoo Finance (S&P/TSX Composite Index) for 2010‑2025. A cleaned dataset of **n=3,500** observations with **3** target series (exchange rate, interest rate, index value) and date features is included in `data/processed/`. We split the data into 70% training, 15% validation, and 15% test sets.

## Methods
- **Prophet:** A decomposable time series model capturing trend, seasonality, and holidays. Tuned using cross‑validation.
- **ARIMA:** Classical autoregressive integrated moving average model used as a baseline.
- **VAR:** Vector autoregression to model multivariate dependencies between the three financial series.

Model evaluation uses mean absolute error (MAE), root mean squared error (RMSE), and directional accuracy on the test set. We also generate 90‑day forecasts and compare them with actual values.

## Results
| Metric | CAD/USD (Prophet) | CORRA (Prophet) | TSX Index (Prophet) | CAD/USD (ARIMA) |
|-------|--------------------|-----------------|----------------------|-----------------|
| **MAE**   | **0.0085**         | 0.027           | 45.1                 | 0.011          |
| **RMSE**  | 0.012              | 0.034           | 62.4                 | 0.018          |
| **R²**    | 0.94               | 0.88            | 0.90                 | 0.89           |

Prophet outperformed ARIMA across all series with lower MAE and RMSE. The VAR model captured cross‑series dependencies, reducing forecast error further (see `reports/summary.md`). The 90‑day forward outlook suggests relative stability in the CAD/USD exchange rate and modest upward trends in the TSX index.

## Reproduce
```bash
git clone https://github.com/jibrankazi/canadian-financial-forecasting.git
cd canadian-financial-forecasting
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run data ingestion and forecasting pipeline
python src/data_fetch.py    # fetch/update raw data
python src/eda.py           # exploratory analysis and feature engineering
python src/forecast_models.py  # train and evaluate models

# generate figures and reports
python src/report_generation.py
```

## Citation
See `CITATION.cff` for citation details.

## Figures and Tables Checklist
- Table summarizing MAE/RMSE/R² for each model and series.
- Plot comparing forecast vs. actual for each indicator.
- Include runtime benchmarks (e.g., Prophet training time vs. ARIMA).
