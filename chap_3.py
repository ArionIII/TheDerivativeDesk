import numpy as np
from config import logger

def compute_basis_hedge(asset_price, futures_price_contract):
    """
    Compute the basis hedge, which is the difference between the spot asset price 
    and the futures contract price.

    Args:
        asset_price (float): Price of the spot asset.
        futures_price_contract (float): Price of the futures contract.

    Returns:
        float: The basis hedge.

    Raises:
        ValueError: If any input is not a float or is None.
    """
    if not isinstance(asset_price, (int, float)) or not isinstance(futures_price_contract, (int, float)):
        raise ValueError("Both inputs must be numeric (int or float).")

    return asset_price - futures_price_contract

def compute_minimum_variance_hedge_ratio(std_change_spot, std_change_futures, correlation):
    """
    Compute the minimum variance hedge ratio.

    Args:
        std_change_spot (float): Standard deviation of changes in the spot asset price.
        std_change_futures (float): Standard deviation of changes in the futures price.
        correlation (float): Correlation coefficient between the spot and futures prices.

    Returns:
        float: The minimum variance hedge ratio.

    Raises:
        ValueError: If inputs are invalid or standard deviations are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [std_change_spot, std_change_futures, correlation]):
        raise ValueError("All inputs must be numeric (int or float).")
    if std_change_spot <= 0 or std_change_futures <= 0:
        raise ValueError("Standard deviations must be positive.")

    return correlation * (std_change_spot / std_change_futures)

def compute_variance(series):
    """
    Compute the variance of a statistical series.

    Args:
        series (list or np.array): Series of numerical data.

    Returns:
        float: The variance of the series.

    Raises:
        ValueError: If the series is empty or contains non-numeric data.
    """
    if len(series) == 0:
        raise ValueError("The series cannot be empty.")
    if not all(isinstance(val, (int, float)) for val in series):
        raise ValueError("The series must contain only numeric values.")

    mean = np.mean(series)
    return np.mean([(x - mean) ** 2 for x in series])

def compute_standard_deviation(variance):
    """
    Compute the standard deviation from a given variance.

    Args:
        variance (float): The variance value.

    Returns:
        float: The standard deviation.

    Raises:
        ValueError: If the input variance is not a positive number.
    """
    if not isinstance(variance, (int, float)) or variance < 0:
        raise ValueError("Variance must be a non-negative numeric value.")

    return np.sqrt(variance)

def compute_covariance(series_a, series_b):
    """
    Compute the covariance between two statistical series.

    Args:
        series_a (list or np.array): Series A of numerical data.
        series_b (list or np.array): Series B of numerical data.

    Returns:
        float: Covariance between the two series.

    Raises:
        ValueError: If the series lengths do not match or contain non-numeric data.
    """
    if len(series_a) != len(series_b):
        raise ValueError("Both series must have the same length.")
    if len(series_a) == 0:
        raise ValueError("The series cannot be empty.")
    if not all(isinstance(val, (int, float)) for val in series_a + series_b):
        raise ValueError("The series must contain only numeric values.")

    mean_a = np.mean(series_a)
    mean_b = np.mean(series_b)
    return np.mean([(a - mean_a) * (b - mean_b) for a, b in zip(series_a, series_b)])

def compute_correlation(series_a, series_b):
    """
    Compute the correlation coefficient between two statistical series.

    Args:
        series_a (list or np.array): Series A of numerical data.
        series_b (list or np.array): Series B of numerical data.

    Returns:
        float: Correlation coefficient between the two series.

    Raises:
        ValueError: If the series lengths do not match or contain non-numeric data.
    """
    covariance = compute_covariance(series_a, series_b)
    std_a = compute_standard_deviation(compute_variance(series_a))
    std_b = compute_standard_deviation(compute_variance(series_b))

    if std_a == 0 or std_b == 0:
        raise ValueError("Standard deviations must be non-zero for correlation computation.")

    return covariance / (std_a * std_b)

def compute_beta(series_asset, series_market):
    """
    Compute the beta of an asset relative to a market.

    Args:
        series_asset (list or np.array): Returns of the asset.
        series_market (list or np.array): Returns of the market.

    Returns:
        float: Beta of the asset.

    Raises:
        ValueError: If the series lengths do not match or contain non-numeric data.
    """
    variance_market = compute_variance(series_market)
    if variance_market == 0:
        raise ValueError("Variance of the market series must be non-zero.")

    return compute_covariance(series_asset, series_market) / variance_market

def compute_optimal_number_futures_contract(asset_quantity, futures_quantity, hedge_ratio):
    """
    Compute the optimal number of futures contracts to hedge.

    Args:
        asset_quantity (float): Quantity of the asset to be hedged.
        futures_quantity (float): Quantity of the futures contract.
        hedge_ratio (float): The hedge ratio.

    Returns:
        float: Optimal number of futures contracts.

    Raises:
        ValueError: If inputs are invalid or quantities are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [asset_quantity, futures_quantity, hedge_ratio]):
        raise ValueError("All inputs must be numeric (int or float).")
    if asset_quantity <= 0 or futures_quantity <= 0:
        raise ValueError("Quantities must be positive.")

    return hedge_ratio * (asset_quantity / futures_quantity)

