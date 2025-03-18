import os
import random
import string
import numpy as np
import matplotlib.pyplot as plt
import io
from flask import send_file
from config import logger
from scipy.optimize import fsolve
from math import log, exp, sqrt
from scipy.stats import norm
from scipy.optimize import brentq



def save_plot(fig, filename):
    """Sauvegarde le graphe en fichier et retourne le chemin."""
    filepath = os.path.join("static/graphs", filename)
    fig.savefig(filepath, format="png")
    plt.close(fig)
    logger.error(f"Saved plot to: {filepath}")
    return f"/static/graphs/{filename}"


def generate_unique_filename(prefix="graph"):
    """Génère un nom de fichier unique avec un identifiant aléatoire."""
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{prefix}_{random_suffix}.png"


# Multiple Linear Regression
def generate_coefficients_graph(data):
    logger.info(f"Generating coefficients graph with data: {data}")
    """Génère un graphique des coefficients estimés."""
    coefficients = data.get("coefficients", [])
    
    if not coefficients:
        raise ValueError("Missing coefficients")

    # Générer les indices des variables X_k
    variable_labels = [f"X{k+1}" for k in range(len(coefficients))]

    # Création du graphique
    fig, ax = plt.subplots()
    ax.bar(variable_labels, coefficients, color="blue", alpha=0.7)
    ax.axhline(0, color="red", linestyle="dashed")
    ax.set_xlabel("Independent Variables")
    ax.set_ylabel("Beta Coefficients")
    ax.set_title("Graph of Betas")

    return save_plot(fig, generate_unique_filename("multiple_regression_1"))

def generate_observed_vs_predicted_graph(data):
    logger.warning(f"Generating observed vs predicted graph with data: {data}")
    """Génère un graphique des valeurs observées vs prédictions."""
    independent_variables = np.array(data.get("independent_variables", []))
    dependent_variables = np.array(data.get("dependent_variables", []))
    logger.info(f"Independent variables: {independent_variables}")
    logger.info(f"Dependent variables: {dependent_variables}")
    if independent_variables.size == 0 or dependent_variables.size == 0:
        raise ValueError("Missing observed or predicted values")
    
    # Vérifier et ajuster la forme de independent_variables
    if independent_variables.shape[0] < independent_variables.shape[1]:  
        # Si le nombre de lignes est inférieur au nombre de colonnes, on transpose
        independent_variables = independent_variables.T


    # Calcul des valeurs prédites avec les coefficients et l'intercept
    coefficients = np.array(data.get("coefficients", [])).flatten()
    logger.warning(f"Coefficients: {coefficients}")
    intercept = np.array(data.get("intercept", 0)).reshape(-1)
    logger.warning(f"Intercept: {intercept}")

    # Vérification manuelle des dimensions avant le produit matriciel
    if independent_variables.shape[1] != coefficients.shape[0]:
        raise ValueError(
            f"Dimension mismatch: independent_variables has {independent_variables.shape[1]} columns, "
            f"but coefficients has {coefficients.shape[0]} elements."
        )

    predicted_values = independent_variables @ coefficients + intercept  # Produit matriciellogg
    logger.warning('Now plotting 2nd graph for multiple regression')
    # Création du graphique
    fig, ax = plt.subplots()
    ax.scatter(dependent_variables, predicted_values, color="green", label="Observed vs Predicted")
    ax.plot(dependent_variables, dependent_variables, color="red", linestyle="dashed", label="Perfect Fit")
    ax.set_xlabel("Observed Values")
    ax.set_ylabel("Predicted Values")
    ax.set_title("Graph Observed vs Predicted")
    ax.legend()

    return save_plot(fig, generate_unique_filename("multiple_regression_2"))


