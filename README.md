# README for SARIMA Forecasting Project

This repository contains a Python-based solution for forecasting sales using SARIMA models. The provided script processes sales data, applies time-series modeling, and generates forecasts for a submission format. Below is an overview of the project and instructions for usage.

---

## Project Overview

This project utilizes a Seasonal Autoregressive Integrated Moving Average (SARIMA) model to forecast sales for different SKU-Warehouse combinations. The main steps include:
1. Loading and preprocessing the data.
2. Checking time-series stationarity using the Augmented Dickey-Fuller test.
3. Applying SARIMA modeling for forecasting.
4. Handling edge cases such as constant time-series and non-stationary data.
5. Generating a forecast and saving results in a submission file.

---

## File Structure

- **`main.py`**: Contains the forecasting script.
- **`data/Submission Format.xlsx`**: Template for the required submission format.
- **`data/Data.xlsx - Final.csv`**: Input data file containing historical sales.
- **`final_submission.csv`**: Output file containing forecasts.

---

## Dependencies

Ensure the following Python libraries are installed:

- pandas
- numpy
- statsmodels
- warnings

You can install them via pip:
```bash
pip install pandas numpy statsmodels
```

---

## How to Use

1. Place the `Submission Format.xlsx` and `Data.xlsx - Final.csv` files in the `data/` directory.
2. Run the script:
   ```bash
   python main.py
   ```
3. The forecasts will be saved in `final_submission.csv`.

---

## Key Functions

### `is_stationary(series, alpha=0.05)`
Checks if a time-series is stationary using the Augmented Dickey-Fuller test.

- **Input**: Time-series data (Pandas Series).
- **Output**: Boolean indicating stationarity.

### `forecast_sarima(data, sku, warehouse)`
Generates a SARIMA-based forecast for a specific SKU-Warehouse combination.

- **Input**: Filtered data, SKU id, and Warehouse id.
- **Output**: Forecast value.

Handles edge cases:
- Constant time-series: Returns the constant value.
- Non-stationary series: Applies differencing.
- Fallback logic in case of modeling errors.

---

## Error Handling

The script includes robust error handling:
- **Constant Series**: Directly returns the constant value.
- **Model Fitting Errors**: Falls back to the mean sales for the SKU-Warehouse pair.
- **Negative Forecasts**: Caps forecasts at zero.

---

## Output

The output file `final_submission.csv` matches the format specified in the `Submission Format.xlsx`. It includes the forecasted sales for June 2021 (column `2021-06-01`).

---

## Contact

For questions or issues, please contact [Your Name or Email].

