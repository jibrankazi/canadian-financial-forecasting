"""
Exploratory Data Analysis (EDA) for Canadian financial forecasting project.

This script loads daily series for CAD/USD exchange rates, interest rates, and the TSX index,
produced by data_fetch.py. It performs basic cleaning, generates summary statistics, plots
the time series and their distributions, and runs stationarity tests (ADF).
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

# Adjust matplotlib settings
sns.set(style='darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)

DATA_DIR = "."

def load_series():
    """Load the CSV time-series files into pandas DataFrames."""
    cadusd = pd.read_csv(os.path.join(DATA_DIR, 'cadusd_rate.csv'), parse_dates=['date'])
    interest = pd.read_csv(os.path.join(DATA_DIR, 'interest_rate.csv'), parse_dates=['date'])
    tsx = pd.read_csv(os.path.join(DATA_DIR, 'tsx_index.csv'), parse_dates=['date'])
    return cadusd, interest, tsx


def summarize_series(df, value_col):
    """Print summary statistics for a series."""
    summary = df[value_col].describe()
    print(f"Summary statistics for {value_col}:")
    print(summary)


def plot_time_series(df, date_col, value_col, title, filename):
    """Plot a time series and save as PNG."""
    plt.figure()
    sns.lineplot(x=date_col, y=value_col, data=df)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(value_col)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def check_stationarity(series, series_name):
    """Perform Augmented Dickey-Fuller test and print the p-value."""
    result = adfuller(series.dropna())
    p_value = result[1]
    print(f"ADF p-value for {series_name}: {p_value:.4f}")
    return p_value


def main():
    cadusd, interest, tsx = load_series()

    # Summaries
    summarize_series(cadusd, 'cadusd_rate')
    summarize_series(interest, 'interest_rate')
    summarize_series(tsx, 'adj_close')

    # Plotting
    plot_time_series(cadusd, 'date', 'cadusd_rate', 'CAD/USD Exchange Rate', 'cadusd_series.png')
    plot_time_series(interest, 'date', 'interest_rate', 'Benchmark Interest Rate', 'interest_rate_series.png')
    plot_time_series(tsx, 'date', 'adj_close', 'TSX Composite Index (Adj Close)', 'tsx_index_series.png')

    # Stationarity tests
    check_stationarity(cadusd['cadusd_rate'], 'CAD/USD')
    check_stationarity(interest['interest_rate'], 'Interest Rate')
    check_stationarity(tsx['adj_close'], 'TSX Index (Adj Close)')


if __name__ == "__main__":
    main()
