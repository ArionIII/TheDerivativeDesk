from math import exp
import numpy as np
from config import logger

def continuous_compounding_rate(rate_m, frequency_m):
    try:
        rate_c = frequency_m * (exp(rate_m / frequency_m) - 1)
        return {"Rate (Continuous Compounding)": rate_c}
    except Exception as e:
        return {"error": str(e)}, 400

def m_compounding_rate(rate_c, frequency_m):
    """
    Convert a continuous compounding rate to m-compounding rate.
    """
    try:
        rate_m = frequency_m * np.log(1 + rate_c / frequency_m)
        return {"Rate (m-Compounding)": rate_m}
    except Exception as e:
        return {"error": str(e)}, 400


def zero_rate_curve(input_rates, rate_type, maturities, space_between_payments=None):
    try:
        if len(input_rates) != len(maturities):
            raise ValueError("Input rates and maturities must have the same length.")

        if rate_type == "Swap" and space_between_payments is None:
            raise ValueError("For Swap rates, space_between_payments must be provided.")

        zero_rates = []

        if rate_type == "FRA":
            # FRA Zero Rate Logic
            for rate, maturity in zip(input_rates, maturities):
                if maturity <= 0:
                    raise ValueError("Maturities must be positive.")
                zero_rate = ((1 + rate) ** maturity - 1)
                zero_rates.append(zero_rate)

        elif rate_type == "Swap":
            # Swap Zero Rate Logic
            # Account for periodic payments spaced by `space_between_payments`.
            for rate, maturity in zip(input_rates, maturities):
                if maturity <= 0:
                    raise ValueError("Maturities must be positive.")
                if space_between_payments <= 0:
                    raise ValueError("Space between payments must be positive.")
                
                # Number of payments over the maturity period
                num_payments = int(maturity / space_between_payments)

                # Approximation of zero rate for swap rates
                # Using average payments adjusted by `space_between_payments`
                zero_rate = (rate / num_payments) * space_between_payments
                zero_rates.append(zero_rate)

        else:
            raise ValueError("Invalid rate type. Must be 'FRA' or 'Swap'.")

        return {"Zero Rate Curve": zero_rates}

    except Exception as e:
        return {"error": str(e)}, 400

def bond_pricing(face_value, coupon_rate, maturity, market_rate):
    try:
        price = sum(
            (face_value * coupon_rate / 100) / ((1 + market_rate / 100) ** t)
            for t in range(1, int(maturity) + 1)
        )
        price += face_value / ((1 + market_rate / 100) ** maturity)
        return {"Bond Price": price}
    except Exception as e:
        return {"error": str(e)}, 400

def determining_zero_rates(bond_prices, maturities, face_values):
    try:
        # Check if all input lists have the same length
        if len(bond_prices) != len(maturities) or len(bond_prices) != len(face_values):
            raise ValueError("Bond prices, maturities, and face values must have the same length.")

        zero_rates = []

        # Calculate zero rates for each bond
        for price, maturity, face_value in zip(bond_prices, maturities, face_values):
            if price <= 0 or maturity <= 0 or face_value <= 0:
                raise ValueError("Bond prices, maturities, and face values must be positive values.")
            # Calculate the zero rate
            zero_rate = (face_value / price) ** (1 / maturity) - 1
            zero_rates.append(zero_rate)

        # Return the result as a dictionary
        return {"Zero Rates": zero_rates}
    except Exception as e:
        return {"error": str(e)}, 400

def extending_libor_curve_with_swap_rates(libor_rates, swap_rates, maturities):
    try:
        if len(swap_rates) != len(maturities):
            raise ValueError("Swap rates and maturities must have the same length.")

        # Initialize the extended curve with LIBOR rates (assumed to be zero rates for short maturities)
        zero_rate_curve = libor_rates[:]
        known_maturities = list(range(1, len(libor_rates) + 1))  # Assume 1-year intervals for LIBOR maturities
        logger.warning(f"known_maturities : {known_maturities}")
        # Bootstrapping for swap rates
        for swap_rate, maturity in zip(swap_rates, maturities):
            if maturity in known_maturities:
                continue  # Skip if the maturity is already covered by LIBOR rates
            
            # Calculate the zero rate for the current maturity using swap rates
            num_payments = int(maturity)  # Assuming annual payments for simplicity
            discount_sum = sum(
                (1 / ((1 + zero_rate_curve[i - 1]) ** i)) for i in range(1, num_payments)
            )
            zero_rate = (
                (1 - swap_rate * discount_sum) / (1 + swap_rate * num_payments)
            ) ** (1 / maturity) - 1
            
            zero_rate_curve.append(zero_rate)
            known_maturities.append(maturity)

        # Sort results by maturity
        extended_curve = sorted(
            zip(known_maturities, zero_rate_curve), key=lambda x: x[0]
        )
        logger.warning(f"extended_curve : {extended_curve}")
        return {"Extended Zero Rate Curve": extended_curve}

    except Exception as e:
        return {"error": str(e)}, 400


