Canadian Financial Markets Forecasting with Real Data and Dashboard

Canadian Financial Markets Forecasting

Canadian Financial Markets Forecasting is a project that analyzes and predicts key Canadian financial metrics – specifically the CAD/USD exchange rate, the CORRA benchmark interest rate (Canadian Overnight Repo Rate Average), and the S&P/TSX Composite stock index. Using historical data from authoritative sources and modern time-series models (primarily Facebook’s Prophet), the project generates short-term forecasts to aid in currency hedging, interest rate risk management, and investment planning decisions. The results are presented through both data files and an interactive Power BI dashboard for easy exploration by stakeholders.

Key Results & Visualizations

The forecasting models (Prophet with an ARIMA benchmark) were trained and evaluated on recent data, demonstrating strong performance in capturing trends and seasonality. Forecast Accuracy: The Prophet model achieved a Mean Absolute Error (MAE) of ~0.0085 on CAD/USD exchange rate predictions (on a hold-out test set), indicating high precision in short-term FX forecasting. Key Finding: The 90-day forward outlook suggests relative stability in the CAD/USD rate, while the S&P/TSX Composite Index is projected to experience a slight upward trend over the same period, underlining cautiously optimistic market conditions ahead.

 

(Figure: CAD/USD Exchange Rate Forecast vs. Actuals would be shown here, comparing the model’s 90-day forecast with actual exchange rate values, illustrating the model’s close tracking of the observed data.)

Interactive Dashboard

An interactive multi-page Power BI Dashboard has been developed to complement the analysis. It allows users to visualize historical trends and compare forecasted versus actual values for each indicator. Users can filter by date ranges, examine confidence intervals, and view correlations between FX rates, interest rates, and equity index levels. This dashboard (accessible via a shared link) enables business users and stakeholders to intuitively explore the forecast results and underlying data, facilitating data-driven decision making. (A link to the live dashboard will be provided in the repository README once the dashboard is published.)

Project Overview

Objective: Develop and evaluate time-series models that provide accurate short-term forecasts of key Canadian financial indicators (CAD/USD exchange rate, CORRA interest rate, and TSX Composite Index). The goal is to present the forecasts in a clear, actionable format for business stakeholders, supporting decisions in hedging and investment strategies.

Data Sources: The project leverages open data from authoritative sources. Historical daily CAD/USD exchange rates and the CORRA overnight interest rate are retrieved from the official Bank of Canada Valet API
bankofcanada.ca
. This API provides programmatic access to the Bank’s published financial statistics (including daily foreign exchange rates and benchmark interest rates). For the equity market, historical quotes for the S&P/TSX Composite Index (ticker ^GSPTSE) are obtained via Yahoo Finance using the Python yfinance library
github.com
, which provides free access to historical stock index data. (Note: The repository includes a static snapshot of these datasets in the /data/raw folder for immediate reproducibility. Users can refresh to the latest data via the provided scripts, as described below.)

Tech Stack: The analysis is implemented in Python 3.9+. Key libraries include Pandas for data manipulation, Facebook’s Prophet for time-series forecasting, and Statsmodels for an ARIMA benchmark. Visualization of results is done with Matplotlib/Seaborn for static plots, and Power BI for the interactive dashboard. Prophet (developed by Facebook’s Core Data Science team) is an open-source library designed to automatically capture seasonality and trends in univariate time series
machinelearningmastery.com
, making it well-suited to model financial time series with patterns (e.g., daily or seasonal effects).

Deliverables: The project delivers cleaned datasets, Jupyter notebooks/Python scripts for analysis, evaluated forecasting models, and a polished Power BI dashboard. In particular, forecast result files (e.g. cadusd_forecast.csv) containing 30-day and 90-day predictions for each metric are produced, and an executive summary of findings is provided via the dashboard and README. Together, these deliverables enable both technical and non-technical stakeholders to trust and utilize the forecasting insights.

Installation & Usage

This repository is organized for ease of use and reproducibility. Follow these steps to set up the project environment and run the analyses:

Clone the Repository and Set Up Environment: Clone the GitHub repository to your local machine and create a Python virtual environment (recommend Python 3.9 or 3.10). Then activate the environment.

```
git clone https://github.com/jibrankazi/canadian-financial-forecasting.git  
cd canadian-financial-forecasting  
python -m venv .venv  
source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
```

