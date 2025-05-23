from config import generate_input_from_file
import os

BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG = {
    "mean": {
        "title": "Mean",
        "description": "Calculate the arithmetic mean of a dataset.",
        "url": "/tools/descriptive-analysis/mean",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'comprehensive_basic_analysis.csv'))}",
                "optional": False,
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Mean Value"],
    },
    "median": {
        "title": "Median",
        "description": "Determine the median value of a dataset.",
        "url": "/tools/descriptive-analysis/median",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Median Value"],
    },
    "mode": {
        "title": "Mode",
        "description": "Identify the most frequently occurring value(s) in a dataset.",
        "url": "/tools/descriptive-analysis/mode",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Mode Value(s)"],
    },
    "range": {
        "title": "Range",
        "description": "Calculate the range of a dataset (difference between max and min values).",
        "url": "/tools/descriptive-analysis/range",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Range Value"],
    },
    "iqr": {
        "title": "Interquartile Range (IQR)",
        "description": "Compute the interquartile range of a dataset.",
        "url": "/tools/descriptive-analysis/iqr",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["IQR Value"],
    },
    "skewness": {
        "title": "Skewness",
        "description": "Measure the asymmetry of the data distribution.",
        "url": "/tools/descriptive-analysis/skewness",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Skewness Value"],
    },
    "kurtosis": {
        "title": "Kurtosis",
        "description": "Measure the 'tailedness' of the data distribution.",
        "url": "/tools/descriptive-analysis/kurtosis",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
        ],
        "outputs": ["Kurtosis Value"],
        "note": "We are using here Fisher's Kurtosis, which is the default in SciPy. This Kurtosis is centered around 0, which is different form Pearson's Kurtosis, which is centered around 3.",
    },
    "comprehensive-basic-analysis": {
        "title": "Comprehensive Basic Analysis",
        "description": "Perform a complete descriptive analysis, including mean, median, mode, range, IQR, skewness, and kurtosis, in one step.",
        "url": "/tools/descriptive-analysis/comprehensive-basic-analysis",
        "inputs": [
            {
                "label": "Dataset",
                "id": "dataset",
                "type": "array",
                "placeholder": generate_input_from_file(
                    os.path.join(
                        os.getcwd(),
                        "static",
                        "templates",
                        "comprehensive_basic_analysis.csv",
                    )
                ),
            },
            {
                "label": "CSV File",
                "id": "csv_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "dataset",
                "template": "/static/templates/comprehensive_basic_analysis.csv",
                "optional": True,
            },
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
    "t-test": {
        "title": "Hypothesis Testing - t-test",
        "description": "Perform a t-test for comparing sample means.",
        "url": "/tools/inferential-statistics/t-test",
        "inputs": [
            {
                "label": "Sample Dataset A",
                "id": "sample_a",
                "type": "array",
                "placeholder": "[1,2,3]",
            },
            {
                "label": "Sample Dataset B (optional)",
                "id": "sample_b",
                "type": "array",
                "placeholder": "[4,5,6]",
                "optional": True,
            },
            {
                "label": "Test Type",
                "id": "test_type",
                "type": "select",
                "options": ["One-Sample", "Two-Sample"],
                "default": "One-Sample",
            },
        ],
        "outputs": ["t-Statistic", "P-Value"],
    },
    "z-test": {
        "title": "Hypothesis Testing - z-test",
        "description": "Conduct a z-test for comparing population means.",
        "url": "/tools/inferential-statistics/z-test",
        "inputs": [
            {
                "label": "Sample Mean",
                "id": "sample_mean",
                "type": "number",
                "placeholder": "5.5",
            },
            {
                "label": "Population Mean",
                "id": "population_mean",
                "type": "number",
                "placeholder": "5.0",
            },
            {
                "label": "Standard Deviation",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1.5",
            },
            {
                "label": "Sample Size",
                "id": "sample_size",
                "type": "number",
                "placeholder": "30",
            },
        ],
        "outputs": ["z-Statistic", "P-Value"],
    },
    "chi-square": {
        "title": "Chi-Square Test",
        "description": "Perform a chi-square test for independence or goodness-of-fit.",
        "url": "/tools/inferential-statistics/chi-square",
        "inputs": [
            {
                "label": "Observed Frequencies",
                "id": "observed",
                "type": "array",
                "placeholder": "[10,20,30]",
            },
            {
                "label": "Expected Frequencies",
                "id": "expected",
                "type": "array",
                "placeholder": "[15,15,30]",
            },
        ],
        "outputs": ["Chi-Square Statistic", "P-Value"],
        "note": "For each axis slice, the sum of the observed frequencies must agree with the sum of the expected frequencies to a relative tolerance of 1e-08",
    },
    "confidence-intervals": {
        "title": "Confidence Intervals",
        "description": "Calculate confidence intervals for population parameters.",
        "url": "/tools/inferential-statistics/confidence-intervals",
        "inputs": [
            {
                "label": "Sample Mean",
                "id": "sample_mean",
                "type": "number",
                "placeholder": "5.5",
            },
            {
                "label": "Standard Deviation",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1.5",
            },
            {
                "label": "Sample Size",
                "id": "sample_size",
                "type": "number",
                "placeholder": "30",
            },
            {
                "label": "Confidence Level",
                "id": "confidence_level",
                "type": "number",
                "placeholder": "0.95",
            },
        ],
        "outputs": ["Confidence Interval"],
    },
    "p-value": {
        "title": "P-Value Calculation",
        "description": "Determine the p-value for hypothesis testing.",
        "url": "/tools/inferential-statistics/p-value-calculation",
        "inputs": [
            {
                "label": "Test Statistic",
                "id": "test_statistic",
                "type": "number",
                "placeholder": "2.5",
            },
            {
                "label": "Degrees of Freedom (optional)",
                "id": "degrees_of_freedom",
                "type": "number",
                "placeholder": "10",
                "optional": True,
            },
            {
                "label": "Distribution Type",
                "id": "distribution_type",
                "type": "select",
                "options": ["Normal", "T-Distribution"],
                "default": "Normal",
            },
        ],
        "outputs": ["P-Value"],
        "note": "For T-Distribution, degrees of freedom are required.",
    },
    "anova": {
        "title": "ANOVA (Analysis of Variance)",
        "description": "Analyze differences between group means in datasets.",
        "url": "/tools/inferential-statistics/anova",
        "inputs": [
            {
                "label": "Group A Data",
                "id": "group_a",
                "type": "array",
                "placeholder": "[1,2,3]",
            },
            {
                "label": "Group B Data",
                "id": "group_b",
                "type": "array",
                "placeholder": "[4,5,6]",
            },
            {
                "label": "Group C Data (optional)",
                "id": "group_c",
                "type": "array",
                "placeholder": "[7,8,9]",
                "optional": True,
            },
        ],
        "outputs": ["F-Statistic", "P-Value"],
    },
    "simple-regression": {
        "title": "Simple Regression",
        "description": "Perform simple linear regression analysis.",
        "url": "/tools/inferential-statistics/simple-regression",
        "inputs": [
            {
                "label": "Independent Variable (X)",
                "id": "independent_variable",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'simple_regression_1.csv'))}",
            },
            {
                "label": "Dependent Variable (Y)",
                "id": "dependent_variable",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'simple_regression_2.csv'))}",
            },
            {
                "label": "CSV File - X",
                "id": "csv_file_1",
                "type": "file",
                "accept": ".csv",
                "data_target": "independent_variable",
                "template": "/static/templates/simple_regression_1.csv",
                "optional": True,
            },
            {
                "label": "CSV File - Y",
                "id": "csv_file_2",
                "type": "file",
                "accept": ".csv",
                "data_target": "dependent_variable",
                "template": "/static/templates/simple_regression_2.csv",
                "optional": True,
            },
        ],
        "outputs": ["Slope", "Intercept", "R-Squared Value"],
    },
    "multiple-regression": {
        "title": "Multiple Regression",
        "description": "Conduct multiple regression for multivariate datasets.",
        "url": "/tools/inferential-statistics/multiple-regression",
        "inputs": [
            {
                "label": "Independent Variables (\( X_k \))",
                "id": "independent_variables",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'multi_regression_1.csv'))}",
            },
            {
                "label": "Dependent Variable (Y)",
                "id": "dependent_variables",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'multi_regression_2.csv'))}",
            },
            {
                "label": "CSV File - (\( X_k \))",
                "id": "csv_file_1",
                "type": "file",
                "accept": ".csv",
                "data_target": "independent_variables",
                "template": "/static/templates/multi_regression_1.csv",
                "optional": True,
            },
            {
                "label": "CSV File - Y",
                "id": "csv_file_2",
                "type": "file",
                "accept": ".csv",
                "data_target": "dependent_variables",
                "template": "/static/templates/multi_regression_2.csv",
                "optional": True,
            },
        ],
        "outputs": [
            "Coefficients",
            "Intercept",
            "R-Squared Value",
            "Mean Squared Error",
        ],
        "graphs": [
            {
                "name": "Estimated Coefficients",
            },
            {
                "name": "Observed vs Predicted",
            },
        ],
    },
    "pdf": {
        "title": "Probability Density Function (PDF)",
        "description": "Calculate the PDF for continuous random variables.",
        "url": "/tools/probability-tools/pdf",
        "inputs": [
            {
                "label": "Value (x)",
                "id": "value",
                "type": "number",
                "placeholder": "1.5",
            },
            {"label": "Mean (μ)", "id": "mean", "type": "number", "placeholder": "0"},
            {
                "label": "Standard Deviation (σ)",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1",
            },
        ],
        "outputs": ["PDF Value"],
    },
    "cdf": {
        "title": "Cumulative Distribution Function (CDF)",
        "description": "Compute the cumulative probability of random variables.",
        "url": "/tools/probability-tools/cdf",
        "inputs": [
            {
                "label": "Value (x)",
                "id": "value",
                "type": "number",
                "placeholder": "1.5",
            },
            {"label": "Mean (μ)", "id": "mean", "type": "number", "placeholder": "0"},
            {
                "label": "Standard Deviation (σ)",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1",
            },
        ],
        "outputs": ["CDF Value"],
        "note": "The CDF is the probability that a random variable X following a Normal distribution will take a value less than or equal to x.",
    },
    "z-score": {
        "title": "Z-Score Calculation",
        "description": "Find the Z-score to standardize data points.",
        "url": "/tools/probability-tools/z-score",
        "inputs": [
            {
                "label": "Value (x)",
                "id": "value",
                "type": "number",
                "placeholder": "1.5",
            },
            {"label": "Mean (μ)", "id": "mean", "type": "number", "placeholder": "0"},
            {
                "label": "Standard Deviation (σ)",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1",
            },
        ],
        "outputs": ["Z-Score"],
    },
    "binomial-distribution": {
        "title": "Binomial Distribution",
        "description": "Analyze binomial random variables and probabilities.",
        "url": "/tools/probability-tools/binomial-distribution",
        "inputs": [
            {
                "label": "Number of Trials (n)",
                "id": "num_trials",
                "type": "number",
                "placeholder": "10",
            },
            {
                "label": "Probability of Success (p)",
                "id": "prob_success",
                "type": "number",
                "placeholder": "0.5",
            },
            {
                "label": "Number of Successes (k)",
                "id": "num_successes",
                "type": "number",
                "placeholder": "5",
            },
        ],
        "outputs": ["Probability"],
    },
    "poisson-distribution": {
        "title": "Poisson Distribution",
        "description": "Evaluate Poisson-distributed random events.",
        "url": "/tools/probability-tools/poisson-distribution",
        "inputs": [
            {
                "label": "Number of Events (k)",
                "id": "num_events",
                "type": "number",
                "placeholder": "3",
            },
            {
                "label": "Average Rate (λ)",
                "id": "rate",
                "type": "number",
                "placeholder": "5",
            },
        ],
        "outputs": ["Probability"],
    },
    "normal-distribution": {
        "title": "Normal Distribution",
        "description": "Compute probabilities for normally distributed variables.",
        "url": "/tools/probability-tools/normal-distribution",
        "inputs": [
            {
                "label": "Value (x)",
                "id": "value",
                "type": "number",
                "placeholder": "1.5",
            },
            {"label": "Mean (μ)", "id": "mean", "type": "number", "placeholder": "0"},
            {
                "label": "Standard Deviation (σ)",
                "id": "std_dev",
                "type": "number",
                "placeholder": "1",
            },
        ],
        "outputs": ["Probability"],
    },
    "t-distribution": {
        "title": "T-Distribution",
        "description": "Work with T-distributed data for small sample sizes.",
        "url": "/tools/probability-tools/t-distribution",
        "inputs": [
            {
                "label": "Value (t)",
                "id": "value",
                "type": "number",
                "placeholder": "2.5",
            },
            {
                "label": "Degrees of Freedom (df)",
                "id": "degrees_freedom",
                "type": "number",
                "placeholder": "10",
            },
        ],
        "outputs": ["Probability"],
    },
}
