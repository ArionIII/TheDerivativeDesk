import numpy as np
from scipy.optimize import newton
from math import log, sqrt, exp
from scipy.stats import norm
from math import exp
from config import logger


def binomial_dividend_pricing(option_type, option_style, underlying_price, strike_price, 
                              time_to_maturity, risk_free_rate, volatility, dividend_yield, steps, position_type):
    """
    Price an option using a binomial tree model adjusted for continuous dividend payments.
    
    Parameters:
    - option_type: "CALL" or "PUT"
    - option_style: "American" or "European"
    - underlying_price: Current price of the underlying asset
    - strike_price: Option strike price
    - time_to_maturity: Time to maturity in years
    - risk_free_rate: Risk-free interest rate
    - volatility: Volatility of the underlying asset
    - dividend_yield: Continuous dividend yield (set to 0 if None)
    - steps: Number of steps in the binomial tree

    Returns:
    - Option Price
    """
    try:
        logger.info("Starting binomial pricing with dividends...")

        # ✅ Vérification des types et conversion
        underlying_price = float(underlying_price)
        strike_price = float(strike_price)
        time_to_maturity = float(time_to_maturity)
        risk_free_rate = float(risk_free_rate)
        volatility = float(volatility)
        steps = int(steps)
        dividend_yield = float(dividend_yield) if dividend_yield is not None and dividend_yield != '' else 0.0

        logger.info(f"Underlying Price: {underlying_price}, Strike Price: {strike_price}, Time to Maturity: {time_to_maturity}")
        logger.info(f"Risk-Free Rate: {risk_free_rate}, Volatility: {volatility}, Dividend Yield: {dividend_yield}, Steps: {steps}")

        dt = time_to_maturity / steps
        discount_factor = exp(-risk_free_rate * dt)

        # ✅ Facteurs de montée (u) et de descente (d) ajustés pour le dividende
        u = exp((risk_free_rate - dividend_yield) * dt + volatility * sqrt(dt))
        d = exp((risk_free_rate - dividend_yield) * dt - volatility * sqrt(dt))

        # ✅ Probabilité neutre au risque ajustée pour le dividende
        p = (exp((risk_free_rate - dividend_yield) * dt) - d) / (u - d)

        logger.info(f"u = {u}, d = {d}, p = {p}")

        # ✅ Initialisation du tableau des prix finaux à la maturité
        option_values = np.zeros(steps + 1)
        for i in range(steps + 1):
            final_price = underlying_price * (u ** (steps - i)) * (d ** i)
            if option_type == "CALL":
                option_values[i] = max(final_price - strike_price, 0)
            elif option_type == "PUT":
                option_values[i] = max(strike_price - final_price, 0)

        # ✅ Rétropropagation dans l'arbre binomial
        for step in range(steps - 1, -1, -1):
            for i in range(step + 1):
                option_value = (p * option_values[i] + (1 - p) * option_values[i + 1]) * discount_factor

                # ✅ Prise en compte du style de l'option (américaine vs européenne)
                final_price = underlying_price * (u ** (step - i)) * (d ** i)
                if option_style == "American":
                    if option_type == "CALL":
                        option_value = max(option_value, final_price - strike_price)
                    elif option_type == "PUT":
                        option_value = max(option_value, strike_price - final_price)

                option_values[i] = option_value

        option_price = option_values[0]
        logger.info(f"✅ Binomial pricing with dividends completed. Result = {option_price}")

        return {"option_price_with_dividend": ("Option Price with Dividend Adjustment:", round(option_price, 4))}

    except Exception as e:
        logger.error(f"Error in binomial_dividend_pricing: {e}")
        return {"error": str(e)}, 400