def compute_dollar_value_of_hedge(asset_quantity, futures_quantity, asset_price, futures_price):
    """
    Compute the dollar value of a hedge.

    Args:
        asset_quantity (float): Quantity of the asset to be hedged.
        futures_quantity (float): Quantity of the futures contract.
        asset_price (float): Dollar value of the asset per unit.
        futures_price (float): Dollar value of the futures contract per unit.

    Returns:
        tuple: Dollar values of the asset and futures.

    Raises:
        ValueError: If inputs are invalid or quantities/dollar values are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [asset_quantity, futures_quantity, asset_price, futures_price]):
        raise ValueError("All inputs must be numeric (int or float).")
    if asset_quantity <= 0 or futures_quantity <= 0 or asset_price <= 0 or futures_price <= 0:
        raise ValueError("Quantities and dollar values must be positive.")

    return (asset_quantity * asset_price, futures_quantity * futures_price)

def compute_tailing_the_hedge_adjustment(asset_value, futures_value, hedge_ratio):
    """
    Compute the adjustment for tailing the hedge.

    Args:
        asset_value (float): Value of the asset.
        futures_value (float): Value of the futures contract.
        hedge_ratio (float): The hedge ratio.

    Returns:
        float: Adjustment for tailing the hedge.

    Raises:
        ValueError: If inputs are invalid or values are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [asset_value, futures_value, hedge_ratio]):
        raise ValueError("All inputs must be numeric (int or float).")
    if asset_value <= 0 or futures_value <= 0:
        raise ValueError("Values must be positive.")

    return hedge_ratio * (asset_value / futures_value)