def generate_zero_rates_curve(data):
    """
    Génère un graphique représentant la courbe des taux zéro (Zero-Coupon Yield Curve).
    
    Paramètres :
    - maturities : Liste des maturités (X-axis)
    - zero_rates : Liste des taux zéro correspondants (Y-axis)
    
    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    maturities = np.array(data.get("maturities", []))
    zero_rates = np.array(data.get("Zero Rate (Continuous Compounding)", []))
    logger.info(f"Generating zero rates curve with maturities: {maturities} and zero rates: {zero_rates}")

    if maturities.size == 0 or zero_rates.size == 0:
        raise ValueError("Missing maturities or zero rates")

    # Création du graphique
    fig, ax = plt.subplots()
    ax.plot(maturities, zero_rates, marker="o", linestyle="-", color="blue", alpha=0.7, label="Zero Rates")
    ax.set_xlabel("Maturities (Years)")
    ax.set_ylabel("Zero Rate (%)")
    ax.set_title("Zero-Coupon Yield Curve")
    ax.grid(True)
    ax.legend()

    logger.info("Generated zero rates curve")

    return save_plot(fig, generate_unique_filename("zero_coupon_yield_curve"))


def generate_zero_rates_vs_bond_prices(data):
    """
    Génère un graphique comparant les taux zéro et les prix des obligations.

    Paramètres :
    - maturities : Liste des maturités (X-axis)
    - zero_rates : Liste des taux zéro correspondants (Y-axis, première courbe)
    - bond_prices : Liste des prix des obligations (Y-axis, deuxième courbe)

    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    maturities = np.array(data.get("maturities", []))
    #Obligé de prendre cette valeur pcq on output un CSV donc on perd l'id, et on ne garde que le display name
    #TODO: à changer (pas tres propre comme méthode)
    zero_rates = np.array(data.get("Zero Rate (Continuous Compounding)", []))
    bond_prices = np.array(data.get("bond_prices", []))
    
    logger.info(f"Generating zero rates vs bond prices graph with maturities: {maturities}, zero rates: {zero_rates}, and bond prices: {bond_prices}")

    if maturities.size == 0 or zero_rates.size == 0 or bond_prices.size == 0:
        raise ValueError("Missing maturities, zero rates, or bond prices")

    # Création du graphique
    fig, ax1 = plt.subplots()

    # Courbe des taux zéro
    ax1.set_xlabel("Maturities (Years)")
    ax1.set_ylabel("Zero Rate (%)", color="blue")
    ax1.plot(maturities, zero_rates, marker="o", linestyle="-", color="blue", alpha=0.7, label="Zero Rates")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Deuxième axe pour les prix des obligations
    ax2 = ax1.twinx()
    ax2.set_ylabel("Bond Prices", color="green")
    ax2.plot(maturities, bond_prices, marker="s", linestyle="--", color="green", alpha=0.7, label="Bond Prices")
    ax2.tick_params(axis="y", labelcolor="green")

    # Titre et légende
    fig.suptitle("Zero Rates vs Bond Prices")
    ax1.grid(True)

    logger.info("Generated zero rates vs bond prices graph")

    return save_plot(fig, generate_unique_filename("zero_rates_vs_bond_prices"))

def generate_duration_contribution_graph(data):
    """
    Génère un graphique montrant la contribution de chaque période à la duration en pourcentage.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "time_periods" : Liste des périodes (X-axis)
      - "cash_flows" : Liste des cash flows correspondants
      - "discount_rates" : Liste des taux d'actualisation

    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    time_periods = np.array(data.get("time_periods", []))
    cash_flows = np.array(data.get("cash_flows", []))
    discount_rates = np.array(data.get("discount_rates", []))

    if time_periods.size == 0 or cash_flows.size == 0 or discount_rates.size == 0:
        raise ValueError("Missing time periods, cash flows, or discount rates")

    # Calcul de la contribution à la duration
    duration_contributions = (time_periods * cash_flows) / ((1 + discount_rates) ** time_periods)

    # Conversion en pourcentage
    total_duration_contribution = np.sum(duration_contributions)
    duration_contributions_percent = (duration_contributions / total_duration_contribution) * 100

    # Création du graphique
    fig, ax = plt.subplots()
    ax.bar(time_periods, duration_contributions_percent, color="blue", alpha=0.7)
    ax.set_xlabel("Time Periods")
    ax.set_ylabel("Contribution à la Duration (%)")
    ax.set_title("Contribution relative de chaque période à la Duration")
    ax.grid(axis="y")

    return save_plot(fig, generate_unique_filename("duration_contribution_percent"))

def generate_cash_flow_discounting_graph(data):
    """
    Génère un graphique montrant la valeur actualisée des cash flows dans le temps.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "time_periods" : Liste des périodes (X-axis)
      - "cash_flows" : Liste des cash flows correspondants
      - "discount_rates" : Liste des taux d'actualisation

    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    time_periods = np.array(data.get("time_periods", []))
    cash_flows = np.array(data.get("cash_flows", []))
    discount_rates = np.array(data.get("discount_rates", []))

    if time_periods.size == 0 or cash_flows.size == 0 or discount_rates.size == 0:
        raise ValueError("Missing time periods, cash flows, or discount rates")

    # Calcul de la valeur actualisée des cash flows
    discounted_cash_flows = cash_flows / ((1 + discount_rates) ** time_periods)

    # Création du graphique
    fig, ax = plt.subplots()
    ax.plot(time_periods, discounted_cash_flows, marker="o", linestyle="-", color="green", alpha=0.7, label="Discounted Cash Flows")
    ax.set_xlabel("Time Periods")
    ax.set_ylabel("Discounted Cash Flow Value")
    ax.set_title("Valeur actualisée des Cash Flows")
    ax.grid(True)
    ax.legend()

    return save_plot(fig, generate_unique_filename("cash_flow_discounting"))
    

