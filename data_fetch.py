import requests
import pandas as pd
import yfinance as yf
from datetime import datetime


def fetch_boc_series(series_id, start_date=None, end_date=None):
    """
    Fetch a time series from the Bank of Canada's Valet API.

    Args:
        series_id (str): Identifier of the series (e.g. 'FXUSDCAD').
        start_date (str, optional): ISO date string ('YYYY-MM-DD') for start.
        end_date (str, optional): ISO date string ('YYYY-MM-DD') for end.

    Returns:
        pandas.DataFrame: DataFrame with 'date' and series_id columns.
    """
    url = f"https://www.bankofcanada.ca/valet/observations/{series_id}/json"
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    observations = data.get('observations', [])
    dates = []
    values = []
    for obs in observations:
        val = obs.get(series_id, {}).get('v')
        dates.append(obs.get('d'))
        values.append(float(val) if val not in (None, '') else None)

    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        series_id: values
    })
    return df


def fetch_tsx_index(start_date='2010-01-01', end_date=None):
    """
    Fetch daily closing prices for the TSX Composite Index using yfinance.

    Args:
        start_date (str): ISO date string for start of data.
        end_date (str, optional): ISO date string for end of data.

    Returns:
        pandas.DataFrame: DataFrame with 'date' and 'adj_close' columns.
    """
    ticker = '^GSPTSE'  # TSX Composite Index symbol on Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    df = df.rename(columns={'Adj Close': 'adj_close'})
    df = df[['adj_close']].reset_index()
    df.rename(columns={'Date': 'date'}, inplace=True)
    return df


if __name__ == '__main__':
    # Example usage to fetch data since 2020 and write to CSVs.
    fx = fetch_boc_series('FXUSDCAD', start_date='2020-01-01')
    # Convert USD/CAD to CAD/USD by taking reciprocal
    fx['CADUSD'] = 1 / fx['FXUSDCAD']
    interest = fetch_boc_series('V39078', start_date='2020-01-01')
    tsx = fetch_tsx_index(start_date='2020-01-01')

    fx.to_csv('cadusd_rate.csv', index=False)
    interest.to_csv('interest_rate.csv', index=False)
    tsx.to_csv('tsx_index.csv', index=False)
