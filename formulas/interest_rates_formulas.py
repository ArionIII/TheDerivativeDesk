from math import exp
import numpy as np
from config import logger
import scipy.interpolate as interp
from scipy.optimize import newton
import QuantLib as ql
from scipy.interpolate import CubicSpline
import os
import pandas as pd
import random

def continuous_compounding_rate(rate_m, frequency_m):
    logger.info(f"Calculating continuous compounding rate with rate_m: {rate_m} and frequency_m: {frequency_m}")
    try:
        rate_c = frequency_m * (exp(rate_m / frequency_m) - 1)
        return {"continuous_compounding_rate": ("Rate (Continuous Compounding) :", rate_c)}
    except Exception as e:
        return {"error": str(e)}, 400

def m_compounding_rate(rate_c, frequency_m):
    logger.info(f"Calculating m-compounding rate with rate_c: {rate_c} and frequency_m: {frequency_m}")
    """
    Convert a continuous compounding rate to m-compounding rate.
    """
    try:
        rate_m = frequency_m * np.log(1 + rate_c / frequency_m)
        return {"m_compounding_rate": ("Rate (m-Compounding) :", rate_m)}
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
            # Bootstrap method for swap zero rates
            discount_factors = []  # Liste des facteurs d'actualisation
            for rate, maturity in zip(input_rates, maturities):
                if maturity <= 0:
                    raise ValueError("Maturities must be positive.")
                if space_between_payments <= 0:
                    raise ValueError("Space between payments must be positive.")
                
                # Nombre total de paiements
                num_payments = int(maturity / space_between_payments)
                
                # Somme des paiements déjà connus
                discount_sum = sum(discount_factors)
                
                # Calcul du facteur d'actualisation pour la nouvelle échéance
                discount_factor = (1 - rate * discount_sum) / (1 + rate * num_payments)

                # Calcul du taux zéro correspondant
                zero_rate = (1 / discount_factor) ** (1 / maturity) - 1
                zero_rates.append(zero_rate)

                # Stocker le facteur d'actualisation pour les prochaines itérations
                discount_factors.append(discount_factor)

        else:
            raise ValueError("Invalid rate type. Must be 'FRA' or 'Swap'.")

        return {"zero_rate_curve": ("Zero Rate Curve :", zero_rates)}

    except Exception as e:
        return {"error": ("Error :", str(e))}, 400

def bond_pricing(face_value, coupon_rate, maturity, market_rate):
    try:
        price = sum(
            (face_value * coupon_rate / 100) / ((1 + market_rate / 100) ** t)
            for t in range(1, int(maturity) + 1)
        )
        price += face_value / ((1 + market_rate / 100) ** maturity)
        return {"bond_price": ("Bond Price :", price)}
    except Exception as e:
        return {"error": str(e)}, 400


