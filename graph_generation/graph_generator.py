import os
import random
import string
import numpy as np
import matplotlib.pyplot as plt
import io
from flask import send_file
from config import logger

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

def generate_extended_zero_rate_curve_graph(data):
    """
    Génère un graphique montrant la courbe des taux zéro avant et après extension avec les taux de swap.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "Maturity" : Liste des maturités disponibles (X-axis)
      - "libor_rates" : Liste des taux zéro LIBOR correspondants
      - "Extended Zero Rates" : Liste des taux zéro après extension

    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    logger.info(data)

    # Extraction des données depuis le CSV
    maturities = np.array(data.get("Maturity", []))
    extended_zero_rates = np.array(data.get("Extended Zero Rates", []))
    libor_rates = np.array(data.get("libor_rates", []))
    libor_tenors = np.array(data.get("libor_tenors", []))  # Maturités LIBOR d'origine

    if maturities.size == 0 or libor_rates.size == 0 or extended_zero_rates.size == 0:
        raise ValueError("Missing maturities, LIBOR rates, or extended zero rates")

    # 🔹 **Sélectionner les bons indices pour libor_maturities**
    libor_maturities = []
    for tenor in libor_tenors:
        if tenor in maturities:
            libor_maturities.append(tenor)

    libor_maturities = np.array(libor_maturities)

    # 🔹 **Vérification des longueurs avant de tracer le graphique**
    if len(libor_maturities) != len(libor_rates):
        raise ValueError(f"Mismatch: libor_maturities ({len(libor_maturities)}) != libor_rates ({len(libor_rates)})")

    # Création du graphique
    fig, ax = plt.subplots()
    libor_rates = [x*100 for x in libor_rates]
    extended_zero_rates = [x*100 for x in extended_zero_rates]
    ax.plot(libor_maturities, libor_rates, marker="o", linestyle="--", color="blue", alpha=0.7, label="LIBOR Zero Rates")
    ax.plot(maturities, extended_zero_rates, marker="s", linestyle="-", color="red", alpha=0.7, label="Extended Zero Rates")

    ax.set_xlabel("Maturities (Years)")
    ax.set_ylabel("Zero Rates (%)")
    ax.set_title("Extended LIBOR curve")
    ax.grid(True)
    ax.legend()

    return save_plot(fig, generate_unique_filename("extended_zero_rate_curve"))




def generate_zero_rate_difference_graph(data):
    """
    Génère un graphique montrant la différence entre les taux zéro LIBOR et les taux zéro après extension.

    Paramètres :
    - data : Dictionnaire contenant les inputs nécessaires :
      - "Maturity" : Liste des maturités disponibles (X-axis)
      - "libor_tenors" : Liste des maturités LIBOR originales
      - "libor_rates" : Liste des taux LIBOR correspondants
      - "Extended Zero Rates" : Liste des taux zéro après extension

    Retourne :
    - Le chemin du fichier où le graphique est sauvegardé.
    """
    logger.info(f"Data received: {data}")

    # Extraction des données
    maturities = np.array(data.get("Maturity", []))
    extended_zero_rates = np.array(data.get("Extended Zero Rates", []))
    libor_tenors = np.array(data.get("libor_tenors", []))  # Maturités des taux LIBOR
    libor_rates = np.array(data.get("libor_rates", []))  # Taux LIBOR correspondants

    if maturities.size == 0 or libor_rates.size == 0 or extended_zero_rates.size == 0:
        raise ValueError("Missing maturities, LIBOR rates, or extended zero rates")

    # Filtrage des maturités communes
    common_indices = np.isin(maturities, libor_tenors)
    maturities_filtered = maturities[common_indices]
    extended_rates_filtered = extended_zero_rates[common_indices]

    # Associer les taux LIBOR correspondants à ces maturités
    libor_rates_filtered = np.array([libor_rates[np.where(libor_tenors == m)[0][0]] for m in maturities_filtered])

    # Calcul de la différence entre les taux zéro avant et après extension
    zero_rate_difference = extended_rates_filtered - libor_rates_filtered
    logger.warning(zero_rate_difference)
    # Création du graphique
    fig, ax = plt.subplots()
    ax.bar(maturities_filtered, zero_rate_difference, color="purple", alpha=0.7)

    ax.set_xlabel("Maturities (Years)")
    ax.set_ylabel("Zero Rate Difference (%)")
    ax.set_title("Différence entre les Taux Zéro LIBOR et Étendus")
    ax.grid(axis="y")

    return save_plot(fig, generate_unique_filename("zero_rate_difference"))