# Concatenate three functions above
def compute_optimal_number_of_futures_contracts_tailing_the_hedge(
    asset_quantity=None,
    futures_quantity=None,
    hedge_ratio=None,
    asset_price=None,
    futures_price=None,
    asset_value=None,
    futures_value=None
):
    """
    Compute the optimal number of futures contracts, dollar value of a hedge, 
    or adjustment for tailing the hedge based on provided inputs.

    Args:
        asset_quantity (float, optional): Quantity of the asset to be hedged.
        futures_quantity (float, optional): Quantity of the futures contract.
        hedge_ratio (float, optional): The hedge ratio.
        asset_price (float, optional): Dollar value of the asset per unit.
        futures_price (float, optional): Dollar value of the futures contract per unit.
        asset_value (float, optional): Value of the asset (optional).
        futures_value (float, optional): Value of the futures contract (optional).

    Returns:
        dict: Results of the calculation, depending on the provided inputs.

    Raises:
        ValueError: If inputs are invalid or insufficient for any computation.
    """
    # Validate inputs
    inputs = {
        "asset_quantity": asset_quantity,
        "futures_quantity": futures_quantity,
        "hedge_ratio": hedge_ratio,
        "asset_price": asset_price,
        "futures_price": futures_price,
        "asset_value": asset_value,
        "futures_value": futures_value,
    }
    for key, value in inputs.items():
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be numeric (int or float).")

    # Ensure hedge ratio is provided for all calculations
    if hedge_ratio is None:
        raise ValueError("Hedge ratio is required for all calculations.")

    results = {}
    results["optimal_n_futures"] = ("Optimal number of contracts : ","N/A")
    results["tailing_hedge_adjustment"] = ("Tailing the hedge : ", "N/A")

    # Compute the optimal number of futures contracts
    if asset_quantity is not None and futures_quantity is not None:
        if asset_quantity <= 0 or futures_quantity <= 0:
            raise ValueError("Asset and futures quantities must be positive.")
        results["optimal_n_futures"] = ("Optimal number of contracts : ", hedge_ratio * (asset_quantity / futures_quantity))

    # Compute the dollar value of the hedge
    if asset_quantity is not None and futures_quantity is not None and asset_price is not None and futures_price is not None:
        if any(val <= 0 for val in [asset_quantity, futures_quantity, asset_price, futures_price]):
            raise ValueError("Asset and futures quantities and prices must be positive.")
        asset_value_calculated = asset_quantity * asset_price
        futures_value_calculated = futures_quantity * futures_price
        results["dollar_value_asset"] = asset_value_calculated
        results["dollar_value_futures"] = futures_value_calculated

    # Compute tailing the hedge adjustment
    if asset_value is not None and futures_value is not None:
        if asset_value <= 0 or futures_value <= 0:
            raise ValueError("Asset and futures values must be positive.")
        results["tailing_hedge_adjustment"] = ("Tailing the hedge : ", hedge_ratio * (asset_value / futures_value))

    # Ensure at least one calculation was performed
    if not results:
        raise ValueError("Insufficient inputs to perform any calculation.")
    logger.info(results)
    return results



def compute_hedge_equity_portfolio(beta, asset_value, futures_value):
    """
    Compute the hedge for an equity portfolio.

    Args:
        beta (float): Beta of the asset.
        asset_value (float): Value of the asset.
        futures_value (float): Value of the futures contract.

    Returns:
        float: Hedge for the equity portfolio.

    Raises:
        ValueError: If inputs are invalid or values are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [beta, asset_value, futures_value]):
        raise ValueError("All inputs must be numeric (int or float).")
    if asset_value <= 0 or futures_value <= 0:
        raise ValueError("Values must be positive.")

    return beta * (asset_value / futures_value)

def compute_change_beta_portfolio(target_beta, current_beta, asset_value, futures_value):
    """
    Compute the adjustment needed to change the beta of a portfolio.

    Args:
        target_beta (float): Target beta.
        current_beta (float): Current beta of the portfolio.
        asset_value (float): Value of the asset.
        futures_value (float): Value of the futures contract.

    Returns:
        tuple: A string indicating 'long', 'short', or 'Nothing to change', and the quantity of contracts.

    Raises:
        ValueError: If inputs are invalid or values are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [target_beta, current_beta, asset_value, futures_value]):
        raise ValueError("All inputs must be numeric (int or float).")
    if asset_value <= 0 or futures_value <= 0:
        raise ValueError("Values must be positive.")

    if current_beta > target_beta:
        return ('short', (current_beta - target_beta) * (asset_value / futures_value))
    if current_beta < target_beta:
        return ('long', (target_beta - current_beta) * (asset_value / futures_value))
    return ('Nothing to change', 0)


def compute_capm(market_expected_return, risk_free_rate, portfolio_beta):
    """
    Compute the expected return of a portfolio using the CAPM formula.

    Args:
        market_expected_return (float): Expected return of the market.
        risk_free_rate (float): Risk-free rate.
        portfolio_beta (float): Beta of the portfolio.

    Returns:
        float: The expected return of the portfolio.

    Raises:
        ValueError: If inputs are invalid or values are non-positive.
    """
    if not all(isinstance(val, (int, float)) for val in [market_expected_return, risk_free_rate, portfolio_beta]):
        raise ValueError("All inputs must be numeric (int or float).")
    if market_expected_return <= 0 or risk_free_rate < 0 or portfolio_beta < 0:
        raise ValueError("Expected return market must be positive, and risk-free rate and beta must be non-negative.")

    return risk_free_rate + portfolio_beta * (market_expected_return - risk_free_rate)
