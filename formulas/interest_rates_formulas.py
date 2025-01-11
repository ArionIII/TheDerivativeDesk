from math import exp

def continuous_compounding_rate(rate_m, frequency_m):
    try:
        rate_c = frequency_m * (exp(rate_m / frequency_m) - 1)
        return {"Rate (Continuous Compounding)": rate_c}
    except Exception as e:
        return {"error": str(e)}, 400

def zero_rate_curve(input_rates, rate_type, maturities):
    try:
        # Placeholder logic for zero-rate calculation
        zero_rates = [rate / maturity for rate, maturity in zip(input_rates, maturities)]
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

def determining_zero_rates(bond_prices, maturities):
    try:
        zero_rates = [(-1 / maturity) * log(price / 100) for price, maturity in zip(bond_prices, maturities)]
        return {"Zero Rates": zero_rates}
    except Exception as e:
        return {"error": str(e)}, 400

def extending_libor_curve_with_swap_rates(libor_rates, swap_rates, maturities):
    try:
        # Placeholder logic for extending LIBOR curve
        extended_curve = libor_rates + swap_rates
        return {"Extended LIBOR Curve": extended_curve}
    except Exception as e:
        return {"error": str(e)}, 400

def extending_libor_curve_with_fra(libor_rates, fra_rates, maturities):
    try:
        # Placeholder logic for extending LIBOR curve
        extended_curve = libor_rates + fra_rates
        return {"Extended LIBOR Curve": extended_curve}
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
