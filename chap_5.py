import numpy as np
import math
### Chapitre 5 - Determination of forward & futures prices
import math

def calculate_forward_price_no_income(spot_price, risk_free_rate, time_to_maturity):
    """
    Calculate the forward price of an investment asset without income.

    Formula:
        F0 = spot_price * e^(risk_free_rate * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp(risk_free_rate * time_to_maturity)


def calculate_forward_price_with_income(spot_price, income, risk_free_rate, time_to_maturity):
    """
    Calculate the forward price of an investment asset with known income.

    Formula:
        F0 = (spot_price - income) * e^(risk_free_rate * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, income, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or income < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return (spot_price - income) * math.exp(risk_free_rate * time_to_maturity)


def calculate_forward_price_with_yield(spot_price, yield_rate, risk_free_rate, time_to_maturity):
    """
    Calculate the forward price of an investment asset with known yield.

    Formula:
        F0 = spot_price * e^((risk_free_rate - yield_rate) * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, yield_rate, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or yield_rate < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp((risk_free_rate - yield_rate) * time_to_maturity)


def calculate_forward_contract_value(forward_price, delivery_price, risk_free_rate, time_to_maturity, long_position):
    """
    Calculate the value of a forward contract.

    Formula:
        Long position: f = (forward_price - delivery_price) * e^(-risk_free_rate * time_to_maturity)
        Short position: f = (delivery_price - forward_price) * e^(-risk_free_rate * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [forward_price, delivery_price, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if forward_price < 0 or delivery_price < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    long_value = (forward_price - delivery_price) * math.exp(-risk_free_rate * time_to_maturity)
    short_value = (delivery_price - forward_price) * math.exp(-risk_free_rate * time_to_maturity)
    return long_value if long_position else short_value


def calculate_futures_price_stock_index(spot_price, dividend_yield, risk_free_rate, time_to_maturity):
    """
    Calculate the futures price of a stock index with dividend yield.

    Formula:
        F0 = spot_price * e^((risk_free_rate - dividend_yield) * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, dividend_yield, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or dividend_yield < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp((risk_free_rate - dividend_yield) * time_to_maturity)


def calculate_forward_price_foreign_currency(spot_price, domestic_rate, foreign_rate, time_to_maturity):
    """
    Calculate the forward price of a foreign currency using interest rate parity.

    Formula:
        F0 = spot_price * e^((domestic_rate - foreign_rate) * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, domestic_rate, foreign_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or domestic_rate < 0 or foreign_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp((domestic_rate - foreign_rate) * time_to_maturity)


def calculate_futures_price_with_storage(spot_price, storage_costs, risk_free_rate, time_to_maturity):
    """
    Calculate the futures price of a commodity considering storage costs.

    Formula:
        F0 = (spot_price + storage_costs) * e^(risk_free_rate * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, storage_costs, risk_free_rate, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or storage_costs < 0 or risk_free_rate < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return (spot_price + storage_costs) * math.exp(risk_free_rate * time_to_maturity)


def calculate_futures_price_with_proportional_costs_and_yield(spot_price, storage_cost_proportional, risk_free_rate, convenience_yield, time_to_maturity):
    """
    Calculate the futures price when storage costs are proportional and include convenience yield.

    Formula:
        F0 = spot_price * e^((risk_free_rate + proportional_cost - convenience_yield) * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, storage_cost_proportional, risk_free_rate, convenience_yield, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or storage_cost_proportional < 0 or risk_free_rate < 0 or convenience_yield < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp((risk_free_rate + storage_cost_proportional - convenience_yield) * time_to_maturity)


def calculate_futures_price_with_non_proportional_costs_and_yield(spot_price, storage_costs, risk_free_rate, convenience_yield, time_to_maturity):
    """
    Calculate the futures price when storage costs are fixed and include convenience yield.

    Formula:
        F0 = (spot_price + storage_costs) * e^((risk_free_rate - convenience_yield) * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, storage_costs, risk_free_rate, convenience_yield, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or storage_costs < 0 or risk_free_rate < 0 or convenience_yield < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return (spot_price + storage_costs) * math.exp((risk_free_rate - convenience_yield) * time_to_maturity)


def calculate_futures_price_cost_of_carry(spot_price, cost_of_carry, time_to_maturity):
    """
    Calculate the futures price of an investment asset using cost of carry.

    Formula:
        F0 = spot_price * e^(cost_of_carry * time_to_maturity)
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, cost_of_carry, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or cost_of_carry < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")
    return spot_price * math.exp(cost_of_carry * time_to_maturity)

def calculate_futures_price_cost_of_carry_with_convenience_yield(spot_price, cost_of_carry, convenience_yield, time_to_maturity):
    """
    Calculate the futures price of a consumption asset using the cost of carry and convenience yield.

    Formula:
        F0 = S0 * e^((c - y) * T)

    Args:
        spot_price (float): Spot price of the consumption asset.
        cost_of_carry (float): Cost of carry (as a decimal).
        convenience_yield (float): Convenience yield (as a decimal).
        time_to_maturity (float): Time to maturity (in years).

    Returns:
        float: The futures price.
    """
    if not all(isinstance(val, (int, float)) for val in [spot_price, cost_of_carry, convenience_yield, time_to_maturity]):
        raise ValueError("All inputs must be numeric.")
    if spot_price < 0 or cost_of_carry < 0 or convenience_yield < 0 or time_to_maturity < 0:
        raise ValueError("Inputs must be non-negative.")

    return spot_price * math.exp((cost_of_carry - convenience_yield) * time_to_maturity)


def delivery_timing_decision(cost_of_carry, convenience_yield):
    """
    Determine the delivery timing for a futures contract based on cost of carry and convenience yield.

    Args:
        cost_of_carry (float): Cost of carry.
        convenience_yield (float): Convenience yield.

    Returns:
        int: 0 if the decision is to deliver as soon as possible, 1 if the decision is to deliver as late as possible.

    Raises:
        ValueError: If inputs are invalid (non-numeric values).
    """
    if not all(isinstance(val, (int, float)) for val in [cost_of_carry, convenience_yield]):
        raise ValueError("Both inputs must be numeric.")

    # Decision logic: deliver asap if cost_of_carry - convenience_yield > 0, deliver late if cost_of_carry - convenience_yield <= 0
    return 0 if cost_of_carry - convenience_yield > 0 else 1
