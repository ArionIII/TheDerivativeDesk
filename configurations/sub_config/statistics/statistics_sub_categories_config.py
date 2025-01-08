from flask import Blueprint, render_template

tool_category_statistics_routes = Blueprint("tool_category_statistics_routes", __name__)

STATISTICS_TOOL_CATEGORIES = {
    # Descriptive Statistics
    "descriptive-analysis": {
        "title": "Descriptive Analysis",
        "description": "Summarize datasets with metrics such as mean, median, mode, range, IQR, skewness, and kurtosis.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Mean", "description": "Calculate the average value of a dataset.", "url": "/tools/descriptive-analysis/mean"},
            {"title": "Median", "description": "Determine the middle value in an ordered dataset.", "url": "/tools/descriptive-analysis/median"},
            {"title": "Mode", "description": "Identify the most frequent value(s) in a dataset.", "url": "/tools/descriptive-analysis/mode"},
            {"title": "Range", "description": "Calculate the difference between the maximum and minimum values.", "url": "/tools/descriptive-analysis/range"},
            {"title": "Interquartile Range (IQR)", "description": "Compute the spread of the middle 50% of the data.", "url": "/tools/descriptive-analysis/iqr"},
            {"title": "Skewness", "description": "Measure the asymmetry of the probability distribution of a dataset.", "url": "/tools/descriptive-analysis/skewness"},
            {"title": "Kurtosis", "description": "Evaluate the 'tailedness' of the data distribution.", "url": "/tools/descriptive-analysis/kurtosis"},
            {"title": "Comprehensive Analysis",
            "description": "Perform a full descriptive analysis on the dataset, including mean, median, mode, range, IQR, skewness, and kurtosis.",
            "url": "/tools/descriptive-analysis/comprehensive-basic-analysis"},
        ],
    },
    # Inferential Statistics
    "inferential-statistics": {
        "title": "Inferential Statistics",
        "description": "Perform hypothesis testing, confidence intervals, p-value calculations, and regression analysis.",
        "parent_category": "statistics",
        "tools": [
            {"title": "t-test", "description": "Perform a t-test to compare means of two groups.", "url": "/tools/inferential-statistics/t-test"},
            {"title": "z-test", "description": "Conduct a z-test for hypothesis testing of large sample sizes.", "url": "/tools/inferential-statistics/z-test"},
            {"title": "Chi-Square Test", "description": "Evaluate the independence of categorical variables.", "url": "/tools/inferential-statistics/chi-square"},
            {"title": "Confidence Intervals", "description": "Calculate intervals to estimate population parameters.", "url": "/tools/inferential-statistics/confidence-intervals"},
            {"title": "P-Value Calculation", "description": "Determine the p-value for hypothesis testing.", "url": "/tools/inferential-statistics/p-value"},
            {"title": "ANOVA (Analysis of Variance)", "description": "Analyze differences between group means in datasets.", "url": "/tools/inferential-statistics/anova"},
            {"title": "Simple Regression", "description": "Perform simple linear regression analysis.", "url": "/tools/inferential-statistics/simple-regression"},
            {"title": "Multiple Regression", "description": "Conduct multiple regression for multivariate datasets.", "url": "/tools/inferential-statistics/multiple-regression"},
        ],
    },
    # Probability Tools
    "probability-tools": {
        "title": "Probability Tools",
        "description": "Work with probability density functions, cumulative functions, and statistical distributions.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Probability Density Function (PDF)", "description": "Calculate the PDF for continuous random variables.", "url": "/tools/probability-tools/pdf"},
            {"title": "Cumulative Distribution Function (CDF)", "description": "Compute the cumulative probability of random variables.", "url": "/tools/probability-tools/cdf"},
            {"title": "Z-Score Calculation", "description": "Find the Z-score to standardize data points.", "url": "/tools/probability-tools/z-score"},
            {"title": "Binomial Distribution", "description": "Analyze binomial random variables and probabilities.", "url": "/tools/probability-tools/binomial-distribution"},
            {"title": "Poisson Distribution", "description": "Evaluate Poisson-distributed random events.", "url": "/tools/probability-tools/poisson-distribution"},
            {"title": "Normal Distribution", "description": "Compute probabilities for normally distributed variables.", "url": "/tools/probability-tools/normal-distribution"},
            {"title": "T-Distribution", "description": "Work with T-distributed data for small sample sizes.", "url": "/tools/probability-tools/t-distribution"},
        ],
    },
    # Time Series Analysis
    "time-series-analysis": {
        "title": "Time Series Analysis",
        "description": "Analyze trends in temporal data using techniques like moving averages and autocorrelation.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Moving Averages", "description": "Calculate moving averages for time series smoothing.", "url": "/tools/time-series-analysis/moving-averages"},
            {"title": "Exponential Smoothing", "description": "Perform exponential smoothing for forecasting.", "url": "/tools/time-series-analysis/exponential-smoothing"},
            {"title": "Autocorrelation", "description": "Analyze the correlation of a time series with its own lags.", "url": "/tools/time-series-analysis/autocorrelation"},
        ],
    },
    # Markov Chains and Random Walks
    "markov-chains-and-random-walks": {
        "title": "Markov Chains and Random Walks",
        "description": "Simulate stochastic processes and study random walks using transition matrices.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Transition Matrices", "description": "Construct and analyze transition matrices for Markov Chains.", "url": "/tools/markov-chains-and-random-walks/transition-matrices"},
            {"title": "Simulation of Random Walks", "description": "Simulate random walks and analyze their outcomes.", "url": "/tools/markov-chains-and-random-walks/random-walks"},
        ],
    },
    # Monte Carlo Simulations
    "monte-carlo-simulations": {
        "title": "Monte Carlo Simulations",
        "description": "Generate random samples for simulating outcomes and conducting risk analysis.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Monte Carlo Simulations", "description": "Perform Monte Carlo simulations to estimate outcomes.", "url": "/tools/monte-carlo-simulations/monte-carlo"},
        ],
    },
    # Bayesian Analysis
    "bayesian-analysis": {
        "title": "Bayesian Analysis",
        "description": "Perform Bayesian updates and calculate prior, likelihood, and posterior probabilities.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Bayesian Updating", "description": "Update beliefs using Bayesian probabilities.", "url": "/tools/bayesian-analysis/bayesian-updating"},
        ],
    },
    # Linear Algebra Tools
    "linear-algebra": {
        "title": "Linear Algebra Tools",
        "description": "Perform fundamental matrix operations like multiplication and inversion.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Matrix Multiplication", "description": "Compute the product of matrices.", "url": "/tools/linear-algebra-tools/matrix-multiplication"},
            {"title": "Inverse Matrices", "description": "Calculate the inverse of a matrix.", "url": "/tools/linear-algebra-tools/inverse-matrices"},
            {"title": "Singular Value Decomposition (SVD)", "description": "Perform SVD for dimensionality reduction and feature extraction.", "url": "/tools/linear-algebra-tools/svd"},
        ],
    },
    # Advanced Calculations
    "advanced-calculations": {
        "title": "Advanced Calculations",
        "description": "Apply advanced mathematical tools like PCA, eigenvalues, and eigenvectors.",
        "parent_category": "statistics",
        "tools": [
            {"title": "Principal Component Analysis (PCA)", "description": "Conduct PCA for feature extraction and data compression.", "url": "/tools/advanced-calculations/pca"},
            {"title": "Eigenvalues and Eigenvectors", "description": "Compute eigenvalues and eigenvectors for matrix transformations.", "url": "/tools/advanced-calculations/eigenvalues"},
        ],
    },
}


@tool_category_statistics_routes.route("/tools/statistics/<category_key>")
def render_statistics_tool_category(category_key):
    category = STATISTICS_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)