def determining_zero_rates(bond_prices, maturities, face_values, coupon_rates, m_compoundings, output_path="static/outputs/interest-rates-and-fixed-income/"):
    """
    Compute the zero-coupon yield curve using the bootstrapping method.

    Parameters:
    - bond_prices: List of bond prices.
    - maturities: List of bond maturities in years.
    - face_values: List of bond face values.
    - coupon_rates: List of coupon rates (decimal format, e.g., 0.05 for 5%).
    - m_compoundings: List of compounding frequencies (1=annual, 2=semi-annual, etc.).

    Returns:
    - Displays a DataFrame containing the computed zero rates.
    """
    try:
        os.makedirs(output_path, exist_ok=True)

        # Sort bonds by maturity in ascending order
        sorted_data = sorted(zip(maturities, bond_prices, face_values, coupon_rates, m_compoundings))
        maturities, bond_prices, face_values, coupon_rates, m_compoundings = zip(*sorted_data)

        zero_rates = {}

        for i in range(len(maturities)):
            P = bond_prices[i]  # Bond price
            T = maturities[i]    # Maturity in years
            FV = face_values[i]  # Face value
            c = coupon_rates[i]  # Coupon rate
            m = m_compoundings[i]  # Compounding frequency

            # Coupon payment
            C = FV * c * m  # Periodic coupon
            logger.info(C)
            if c == 0:  # Zero-coupon bond
                r = np.log(FV/P)/T
                logger.info("rate :")
                logger.info(r)
            else:  # Coupon-paying bond (bootstrapping method)
                logger.info(f"Calcul du taux zéro pour maturité {T} ans")
                logger.info(f"Prix de l'obligation : {P}")
                logger.info(f"Valeur faciale : {FV}")
                logger.info(f"Coupon annuel : {C}")
                logger.info(f"Compounding frequency : {m}")

                # Sum of discounted coupon payments using previously computed rates
                coupon_sum = 0
                for t in zero_rates:
                    if t < T and (t*m).is_integer():
                        discounted_coupon = (C / m) / (1 + zero_rates[t]) ** t
                        coupon_sum += discounted_coupon
                        logger.info(f"Coupon à l'année {t} : {C/m}, actualisé à {discounted_coupon}")

                logger.info(f"Somme des coupons actualisés : {coupon_sum}")

                logger.info('equation :')
                logger.info(f'{coupon_sum} + {FV+C} * e^(-R * {T}) = {P}')
                logger.info(f"Coupon sum (Somme des coupons actualisés) : {coupon_sum}")
                logger.warning(f"Valeur faciale (FV) : {FV}")
                logger.warning(f"Dernier coupon (C) : {C}")
                logger.warning(f"Prix de l'obligation (P) : {P}")
                logger.warning(f"Maturité (T) : {T}")
                logger.warning(f"Expression complète avant résolution : {coupon_sum} + ({FV+(C/m)} * e^(-R * {T})) = {P}")


                logger.warning(f"Taux zéro continûment composé (R) trouvé : {r}")

                # Solve for the zero rate of the final cash flow
                r = -1/T * np.log((P-coupon_sum)/(FV+(C/m)))
                logger.info(f"Taux zéro calculé pour maturité {T} ans : {r}")
            zero_rates[T] = r  # Store the annualized zero rate


        # Convert to DataFrame for display
        df = pd.DataFrame({
            "Maturity": zero_rates.keys(),
            "Zero Rate (Continuous Compounding)": zero_rates.values()
        })

        # Générer un nom de fichier unique
        random_file_name = f"zero_rates_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV (compatible Excel)
        df.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df.to_excel(xlsx_path, index=False, engine="openpyxl")

        logger.info(f"zero-rates saved to: {csv_path} and {xlsx_path}")
        return csv_path, xlsx_path

    except Exception as e:
        raise ValueError(f"Error computing zero rates: {e}")



def extending_libor_curve_with_swap_rates(libor_rates, swap_rates, libor_tenors, swap_tenors,
                                          day_count_convention="ACT/360",
                                          fixed_leg_frequency="Annual",
                                          floating_leg_frequency="6M"):
    """
    Étend une courbe de taux LIBOR avec des taux de swap via bootstrapping simple.
    """
    
    # Convertir en numpy arrays pour faciliter les calculs
    libor_tenors = np.array(libor_tenors, dtype=float)
    swap_tenors = np.array(swap_tenors, dtype=float)
    libor_rates = np.array(libor_rates, dtype=float)
    swap_rates = np.array(swap_rates, dtype=float)

    # Initialisation des taux zéro avec les taux LIBOR
    known_maturities = np.concatenate((libor_tenors, swap_tenors))
    zero_rate_curve = np.concatenate((libor_rates, np.zeros_like(swap_rates)))  # Placeholder pour bootstrapping

    # Bootstrapping sur les nouveaux points de swap
    for i in range(len(swap_tenors)):
        tenor = swap_tenors[i]
        swap_rate = swap_rates[i]

        # Approximation du taux zéro par une interpolation linéaire des valeurs précédentes
        if tenor in libor_tenors:
            rate = libor_rates[np.where(libor_tenors == tenor)[0][0]]
        else:
            prev_tenor = known_maturities[i + len(libor_tenors) - 1]
            prev_rate = zero_rate_curve[i + len(libor_tenors) - 1]

            # Interpolation linéaire entre le dernier point connu et le swap actuel
            rate = prev_rate + (swap_rate - prev_rate) * (tenor - prev_tenor) / (tenor - prev_tenor)

        zero_rate_curve[i + len(libor_tenors)] = rate

    # Trier les maturités et taux pour garantir une courbe ordonnée
    extended_curve = sorted(zip(known_maturities, zero_rate_curve), key=lambda x: x[0])

    return {"extended_zero_rate_curve_fra": ("Extended Zero Rate Curve FRA :", extended_curve)}