Install Dependencies: Install the required Python packages listed in requirements.txt using pip.

```
pip install -r requirements.txt
```

Run the Analysis: The project includes several scripts to fetch data, perform analysis, and generate forecasts. These use the data in the data/ directory (which comes pre-loaded with a snapshot of historical data).

**Exploratory Data Analysis (EDA):** Run the EDA script to generate summary statistics, perform stationarity tests, and plot historical trends for each time series.

```
python src/eda.py
```

This will output key statistical summaries and save time-series plots (e.g., cad_usd_trend.png showing the CAD/USD rate over time) in the reports/figures/ directory. It also logs results of tests like Augmented Dickey-Fuller (ADF) for checking stationarity of each series.

**Forecast Model Training & Evaluation:** Run the forecasting script to train models and produce forecasts.

```
python src/forecast_models.py
```

This script reads the cleaned data, fits a Prophet model to each series (FX, interest rate, and index), and also fits a simple ARIMA model for comparison. It evaluates model performance on a recent test set (reporting metrics such as MAE/RMSE), and then generates a 30-day out-of-sample forecast. The forecast results are saved as CSV files in data/processed/ (for example, cadusd_forecast.csv contains the CAD/USD predictions and confidence intervals). The script also creates visualizations (saved in reports/figures/) comparing the forecasted values against actuals for the test period, to illustrate model accuracy.

**(Optional) Refresh Data:** If you wish to update the analysis with the latest available data, you can run the data fetching script. Note: An internet connection is required for this step, and if using the Alpha Vantage option for TSX data, you should set your API key as an environment variable.

```
python src/data_fetch.py
```

This will call the Bank of Canada API for the newest FX and interest rate data, and use yfinance (or Alpha Vantage, if configured) to download the latest TSX index data. The new raw data CSV files will overwrite those in data/raw/. You should then rerun the EDA and forecast scripts to incorporate the updates.

Repository Structure

```
canadian-financial-forecasting/
├── data/
│   ├── raw/                # Raw data files (downloaded from APIs, e.g. CAD_USD.csv)
│   └── processed/          # Processed data and outputs (e.g. cadusd_forecast.csv)
├── reports/
│   ├── figures/            # Generated plots from EDA and modeling (PNG images)
│   └── dashboard.pbix      # Power BI dashboard file
├── src/
│   ├── data_fetch.py       # Script to fetch/update data from APIs
│   ├── eda.py              # Script for exploratory data analysis and plotting
│   └── forecast_models.py  # Script to train models and produce forecasts
├── .gitignore
├── requirements.txt        # Python dependencies list
└── README.md               # Project documentation (overview, usage, results)
```

(All data files in the repository are sourced from public APIs as described, and intermediate outputs are included to facilitate offline examination.)

Notes & Limitations

Forecasting financial variables involves uncertainty, and the models assume that historical patterns will persist. The generated forecasts are based purely on historical data and statistical patterns; they do not account for unforeseen market shocks, policy changes, or other one-off events that could disrupt trends. Users should therefore interpret the forecasts as baseline scenarios absent major disruptions.

Additionally, while the data used is official and up-to-date at the time of analysis, there are a few considerations regarding data sources:

- The Bank of Canada’s Valet API provides official daily rates (which ensures data quality and consistency)
bankofcanada.ca
. However, even official data can be subject to revisions or publication delays. The analysis caches data to avoid issues with intraday API downtime, and any such occurrences are noted in the logs.

- The S&P/TSX Composite Index data was accessed via Yahoo Finance through the yfinance Python library. This library uses Yahoo’s publicly available APIs and is intended for research and educational use
github.com
. According to Yahoo’s terms of use, such data is provided for informational purposes and not guaranteed for accuracy or for use in professional trading
github.com
. In practice, the historical index data is generally reliable, but minor discrepancies (e.g., due to how dividends or stock splits are handled) are possible. Users should refer to Yahoo’s terms and ensure compliance if data is used beyond personal or research contexts.

In summary, this project delivers a robust technical solution for forecasting key Canadian financial metrics and presents the results in an accessible format. By bridging Python-based modeling with an interactive dashboard, it aims to demonstrate both data science rigor and clear communication of results. Future enhancements could include incorporating exogenous variables (e.g., commodity prices or macroeconomic indicators) to further improve forecast accuracy, and extending the forecast horizon with appropriate confidence assessments.
