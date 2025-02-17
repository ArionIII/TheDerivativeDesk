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
from scipy.interpolate import CubicSpline
from scipy.optimize import fsolve

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
                                               output_path="static/outputs/interest-rates-and-fixed-income/"):
    """
    Étend une courbe de taux LIBOR avec des taux de swap via interpolation spline cubique,
    en supprimant les doublons et en moyennant les taux lorsque des maturités se répètent.
    """

    try:
        # Vérifier et créer le répertoire de sortie si nécessaire
        os.makedirs(output_path, exist_ok=True)

        # Convertir en numpy arrays
        libor_tenors = np.array(libor_tenors, dtype=float)
        swap_tenors = np.array(swap_tenors, dtype=float)
        libor_rates = np.array(libor_rates, dtype=float)
        swap_rates = np.array(swap_rates, dtype=float)

        # Fusion des maturités et des taux
        all_tenors = np.concatenate((libor_tenors, swap_tenors))
        all_rates = np.concatenate((libor_rates, swap_rates))

        # Suppression des doublons en moyennant les taux associés
        tenor_rate_dict = {}
        for tenor, rate in zip(all_tenors, all_rates):
            if tenor in tenor_rate_dict:
                tenor_rate_dict[tenor].append(rate)
            else:
                tenor_rate_dict[tenor] = [rate]

        # Calcul de la moyenne pour chaque maturité unique
        unique_tenors = sorted(tenor_rate_dict.keys())  # Assurer l'ordre croissant
        averaged_rates = np.array([np.mean(tenor_rate_dict[t]) for t in unique_tenors])

        # Appliquer une interpolation spline cubique
        spline = CubicSpline(unique_tenors, averaged_rates)

        # Générer des points plus fins pour la courbe interpolée
        smooth_tenors = np.linspace(unique_tenors[0], unique_tenors[-1], 300)
        smooth_rates = spline(smooth_tenors)

        # Convertir en DataFrame pour l'export
        df_interpolated = pd.DataFrame({"Maturity": smooth_tenors, "Interpolated Zero Rates": smooth_rates})

        # Générer un nom de fichier unique
        random_file_name = f"smoothed_zero_rates_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV (compatible Excel)
        df_interpolated.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df_interpolated.to_excel(xlsx_path, index=False, engine="openpyxl")

        return csv_path, xlsx_path

    except Exception as e:
        raise ValueError(f"Error computing smoothed LIBOR curve: {e}")


def extending_zero_curve_with_fra(libor_rates, fra_rates, libor_tenors, fra_tenors,
                                         output_path="static/outputs/interest-rates-and-fixed-income/"):
    """
    Étend une courbe de taux LIBOR avec des taux de FRA via bootstrapping et interpolation spline cubique.

    Différences avec les swaps :
    - On calcule les taux zéro des nouveaux points en utilisant la formule des FRA.
    - On ajoute ces points à la courbe et on applique une interpolation pour lisser la transition.

    Paramètres :
    - libor_rates : Taux zéro initiaux (LIBOR)
    - fra_rates : Taux FRA pour compléter la courbe
    - libor_tenors : Maturités associées aux taux LIBOR
    - fra_tenors : Maturités associées aux taux FRA

    Retourne :
    - Chemins des fichiers CSV et XLSX avec la courbe étendue et lissée.
    """

    try:
        # Vérifier et créer le répertoire de sortie si nécessaire
        os.makedirs(output_path, exist_ok=True)

        # Convertir en numpy arrays
        libor_tenors = np.array(libor_tenors, dtype=float)
        fra_tenors = np.array(fra_tenors, dtype=float)
        libor_rates = np.array(libor_rates, dtype=float)
        fra_rates = np.array(fra_rates, dtype=float)

        # Fusion des maturités et des taux initiaux
        all_tenors = np.concatenate((libor_tenors, fra_tenors))
        all_rates = np.concatenate((libor_rates, np.zeros_like(fra_rates)))  # Placeholder pour FRA

        # Calcul des taux zéro à partir des FRA en utilisant la formule :
        # (1 + r_2 * T_2) = (1 + r_1 * T_1) * (1 + FRA * (T_2 - T_1))
        for i, T2 in enumerate(fra_tenors):
            T1 = libor_tenors[-1] if len(libor_tenors) > 0 else 0  # Dernier point connu
            r1 = libor_rates[-1] if len(libor_rates) > 0 else 0  # Dernier taux connu
            FRA = fra_rates[i]  # Taux FRA actuel

            # Calcul du taux zéro du nouvel échéancier
            r2 = ((1 + r1 * T1) * (1 + FRA * (T2 - T1)) - 1) / T2
            all_rates[len(libor_rates) + i] = r2  # Mise à jour du taux dans la courbe

        # Suppression des doublons en moyennant les taux associés
        tenor_rate_dict = {}
        for tenor, rate in zip(all_tenors, all_rates):
            if tenor in tenor_rate_dict:
                tenor_rate_dict[tenor].append(rate)
            else:
                tenor_rate_dict[tenor] = [rate]

        # Calcul de la moyenne pour chaque maturité unique
        unique_tenors = sorted(tenor_rate_dict.keys())  # Assurer l'ordre croissant
        averaged_rates = np.array([np.mean(tenor_rate_dict[t]) for t in unique_tenors])

        # Appliquer une interpolation spline cubique
        spline = CubicSpline(unique_tenors, averaged_rates)

        # Générer des points plus fins pour la courbe interpolée
        smooth_tenors = np.linspace(unique_tenors[0], unique_tenors[-1], 300)
        smooth_rates = spline(smooth_tenors)

        # Convertir en DataFrame pour l'export
        df_interpolated = pd.DataFrame({"Maturity": smooth_tenors, "Interpolated Zero Rates": smooth_rates})

        # Générer un nom de fichier unique
        random_file_name = f"fra_smoothed_zero_rates_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV (compatible Excel)
        df_interpolated.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df_interpolated.to_excel(xlsx_path, index=False, engine="openpyxl")

        return csv_path, xlsx_path

    except Exception as e:
        raise ValueError(f"Error computing smoothed LIBOR curve with FRA rates: {e}")

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



