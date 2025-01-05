import numpy as np
import scipy.stats as stats

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
    if test_type == "One-Sample":
        t_stat, p_value = stats.ttest_1samp(sample_a, 0)  # Test against mean = 0
    elif test_type == "Two-Sample":
        t_stat, p_value = stats.ttest_ind(sample_a, sample_b, equal_var=False)
    else:
        raise ValueError("Invalid test type. Choose 'One-Sample' or 'Two-Sample'.")
    return {"t-Statistic": t_stat, "P-Value": p_value}


def z_test(sample_mean, population_mean, std_dev, sample_size):
    """
    Perform a z-test.
    """
    z_stat = (sample_mean - population_mean) / (std_dev / np.sqrt(sample_size))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return {"z-Statistic": z_stat, "P-Value": p_value}


def chi_square_test(observed, expected):
    """
    Perform a chi-square test.
    """
    chi_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    return {"Chi-Square Statistic": chi_stat, "P-Value": p_value}


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
    return {"F-Statistic": f_stat, "P-Value": p_value}


def simple_regression(x, y):
    """
    Perform simple linear regression (y = mx + b).
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return {
        "Slope (m)": slope,
        "Intercept (b)": intercept,
        "R-Squared": r_value**2,
        "P-Value": p_value,
        "Standard Error": std_err,
    }


def multiple_regression(X, y):
    """
    Perform multiple linear regression.
    X: 2D array-like (independent variables)
    y: 1D array-like (dependent variable)
    """
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    coefficients = model.coef_
    intercept = model.intercept_
    r_squared = model.score(X, y)
    return {
        "Coefficients": coefficients.tolist(),
        "Intercept": intercept,
        "R-Squared": r_squared,
    }

def calculate_pdf_cdf(distribution, parameters):
    """
    Compute PDF and CDF for a given distribution.
    """
    if distribution == "Normal":
        mean, std = parameters.get("mean", 0), parameters.get("std", 1)
        x = parameters.get("x", 0)
        pdf_value = stats.norm.pdf(x, mean, std)
        cdf_value = stats.norm.cdf(x, mean, std)
    elif distribution == "Binomial":
        n, p, x = parameters.get("n"), parameters.get("p"), parameters.get("x")
        pdf_value = stats.binom.pmf(x, n, p)
        cdf_value = stats.binom.cdf(x, n, p)
    elif distribution == "Poisson":
        mu, x = parameters.get("mu"), parameters.get("x")
        pdf_value = stats.poisson.pmf(x, mu)
        cdf_value = stats.poisson.cdf(x, mu)
    elif distribution == "T-Distribution":
        df, x = parameters.get("df"), parameters.get("x")
        pdf_value = stats.t.pdf(x, df)
        cdf_value = stats.t.cdf(x, df)
    else:
        raise ValueError("Unsupported distribution type.")
    return {"PDF Value": pdf_value, "CDF Value": cdf_value}

def calculate_z_score(data_point, mean, std_dev):
    """
    Calculate the z-score of a data point.
    """
    z_score = (data_point - mean) / std_dev
    return {"Z-Score": z_score}
