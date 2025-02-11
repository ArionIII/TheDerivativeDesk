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
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import os
import openpyxl

import numpy as np
import scipy.stats as stats

def calculate_mean(dataset):
    """
    Calculate the mean of a dataset.
    """
    mean_value = np.mean(dataset)
    return {"mean_value": ("Mean Value :", str(mean_value))}

def calculate_median(dataset):
    """
    Calculate the median of a dataset.
    """
    dataset = np.array([float(x) for x in dataset])
    logger.warning(f"Calculating median for dataset: {dataset}")
    logger.warning(f"Type of dataset: {type(dataset)}")
    median_value = np.median(dataset)
    return {"median_value": ("Median Value :", str(median_value))}

def calculate_mode(dataset):
    """
    Calculate the mode of a dataset.
    """
    mode_result = stats.mode(dataset, keepdims=True)  # keepdims=True pour éviter FutureWarning
    mode_value = mode_result.mode.tolist()
    return {"mode_values": ("Mode Value(s) :", str(mode_value))}

def calculate_range(dataset):
    """
    Calculate the range of a dataset.
    """
    range_value = np.ptp(dataset)
    return {"range_value": ("Range Value :", str(range_value))}

def calculate_iqr(dataset):
    """
    Calculate the interquartile range of a dataset.
    """
    q1, q3 = np.percentile(dataset, [25, 75])
    iqr_value = q3 - q1
    return {"iqr_value": ("IQR Value :", str(iqr_value))}

def calculate_skewness(dataset):
    """
    Calculate the skewness of a dataset.
    """
    skewness_value = stats.skew(dataset, nan_policy="omit")
    return {"skewness_value": ("Skewness Value :", str(skewness_value))}

def calculate_kurtosis(dataset):
    """
    Calculate the kurtosis of a dataset.
    """
    kurtosis_value = stats.kurtosis(dataset, nan_policy="omit")
    return {"kurtosis_value": ("Kurtosis Value :", str(kurtosis_value))}

def perform_comprehensive_analysis(dataset):
    """
    Perform a full descriptive analysis on the dataset.
    """
    results = {
        "mean_value": calculate_mean(dataset)["mean_value"],
        "median_value": calculate_median(dataset)["median_value"],
        "mode_values": calculate_mode(dataset)["mode_values"],
        "range_value": calculate_range(dataset)["range_value"],
        "iqr_value": calculate_iqr(dataset)["iqr_value"],
        "skewness_value": calculate_skewness(dataset)["skewness_value"],
        "kurtosis_value": calculate_kurtosis(dataset)["kurtosis_value"],
    }
    return results


def t_test(sample_a, sample_b=None, test_type="One-Sample"):
    """
    Perform a t-test.
    """
    logger.info(f"Performing {test_type} t-test")
    signi = "The test is significant at the 0.05 level."
    not_signi = "The test is not significant at the 0.05 level."
    if test_type == "One-Sample":
        logger.info(f"Sample A: {sample_a}")
        t_stat, p_value = stats.ttest_1samp(sample_a, 0)  # Test against mean = 0
    elif test_type == "Two-Sample":
        logger.info(f"Sample A: {sample_a}")
        logger.info(f"Sample B: {sample_b}")
        t_stat, p_value = stats.ttest_ind(sample_a, sample_b, equal_var=False)
    else:
        raise ValueError("Invalid test type. Choose 'One-Sample' or 'Two-Sample'.")
    logger.info(f"t-statistic: {t_stat}, p-value: {p_value}")
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
    logger.info(f"Observed Frequencies: {observed}")    
    chi_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    logger.info(f"Chi-Square Statistic: {chi_stat}, P-Value: {p_value}")
    if isinstance(chi_stat, np.ndarray):
        chi_stat = chi_stat.sum()  # Additionner toutes les valeurs si plusieurs catégories
    if isinstance(p_value, np.ndarray):
        p_value = p_value.sum()  # Additionner toutes les valeurs
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
    return {"confidence_interval" : ("Confidence Interval :", (f"[{ci_lower} ; {ci_upper}"))}