def extending_zero_curve_with_fra(libor_rates, fra_rates, libor_tenors, fra_tenors,
                                  day_count_convention="ACT/360"):
    """
    Étend une courbe des taux zéro en intégrant des taux FRA via bootstrapping.
    """
    
    # Convertir les entrées en arrays numpy
    libor_tenors = np.array(libor_tenors, dtype=float)
    fra_tenors = np.array(fra_tenors, dtype=float)
    libor_rates = np.array(libor_rates, dtype=float)
    fra_rates = np.array(fra_rates, dtype=float)

    # Initialisation des taux zéro avec les taux LIBOR
    known_maturities = np.concatenate((libor_tenors, fra_tenors))
    zero_rate_curve = np.concatenate((libor_rates, np.zeros_like(fra_rates)))  # Placeholder pour bootstrapping

    # Bootstrapping des taux zéro à partir des FRA
    for i in range(len(fra_tenors)):
        T1 = libor_tenors[-1] if i == 0 else fra_tenors[i - 1]  # Dernier point connu
        T2 = fra_tenors[i]  # Nouveau point à calculer
        FRA = fra_rates[i]

        # On récupère le dernier taux zéro connu
        r_T1 = zero_rate_curve[np.where(known_maturities == T1)[0][0]]

        # Calcul du taux zéro à T2 à partir du taux FRA
        r_T2 = ((1 + r_T1 * T1) * (1 + FRA * (T2 - T1)) - 1) / T2

        zero_rate_curve[np.where(known_maturities == T2)[0][0]] = r_T2

    # Trier les maturités et taux pour garantir une courbe ordonnée
    extended_curve = sorted(zip(known_maturities, zero_rate_curve), key=lambda x: x[0])

    return {"extended_zero_rate_curve_fra": ("Extended Zero Rate Curve FRA :", extended_curve)}


def payoff_of_fra(contract_rate, settlement_rate, notional_value, time):
    try:
        payoff = notional_value * (settlement_rate - contract_rate) * time / (1 + settlement_rate * time)
        return {"fra_payoff": ("FRA Payoff :", payoff)}
    except Exception as e:
        return {"error": str(e)}, 400

def duration_and_convexity(cash_flows, discount_rates, time_periods):
    try:
        # Actualisation des cash flows
        pv_cash_flows = [cf / ((1 + r) ** t) for cf, r, t in zip(cash_flows, discount_rates, time_periods)]
        pv_total = sum(pv_cash_flows)  # Valeur actuelle totale de l'obligation

        # Calcul de la duration pondérée
        durations = [(t * cf) / ((1 + r) ** t) for t, cf, r in zip(time_periods, cash_flows, discount_rates)]
        duration = np.round(sum(durations) / pv_total, 3)  # Normalisation par la valeur actuelle

        # Calcul de la convexité pondérée
        convexities = [(t * (t + 1) * cf) / ((1 + r) ** (t + 2)) for t, cf, r in zip(time_periods, cash_flows, discount_rates)]
        convexity = np.round(sum(convexities) / pv_total, 3)  # Normalisation par la valeur actuelle

        return {
    "duration": ("Duration :", str(duration)),
    "convexity": ("Convexity :", str(convexity))
}

    except Exception as e:
        return {"error": str(e)}, 400