def payoff_of_fra(contract_rate, settlement_rates, notional_value, interval_between_payments):
    """
    Calcule le payoff total d'un FRA sur plusieurs périodes.

    Paramètres :
    - contract_rate : Taux fixe du FRA (ex: 0.03 pour 3%).
    - settlement_rates : Liste des taux flottants observés (ex: [0.032, 0.035, 0.031, 0.037]).
    - notional_value : Valeur notionnelle du contrat (ex: 1 000 000€).
    - interval_between_payments : Durée d’une période en années (ex: 0.5 pour 6 mois).

    Retourne :
    - Un dictionnaire avec le payoff total du FRA.
    """

    try:
        # Vérifier que settlement_rates est bien une liste
        if not isinstance(settlement_rates, list):
            raise ValueError("settlement_rates doit être une liste de taux.")

        total_payoff = 0

        # Boucle sur chaque période pour calculer le payoff
        logger.warning(settlement_rates)
        logger.warning(contract_rate)
        logger.warning(notional_value)
        logger.warning(interval_between_payments)
        
        # Vérification et conversion en un tableau numpy bien formaté
        logger.warning(type(settlement_rates))
        logger.warning(type(contract_rate))
        logger.warning(type(notional_value))
        logger.warning(type(interval_between_payments))
        for R_s in settlement_rates:
            logger.warning(R_s)
            logger.warning(type(R_s))
            payoff = notional_value * (R_s - contract_rate) * interval_between_payments / (1 + R_s * interval_between_payments)
            total_payoff += payoff  # Accumuler tous les payoffs
        logger.warning(total_payoff)
        return {"fra_total_payoff": ("Total FRA Payoff :", total_payoff)}

    except Exception as e:
        return {"error": str(e)}, 400


def calculate_valuation_of_fra(contract_rate, forward_rates, notional_value, interval_between_payments):
    """
    Calcule le payoff total d'un FRA sur plusieurs périodes.

    Paramètres :
    - contract_rate : Taux fixe du FRA (ex: 0.03 pour 3%).
    - settlement_rates : Liste des taux flottants observés (ex: [0.032, 0.035, 0.031, 0.037]).
    - notional_value : Valeur notionnelle du contrat (ex: 1 000 000€).
    - interval_between_payments : Durée d’une période en années (ex: 0.5 pour 6 mois).

    Retourne :
    - Un dictionnaire avec le payoff total du FRA.
    """

    try:
        # Vérifier que settlement_rates est bien une liste
        if not isinstance(forward_rates, list):
            raise ValueError("forward_rates doit être une liste de taux.")

        total_payoff = 0

        # Boucle sur chaque période pour calculer le payoff
        logger.warning(forward_rates)
        logger.warning(contract_rate)
        logger.warning(notional_value)
        logger.warning(interval_between_payments)
        
        # Vérification et conversion en un tableau numpy bien formaté
        logger.warning(type(forward_rates))
        logger.warning(type(contract_rate))
        logger.warning(type(notional_value))
        logger.warning(type(interval_between_payments))
        for R_s in forward_rates:
            logger.warning(R_s)
            logger.warning(type(R_s))
            payoff = notional_value * (R_s - contract_rate) * interval_between_payments / (1 + R_s * interval_between_payments)
            total_payoff += payoff  # Accumuler tous les payoffs
        logger.warning(total_payoff)
        return {"fra_total_valuation": ("Total FRA Valuation :", total_payoff)}

    except Exception as e:
        return {"error": str(e)}, 400

