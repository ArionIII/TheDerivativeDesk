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
    ax.set_xlabel("Variables Indépendantes")
    ax.set_ylabel("Valeur du Coefficient")
    ax.set_title("Graphique des Coefficients Estimés")

    return save_plot(fig, generate_unique_filename("multiple_regression_1"))

def generate_observed_vs_predicted_graph(data):
    logger.info(f"Generating observed vs predicted graph with data: {data}")
    """Génère un graphique des valeurs observées vs prédictions."""
    independent_variables = np.array(data.get("independent_variables", []))
    dependent_variables = np.array(data.get("dependent_variables", []))
    logger.info(f"Independent variables: {independent_variables}")
    logger.info(f"Dependent variables: {dependent_variables}")
    if independent_variables.size == 0 or dependent_variables.size == 0:
        raise ValueError("Missing observed or predicted values")

    # Calcul des valeurs prédites avec les coefficients et l'intercept
    coefficients = np.array(data.get("coefficients", []))
    intercept = data.get("intercept", 0)
    predicted_values = independent_variables @ coefficients + intercept  # Produit matriciel

    # Création du graphique
    fig, ax = plt.subplots()
    ax.scatter(dependent_variables, predicted_values, color="green", label="Observed vs Predicted")
    ax.plot(dependent_variables, dependent_variables, color="red", linestyle="dashed", label="Perfect Fit")
    ax.set_xlabel("Valeurs Observées")
    ax.set_ylabel("Valeurs Prédites")
    ax.set_title("Graphique Observed vs Predicted")
    ax.legend()

    return save_plot(fig, generate_unique_filename("multiple_regression_2"))