def anova(group_a, group_b, group_c=None):
    """
    Perform ANOVA test.
    """
    logger.info(f"Group A: {group_a}")
    logger.info(f"Group B: {group_b}")
    logger.info(f"Group C: {group_c}")
    if group_c is not None and group_c!="":
        logger.info(f"Performing ANOVA test for three groups")
        f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
    else:
        logger.info(f"Performing ANOVA test for two groups")
        f_stat, p_value = stats.f_oneway(group_a, group_b)
    logger.info(f"F-Statistic: {f_stat}, P-Value: {p_value}")
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
    Supports:
    - `independent_variables` as a list of lists (each containing `n` values).
    - `dependent_variables` as a list of `n` values.
    """

    logger.warning(f"✅ Y length: {len(dependent_variables)}")
    logger.warning(f"✅ X number of variables: {len(independent_variables)}")
    for i, x_list in enumerate(independent_variables):
        logger.warning(f"✅ Independent Variable {i+1} Length: {len(x_list)}")

    # ✅ Transposer X pour qu'il soit sous forme (100,3) au lieu de (3,100)
    X = np.array(independent_variables).T  # (100,3)

    # ✅ Convertir `dependent_variables` en un vecteur (100,)
    Y = np.array(dependent_variables)  # (100,)

    logger.warning(f"📊 X shape: {X.shape}, Y shape: {Y.shape}")

    # Vérifier que les dimensions correspondent
    if X.shape[0] != Y.shape[0]:
        raise ValueError(f"❌ Mismatch: X has {X.shape[0]} rows but Y has {Y.shape[0]} rows.")

    # Régression multiple
    model = LinearRegression()
    model.fit(X, Y)

    predictions = model.predict(X)
    r_squared = r2_score(Y, predictions)
    mse = mean_squared_error(Y, predictions)

    return {
        "coefficients": ("Coefficients :", model.coef_.tolist()),
        "intercept": ("Intercept :", model.intercept_),
        "r_squared": ("R-Squared :", r_squared),
        "mean_squared_error": ("Mean Squared Error :", mse),
    }


def calculate_pdf(value, mean, std_dev):
    try:
        pdf_value = norm.pdf(value, loc=mean, scale=std_dev)
        return ({"pdf_value" : ("PDF Value :", pdf_value)})
    except Exception as e:
        return ({"error": str(e)}), 400

def calculate_cdf(value, mean, std_dev):
    try:
        cdf_value = norm.cdf(value, loc=mean, scale=std_dev)
        return {"cdf_value": ("CDF Value :", cdf_value)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def calculate_z_score(value, mean, std_dev):
    try:
        z_score = (value - mean) / std_dev
        return {"z_score": ("Z-Score :", z_score)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def calculate_binomial(num_trials, prob_success, num_successes):
    try:
        probability = binom.pmf(num_successes, num_trials, prob_success)
        return {"binomial_probability": ("Binomial Probability :", probability)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def calculate_poisson(num_events, rate):
    try:
        probability = poisson.pmf(num_events, rate)
        return {"poisson_probability": ("Poisson Probability :", probability)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def calculate_normal_distribution(value, mean, std_dev):
    try:
        probability = norm.cdf(value, loc=mean, scale=std_dev)
        return {"normal_distribution_probability": ("Normal Distribution Probability :", probability)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def calculate_t_distribution(value, degrees_freedom):
    try:
        probability = t.cdf(value, degrees_freedom)
        return {"t_distribution_probability": ("T-Distribution Probability :", probability)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400


def calculate_moving_averages(dataset, window_size, output_path="static/outputs/statistics/"):
    """
    Compute moving averages for a given dataset and save results in both CSV and XLSX formats.

    Parameters:
    - dataset: A list of numbers (single series) or a dictionary of lists (multiple series).
    - window_size: The window size for the moving average calculation.
    - output_path: Path to save the resulting CSV and XLSX files.

    Returns:
    - A tuple (csv_path, xlsx_path) containing the paths to the saved files.
    """
    try:
        # Vérifier et créer le répertoire de sortie si nécessaire
        os.makedirs(output_path, exist_ok=True)

        window_size = int(window_size)  # Convert window_size to integer
        logger.info(f"Window Size: {window_size}")

        if isinstance(dataset, list):
            # Cas d'une seule colonne : convertir en DataFrame
            df = pd.DataFrame({"Series": dataset})
            df["Moving_Average"] = df["Series"].rolling(window=window_size).mean()
            df_output = df.copy()

        elif isinstance(dataset, dict):
            # Aligner toutes les colonnes sur la même longueur
            max_length = max(len(v) for v in dataset.values())
            dataset_aligned = {
                key: v + [np.nan] * (max_length - len(v)) for key, v in dataset.items()
            }
            df = pd.DataFrame(dataset_aligned)

            # Calcul des moyennes mobiles
            moving_averages = df.rolling(window=window_size).mean()

            # Réintégrer les noms des colonnes en haut du fichier
            df_output = pd.DataFrame(columns=df.columns)  # Créer un header
            df_output = pd.concat([df_output, moving_averages], ignore_index=True)
        else:
            raise ValueError("Invalid dataset format. Expected list or dict of lists.")

        # Supprimer les lignes vides uniquement si toutes les colonnes sont NaN
        df_output.dropna(inplace=True, how="all")

        # Générer un nom de fichier unique
        random_file_name = f"moving_average_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV (compatible Excel)
        df_output.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df_output.to_excel(xlsx_path, index=False, engine="openpyxl")

        logger.info(f"Moving averages saved to: {csv_path} and {xlsx_path}")
        return csv_path, xlsx_path

    except Exception as e:
        logger.error(f"Error computing moving averages: {e}")
        return {"error": f"Error computing moving averages: {e}"}, 400


def calculate_exponential_smoothing(dataset, smoothing_factor):
    try:
        dataset = list(map(float, dataset))  # Convert to float
        smoothed = []
        for i, value in enumerate(dataset):
            if i == 0:
                smoothed.append(value)  # Initialize with the first value
            else:
                smoothed.append(smoothing_factor * value + (1 - smoothing_factor) * smoothed[i-1])
        return {"exponential_smoothing": ("Smoothed Time Series :", smoothed)}
    except Exception as e:
        return {"error": ("Error :", str(e))}, 400


def calculate_autocorrelation(dataset, lag_order=1):
    try:
        dataset = list(map(float, dataset))  # Convert to float
        n = len(dataset)
        mean = sum(dataset) / n
        lagged_series = dataset[lag_order:]
        original_series = dataset[:-lag_order]
        numerator = sum(
            (original_series[i] - mean) * (lagged_series[i] - mean) 
            for i in range(len(lagged_series))
        )
        denominator = sum((x - mean) ** 2 for x in dataset)
        autocorrelation = numerator / denominator
        return {"autocorrelation": ("Autocorrelation :", autocorrelation)}
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
        return {"transition_matrix": ("Transition Matrix :", matrix)}
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
        return {"simulation_paths": ("Simulation Paths :", simulations)}
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
        return {"simulation_results": ("Simulation Results :", outcomes)}
    except Exception as e:
        return {"error": str(e)}, 400

# Bayesian Updating
def perform_bayesian_updating(prior, likelihood, evidence):
    try:
        updated_probability = (likelihood * prior) / evidence
        return {"updated_probability": ("Updated Probability :", updated_probability)}
    except Exception as e:
        return {"error": str(e)}, 400
    
def calculate_matrix_multiplication(matrix_a, matrix_b):
    try:
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        result = np.matmul(a, b)
        return {"matrix_product": ("Matrix Product :", result.tolist())}
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_inverse_matrix(matrix):
    try:
        mat = np.array(matrix)
        inverse = np.linalg.inv(mat)
        return {"inverse_matrix": ("Inverse Matrix :", inverse.tolist())}
    except Exception as e:
        return {"error": str(e)}, 400

def perform_svd(matrix):
    try:
        mat = np.array(matrix)
        u, sigma, v_transposed = np.linalg.svd(mat)
        return {
    "u_matrix": ("U Matrix :", u.tolist()),
    "sigma_values": ("Sigma (Singular Values) :", sigma.tolist()),
    "v_transposed": ("V Transposed :", v_transposed.tolist()),
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
    "principal_components": ("Principal Components :", v.tolist()),
    "explained_variance": ("Explained Variance :", explained_variance.tolist()),
}
    except Exception as e:
        return {"error": str(e)}, 400

def calculate_eigenvalues_eigenvectors(matrix):
    try:
        mat = np.array(matrix)
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        return {
    "eigenvalues": ("Eigenvalues :", eigenvalues.tolist()),
    "eigenvectors": ("Eigenvectors :", eigenvectors.tolist()),
}
    except Exception as e:
        return {"error": str(e)}, 400

def determine_best_model(dataset):
    """
    Détermine si la série suit un modèle AR, MA ou ARMA et trouve les meilleurs paramètres (p, q).
    """
    # 1. Vérifier la stationnarité (ADF Test)
    result = adfuller(dataset)
    is_stationary = result[1] < 0.05  # p-value < 0.05 → série stationnaire
    
    if not is_stationary:
        dataset = pd.Series(dataset)
        print("La série n'est pas stationnaire. On applique une différenciation.")
        dataset = dataset.diff().dropna().tolist()  # Appliquer la différenciation pour stationnariser

    # 2. Calculer ACF et PACF
    lag_acf = acf(dataset, nlags=10)
    lag_pacf = pacf(dataset, nlags=10)

    # 3. Déterminer p et q en regardant où l'ACF/PACF coupent brusquement
    p = np.argmax(lag_pacf < 0.2)  # PACF coupe → AR(p)
    q = np.argmax(lag_acf < 0.2)   # ACF coupe → MA(q)
    
    # Si aucun des deux ne coupe net, tester ARMA avec plusieurs valeurs
    best_aic = np.inf
    best_order = (p, 0, q)  # Default: ARMA(p, q)
    
    for p_try in range(4):  # Tester jusqu'à AR(3)
        for q_try in range(4):  # Tester jusqu'à MA(3)
            try:
                model = ARIMA(dataset, order=(p_try, 0, q_try))
                result = model.fit()
                if result.aic < best_aic:
                    best_aic = result.aic
                    best_order = (p_try, 0, q_try)
            except:
                continue
    
    print(f"Modèle sélectionné : ARMA{best_order} (basé sur AIC={best_aic})")
    return (best_order, best_aic)



def forecast_series(dataset, n_previsions, temporal_step):
    """
    Applique le modèle ARMA optimal et prédit les prochaines valeurs en utilisant un index numérique.
    """
    # Vérifier que temporal_step est un entier valide
    try:
        temporal_step = int(temporal_step)
        n_previsions = int(n_previsions)
    except ValueError:
        logger.error(f"Invalid format: temporal_step={temporal_step}, n_previsions={n_previsions}")
        return {"error": "Temporal Step and Number of Predictions must be integers."}, 400

    # Générer un index numérique basé sur temporal_step
    start_index = 0  # Index de départ
    time_index = np.arange(start_index, start_index + len(dataset) * temporal_step, temporal_step)

    # Convertir dataset en Pandas Series avec un index numérique
    dataset = pd.Series(dataset, index=time_index)
    logger.info(f"Dataset transformed into numerical index with step {temporal_step}.")

    # Trouver le meilleur modèle (AR, MA, ARMA)
    best_order, best_aic = determine_best_model(dataset)
    model = ARIMA(dataset, order=best_order)
    logger.info("Model has been chosen")
    result = model.fit()
    logger.info("Model has been fitted")

    # 🛠 Correction du problème avec forecast_index
    last_index = time_index[-1]  # Dernier point observé
    forecast_index = np.arange(last_index + temporal_step, last_index + (n_previsions + 1) * temporal_step, temporal_step)

    # Vérification des valeurs de forecast_index
    if forecast_index[0] <= last_index:
        logger.error(f"Invalid forecast index: {forecast_index}")
        return {"error": "Forecast index must start after the last observed index."}, 400

    # Faire la prévision
    forecast = result.forecast(steps=n_previsions)
    forecast_series = pd.Series(forecast, index=forecast_index)

    logger.info("Forecast has been made")
    logger.info("End AR-MA-ARMA")

    return forecast_series.to_dict()  # Retourner en format dict pour API

def compute_log_returns_csv_xlsx(dataset, output_path="static/outputs/statistics/"):
    """
    Compute log returns for a given dataset and save results in both CSV and XLSX formats.

    Parameters:
    - dataset: A list of numbers (single series) or a dictionary of lists (multiple series).
    - output_path: Path to save the resulting CSV and XLSX files.

    Returns:
    - A tuple (csv_path, xlsx_path) containing the paths to the saved files.
    """
    try:
        # Vérifier et créer le répertoire de sortie si nécessaire
        os.makedirs(output_path, exist_ok=True)

        if isinstance(dataset, list):
            # Cas d'une seule colonne : convertir en DataFrame
            df = pd.DataFrame({"Series": dataset})
            df["Log_Returns"] = np.log(df["Series"] / df["Series"].shift(1))
            df_output = df.copy()
        elif isinstance(dataset, dict):
            # Aligner toutes les colonnes sur la même longueur
            max_length = max(len(v) for v in dataset.values())
            dataset_aligned = {
                key: v + [np.nan] * (max_length - len(v)) for key, v in dataset.items()
            }
            df = pd.DataFrame(dataset_aligned)

            # Calcul des log-returns
            log_returns = np.log(df / df.shift(1))

            # Réintégrer les noms des colonnes en haut du fichier
            df_output = pd.DataFrame(columns=df.columns)  # Créer un header
            df_output = pd.concat([df_output, log_returns], ignore_index=True)
        else:
            raise ValueError("Invalid dataset format. Expected list or dict of lists.")

        # Supprimer les lignes vides uniquement si toutes les colonnes sont NaN
        df_output.dropna(inplace=True, how="all")

        # Générer un nom de fichier unique
        random_file_name = f"log_returns_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV (compatible Excel)
        df_output.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df_output.to_excel(xlsx_path, index=False, engine="openpyxl")

        logger.info(f"Log returns saved to: {csv_path} and {xlsx_path}")
        return csv_path, xlsx_path
    except Exception as e:
        raise ValueError(f"Error computing log returns: {e}")
