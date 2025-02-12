TIME_SERIES_AND_MODELING_TOOL_CONFIG = ({
    "log-returns-calculator": {
    "title": "Log Returns Calculator",
    "description": "Compute log returns for time series in a CSV file.",
    "url": "/tools/time-series-analysis/log-returns-calculator",
    "inputs": [
        {"label": "Time Series Data", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
        {
            "label": "CSV File",
            "id": "csv_file",
            "type": "file",
            "accept": ".csv",
            "data_target": "dataset",
            "optional": True,
            "template": "/static/templates/sample_time_series.csv",
            "header": True
        }
    ],
    "outputs": ["CSV File with Log Returns"],
    "note": "You will automatically download a CSV file AND a XLSX file with the log returns of the input time series."
},
    "moving-averages": {
        "title": "Moving Averages",
        "description": "Calculate moving averages for time series smoothing.",
        "url": "/tools/time-series-analysis/moving-averages",
        "inputs": [
            {"label": "Time Series Data", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
            {"label": "Window Size", "id": "window_size", "type": "number", "placeholder": "e.g., 3", "optional": False},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "dataset", "optional": True, "template": "/static/templates/comprehensive_basic_analysis.csv"},
        ],
        "outputs": ["CSV File with Smoothed Time Series"],
    },
    "exponential-smoothing": {
        "title": "Exponential Smoothing",
        "description": "Perform exponential smoothing for forecasting.",
        "url": "/tools/time-series-analysis/exponential-smoothing",
        "inputs": [
            {"label": "Time Series Data", "id": "time_series", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
            {"label": "Smoothing Factor (Alpha)", "id": "smoothing_factor", "type": "number", "placeholder": "e.g., 0.3", "optional": False},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "time_series", "optional": True, "template": "/static/templates/comprehensive_basic_analysis.csv"},
        ],
        "outputs": ["Smoothed Time Series"],
    },
    "autocorrelation": {
        "title": "Autocorrelation",
        "description": "Analyze the correlation of a time series with its own lags.",
        "url": "/tools/time-series-analysis/autocorrelation",
        "inputs": [
            {"label": "Time Series Data", "id": "time_series", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
            {"label": "Lag Order", "id": "lag_order", "type": "number", "placeholder": "e.g., 1", "optional": True},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "time_series", "optional": True, "template": "/static/templates/comprehensive_basic_analysis.csv"},
        ],
        "outputs": ["Autocorrelation Values"],
    },
    "AR-MA-ARMA-previsions": {
    "title": "AR, MA, ARIMA Predictions",
    "description": "Automatically determine the best model (AR, MA, or ARIMA) and generate future predictions.",
    "url": "/tools/time-series-analysis/AR-MA-ARMA-previsions",
    "inputs": [
        {
            "label": "Time Series Data",
            "id": "dataset",
            "type": "array",
            "placeholder": "e.g., [1,2,3,4,5,6]",
            "optional": False
        },
        {
            "label": "Number of Predictions",
            "id": "n_previsions",
            "type": "number",
            "placeholder": "e.g., 10",
            "optional": False
        },
        {"label": "Temporal Step", "id": "temporal_step", "type": "number", "placeholder": "1, 7, 30, 90, 365...", "optional": False},
        {
            "label": "CSV File",
            "id": "csv_file",
            "type": "file",
            "accept": ".csv",
            "data_target": "dataset",
            "optional": True,
            "template": "/static/templates/ar_ma_arma.csv"
        }
    ],
    "note":"Can only compute partial correlations for lags up to 50% of the sample size. Base lag is set to 10, so the time series must be at least 20 observations long.",
    "outputs": [
        "Predicted Time Series",
        "Best Model Selected (AR, MA, or ARIMA)",
        "Model Parameters (p, q)"
    ]
},
    "transition-matrices": {
        "title": "Transition Matrices",
        "description": "Construct and analyze transition matrices for Markov Chains.",
        "url": "/tools/markov-chains-and-random-walks/transition-matrices",
        "inputs": [
            {"label": "State Sequence", "id": "state_sequence", "type": "array", "placeholder": "e.g., [1,2,1,3,1,2]", "optional": False},
            {"label": "Number of States", "id": "num_states", "type": "number", "placeholder": "e.g., 3", "optional": False},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "state_sequence", "optional": True},
        ],
        "outputs": ["Transition Matrix"],
    },
    "random-walks": {
        "title": "Simulation of Random Walks",
        "description": "Simulate random walks and analyze their outcomes.",
        "url": "/tools/markov-chains-and-random-walks/random-walks",
        "inputs": [
            {"label": "Number of Steps", "id": "num_steps", "type": "number", "placeholder": "e.g., 100", "optional": False},
            {"label": "Number of Simulations", "id": "num_simulations", "type": "number", "placeholder": "e.g., 50", "optional": False},
            {"label": "Step Size", "id": "step_size", "type": "number", "placeholder": "e.g., 1", "optional": True},
        ],
        "outputs": ["Simulation Paths"],
    },
})
