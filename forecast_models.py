"""
Forecasting models for Canadian financial time series using Prophet.

This script loads daily CAD/USD exchange rate, interest rate, and TSX index data,
splits each series into training and test sets, fits a Prophet model,
evaluates forecast accuracy, and produces forward forecasts.
"""

import os
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

DATA_DIR = "."
FORECAST_HORIZON = 30  # number of days to forecast ahead
TEST_SIZE = 90  # number of observations reserved for testing

def load_series():
    """Load time-series CSV files returned by data_fetch.py."""
    cadusd = pd.read_csv(os.path.join(DATA_DIR, 'cadusd_rate.csv'), parse_dates=['date'])
    interest = pd.read_csv(os.path.join(DATA_DIR, 'interest_rate.csv'), parse_dates=['date'])
    tsx = pd.read_csv(os.path.join(DATA_DIR, 'tsx_index.csv'), parse_dates=['date'])
    return cadusd, interest, tsx


def prepare_prophet_df(df, date_col, value_col):
    """Prepare DataFrame with columns ds and y for Prophet."""
    return df[[date_col, value_col]].rename(columns={date_col: 'ds', value_col: 'y'})


def train_prophet_model(train_df):
    """Train Prophet model with default seasonality settings."""
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(train_df)
    return model


def evaluate_forecast(actual, predicted):
    """Compute RMSE and MAPE for evaluation."""
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = mean_absolute_percentage_error(actual, predicted)
    return rmse, mape


def forecast_series(df, date_col, value_col, periods=FORECAST_HORIZON, test_size=TEST_SIZE):
    """Fit Prophet, evaluate on test set, and forecast future periods."""
    df_sorted = df.sort_values(date_col).dropna().reset_index(drop=True)
    prophet_df = prepare_prophet_df(df_sorted, date_col, value_col)

    # Split train/test
    train_df = prophet_df.iloc[:-test_size]
    test_df = prophet_df.iloc[-test_size:]

    # Fit model
    model = train_prophet_model(train_df)

    # In-sample prediction
    full_forecast = model.predict(prophet_df[['ds']])
    predictions = full_forecast['yhat'].iloc[-test_size:].values
    actual = test_df['y'].values
    rmse, mape = evaluate_forecast(actual, predictions)

    # Future forecast
    future = model.make_future_dataframe(periods=periods)
    future_forecast = model.predict(future)

    return full_forecast, future_forecast, rmse, mape


def save_forecast(forecast_df, filename):
    """Save forecast DataFrame to CSV."""
    forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(filename, index=False)


def main():
    cadusd, interest, tsx = load_series()

    results = {}

    # CAD/USD forecast
    cadusd_fc, cadusd_future, cadusd_rmse, cadusd_mape = forecast_series(cadusd, 'date', 'cadusd_rate')
    save_forecast(cadusd_future, 'cadusd_forecast.csv')
    results['cadusd'] = {'rmse': cadusd_rmse, 'mape': cadusd_mape}

    # Interest rate forecast
    interest_fc, interest_future, interest_rmse, interest_mape = forecast_series(interest, 'date', 'interest_rate')
    save_forecast(interest_future, 'interest_rate_forecast.csv')
    results['interest_rate'] = {'rmse': interest_rmse, 'mape': interest_mape}

    # TSX index forecast
    tsx_fc, tsx_future, tsx_rmse, tsx_mape = forecast_series(tsx, 'date', 'adj_close')
    save_forecast(tsx_future, 'tsx_index_forecast.csv')
    results['tsx_index'] = {'rmse': tsx_rmse, 'mape': tsx_mape}

    # Print evaluation results
    for name, metrics in results.items():
        print(f"{name} - RMSE: {metrics['rmse']:.4f}, MAPE: {metrics['mape']:.4f}")


if __name__ == '__main__':
    main()
