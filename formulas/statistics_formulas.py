import numpy as np
import scipy.stats as stats
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import norm, t
from scipy.stats import binom, poisson
from config import logger
import math
import random

def calculate_mean(dataset):
    """
    Calculate the mean of a dataset.
    """
    mean_value = np.mean(dataset)
    return {"Mean Value": mean_value}


def calculate_median(dataset):
    """
    Calculate the median of a dataset.
    """
    median_value = np.median(dataset)
    return {"Median Value": median_value}


def calculate_mode(dataset):
    """
    Calculate the mode of a dataset.
    """
    mode_value = stats.mode(dataset)
    return {"Mode Value(s)": mode_value.mode.tolist()}


def calculate_range(dataset):
    """
    Calculate the range of a dataset.
    """
    range_value = np.ptp(dataset)
    return {"Range Value": range_value}


def calculate_iqr(dataset):
    """
    Calculate the interquartile range of a dataset.
    """
    q1, q3 = np.percentile(dataset, [25, 75])
    iqr_value = q3 - q1
    return {"IQR Value": iqr_value}


def calculate_skewness(dataset):
    """
    Calculate the skewness of a dataset.
    """
    skewness_value = stats.skew(dataset)
    return {"Skewness Value": skewness_value}


def calculate_kurtosis(dataset):
    """
    Calculate the kurtosis of a dataset.
    """
    kurtosis_value = stats.kurtosis(dataset)
    return {"Kurtosis Value": kurtosis_value}

def perform_comprehensive_analysis(dataset):
    """
    Perform a full descriptive analysis on the dataset.
    """
    results = {
        "mean_value": ("Mean Value : ", calculate_mean(dataset)["Mean Value"]),
        "median_value": ("Median Value : ", calculate_median(dataset)["Median Value"]),
        "mode_values": ("Mode Value(s) : ", calculate_mode(dataset)["Mode Value(s)"]),
        "range_value": ("Range Value : ", calculate_range(dataset)["Range Value"]),
        "iqr_value": ("IQR Value : ", calculate_iqr(dataset)["IQR Value"]),
        "skewness_value": ("Skewness Value : ", calculate_skewness(dataset)["Skewness Value"]),
        "kurtosis_value": ("Kurtosis Value : ", calculate_kurtosis(dataset)["Kurtosis Value"]),
    }
    return results

def t_test(sample_a, sample_b=None, test_type="One-Sample"):
    """
    Perform a t-test.
    """
    signi = "The test is significant at the 0.05 level."
    not_signi = "The test is not significant at the 0.05 level."
    if test_type == "One-Sample":
        t_stat, p_value = stats.ttest_1samp(sample_a, 0)  # Test against mean = 0
    elif test_type == "Two-Sample":
        t_stat, p_value = stats.ttest_ind(sample_a, sample_b, equal_var=False)
    else:
        raise ValueError("Invalid test type. Choose 'One-Sample' or 'Two-Sample'.")
    return {"t_statistic" : ("t-Statistic :", t_stat), "p_value" : ("P-Value : ", f"{p_value} : {signi if p_value <= 0.05 else not_signi}")}


def z_test(sample_mean, population_mean, std_dev, sample_size):
    """
    Perform a z-test.
    """
    z_stat = (sample_mean - population_mean) / (std_dev / np.sqrt(sample_size))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return {
    "z_statistic": ("z-Statistic :", z_stat), 
    "p_value": ("P-Value : ", f"{p_value} : {'Significant' if p_value <= 0.05 else 'Not Significant'}")
}




def chi_square_test(observed, expected):
    """
    Perform a chi-square test.
    """
    chi_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    return {
    "chi_square_statistic": ("Chi-Square Statistic :", chi_stat), 
    "p_value": ("P-Value : ", f"{p_value} : {'Significant' if p_value <= 0.05 else 'Not Significant'}")
}




def calculate_confidence_intervals(sample_mean, std_dev, sample_size, confidence_level):
    """
    Calculate confidence intervals for a sample.
    """
    z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    margin_error = z_score * (std_dev / np.sqrt(sample_size))
    ci_lower = sample_mean - margin_error
    ci_upper = sample_mean + margin_error
    return {"Confidence Interval": (ci_lower, ci_upper)}


def anova(group_a, group_b, group_c=None):
    """
    Perform ANOVA test.
    """
    if group_c is not None:
        f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
    else:
        f_stat, p_value = stats.f_oneway(group_a, group_b)
    return {
    "f_statistic": ("F-Statistic :", f_stat), 
    "p_value": ("P-Value : ", f"{p_value} : {'Significant' if p_value <= 0.05 else 'Not Significant'}")
}

