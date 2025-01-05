BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG = {
    "mean": {
        "title": "Mean",
        "description": "Calculate the arithmetic mean of a dataset.",
        "url": "/tools/descriptive-analysis/mean",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["Mean Value"],
    },
    "median": {
        "title": "Median",
        "description": "Determine the median value of a dataset.",
        "url": "/tools/descriptive-analysis/median",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["Median Value"],
    },
    "mode": {
        "title": "Mode",
        "description": "Identify the most frequently occurring value(s) in a dataset.",
        "url": "/tools/descriptive-analysis/mode",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,4]"}
        ],
        "outputs": ["Mode Value(s)"],
    },
    "range": {
        "title": "Range",
        "description": "Calculate the range of a dataset (difference between max and min values).",
        "url": "/tools/descriptive-analysis/range",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["Range Value"],
    },
    "iqr": {
        "title": "Interquartile Range (IQR)",
        "description": "Compute the interquartile range of a dataset.",
        "url": "/tools/descriptive-analysis/iqr",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["IQR Value"],
    },
    "skewness": {
        "title": "Skewness",
        "description": "Measure the asymmetry of the data distribution.",
        "url": "/tools/descriptive-analysis/skewness",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["Skewness Value"],
    },
    "kurtosis": {
        "title": "Kurtosis",
        "description": "Measure the 'tailedness' of the data distribution.",
        "url": "/tools/descriptive-analysis/kurtosis",
        "inputs": [
            {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
        ],
        "outputs": ["Kurtosis Value"],
    },
    "comprehensive-basic-analysis": {
    "title": "Comprehensive Basic Analysis",
    "description": "Perform a complete descriptive analysis, including mean, median, mode, range, IQR, skewness, and kurtosis, in one step.",
    "url": "/tools/descriptive-analysis/comprehensive-basic-analysis",
    "inputs": [
        {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1, 2, 3, 4, 5]"}
    ],
    "outputs": [
        "Mean Value",
        "Median Value",
        "Mode Value(s)",
        "Range Value",
        "IQR Value",
        "Skewness Value",
        "Kurtosis Value",
    ],
},
    "t_test": {
        "title": "Hypothesis Testing - t-test",
        "description": "Perform a t-test for comparing sample means.",
        "url": "/tools/statistical-analysis/t_test",
        "inputs": [
            {"label": "Sample Dataset A", "id": "sample_a", "type": "array", "placeholder": "e.g., [1,2,3]"},
            {"label": "Sample Dataset B (optional)", "id": "sample_b", "type": "array", "placeholder": "e.g., [4,5,6]", "optional": True},
            {"label": "Test Type", "id": "test_type", "type": "select", "options": ["One-Sample", "Two-Sample"], "default": "One-Sample"},
        ],
        "outputs": ["t-Statistic", "P-Value"],
    },
    "z_test": {
        "title": "Hypothesis Testing - z-test",
        "description": "Conduct a z-test for comparing population means.",
        "url": "/tools/statistical-analysis/z_test",
        "inputs": [
            {"label": "Sample Mean", "id": "sample_mean", "type": "number", "placeholder": "e.g., 5.5"},
            {"label": "Population Mean", "id": "population_mean", "type": "number", "placeholder": "e.g., 5.0"},
            {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.5"},
            {"label": "Sample Size", "id": "sample_size", "type": "number", "placeholder": "e.g., 30"},
        ],
        "outputs": ["z-Statistic", "P-Value"],
    },
    "chi_square": {
        "title": "Chi-Square Test",
        "description": "Perform a chi-square test for independence or goodness-of-fit.",
        "url": "/tools/statistical-analysis/chi_square",
        "inputs": [
            {"label": "Observed Frequencies", "id": "observed", "type": "array", "placeholder": "e.g., [10,20,30]"},
            {"label": "Expected Frequencies", "id": "expected", "type": "array", "placeholder": "e.g., [15,15,30]"}
        ],
        "outputs": ["Chi-Square Statistic", "P-Value"],
    },
    "confidence_intervals": {
        "title": "Confidence Intervals",
        "description": "Calculate confidence intervals for population parameters.",
        "url": "/tools/statistical-analysis/confidence_intervals",
        "inputs": [
            {"label": "Sample Mean", "id": "sample_mean", "type": "number", "placeholder": "e.g., 5.5"},
            {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.5"},
            {"label": "Sample Size", "id": "sample_size", "type": "number", "placeholder": "e.g., 30"},
            {"label": "Confidence Level", "id": "confidence_level", "type": "number", "placeholder": "e.g., 0.95"}
        ],
        "outputs": ["Confidence Interval"],
    },
    "anova": {
        "title": "ANOVA",
        "description": "Perform ANOVA for analyzing variance between groups.",
        "url": "/tools/statistical-analysis/anova",
        "inputs": [
            {"label": "Group A Data", "id": "group_a", "type": "array", "placeholder": "e.g., [1,2,3]"},
            {"label": "Group B Data", "id": "group_b", "type": "array", "placeholder": "e.g., [4,5,6]"},
            {"label": "Group C Data (optional)", "id": "group_c", "type": "array", "placeholder": "e.g., [7,8,9]", "optional": True},
        ],
        "outputs": ["F-Statistic", "P-Value"],
    },
    "pdf_cdf": {
    "title": "PDF and CDF",
    "description": "Compute the Probability Density and Cumulative Distribution functions.",
    "url": "/tools/statistical-analysis/pdf_cdf",
    "inputs": [
        {"label": "Distribution Type", "id": "distribution", "type": "select", "options": ["Normal", "Binomial", "Poisson"], "default": "Normal"},
        {"label": "Parameters", "id": "parameters", "type": "text", "placeholder": "e.g., mean=0,std=1"},
        {"label": "Value (x)", "id": "x_value", "type": "number", "placeholder": "e.g., 1.5"},
    ],
    "outputs": ["PDF Value", "CDF Value"],
},
"z_score": {
    "title": "Z-Score Calculation",
    "description": "Calculate Z-scores for data points.",
    "url": "/tools/statistical-analysis/z_score",
    "inputs": [
        {"label": "Data Point", "id": "data_point", "type": "number", "placeholder": "e.g., 5"},
        {"label": "Mean", "id": "mean", "type": "number", "placeholder": "e.g., 3.5"},
        {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.2"},
    ],
    "outputs": ["Z-Score"],
},

    
}