def calculate_fra_break_even_rate(forward_rates, interval_between_payments):
    """
    Calcule le taux FRA Break-Even, c'est-à-dire le taux fixe qui rend la valeur totale du FRA égale à zéro.

    Paramètres :
    - forward_rates : Liste des taux forward observés (ex: [0.032, 0.035, 0.031, 0.037]).
    - interval_between_payments : Durée d’une période en années (ex: 0.5 pour 6 mois).

    Retourne :
    - Un dictionnaire avec le taux FRA Break-Even.
    """

    try:
        # Vérifier que forward_rates est bien une liste
        if not isinstance(forward_rates, list) or len(forward_rates) == 0:
            raise ValueError("forward_rates doit être une liste non vide de taux.")

        # Fonction à minimiser : on cherche R_f tel que total_payoff = 0
        def equation(R_f):
            total_payoff = 0
            for R_s in forward_rates:
                payoff = (R_s - R_f) * interval_between_payments / (1 + R_s * interval_between_payments)
                total_payoff += payoff
            return total_payoff  # Doit être égal à 0

        # Trouver la racine de l'équation (break-even rate)
        R_f_solution = fsolve(equation, np.mean(forward_rates))[0]  # On initialise à la moyenne des forward rates

        return {"fra_break_even_rate": ("FRA Break-Even Rate:", R_f_solution)}

    except Exception as e:
        return {"error": str(e)}, 400
    
def calculate_forward_rate_curve(spot_rates, maturities, output_path="static/outputs/interest-rates-and-fixed-income/"):
    """
    Calcule toute la courbe des taux forward à partir d'une liste de taux spot et de maturités,
    puis enregistre les résultats en CSV et XLSX.
    """

    try:
        os.makedirs(output_path, exist_ok=True)
        # Vérification et conversion en numpy array
        spot_rates = np.array(spot_rates, dtype=float)
        maturities = np.array(maturities, dtype=float)

        # Vérification des entrées
        if len(spot_rates) != len(maturities):
            raise ValueError("Spot rates and maturities must have the same length.")
        if any(np.diff(maturities) <= 0):
            raise ValueError("Maturities must be strictly increasing.")

        # Calcul des taux forward pour chaque intervalle
        forward_rates = []
        forward_periods = []  # Stocker les périodes couvertes

        for i in range(len(spot_rates) - 1):
            spot_rate_1, spot_rate_2 = spot_rates[i], spot_rates[i + 1]
            time_period_1, time_period_2 = maturities[i], maturities[i + 1]

            # Calcul du taux forward
            forward_rate = ((1 + spot_rate_2) ** time_period_2 / (1 + spot_rate_1) ** time_period_1) ** (1 / (time_period_2 - time_period_1)) - 1
            forward_rates.append(forward_rate)
            forward_periods.append(f"{time_period_1} → {time_period_2}")  # Exprime la période en texte

        # Création d'un DataFrame pour les résultats avec colonnes explicites
        df_forward_rates = pd.DataFrame({
            "Forward Period": forward_periods,
            "Start Maturity (Years)": maturities[:-1],
            "End Maturity (Years)": maturities[1:],
            "Forward Rate": forward_rates
        })

        # Générer un nom de fichier unique
        random_file_name = f"forward_rate_curve_{random.randint(10**9, 10**10 - 1)}"
        csv_path = os.path.join(output_path, f"{random_file_name}.csv")
        xlsx_path = os.path.join(output_path, f"{random_file_name}.xlsx")

        # ✅ Sauvegarde du CSV
        df_forward_rates.to_csv(csv_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")

        # ✅ Sauvegarde du fichier Excel
        df_forward_rates.to_excel(xlsx_path, index=False, engine="openpyxl")

        return csv_path, xlsx_path

    except Exception as e:
        return {"error": str(e)}, 400
    

def calculate_hedging_strategy_analysis(current_position,target_rate,market_rate,fra_period,position_type):
    """
    Calcule l'impact d'une stratégie de couverture avec un FRA.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "current_position" : Montant notionnel du contrat FRA.
      - "target_rate" : Taux d'intérêt cible après couverture.
      - "market_rate" : Taux d'intérêt actuel du marché.
      - "fra_period" : Durée du FRA en années.
      - "position_type" : Type de position ("Payer" ou "Receiver").

    Retourne :
    - Un dictionnaire contenant l'analyse de la couverture.
    """
    try:
        if position_type not in ["Payer", "Receiver"]:
            raise ValueError("Position Type doit être 'Payer' ou 'Receiver'.")

        # Calcul du gain ou de la perte de la couverture
        rate_difference = market_rate - target_rate if position_type == "Payer" else target_rate - market_rate
        hedging_result = current_position * rate_difference * fra_period

        # Analyse de l'efficacité de la couverture
        hedge_effectiveness = (abs(rate_difference) / market_rate) * 100 if market_rate != 0 else 0

        return {
    "hedging_impact": ("Hedging Impact (€) :", round(hedging_result, 2)),
    "hedge_effectiveness": ("Hedge Effectiveness (%) :", round(hedge_effectiveness, 2)),
    "optimal_position": ("Optimal Position :", position_type),
    "target_achieved": ("Target Achieved :", "Yes" if abs(rate_difference) < 0.0001 else "No")
}

    except Exception as e:
        return {"error": str(e)}, 400



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