def calculate_p_value(test_statistic: float, distribution_type: str, degrees_of_freedom: int = None) -> dict:
    """
    Calculate the p-value for a given test statistic based on the distribution type.
    
    Parameters:
    - test_statistic (float): The test statistic value.
    - distribution_type (str): Type of distribution ("Normal" or "T-Distribution").
    - degrees_of_freedom (int, optional): Degrees of freedom (required for T-Distribution).
    
    Returns:
    - dict: A dictionary containing the p-value and details of the calculation.
    """
    try:
        distribution_type = distribution_type.lower()
        if distribution_type == "normal":
            # Two-tailed p-value for normal distribution
            p_value = 2 * (1 - norm.cdf(abs(test_statistic)))
        elif distribution_type == "t-distribution":
            if degrees_of_freedom is None:
                raise ValueError("Degrees of freedom must be provided for T-Distribution.")
            # Two-tailed p-value for t-distribution
            p_value = 2 * (1 - t.cdf(abs(test_statistic), df=degrees_of_freedom))
        else:
            raise ValueError("Unsupported distribution type. Use 'Normal' or 'T-Distribution'.")
        
        return {
    "p_value": ("P-Value :", f"{p_value} : {'Significant' if p_value <= 0.05 else 'Not Significant'}"),
}

    except Exception as e:
        return {"Error": str(e)}


def simple_regression(independent_variable, dependent_variable):
    """
    Perform simple linear regression analysis.
    """
    if len(independent_variable) != len(dependent_variable):
        raise ValueError("Input arrays x and y must have the same length.")
    
    # Using scipy's linregress
    slope, intercept, r_value, p_value, std_err = linregress(independent_variable, dependent_variable)
    
    return {
        "slope": ("Slope :", slope),
        "intercept": ("Intercept :", intercept),
        "r_squared": ("R-Squared :", r_value**2),
        "p_value": ("P-Value :", f"{p_value} : {'Significant' if p_value <= 0.05 else 'Not Significant'}"),
        "std_err": ("Standard Error :", std_err),
    }


def multiple_regression(independent_variables, dependent_variables):
    """
    Perform multiple linear regression analysis.
    """
    # Ensure X is a 2D array
    X = np.array(independent_variables)
    y = np.array(dependent_variables)

    if len(X.shape) == 1:
        X = X.reshape(-1, 1)  # Convert to 2D if it's a single feature
    
    if len(y) != X.shape[0]:
        raise ValueError("The number of rows in X must match the length of y.")
    
    # Using sklearn's LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    r_squared = r2_score(y, predictions)
    mse = mean_squared_error(y, predictions)
    
    return {
        "coefficients": ("Coefficients ", model.coef_.tolist()),
        "intercept": ("Intercept ", model.intercept_),
        "r_squared": ("R-Squared ", r_squared),
        "mean_squared_error": ("Mean Squared Error ", mse),
    }

def calculate_pdf(value, mean, std_dev):
    try:
        pdf_value = norm.pdf(value, loc=mean, scale=std_dev)
        return ({"PDF Value": pdf_value})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_cdf(value, mean, std_dev):
    try:
        cdf_value = norm.cdf(value, loc=mean, scale=std_dev)
        return ({"CDF Value": cdf_value})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_z_score(value, mean, std_dev):
    try:
        z_score = (value - mean) / std_dev
        return ({"Z-Score": z_score})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_binomial(num_trials, prob_success, num_successes):
    try:
        probability = binom.pmf(num_successes, num_trials, prob_success)
        return ({"Probability": probability})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_poisson(num_events, rate):
    try:
        probability = poisson.pmf(num_events, rate)
        return ({"Probability": probability})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_normal_distribution(value, mean, std_dev):
    try:
        probability = norm.cdf(value, loc=mean, scale=std_dev)
        return ({"Probability": probability})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_t_distribution(value, degrees_freedom):
    try:
        probability = t.cdf(value, degrees_freedom)
        return ({"Probability": probability})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_moving_averages(time_series, window_size):
    logger.info(f"Calculating moving averages for time series: {time_series}")
    try:
        time_series = list(map(float, time_series))  # Convert to float
        window_size = int(window_size)  # Convert window_size to integer
        logger.info(f"Window Size: {window_size}")
        smoothed = [
            sum(time_series[i:i + window_size]) / window_size 
            for i in range(len(time_series) - window_size + 1)
        ]
        logger.info(f"Smoothed Time Series: {smoothed}")
        return {"Smoothed Time Series": smoothed}
    except Exception as e:
        logger.error(f"Error in calculate_moving_averages: {e}")
        return {"error": str(e)}, 400

