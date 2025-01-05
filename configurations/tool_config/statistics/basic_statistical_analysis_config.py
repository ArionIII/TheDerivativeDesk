BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG = {
    # 1.1 Descriptive Statistics
    "descriptive_statistics": {
        "title": "Descriptive Statistics Tools",
        "description": "Explore tools to measure central tendency, dispersion, and shape of data distributions.",
        "tools": [
            {
                "title": "Mean",
                "description": "Calculate the arithmetic mean of a dataset.",
                "url": "/tools/statistical-analysis/descriptive/mean",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["Mean Value"],
            },
            {
                "title": "Median",
                "description": "Determine the median value of a dataset.",
                "url": "/tools/statistical-analysis/descriptive/median",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["Median Value"],
            },
            {
                "title": "Mode",
                "description": "Identify the most frequently occurring value(s) in a dataset.",
                "url": "/tools/statistical-analysis/descriptive/mode",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,4]"}
                ],
                "outputs": ["Mode Value(s)"],
            },
            {
                "title": "Range",
                "description": "Calculate the range of a dataset (difference between max and min values).",
                "url": "/tools/statistical-analysis/descriptive/range",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["Range Value"],
            },
            {
                "title": "Interquartile Range (IQR)",
                "description": "Compute the interquartile range of a dataset.",
                "url": "/tools/statistical-analysis/descriptive/iqr",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["IQR Value"],
            },
            {
                "title": "Skewness",
                "description": "Measure the asymmetry of the data distribution.",
                "url": "/tools/statistical-analysis/descriptive/skewness",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["Skewness Value"],
            },
            {
                "title": "Kurtosis",
                "description": "Measure the 'tailedness' of the data distribution.",
                "url": "/tools/statistical-analysis/descriptive/kurtosis",
                "inputs": [
                    {"label": "Dataset", "id": "dataset", "type": "array", "placeholder": "e.g., [1,2,3,4,5]"}
                ],
                "outputs": ["Kurtosis Value"],
            },
        ],
    },
    # 1.2 Inferential Statistics
    "inferential_statistics": {
        "title": "Inferential Statistics Tools",
        "description": "Leverage statistical methods to infer population parameters and relationships.",
        "tools": [
            {
                "title": "Hypothesis Testing - t-test",
                "description": "Perform a t-test for comparing sample means.",
                "url": "/tools/statistical-analysis/inferential/t_test",
                "inputs": [
                    {"label": "Sample Dataset A", "id": "sample_a", "type": "array", "placeholder": "e.g., [1,2,3]"},
                    {"label": "Sample Dataset B (optional)", "id": "sample_b", "type": "array", "placeholder": "e.g., [4,5,6]", "optional": True},
                    {"label": "Test Type", "id": "test_type", "type": "select", "options": ["One-Sample", "Two-Sample"], "default": "One-Sample"},
                ],
                "outputs": ["t-Statistic", "P-Value"],
            },
            {
                "title": "Hypothesis Testing - z-test",
                "description": "Conduct a z-test for comparing population means.",
                "url": "/tools/statistical-analysis/inferential/z_test",
                "inputs": [
                    {"label": "Sample Mean", "id": "sample_mean", "type": "number", "placeholder": "e.g., 5.5"},
                    {"label": "Population Mean", "id": "population_mean", "type": "number", "placeholder": "e.g., 5.0"},
                    {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.5"},
                    {"label": "Sample Size", "id": "sample_size", "type": "number", "placeholder": "e.g., 30"},
                ],
                "outputs": ["z-Statistic", "P-Value"],
            },
            {
                "title": "Chi-Square Test",
                "description": "Perform a chi-square test for independence or goodness-of-fit.",
                "url": "/tools/statistical-analysis/inferential/chi_square",
                "inputs": [
                    {"label": "Observed Frequencies", "id": "observed", "type": "array", "placeholder": "e.g., [10,20,30]"},
                    {"label": "Expected Frequencies", "id": "expected", "type": "array", "placeholder": "e.g., [15,15,30]"}
                ],
                "outputs": ["Chi-Square Statistic", "P-Value"],
            },
            {
                "title": "Confidence Intervals",
                "description": "Calculate confidence intervals for population parameters.",
                "url": "/tools/statistical-analysis/inferential/confidence_intervals",
                "inputs": [
                    {"label": "Sample Mean", "id": "sample_mean", "type": "number", "placeholder": "e.g., 5.5"},
                    {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.5"},
                    {"label": "Sample Size", "id": "sample_size", "type": "number", "placeholder": "e.g., 30"},
                    {"label": "Confidence Level", "id": "confidence_level", "type": "number", "placeholder": "e.g., 0.95"}
                ],
                "outputs": ["Confidence Interval"],
            },
            {
                "title": "ANOVA",
                "description": "Perform ANOVA for analyzing variance between groups.",
                "url": "/tools/statistical-analysis/inferential/anova",
                "inputs": [
                    {"label": "Group A Data", "id": "group_a", "type": "array", "placeholder": "e.g., [1,2,3]"},
                    {"label": "Group B Data", "id": "group_b", "type": "array", "placeholder": "e.g., [4,5,6]"},
                    {"label": "Group C Data (optional)", "id": "group_c", "type": "array", "placeholder": "e.g., [7,8,9]", "optional": True},
                ],
                "outputs": ["F-Statistic", "P-Value"],
            },
        ],
    },
    # 1.3 Probability Tools
    "probability_tools": {
        "title": "Probability Tools",
        "description": "Explore tools for probability calculations and distribution analysis.",
        "tools": [
            {
                "title": "PDF and CDF",
                "description": "Compute the Probability Density and Cumulative Distribution functions.",
                "url": "/tools/statistical-analysis/probability/pdf_cdf",
                "inputs": [
                    {"label": "Distribution Type", "id": "distribution", "type": "select", "options": ["Normal", "Binomial", "Poisson"], "default": "Normal"},
                    {"label": "Parameters", "id": "parameters", "type": "text", "placeholder": "e.g., mean=0,std=1"}
                ],
                "outputs": ["PDF Value", "CDF Value"],
            },
            {
                "title": "Z-Score Calculation",
                "description": "Calculate Z-scores for data points.",
                "url": "/tools/statistical-analysis/probability/z_score",
                "inputs": [
                    {"label": "Data Point", "id": "data_point", "type": "number", "placeholder": "e.g., 5"},
                    {"label": "Mean", "id": "mean", "type": "number", "placeholder": "e.g., 3.5"},
                    {"label": "Standard Deviation", "id": "std_dev", "type": "number", "placeholder": "e.g., 1.2"},
                ],
                "outputs": ["Z-Score"],
            },
        ],
    },
}
