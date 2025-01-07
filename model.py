import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller


# Load the provided data files
submission_format_path = 'data/Submission Format.xlsx'
data_path = 'data/Data.xlsx - Final.csv'

submission_format = pd.read_excel(submission_format_path)
data = pd.read_csv(data_path)

# Convert data to a time-series format
data_long = data.melt(
    id_vars=["Warehouse id", "Region", "SKU id"],
    var_name="Month",
    value_name="Sales"
)

# Convert 'Month' to datetime format
data_long["Month"] = pd.to_datetime(data_long["Month"], format='%b-%y')

from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

# Suppress warnings from statsmodels
warnings.filterwarnings("ignore")

def is_stationary(series, alpha=0.05):
    """
    Check if a time-series is stationary using the Augmented Dickey-Fuller test.
    Handles constant series gracefully.
    """
    # Check if the series is constant
    if series.nunique() == 1:
        return True  # Constant series are stationary by definition
    
    # Perform the Augmented Dickey-Fuller test
    result = adfuller(series.dropna())
    return result[1] < alpha  # P-value < alpha means stationary

def forecast_sarima(data, sku, warehouse):
    """
    Forecast sales for a specific SKU and warehouse using SARIMA model with fallback logic.
    """
    # Filter data for the specific SKU and Warehouse
    sku_data = data[(data["SKU id"] == sku) & (data["Warehouse id"] == warehouse)]
    sku_data = sku_data[["Month", "Sales"]].set_index("Month")
    sku_data = sku_data.asfreq('MS')  # Ensure frequency is set

    # Check for constant series
    if sku_data["Sales"].nunique() == 1:
        return sku_data["Sales"].iloc[0]  # Return the constant value as forecast

    # Apply differencing if needed (check for stationarity)
    if not is_stationary(sku_data["Sales"]):
        sku_data["Sales_diff"] = sku_data["Sales"].diff().dropna()
        train_data = sku_data["Sales_diff"]
    else:
        train_data = sku_data["Sales"]

    try:
        # Fit a simpler SARIMA model
        model = SARIMAX(
            train_data,
            order=(1, 1, 1),  # Simpler non-seasonal orders
            seasonal_order=(1, 1, 0, 12),  # Seasonal order
            enforce_stationarity=False,  # Relax stationarity constraint
            enforce_invertibility=False,  # Relax invertibility constraint
        )
        model_fit = model.fit(disp=False)

        # Forecast and reverse differencing if applied
        forecast = model_fit.get_forecast(steps=1).predicted_mean.values[0]
        if "Sales_diff" in sku_data:
            forecast += sku_data["Sales"].iloc[-1]  # Reverse differencing
        return max(0, forecast)  # Ensure no negative forecasts

    except Exception as e:
        print(f"Error forecasting for SKU {sku} and Warehouse {warehouse}: {e}")
        return sku_data["Sales"].mean()  # Fallback to mean sales


# Generate forecasts for all SKU-Warehouse combinations
forecast_results = []

for _, row in submission_format.iterrows():
    sku = row["SKU id"]
    warehouse = row["Warehouse id"]
    prediction = forecast_sarima(data_long, sku, warehouse)
    forecast_results.append(prediction)

# Add forecasts to the submission format
submission_format["2021-06-01"] = forecast_results

# Save the results to a CSV file
submission_file_path = "final_submission.csv"
submission_format.to_csv(submission_file_path, index=False)

print(f"Forecasting completed. Submission file saved as: {submission_file_path}")
