"""
Data ingestion module for Canadian Financial Markets Forecasting.

This module provides functions to fetch time series data from public APIs
including the Bank of Canada's Valet API and a free financial market API for
stock index data. Each function returns a pandas DataFrame which can be
persisted to disk or passed to downstream processing functions.
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
import requests
# Note: yfinance is optional and may be replaced with another data source
# during production; import only if available.
try:
    import yfinance as yf
except ImportError:
    yf = None

def fetch_boc_series(series_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """Fetch a series from the Bank of Canada Valet API.

    Args:
        series_id: The identifier for the series (e.g., 'FXUSDCAD').
        start_date: Optional start date in ISO format (YYYY-MM-DD).
        end_date: Optional end date in ISO format (YYYY-MM-DD).

    Returns:
        DataFrame with columns ['date', 'value'] sorted by date.

    Raises:
        RuntimeError: If the HTTP request fails or JSON is malformed.
    """
    # Construct URL for Valet API
    url = f"https://www.bankofcanada.ca/valet/observations/{series_id}/json"
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    response = requests.get(url, params=params)
    if not response.ok:
        raise RuntimeError(f"Failed to fetch {series_id}: {response.status_code}")

    data = response.json().get('observations', [])
    records = []
    for obs in data:
        date_str = obs.get('d')
        value = obs.get(series_id, {}).get('v')
        if date_str and value is not None:
            records.append({'date': date_str, 'value': float(value)})
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    return df

def fetch_tsx_index(symbol: str = "^GSPTSE", start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """Fetch TSX index data from yfinance.

    Args:
        symbol: Ticker symbol for the TSX composite index.
        start_date: Optional start date in ISO format.
        end_date: Optional end date in ISO format.

    Returns:
        DataFrame with columns ['date', 'adj_close'].

    Raises:
        ImportError: If yfinance is not installed.
    """
    if yf is None:
        raise ImportError("yfinance must be installed to fetch index data")

    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    data = data.reset_index()[['Date', 'Adj Close']]
    data.columns = ['date', 'adj_close']
    return data

def save_to_csv(df: pd.DataFrame, path: str) -> None:
    """Save DataFrame to a CSV file.

    Args:
        df: DataFrame to save.
        path: File path to write CSV to.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