def generate_extended_zero_rate_curve_graph_fixed(data):
    """
    Génère un graphique montrant la courbe des taux zéro avant et après extension avec les taux de swap.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "Maturity" : Liste des maturités disponibles (X-axis)
      - "libor_rates" : Liste des taux zéro LIBOR correspondants
      - "Interpolated Zero Rates" : Liste des taux zéro après extension

    Retourne :
    - Un objet `fig` matplotlib contenant le graphique (sans le sauvegarder).
    """

    try:
        # Extraction des données
        maturities = np.array(data.get("Maturity", []))
        libor_rates = np.array(data.get("libor_rates", []))
        extended_rates = np.array(data.get("Interpolated Zero Rates", []))

        # Vérification de la présence des données nécessaires
        if maturities.size == 0 or libor_rates.size == 0 or extended_rates.size == 0:
            raise ValueError("Missing maturities, LIBOR rates, or extended zero rates")

        # Création du graphique avec un design amélioré
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(maturities, extended_rates, marker="s", linestyle="-", 
                color="crimson", alpha=0.9, markersize=5, linewidth=2, label="Extended Zero Rates")

        ax.set_xlabel("Maturity (Years)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Zero Rates (%)", fontsize=12, fontweight="bold")
        ax.set_title("Extended LIBOR Curve", fontsize=14, fontweight="bold", color="darkblue")
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
        ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
        ax.set_facecolor("#f5f5f5")

        return save_plot(fig, generate_unique_filename("extended_zero_curve_swap_rates"))

    except Exception as e:
        raise ValueError(f"Error generating extended zero rate curve graph: {e}")
    

def generate_extended_zero_rate_curve_graph_fra(data):
    """
    Génère un graphique montrant la courbe des taux zéro avant et après extension avec les taux FRA.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "Maturity" : Liste des maturités disponibles (X-axis)
      - "libor_rates" : Liste des taux zéro LIBOR correspondants
      - "Interpolated Zero Rates" : Liste des taux zéro après extension avec les FRA

    Retourne :
    - Un objet `fig` matplotlib contenant le graphique (sans le sauvegarder).
    """

    try:
        # Extraction des données
        maturities = np.array(data.get("Maturity", []))
        libor_rates = np.array(data.get("libor_rates", []))
        extended_rates = np.array(data.get("Interpolated Zero Rates", []))

        # Vérification de la présence des données nécessaires
        if maturities.size == 0 or libor_rates.size == 0 or extended_rates.size == 0:
            raise ValueError("Missing maturities, LIBOR rates, or extended zero rates")

        # Création du graphique avec un design amélioré
        fig, ax = plt.subplots(figsize=(9, 6))

        #TODO : Impossible actuellement car je ne garde pas les maturités initiales (à changer, et c'est pareil pour SWAP rates : ca bloque l'affichage des taux libor initiaux, ce qui est dommage).
        # # Affichage des LIBOR Zero Rates initiaux
        # ax.plot(maturities[:len(libor_rates)], libor_rates, marker="o", linestyle="--", 
        #         color="royalblue", alpha=0.8, markersize=6, linewidth=2, label="LIBOR Zero Rates")

        # Affichage des taux étendus via FRA
        ax.plot(maturities, extended_rates, marker="s", linestyle="-", 
                color="darkorange", alpha=0.9, markersize=5, linewidth=2, label="Extended Zero Rates (FRA)")

        ax.set_xlabel("Maturity (Years)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Zero Rates (%)", fontsize=12, fontweight="bold")
        ax.set_title("Extended Zero Curve with FRA Rates", fontsize=14, fontweight="bold", color="darkblue")
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
        ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
        ax.set_facecolor("#f5f5f5")

        return save_plot(fig, generate_unique_filename("extended_zero_curve_fra_rates"))

    except Exception as e:
        raise ValueError(f"Error generating extended zero rate curve graph with FRA: {e}")
    

def generate_fra_payoff_evolution_graph(data):
    """
    Génère un graphique montrant l'évolution du payoff du FRA sur plusieurs périodes.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "settlement_rates" : Liste des taux flottants observés.
      - "contract_rate" : Taux contractuel fixe.
      - "notional_value" : Valeur notionnelle du FRA.
      - "interval_between_payments" : Durée d'une période en années.

    Retourne :
    - Un objet `fig` matplotlib contenant le graphique (sans le sauvegarder).
    """

    try:
        # Extraction des données
        settlement_rates = np.array(data.get("settlement_rates", []))
        contract_rate = data.get("contract_rate", 0.0)
        notional_value = data.get("notional_value", 1_000_000)  # Par défaut 1 million
        interval = data.get("interval_between_payments", 0.5)  # Par défaut 6 mois

        # Vérification de la présence des données nécessaires
        if settlement_rates.size == 0:
            raise ValueError("Missing settlement rates")

        # Calcul des payoffs pour chaque période
        payoff_per_period = notional_value * (settlement_rates - contract_rate) * interval / (1 + settlement_rates * interval)
        periods = np.arange(1, len(settlement_rates) + 1)

        # Création du graphique
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(periods, payoff_per_period, marker="o", linestyle="-", color="green", markersize=6, linewidth=2, label="FRA Payoff per Period")

        ax.axhline(0, color="black", linestyle="--", linewidth=1.2)  # Ligne horizontale zéro

        ax.set_xlabel("Periods", fontsize=12, fontweight="bold")
        ax.set_ylabel("Payoff (€)", fontsize=12, fontweight="bold")
        ax.set_title("Evolution of FRA Payoff Over Time", fontsize=14, fontweight="bold", color="darkblue")
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
        ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
        ax.set_facecolor("#f5f5f5")

        return save_plot(fig, generate_unique_filename("fra_payoff_evolution"))

    except Exception as e:
        raise ValueError(f"Error generating FRA payoff evolution graph: {e}")


