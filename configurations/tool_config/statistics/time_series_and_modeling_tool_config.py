TIME_SERIES_AND_MODELING_TOOL_CONFIG = ({
    "moving-averages": {
        "title": "Moving Averages",
        "description": "Calculate moving averages for time series smoothing.",
        "url": "/tools/time-series-analysis/moving-averages",
        "inputs": [
            {"label": "Time Series Data", "id": "time_series", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
            {"label": "Window Size", "id": "window_size", "type": "number", "placeholder": "e.g., 3", "optional": False},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "time_series", "optional": True},
        ],
        "outputs": ["Smoothed Time Series"],
    },
    "exponential-smoothing": {
        "title": "Exponential Smoothing",
        "description": "Perform exponential smoothing for forecasting.",
        "url": "/tools/time-series-analysis/exponential-smoothing",
        "inputs": [
            {"label": "Time Series Data", "id": "time_series", "type": "array", "placeholder": "e.g., [1,2,3,4,5]", "optional": False},
            {"label": "Smoothing Factor (Alpha)", "id": "smoothing_factor", "type": "number", "placeholder": "e.g., 0.3", "optional": False},
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "time_series", "optional": True},
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
            {"label": "CSV File", "id": "csv_file", "type": "file", "accept": ".csv", "data_target": "time_series", "optional": True},
        ],
        "outputs": ["Autocorrelation Values"],
    },
    "transition-matrices": {
        "title": "Transition Matrices",
        "description": "Construct and analyze transition matrices for Markov Chains.",
        "url": "/tools/markov-chains/transition-matrices",
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
        "url": "/tools/simulation/random-walk",
        "inputs": [
            {"label": "Number of Steps", "id": "num_steps", "type": "number", "placeholder": "e.g., 100", "optional": False},
            {"label": "Number of Simulations", "id": "num_simulations", "type": "number", "placeholder": "e.g., 50", "optional": False},
            {"label": "Step Size", "id": "step_size", "type": "number", "placeholder": "e.g., 1", "optional": True},
        ],
        "outputs": ["Simulation Paths"],
    },
})