def calculate_payoff_of_fra(contract_rate, settlement_rate, notional_value, time):
    payoff = notional_value * (settlement_rate - contract_rate) * time
    return {"fra_payoff": ("FRA Payoff :", payoff)}

def calculate_valuation_of_fra(forward_rate, contract_rate, notional_value, discount_factor):
    valuation = notional_value * (forward_rate - contract_rate) * discount_factor
    return {"fra_valuation": ("FRA Valuation :", valuation)}

def calculate_forward_rate(spot_rate_1, spot_rate_2, time_period_1, time_period_2):
    """
    Calcule le taux forward à partir de deux taux spot (zéro) et leurs maturités respectives.
    """
    # Vérification des entrées
    if time_period_2 <= time_period_1:
        raise ValueError("Time Period 2 must be greater than Time Period 1.")

    # Calcul du taux forward
    forward_rate = ((1 + spot_rate_2) ** time_period_2 / (1 + spot_rate_1) ** time_period_1) ** (1 / (time_period_2 - time_period_1)) - 1

    # Retour formaté
    return {"forward_rate": ("Forward Rate :", forward_rate)}

def calculate_fra_break_even_rate(notional_value, forward_rate, time_to_settlement):
    break_even_rate = forward_rate / time_to_settlement
    return {"fra_break_even_rate": ("FRA Break-even Rate :", break_even_rate)}

def calculate_interest_rate_swap_cash_flows(notional_value, fixed_rate, floating_rate, time_periods):
    fixed_cash_flows = [notional_value * fixed_rate * t for t in time_periods]
    floating_cash_flows = [notional_value * floating_rate * t for t in time_periods]
    return {"interest_rate_swap_cash_flows": ("Interest Rate Swap Cash Flows :", {"Fixed Cash Flows": fixed_cash_flows, "Floating Cash Flows": floating_cash_flows})}

def calculate_interest_rate_swap_valuation(fixed_rate, floating_rate, notional_value, discount_factors):
    fixed_leg = sum([notional_value * fixed_rate * d for d in discount_factors])
    floating_leg = sum([notional_value * floating_rate * d for d in discount_factors])
    valuation = floating_leg - fixed_leg
    return {"interest_rate_swap_valuation": ("Interest Rate Swap Valuation :", valuation)}

def calculate_pricing_interest_rate_futures(settlement_price, tick_size, contract_value):
    price = (100 - settlement_price) * contract_value / tick_size
    return {"pricing_interest_rate_futures": ("Pricing Interest Rate Futures :", price)}

def calculate_swap_spread_analysis(swap_rate, treasury_yield):
    spread = swap_rate - treasury_yield
    return {"swap_spread_analysis": ("Swap Spread Analysis :", spread)}

def calculate_swaption_valuation(notional_value, volatility, time_to_maturity, strike_price, forward_rate):
    from math import exp, sqrt, log
    from scipy.stats import norm
    d1 = (log(forward_rate / strike_price) + (volatility ** 2 / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)
    swaption_value = notional_value * (forward_rate * norm.cdf(d1) - strike_price * norm.cdf(d2))
    return {"swaption_valuation": ("Swaption Valuation :", swaption_value)}

def calculate_basis_swap_analysis(notional_value, benchmark_rate1, benchmark_rate2):
    spread = (benchmark_rate1 - benchmark_rate2) * notional_value
    return {"basis_swap_analysis": ("Basis Swap Analysis :", spread)}

def calculate_interest_rate_swap_delta_hedging(notional_value, duration, delta):
    delta_hedging_position = notional_value * duration * delta
    return {"interest_rate_swap_delta_hedging": ("Interest Rate Swap Delta Hedging :", delta_hedging_position)}