def generate_fra_fixed_vs_floating_rates_graph(data):
    """
    Génère un graphique comparant le taux contractuel fixe et les taux flottants sur plusieurs périodes.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "settlement_rates" : Liste des taux flottants observés.
      - "contract_rate" : Taux contractuel fixe.

    Retourne :
    - Un objet `fig` matplotlib contenant le graphique (sans le sauvegarder).
    """

    try:
        # Extraction des données
        settlement_rates = np.array(data.get("settlement_rates", []))
        contract_rate = data.get("contract_rate", 0.0)

        # Vérification de la présence des données nécessaires
        if settlement_rates.size == 0:
            raise ValueError("Missing settlement rates")

        # Création de l'axe des périodes
        periods = np.arange(1, len(settlement_rates) + 1)

        # Création du graphique
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(periods, settlement_rates, marker="o", linestyle="-", color="red", markersize=6, linewidth=2, label="Floating Rates (Market)")
        ax.axhline(contract_rate, color="blue", linestyle="--", linewidth=2, label="Fixed Contract Rate")

        ax.set_xlabel("Periods", fontsize=12, fontweight="bold")
        ax.set_ylabel("Interest Rates (%)", fontsize=12, fontweight="bold")
        ax.set_title("Comparison of Fixed vs Floating Rates", fontsize=14, fontweight="bold", color="darkblue")
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
        ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
        ax.set_facecolor("#f5f5f5")

        return save_plot(fig, generate_unique_filename("fra_fixed_vs_floating_rates"))

    except Exception as e:
        raise ValueError(f"Error generating FRA fixed vs floating rates graph: {e}")

def generate_forward_rate_curve(data):
    logger.warning(data)
    maturities = np.array(data.get("maturities", []))
    #TODO
    forward_rates = np.array(data.get("Forward Rate", []))
    forward_period = float((data.get("forward_period", "1")))
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(maturities[1:], forward_rates, marker="o", linestyle="-", color="blue", markersize=6, linewidth=2, label=f"{forward_period}-year Forward Rate Curve")

    ax.set_xlabel("Maturities (Years)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Forward Rate", fontsize=12, fontweight="bold")
    ax.set_title("Forward Rate Curve", fontsize=14, fontweight="bold", color="darkblue")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
    ax.set_facecolor("#f5f5f5")

    return save_plot(fig, generate_unique_filename("forward_rate_curve"))

# Function to generate spot vs forward rate comparison plot
def generate_spot_vs_forward_comparison(data):
    maturities = np.array(data.get("maturities", []))
    #TODO
    forward_rates = np.array(data.get("Forward Rate", []))
    spot_rates = np.array(data.get("spot_rates", []))
    forward_period = float((data.get("forward_period", "1")))
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(maturities, spot_rates, marker="o", linestyle="-", color="red", markersize=6, linewidth=2, label="Spot Rates")
    ax.plot(maturities[1:], forward_rates, marker="s", linestyle="--", color="blue", markersize=6, linewidth=2, label=f"{forward_period}-year Forward Rates")

    ax.set_xlabel("Maturities (Years)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Rate", fontsize=12, fontweight="bold")
    ax.set_title("Spot Rates vs Forward Rates", fontsize=14, fontweight="bold", color="darkblue")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)
    ax.set_facecolor("#f5f5f5")

    return save_plot(fig, generate_unique_filename("forward_rate_vs_spot_rate_curve"))



def plot_fra_payoff(data):
    """
    Génère un graphique montrant l'évolution du payoff du FRA sur plusieurs périodes.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "forward_rates" : Liste des taux forward observés.
      - "contract_rate" : Taux contractuel fixe.
      - "notional_value" : Valeur notionnelle du FRA.
      - "interval_between_payments" : Durée d'une période en années.

    Retourne :
    - Un graphique matplotlib contenant l'évolution du payoff du FRA.
    """
    try:
        forward_rates = np.array(data.get("forward_rates", []), dtype=float)
        contract_rate = float(data.get('contract_rate'))
        notional_value = float(data.get('notional_value'))
        interval_between_payments = float(data.get('interval_between_payments'))

        # Vérification des données
        if forward_rates.size == 0:
            raise ValueError("Les taux forward sont vides.")

        periods = np.arange(1, len(forward_rates) + 1)
        payoffs = [
            notional_value * (R_s - contract_rate) * interval_between_payments / (1 + R_s * interval_between_payments)
            for R_s in forward_rates
        ]

        # Création du graphique
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.plot(periods, payoffs, marker="o", linestyle="-", color="green", linewidth=2, label="FRA Payoff")

        ax.axhline(0, color="black", linestyle="--", linewidth=1.2)  # Ligne horizontale zéro
        ax.set_xlabel("Périodes", fontsize=12, fontweight="bold")
        ax.set_ylabel("Payoff (€)", fontsize=12, fontweight="bold")
        ax.set_title("Évolution du Payoff du FRA", fontsize=14, fontweight="bold", color="darkblue")
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
        ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)

        return save_plot(fig, generate_unique_filename("fra_valuation"))

    except Exception as e:
        print(f"Erreur lors de la génération du graphique: {e}")


