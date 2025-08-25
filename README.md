# Canadian Financial Markets Forecasting

This repository contains code and documentation for forecasting key Canadian financial metrics—CAD/USD exchange rate, benchmark interest rates, and the TSX Composite Index—using open data sources and modern time‑series techniques.

## Project Overview

- **Objective:** Provide accurate short‑term forecasts of FX rates, interest rates, and stock market trends to support currency hedging, interest rate management, and investment decisions.
- **Data Sources:** Bank of Canada Valet API (FX and interest rates) and freely accessible TSX index data via yfinance.
- **Tech Stack:** Python 3.9/3.10, Pandas, Prophet, Matplotlib/Seaborn, scikit‑learn. Forecasting is done primarily with Prophet, with ARIMA as an optional benchmark.
- **Deliverables:** Data collection scripts, exploratory data analysis, forecasting models, and an interactive Power BI dashboard.

## Installation

1. Clone this repository and navigate into it.
2. Create a virtual environment (Python 3.9 or 3.10 is recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Obtain an Alpha Vantage API key (for TSX data) or use the included yfinance script for free index data. Set your API key as an environment variable if using Alpha Vantage.

## Usage

1. **Fetch Data:**

   ```bash
   python data_fetch.py
   ```

   This script downloads daily CAD/USD rates, interest rates, and TSX index prices and saves them as CSV files in the project root.

2. **Explore Data:**

   ```bash
   python eda.py
   ```

   Generates summary statistics, stationarity tests, and time‑series plots. Output PNG files are saved in the project directory.

3. **Forecast:**

   ```bash
   python forecast_models.py
   ```

   Fits Prophet models to each series, evaluates performance on a recent test set, and produces 30‑day forecasts. Forecast results are saved as CSV files (e.g., `cadusd_forecast.csv`).

## Repository Structure

- `data_fetch.py` – Fetches raw data from APIs.
- `eda.py` – Exploratory analysis and stationarity checks.
- `forecast_models.py` – Builds and evaluates Prophet forecasting models.
- `requirements.txt` – Python dependencies.
- `README.md` – Project documentation.

## Notes

- Ensure your machine has internet access to call the Bank of Canada Valet API and to download TSX data.
- Prophet may issue warnings about deprecations; these can typically be ignored.
- The Power BI dashboard is hosted separately and can be linked here once published.