def calculate_exponential_smoothing(time_series, smoothing_factor):
    try:
        time_series = list(map(float, time_series))  # Convert to float
        smoothed = []
        for i, value in enumerate(time_series):
            if i == 0:
                smoothed.append(value)  # Initialize with the first value
            else:
                smoothed.append(smoothing_factor * value + (1 - smoothing_factor) * smoothed[i-1])
        return {"Smoothed Time Series": smoothed}
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_autocorrelation(time_series, lag_order=1):
    try:
        time_series = list(map(float, time_series))  # Convert to float
        n = len(time_series)
        mean = sum(time_series) / n
        lagged_series = time_series[lag_order:]
        original_series = time_series[:-lag_order]
        numerator = sum(
            (original_series[i] - mean) * (lagged_series[i] - mean) 
            for i in range(len(lagged_series))
        )
        denominator = sum((x - mean) ** 2 for x in time_series)
        autocorrelation = numerator / denominator
        return {"Autocorrelation": autocorrelation}
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_transition_matrices(state_sequence, num_states):
    try:
        state_sequence = list(map(int, state_sequence))  # Convert to int
        num_states = int(num_states)
        matrix = [[0] * num_states for _ in range(num_states)]
        for i in range(len(state_sequence) - 1):
            current_state = state_sequence[i]
            next_state = state_sequence[i+1]
            matrix[current_state-1][next_state-1] += 1

        for row in matrix:
            row_sum = sum(row)
            if row_sum > 0:
                for i in range(len(row)):
                    row[i] /= row_sum
        return {"Transition Matrix": matrix}
    except Exception as e:
        return {"error": str(e)}, 400

def simulate_random_walk(num_steps, num_simulations, step_size=1):
    try:
        num_steps = int(num_steps)
        num_simulations = int(num_simulations)
        step_size = float(step_size)
        simulations = []
        for _ in range(num_simulations):
            position = 0
            walk = [position]
            for _ in range(num_steps):
                step = random.choice([-step_size, step_size])
                position += step
                walk.append(position)
            simulations.append(walk)
        return {"Simulation Paths": simulations}
    except Exception as e:
        return {"error": str(e)}, 400

# Monte Carlo Simulations
def perform_monte_carlo_simulations(num_simulations, random_seed=None):
    try:
        # Ensure num_simulations is an integer
        num_simulations = int(num_simulations)
        
        if random_seed is not None:
            random.seed(random_seed)
        
        # Generate random outcomes
        outcomes = [random.random() for _ in range(num_simulations)]
        return {"Simulation Results": outcomes}
    except Exception as e:
        return {"error": str(e)}, 400

# Bayesian Updating
def perform_bayesian_updating(prior, likelihood, evidence):
    try:
        updated_probability = (likelihood * prior) / evidence
        return {"Updated Probability": updated_probability}
    except Exception as e:
        return {"error": str(e)}, 400
    
def calculate_matrix_multiplication(matrix_a, matrix_b):
    try:
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        result = np.matmul(a, b)
        return {"Matrix Product": result.tolist()}
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_inverse_matrix(matrix):
    try:
        mat = np.array(matrix)
        inverse = np.linalg.inv(mat)
        return {"Inverse Matrix": inverse.tolist()}
    except Exception as e:
        return {"error": str(e)}, 400

def perform_svd(matrix):
    try:
        mat = np.array(matrix)
        u, sigma, v_transposed = np.linalg.svd(mat)
        return {
            "U Matrix": u.tolist(),
            "Sigma (Singular Values)": sigma.tolist(),
            "V Transposed": v_transposed.tolist(),
        }
    except Exception as e:
        return {"error": str(e)}, 400

def perform_pca(data_matrix):
    try:
        data = np.array(data_matrix)
        mean_centered = data - np.mean(data, axis=0)
        u, s, v = np.linalg.svd(mean_centered, full_matrices=False)
        explained_variance = (s**2) / (len(data) - 1)
        return {
            "Principal Components": v.tolist(),
            "Explained Variance": explained_variance.tolist(),
        }
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_eigenvalues_eigenvectors(matrix):
    try:
        mat = np.array(matrix)
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        return {
            "Eigenvalues": eigenvalues.tolist(),
            "Eigenvectors": eigenvectors.tolist(),
        }
    except Exception as e:
        return {"error": str(e)}, 400