def plot_fra_fixed_vs_forward(data):
    forward_rates = np.array(data.get("forward_rates", []), dtype=float)
    contract_rate = float(data.get('contract_rate'))
    periods = np.arange(1, len(forward_rates) + 1)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(periods, forward_rates, marker="o", linestyle="--", color="blue", linewidth=2, label="Forward Rates")
    ax.axhline(y=contract_rate, color="red", linestyle="-", linewidth=2, label="Fixed Rate (Contract)")

    ax.set_xlabel("Périodes", fontsize=12, fontweight="bold")
    ax.set_ylabel("Taux (%)", fontsize=12, fontweight="bold")
    ax.set_title("Comparaison du Taux Contractuel et des Taux Forward", fontsize=14, fontweight="bold", color="darkblue")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)

    return save_plot(fig, generate_unique_filename("fra_valuation_fix_vs_float"))

# def plot_fra_break_even_vs_forward(data):
#     forward_rates = np.array(data.get("forward_rates", []), dtype=float)
#     break_even_rate = float(data.get("fra_break_even_rate"))

#     if forward_rates.size == 0:
#         raise ValueError("Les taux forward sont vides.")

#     fig, ax = plt.subplots(figsize=(9, 6))
#     ax.plot(forward_rates, [break_even_rate] * len(forward_rates), marker="o", linestyle="-", color="purple", linewidth=2, label="FRA Break-Even Rate")

#     ax.set_xlabel("Taux Forward (%)", fontsize=12, fontweight="bold")
#     ax.set_ylabel("FRA Break-Even Rate (%)", fontsize=12, fontweight="bold")
#     ax.set_title("Relation entre Taux Forward et FRA Break-Even", fontsize=14, fontweight="bold", color="darkblue")
#     ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
#     ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)

#     return save_plot(fig, generate_unique_filename("fra_break_even_vs_forward"))


# def plot_fra_break_even_vs_maturity(data):
#     forward_rates = np.array(data.get("forward_rates", []), dtype=float)
#     interval_between_payments = float(data.get("interval_between_payments"))
#     break_even_rate = float(data.get("fra_break_even_rate"))
#     maturities = [interval_between_payments*i for i in range(1,len(forward_rates))]
#     if len(maturities) == 0:
#         raise ValueError("Les maturités sont vides.")

#     fig, ax = plt.subplots(figsize=(9, 6))
#     ax.plot(maturities, [break_even_rate] * len(maturities), marker="s", linestyle="--", color="orange", linewidth=2, label="FRA Break-Even Rate")

#     ax.set_xlabel("Durée du FRA (Années)", fontsize=12, fontweight="bold")
#     ax.set_ylabel("FRA Break-Even Rate (%)", fontsize=12, fontweight="bold")
#     ax.set_title("Sensibilité du FRA Break-Even Rate en fonction de la Durée", fontsize=14, fontweight="bold", color="darkblue")
#     ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
#     ax.legend(fontsize=11, loc="best", frameon=True, shadow=True, fancybox=True)

#     return save_plot(fig, generate_unique_filename("fra_break_even_vs_maturity"))


def plot_binomial_tree_with_dividend(data):
    logger.info(f"Generating binomial tree graph with data: {data}")

    underlying_price = float(data.get("underlying_price"))
    strike_price = float(data.get("strike_price", 0) or 0)
    time_to_maturity = float(data.get("time_to_maturity", 0) or 0)
    risk_free_rate = float(data.get("risk_free_rate", 0) or 0)
    volatility = float(data.get("volatility", 0) or 0)
    steps = int(data.get("steps"))
    dividend_yield = (data.get("dividend_yield", 0))
    dividend_yield = float(dividend_yield) if dividend_yield else 0

    if None in (underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, steps):
        raise ValueError("Missing one or more required inputs for binomial tree")

    dt = time_to_maturity / steps
    u = np.exp((risk_free_rate - dividend_yield) * dt + volatility * np.sqrt(dt))
    d = np.exp((risk_free_rate - dividend_yield) * dt - volatility * np.sqrt(dt))

    stock_price_tree = np.zeros((steps + 1, steps + 1))
    logger.info(f"Building binomial tree with {steps} steps")
    # Construire l'arbre binomial
    for i in range(steps + 1):
        for j in range(i + 1):
            stock_price_tree[j, i] = underlying_price * (u ** (i - j)) * (d ** j)
    logger.info("Built binomial tree")
    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i in range(steps + 1):
        for j in range(i + 1):
            ax.text(i, stock_price_tree[j, i], f"{stock_price_tree[j, i]:.2f}", ha="center", va="center", fontsize=8)
            if i < steps:
                ax.plot([i, i + 1], [stock_price_tree[j, i], stock_price_tree[j, i + 1]], 'k-', lw=0.5)
                ax.plot([i, i + 1], [stock_price_tree[j, i], stock_price_tree[j + 1, i + 1]], 'k-', lw=0.5)
    logger.info("Plotted binomial tree")
    ax.set_title("Binomial Tree with Dividend Adjustment")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Underlying Price")
    
    return save_plot(fig, generate_unique_filename("binomial_tree_with_dividend"))