def black_scholes_pricing(option_type, underlying_price, strike_price, time_to_maturity, 
                          risk_free_rate, volatility, dividend_yield, position_type):
    try:
        underlying_price = float(underlying_price)
        strike_price = float(strike_price)
        time_to_maturity = float(time_to_maturity)
        risk_free_rate = float(risk_free_rate)
        volatility = float(volatility)
        dividend_yield = float(dividend_yield if dividend_yield not in [None, ""] else 0.0)


        # Ajustement du prix sous-jacent pour le dividende
        adjusted_underlying_price = underlying_price * exp(-dividend_yield * time_to_maturity)

        # Calcul des termes d1 et d2
        d1 = (log(adjusted_underlying_price / strike_price) + (risk_free_rate + (volatility ** 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        if option_type == "CALL":
            price = adjusted_underlying_price * norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
        elif option_type == "PUT":
            # Utiliser la parité put-call : Put = Call - S * exp(-qT) + K * exp(-rT)
            call_price = adjusted_underlying_price * norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
            price = call_price - adjusted_underlying_price + strike_price * exp(-risk_free_rate * time_to_maturity)
        else:
            raise ValueError("Invalid option type. Must be 'CALL' or 'PUT'.")

        return {"option_price": ("Option Price :", round(price, 4))}

    except Exception as e:
        return {"error": str(e)}, 400




def implied_volatility(option_type, underlying_price, strike_price, option_price, 
                       time_to_maturity, risk_free_rate, dividend_yield):
    underlying_price = float(underlying_price)
    strike_price = float(strike_price)
    option_price = float(option_price)
    time_to_maturity = float(time_to_maturity)
    risk_free_rate = float(risk_free_rate)
    dividend_yield = float(dividend_yield if dividend_yield not in [None, ""] else 0.0)
    
    try:
        def bs_price(volatility):
            # Ajustement avec le rendement du dividende
            d1 = (log(underlying_price / strike_price) + 
                  (risk_free_rate - dividend_yield + (volatility ** 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
            d2 = d1 - volatility * sqrt(time_to_maturity)
            
            if option_type == "CALL":
                return (underlying_price * exp(-dividend_yield * time_to_maturity) * norm.cdf(d1) - 
                        strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2) - option_price)
            else:
                return (strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - 
                        underlying_price * exp(-dividend_yield * time_to_maturity) * norm.cdf(-d1) - option_price)

        # Trouver la volatilité implicite avec Newton-Raphson
        implied_vol = newton(bs_price, 0.2, tol=1e-6, maxiter=100)

        return {"implied_volatility": ("Implied Volatility :", round(implied_vol, 4))}

    except Exception as e:
        return {"error": str(e)}, 400




def monte_carlo_pricing(option_type, option_style, underlying_price, strike_price, 
                        time_to_maturity, risk_free_rate, volatility, dividend_yield, num_steps, num_simulations):
    try:
        # ✅ Conversion des paramètres
        num_simulations = int(num_simulations)
        num_steps = int(num_steps)
        time_to_maturity = float(time_to_maturity)
        dividend_yield = float(dividend_yield) if dividend_yield is not None and dividend_yield != '' else 0.0
        np.random.seed(42)

        dt = time_to_maturity / num_steps  # ✅ Pas de temps en fraction d'année
        payoffs = []
        antithetic_payoffs = []  # Pour améliorer la convergence

        for _ in range(num_simulations):
            path = [underlying_price]
            antithetic_path = [underlying_price]

            for _ in range(num_steps):
                # ✅ Bruit gaussien standard
                z = np.random.randn()

                # ✅ Processus stochastique avec dividendes
                next_price = path[-1] * np.exp(
                    (risk_free_rate - dividend_yield - 0.5 * volatility ** 2) * dt +
                    volatility * np.sqrt(dt) * z
                )
                
                # ✅ Antithetic sampling (réduction de variance)
                next_price_antithetic = antithetic_path[-1] * np.exp(
                    (risk_free_rate - dividend_yield - 0.5 * volatility ** 2) * dt +
                    volatility * np.sqrt(dt) * -z
                )

                path.append(next_price)
                antithetic_path.append(next_price_antithetic)

            # ✅ Payoff final selon le style d'option
            if option_style == "European":
                if option_type == "CALL":
                    payoff = max(0, path[-1] - strike_price)
                    antithetic_payoff = max(0, antithetic_path[-1] - strike_price)
                else:
                    payoff = max(0, strike_price - path[-1])
                    antithetic_payoff = max(0, strike_price - antithetic_path[-1])
            
            elif option_style == "Asian":
                average_price = np.mean(path)
                antithetic_average_price = np.mean(antithetic_path)
                if option_type == "CALL":
                    payoff = max(0, average_price - strike_price)
                    antithetic_payoff = max(0, antithetic_average_price - strike_price)
                else:
                    payoff = max(0, strike_price - average_price)
                    antithetic_payoff = max(0, strike_price - antithetic_average_price)

            else:
                raise ValueError("Invalid option style. Must be 'European' or 'Asian'.")

            payoffs.append(payoff)
            antithetic_payoffs.append(antithetic_payoff)

        # ✅ Moyenne des payoffs et antithetic sampling (réduction de variance)
        price = np.exp(-risk_free_rate * time_to_maturity) * (np.mean(payoffs) + np.mean(antithetic_payoffs)) / 2

        return {"option_price": ("Option Price :", round(price, 4))}

    except Exception as e:
        return {"error": str(e)}, 400







def compare_american_vs_european(option_type, underlying_price, strike_price, time_to_maturity, dividend_yield, 
                                  risk_free_rate, volatility):
    try:
        american_price = binomial_dividend_pricing(option_type, "AMERICAN", underlying_price, strike_price, 
                                                time_to_maturity, risk_free_rate, volatility, dividend_yield, 100)["option_price"][1]
        european_price = binomial_dividend_pricing(option_type, "EUROPEAN", underlying_price, strike_price, 
                                                time_to_maturity, risk_free_rate, volatility, dividend_yield, 100)["option_price"][1]
        
        spread = american_price - european_price
        
        return {
            "american_price": ("American Option Price :", round(american_price, 4)),
            "european_price": ("European Option Price :", round(european_price, 4)),
            "spread": ("American - European Spread :", round(spread, 4))
        }

    except Exception as e:
        return {"error": str(e)}, 400


def plot_greeks_sensitivity_formula(option_type, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, dividend_yield, position_type):
    if None in (option_type, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        raise ValueError("Missing one or more required inputs for Greeks")
    logger.warning('Start of plot_greeks_sensitivity_formula')

    underlying_price = float(underlying_price)
    strike_price = float(strike_price)
    time_to_maturity = float(time_to_maturity)
    risk_free_rate = float(risk_free_rate)
    volatility = float(volatility)
    dividend_yield = float(dividend_yield)

    # ✅ Plage de prix du sous-jacent pour la courbe
    multiplier = max(1.05, 1 + (volatility * sqrt(max(0.01, time_to_maturity))))
    lower_bound = max(0.5 * strike_price, strike_price * (1 - multiplier))
    upper_bound = max(lower_bound + 0.01, strike_price * (1 + multiplier))

    # ✅ Plage de prix dynamique propre et réaliste
    price_range = np.linspace(lower_bound, upper_bound, 100)
    
    delta = []
    gamma = []
    theta = []
    vega = []
    call_value = []  # ✅ Courbe de valeur du call

    # ✅ Générer la courbe complète des Greeks
    for S in price_range:
        d1 = (log(S / strike_price) + (risk_free_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        if option_type == "CALL":
            delta.append(exp(-dividend_yield * time_to_maturity) * norm.cdf(d1))
            call_price = exp(-dividend_yield * time_to_maturity) * S * norm.cdf(d1) - exp(-risk_free_rate * time_to_maturity) * strike_price * norm.cdf(d2)
        else:
            delta.append(-exp(-dividend_yield * time_to_maturity) * norm.cdf(-d1))
            call_price = exp(-risk_free_rate * time_to_maturity) * strike_price * norm.cdf(-d2) - exp(-dividend_yield * time_to_maturity) * S * norm.cdf(-d1)

        gamma.append(norm.pdf(d1) / (S * volatility * sqrt(time_to_maturity)))
        theta.append((-S * norm.pdf(d1) * volatility * exp(-dividend_yield * time_to_maturity) / (2 * sqrt(time_to_maturity))
                      - risk_free_rate * strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2 if option_type == "CALL" else -d2)
                      + dividend_yield * S * exp(-dividend_yield * time_to_maturity) * norm.cdf(d1 if option_type == "CALL" else -d1)) / 365)
        vega.append((S * exp(-dividend_yield * time_to_maturity) * norm.pdf(d1) * sqrt(time_to_maturity)) / 100)

        call_value.append(call_price)  # ✅ Stocker la valeur du call

    logger.warning('End of plot_greeks_sensitivity_formula')

    # ✅ Retourner le résultat sous forme de JSON (pour le frontend)
    # TOOL DE VISUALISATION VISUALIZATION
    # S'inspirer de ca pour la suite pour faire d'autres tools de visualisation :
    # is_live : True
    # soit 1 axe x, 1 axe y (2D simple)
    # soit 1 axe x, 2 axes y (2D avec 2 axes y)
    # soit 1 axe x, 1 axe y, 1 axe z (3D simple)
    # les différentes courbes avec leurs parametres et leurs values qui sont des listes
    return {
        "is_live": True,
        "x_axis": {
            "label": "Underlying Price",  
            "value": list(map(lambda x: round(x, 1), price_range.tolist()))
        },
        "primary_y_axis": {
            "label": "Greeks Sensitivity",
            "value": [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1]
        },
        "secondary_y_axis": {
            "label": "Option Value",
            "value": list(map(lambda x: round(x, 2), call_value))  # ✅ Ajout d'une échelle secondaire
        },
        "delta": {
            "label": "Delta",
            "data": delta if position_type == "LONG" else [-d for d in delta],
            "borderColor": "blue",
            "fill": False,
            "yAxisID": "primary"  # ✅ Assignation de l'axe Y
        },
        "gamma": {
            "label": "Gamma",
            "data": gamma,
            "borderColor": "red",
            "fill": False,
            "yAxisID": "primary"
        },
        "theta": {
            "label": "Theta",
            "data": theta if position_type == "LONG" else [-t for t in theta],
            "borderColor": "green",
            "fill": False,
            "yAxisID": "primary"
        },
        "vega": {
            "label": "Vega",
            "data": vega if position_type == "LONG" else [-v for v in vega],
            "borderColor": "purple",
            "fill": False,
            "yAxisID": "primary"
        },
        "call_value": {
            "label": "Option Value",
            "data": call_value if position_type == "LONG" else [-c for c in call_value],
            "borderColor": "orange",
            "fill": False,
            "yAxisID": "secondary"  # ✅ Courbe sur le 2ème axe Y
        }
    }