def extending_libor_curve_with_fra(libor_rates, fra_rates, maturities):
    try:
        if len(fra_rates) != len(maturities):
            raise ValueError("FRA rates and maturities must have the same length.")

        # Initialize the zero rate curve with known LIBOR rates
        zero_rate_curve = libor_rates[:]
        known_maturities = list(range(1, len(libor_rates) + 1))  # Assume 1-year intervals for LIBOR maturities

        # Bootstrapping FRA rates to extend the curve
        for fra_rate, maturity in zip(fra_rates, maturities):
            if maturity in known_maturities:
                continue  # Skip if the maturity is already covered by LIBOR rates

            # Previous zero rate and discount factor for the prior maturity
            previous_maturity = max(known_maturities)
            previous_zero_rate = zero_rate_curve[previous_maturity - 1]
            previous_discount_factor = 1 / ((1 + previous_zero_rate) ** previous_maturity)

            # Calculate the discount factor for the current maturity
            discount_factor = previous_discount_factor / (1 + fra_rate * (maturity - previous_maturity))

            # Calculate the zero rate for the current maturity
            zero_rate = (1 / discount_factor) ** (1 / maturity) - 1

            zero_rate_curve.append(zero_rate)
            known_maturities.append(maturity)

        # Sort results by maturity
        extended_curve = sorted(
            zip(known_maturities, zero_rate_curve), key=lambda x: x[0]
        )
        return {"Extended Zero Rate Curve": extended_curve}

    except Exception as e:
        return {"error": str(e)}, 400


def payoff_of_fra(contract_rate, settlement_rate, notional_value, time):
    try:
        payoff = notional_value * (settlement_rate - contract_rate) * time / (1 + settlement_rate * time)
        return {"FRA Payoff": payoff}
    except Exception as e:
        return {"error": str(e)}, 400

def duration_and_convexity(cash_flows, discount_rates, time_periods):
    try:
        durations = [
            (t * cf) / ((1 + r) ** t) for t, cf, r in zip(time_periods, cash_flows, discount_rates)
        ]
        convexities = [
            (t * (t + 1) * cf) / ((1 + r) ** (t + 2)) for t, cf, r in zip(time_periods, cash_flows, discount_rates)
        ]
        duration = sum(durations)
        convexity = sum(convexities)
        return {"Duration": duration, "Convexity": convexity}
    except Exception as e:
        return {"error": str(e)}, 400


def calculate_payoff_of_fra(contract_rate, settlement_rate, notional_value, time):
    payoff = notional_value * (settlement_rate - contract_rate) * time
    return payoff

def calculate_valuation_of_fra(forward_rate, contract_rate, notional_value, discount_factor):
    valuation = notional_value * (forward_rate - contract_rate) * discount_factor
    return valuation

def calculate_forward_rate_calculation(spot_rates, times):
    if len(spot_rates) != 2 or len(times) != 2:
        raise ValueError("Exactly two spot rates and times are required.")
    rate1, rate2 = spot_rates
    time1, time2 = times
    forward_rate = ((1 + rate2) ** time2 / (1 + rate1) ** time1) ** (1 / (time2 - time1)) - 1
    return forward_rate

def calculate_fra_break_even_rate(notional_value, forward_rate, time_to_settlement):
    break_even_rate = forward_rate / time_to_settlement
    return break_even_rate

def calculate_interest_rate_swap_cash_flows(notional_value, fixed_rate, floating_rate, time_periods):
    fixed_cash_flows = [notional_value * fixed_rate * t for t in time_periods]
    floating_cash_flows = [notional_value * floating_rate * t for t in time_periods]
    return fixed_cash_flows, floating_cash_flows

def calculate_interest_rate_swap_valuation(fixed_rate, floating_rate, notional_value, discount_factors):
    fixed_leg = sum([notional_value * fixed_rate * d for d in discount_factors])
    floating_leg = sum([notional_value * floating_rate * d for d in discount_factors])
    valuation = floating_leg - fixed_leg
    return valuation

def calculate_pricing_interest_rate_futures(settlement_price, tick_size, contract_value):
    price = (100 - settlement_price) * contract_value / tick_size
    return price

def calculate_swap_spread_analysis(swap_rate, treasury_yield):
    spread = swap_rate - treasury_yield
    return spread

def calculate_swaption_valuation(notional_value, volatility, time_to_maturity, strike_price, forward_rate):
    from math import exp, sqrt, log
    from scipy.stats import norm
    d1 = (log(forward_rate / strike_price) + (volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)
    swaption_value = notional_value * (forward_rate * norm.cdf(d1) - strike_price * norm.cdf(d2))
    return swaption_value

def calculate_basis_swap_analysis(notional_value, benchmark_rate1, benchmark_rate2):
    spread = (benchmark_rate1 - benchmark_rate2) * notional_value
    return spread

def calculate_interest_rate_swap_delta_hedging(notional_value, duration, delta):
    delta_hedging_position = notional_value * duration * delta
    return delta_hedging_position