def plot_pnl_diagram_with_dividend(data):
    logger.info(f"Generating P&L diagram with data: {data}")

    # ✅ Extraction et conversion des paramètres
    option_type = data.get("option_type")
    underlying_price = float(data.get("underlying_price"))
    strike_price = float(data.get("strike_price"))
    option_price = float(data.get("option_price_with_dividend"))  # Prix de l'option (c)
    dividend_yield = data.get("dividend_yield", 0)
    position_type = data.get("position_type", "LONG")  # Par défaut en LONG

    logger.info(f"Option type: {option_type}, Underlying Price: {underlying_price}, Strike Price: {strike_price}, Option Price: {option_price}, Dividend Yield: {dividend_yield}, Position Type: {position_type}")

    if dividend_yield:
        dividend_yield = float(dividend_yield)

    if None in (option_type, underlying_price, strike_price, option_price):
        raise ValueError("Missing one or more required inputs for P&L diagram")

    # ✅ Génération de la plage de prix à la maturité
    price_range = np.linspace(0.5 * underlying_price, 1.5 * underlying_price, 100)

    # ✅ Calcul du P&L en fonction du type d'option et de la position
    if option_type == "CALL":
        pnl = np.maximum(price_range - strike_price, 0) - option_price
    else:
        pnl = np.maximum(strike_price - price_range, 0) - option_price
    
    # 🔄 Si la position est SHORT, on inverse le payoff
    if position_type == "SHORT":
        pnl = -pnl

    # ✅ Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(price_range, pnl, label=f"{position_type} {option_type} Option P&L", color="blue", linewidth=2)
    
    # ✅ Ligne de coût initial
    ax.axhline(-option_price if position_type == "LONG" else option_price, color="red", linestyle="--", label=f"Initial Cost ({-option_price if position_type == 'LONG' else option_price})")

    # ✅ Ligne du prix d'exercice (K)
    ax.axvline(strike_price, color="green", linestyle="--", label=f"Strike Price (K={strike_price})")

    # ✅ Breakeven point = K + c pour un CALL, K - c pour un PUT
    breakeven = strike_price + option_price if option_type == "CALL" else strike_price - option_price
    ax.axvline(breakeven, color="orange", linestyle="--", label=f"Breakeven at {round(breakeven, 2)}")

    # ✅ Titres et légende
    ax.set_title(f"{position_type} {option_type} Option P&L at Maturity")
    ax.set_xlabel("Underlying Price at Maturity")
    ax.set_ylabel("Profit / Loss")
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.legend()

    plt.grid(True)

    # ✅ Sauvegarde du graphe
    return save_plot(fig, generate_unique_filename(f"pnl_with_dividend_{position_type.lower()}"))



# ✅ Payoff Curve
def plot_payoff_curve(data):
    logger.info(f"Generating payoff curve with data: {data}")
    
    option_type = data.get("option_type")
    underlying_price = data.get("underlying_price")
    strike_price = data.get("strike_price")

    if None in (option_type, underlying_price, strike_price):
        raise ValueError("Missing one or more required inputs for payoff curve")

    price_range = np.linspace(0.5 * strike_price, 1.5 * strike_price, 100)

    if option_type == "CALL":
        payoff = np.maximum(price_range - strike_price, 0)
    else:
        payoff = np.maximum(strike_price - price_range, 0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(price_range, payoff, label=f'{option_type} Option Payoff', color='blue')
    ax.axhline(0, color='black', linewidth=1, linestyle="--")
    ax.axvline(strike_price, color='red', linestyle="--", label=f"Strike Price: {strike_price}")

    ax.set_title(f"{option_type} Option Payoff Curve")
    ax.set_xlabel("Underlying Price")
    ax.set_ylabel("Payoff")
    ax.legend()
    plt.grid(True)

    return save_plot(fig, generate_unique_filename("black_scholes_payoff"))

from scipy.stats import norm
from numpy import log, sqrt, exp
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from math import log, sqrt, exp

def plot_greeks_sensitivity(data):
    logger.info(f"Generating greeks sensitivity with data: {data}")
    
    # ✅ Extraction des inputs depuis le dictionnaire `data`
    option_type = data.get("option_type")
    position_type = data.get("position_type")  # Ajout de la position (LONG/SHORT)
    underlying_price = float(data.get("underlying_price"))
    strike_price = float(data.get("strike_price"))
    time_to_maturity = float(data.get("time_to_maturity"))
    risk_free_rate = float(data.get("risk_free_rate"))
    volatility = float(data.get("volatility"))
    dividend_yield = float(data.get("dividend_yield")) if data.get("dividend_yield") else 0.0

    if None in (option_type, position_type, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        raise ValueError("Missing one or more required inputs for Greeks")

    # ✅ Plage de prix du sous-jacent pour la courbe
    price_range = np.linspace(0.5 * strike_price, 1.5 * strike_price, 100)
    
    delta = []
    gamma = []
    theta = []
    vega = []

    # ✅ Calculer la valeur fixe des Greeks au prix du sous-jacent (pour affichage dans la légende)
    d1 = (log(underlying_price / strike_price) + (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)

    if option_type == "CALL":
        base_delta = exp(-dividend_yield * time_to_maturity) * norm.cdf(d1)
    else:
        base_delta = -exp(-dividend_yield * time_to_maturity) * norm.cdf(-d1)

    base_gamma = norm.pdf(d1) / (underlying_price * volatility * sqrt(time_to_maturity))
    base_theta = (-underlying_price * norm.pdf(d1) * volatility * exp(-dividend_yield * time_to_maturity) / (2 * sqrt(time_to_maturity))
                  - risk_free_rate * strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2 if option_type == "CALL" else -d2)
                  + dividend_yield * underlying_price * exp(-dividend_yield * time_to_maturity) * norm.cdf(d1 if option_type == "CALL" else -d1)) / 365
    base_vega = (underlying_price * exp(-dividend_yield * time_to_maturity) * norm.pdf(d1) * sqrt(time_to_maturity)) / 100
    
    # ✅ Ajustement pour la position LONG/SHORT
    if position_type == "SHORT":
        final_delta = -base_delta
        final_theta = -base_theta
        final_vega = -base_vega
    else:
        final_delta = base_delta
        final_theta = base_theta
        final_vega = base_vega

    final_gamma = base_gamma  # Gamma reste inchangé

    # ✅ Générer la courbe complète des Greeks
    for S in price_range:
        d1 = (log(S / strike_price) + (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        if option_type == "CALL":
            base_delta = exp(-dividend_yield * time_to_maturity) * norm.cdf(d1)
        else:
            base_delta = -exp(-dividend_yield * time_to_maturity) * norm.cdf(-d1)

        base_gamma = norm.pdf(d1) / (S * volatility * sqrt(time_to_maturity))
        base_theta = (-S * norm.pdf(d1) * volatility * exp(-dividend_yield * time_to_maturity) / (2 * sqrt(time_to_maturity))
                     - risk_free_rate * strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2 if option_type == "CALL" else -d2)
                     + dividend_yield * S * exp(-dividend_yield * time_to_maturity) * norm.cdf(d1 if option_type == "CALL" else -d1)) / 365
        base_vega = (S * exp(-dividend_yield * time_to_maturity) * norm.pdf(d1) * sqrt(time_to_maturity)) / 100

        # ✅ Ajustement selon LONG/SHORT
        delta.append(-base_delta if position_type == "SHORT" else base_delta)
        gamma.append(base_gamma)  # Gamma reste inchangé
        theta.append(-base_theta if position_type == "SHORT" else base_theta)
        vega.append(-base_vega if position_type == "SHORT" else base_vega)

    # ✅ Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(price_range, delta, label=f"Delta (Current: {round(final_delta, 4)})", color="blue")
    ax.plot(price_range, gamma, label=f"Gamma (Current: {round(final_gamma, 4)})", color="red")
    ax.plot(price_range, theta, label=f"Theta (Current: {round(final_theta, 4)})", color="green")
    ax.plot(price_range, vega, label=f"Vega (Current: {round(final_vega, 4)})", color="purple")

    # ✅ Marquer le prix actuel du sous-jacent avec une ligne verticale
    ax.axvline(underlying_price, color="black", linestyle="--", label=f"Underlying Price: {underlying_price}")

    # ✅ Configurations supplémentaires
    ax.set_title(f"{position_type} {option_type} Option Greeks Sensitivity")
    ax.set_xlabel("Underlying Price")
    ax.set_ylabel("Value")
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.legend()

    plt.grid(True)

    # ✅ Sauvegarde du graphe
    return save_plot(fig, generate_unique_filename(f"{position_type.lower()}_{option_type.lower()}_greeks_with_dividend"))







def plot_simulation_results_histogram(data):
    logger.info(f"Generating simulation results histogram with data: {data}")
    
    option_type = data.get("option_type")
    option_style = data.get("option_style")
    underlying_price = float(data.get("underlying_price"))
    strike_price = float(data.get("strike_price"))
    risk_free_rate = float(data.get("risk_free_rate"))
    volatility = float(data.get("volatility"))
    dividend_yield = float(data.get("dividend_yield") or 0)
    num_simulations = int(data.get("num_simulations"))
    num_steps = int(data.get("num_steps"))
    option_price = float(data.get("option_price"))

    if None in (option_type, option_style, underlying_price, strike_price, risk_free_rate, volatility, dividend_yield, num_simulations, num_steps, option_price):
        raise ValueError("Missing one or more required inputs for simulation histogram")

    # ✅ Fix: dt basé sur le temps de maturité divisé par le nombre de pas
    dt = data.get("time_to_maturity") / num_steps
    payoffs = []

    np.random.seed(42)
    for _ in range(num_simulations):
        path = [underlying_price]
        for _ in range(num_steps):
            path.append(path[-1] * np.exp(
                (risk_free_rate - dividend_yield - 0.5 * volatility ** 2) * dt +
                volatility * np.sqrt(dt) * np.random.randn()
            ))
        
        # ✅ Payoff final basé sur le type d'option
        if option_type == "CALL":
            payoff = max(0, path[-1] - strike_price)
        else:
            payoff = max(0, strike_price - path[-1])

        payoffs.append(payoff)

    # ✅ Création de l'histogramme
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(payoffs, bins=50, color="skyblue", edgecolor="black", alpha=0.7)

    # ✅ Ajout d'une ligne verticale pour le prix de l'option simulé
    ax.axvline(option_price, color="red", linestyle="--", label=f"Theoretical Option Price: {round(option_price, 4)}")

    ax.set_title(f"{option_type} Option Simulation Results Histogram")
    ax.set_xlabel("Simulated Payoff")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.grid(True)

    # ✅ Sauvegarde du graphe
    return save_plot(fig, generate_unique_filename("monte_carlo_histogram"))

# ==================================
def plot_convergence_plot(data):
    logger.info(f"Generating convergence plot with data: {data}")
    
    option_type = data.get("option_type")
    option_style = data.get("option_style")
    underlying_price = float(data.get("underlying_price"))
    strike_price = float(data.get("strike_price"))
    risk_free_rate = float(data.get("risk_free_rate"))
    volatility = float(data.get("volatility"))
    dividend_yield = float(data.get("dividend_yield") or 0)
    num_simulations = int(data.get("num_simulations"))
    num_steps = int(data.get("num_steps"))
    time_to_maturity = float(data.get("time_to_maturity"))
    option_price = float(data.get("option_price"))

    if None in (option_type, option_style, underlying_price, strike_price, risk_free_rate, volatility, dividend_yield, num_simulations, num_steps, option_price):
        raise ValueError("Missing one or more required inputs for convergence plot")

    # ✅ Fix: dt basé sur le temps de maturité divisé par le nombre de pas
    dt = time_to_maturity / num_steps
    discount_factor = np.exp(-risk_free_rate * time_to_maturity)  # ✅ Facteur d'actualisation
    payoffs = []
    cumulative_mean = []

    np.random.seed(42)  # ✅ Fixer le seed pour la reproductibilité

    for i in range(num_simulations):
        path = np.zeros(num_steps + 1)
        path[0] = underlying_price
        
        for t in range(1, num_steps + 1):
            z = np.random.randn()
            path[t] = path[t - 1] * np.exp(
                (risk_free_rate - dividend_yield - 0.5 * volatility ** 2) * dt +
                volatility * np.sqrt(dt) * z
            )

        # ✅ Payoff en fonction du type d'option
        if option_style == "European":
            if option_type == "CALL":
                payoff = max(0, path[-1] - strike_price)
            elif option_type == "PUT":
                payoff = max(0, strike_price - path[-1])
            else:
                raise ValueError("Invalid option type. Must be 'CALL' or 'PUT'.")

        elif option_style == "Asian":
            average_price = np.mean(path)
            if option_type == "CALL":
                payoff = max(0, average_price - strike_price)
            elif option_type == "PUT":
                payoff = max(0, strike_price - average_price)
            else:
                raise ValueError("Invalid option type. Must be 'CALL' or 'PUT'.")

        else:
            raise ValueError("Invalid option style. Must be 'European' or 'Asian'.")

        payoffs.append(payoff)
        cumulative_mean.append(np.mean(payoffs) * discount_factor)

    # ✅ Création du graphique de convergence
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, num_simulations + 1), cumulative_mean, label="Convergence", color="blue")
    ax.axhline(option_price, color="red", linestyle="--", label=f"Theoretical Option Price: {round(option_price, 4)}")

    ax.set_title(f"{option_style} {option_type} Option Convergence Plot")
    ax.set_xlabel("Number of Simulations")
    ax.set_ylabel("Option Price")
    ax.legend()
    plt.grid(True)

    # ✅ Sauvegarde du graphe
    return save_plot(fig, generate_unique_filename("monte_carlo_convergence"))
