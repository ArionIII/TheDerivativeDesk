import numpy as np
from scipy.optimize import newton
from math import log, sqrt, exp
from scipy.stats import norm
from math import exp
from config import logger


def binomial_dividend_pricing(option_type, option_style, underlying_price, strike_price, time_to_maturity, risk_free_rate, volatility, dividend_yield, steps):
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
    - dividend_yield: Continuous dividend yield
    - steps: Number of steps in the binomial tree

    Returns:
    - Option Price
    """
    try:
        steps=int(steps)
        logger.info("Starting binomial pricing with dividends...")

        dt = time_to_maturity / steps
        discount_factor = exp(-risk_free_rate * dt)

        # Ajustement du prix sous-jacent en fonction des dividendes
        adjusted_underlying_price = underlying_price * exp(-dividend_yield * time_to_maturity)

        # Facteurs de montée (u) et de descente (d) dans le modèle binomial
        u = exp(volatility * np.sqrt(dt))
        d = 1 / u
        p = (exp((risk_free_rate - dividend_yield) * dt) - d) / (u - d)

        # Initialisation du tableau des prix finaux à la maturité
        option_values = np.zeros(steps + 1)
        for i in range(steps + 1):
            final_price = adjusted_underlying_price * (u ** (steps - i)) * (d ** i)
            if option_type == "CALL":
                option_values[i] = max(final_price - strike_price, 0)
            elif option_type == "PUT":
                option_values[i] = max(strike_price - final_price, 0)

        # Rétropropagation dans l'arbre binomial
        for step in range(steps - 1, -1, -1):
            for i in range(step + 1):
                option_value = (p * option_values[i] + (1 - p) * option_values[i + 1]) * discount_factor

                if option_style == "American":
                    final_price = adjusted_underlying_price * (u ** (step - i)) * (d ** i)
                    if option_type == "CALL":
                        option_value = max(option_value, final_price - strike_price)
                    elif option_type == "PUT":
                        option_value = max(option_value, strike_price - final_price)

                option_values[i] = option_value

        option_price = option_values[0]
        logger.info(f"Binomial pricing with dividends completed. Result = {option_price}")
        return {"option_price_with_dividend": ("Option Price with Dividend Adjustment:", round(option_price, 4))}

    except Exception as e:
        logger.error(f"Error in binomial_dividend_pricing: {e}")
        return {"error": str(e)}, 400


def black_scholes_pricing(option_type, underlying_price, strike_price, time_to_maturity, 
                          risk_free_rate, volatility):
    try:
        d1 = (log(underlying_price / strike_price) + (risk_free_rate + (volatility ** 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
        d2 = d1 - volatility * sqrt(time_to_maturity)

        if option_type == "CALL":
            price = underlying_price * norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
        else:
            price = strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - underlying_price * norm.cdf(-d1)

        return {"option_price": ("Option Price :", round(price, 4))}

    except Exception as e:
        return {"error": str(e)}, 400



def implied_volatility(option_type, underlying_price, strike_price, option_price, 
                       time_to_maturity, risk_free_rate):
    try:
        def bs_price(volatility):
            d1 = (log(underlying_price / strike_price) + (risk_free_rate + (volatility ** 2) / 2) * time_to_maturity) / (volatility * sqrt(time_to_maturity))
            d2 = d1 - volatility * sqrt(time_to_maturity)
            if option_type == "CALL":
                return underlying_price * norm.cdf(d1) - strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2) - option_price
            else:
                return strike_price * exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - underlying_price * norm.cdf(-d1) - option_price

        implied_vol = newton(bs_price, 0.2, tol=1e-6, maxiter=100)
        return {"implied_volatility": ("Implied Volatility :", round(implied_vol, 4))}

    except Exception as e:
        return {"error": str(e)}, 400



def monte_carlo_pricing(option_type, option_style, underlying_price, strike_price, 
                        risk_free_rate, volatility, num_simulations):
    try:
        np.random.seed(42)
        dt = 1 / 365
        payoffs = []
        for _ in range(num_simulations):
            path = [underlying_price]
            for _ in range(int(1 / dt)):
                path.append(path[-1] * np.exp((risk_free_rate - 0.5 * volatility ** 2) * dt +
                                              volatility * np.sqrt(dt) * np.random.randn()))
            if option_type == "CALL":
                payoff = max(0, path[-1] - strike_price)
            else:
                payoff = max(0, strike_price - path[-1])

            if option_style == "AMERICAN":
                payoff = max(payoff, path[-1] - strike_price if option_type == "CALL" else strike_price - path[-1])

            payoffs.append(payoff)

        price = np.exp(-risk_free_rate) * np.mean(payoffs)
        return {"option_price": ("Option Price :", round(price, 4))}

    except Exception as e:
        return {"error": str(e)}, 400



def compare_american_vs_european(option_type, underlying_price, strike_price, time_to_maturity, 
                                  risk_free_rate, volatility):
    try:
        american_price = binomial_trees_pricing(option_type, "AMERICAN", underlying_price, strike_price, 
                                                time_to_maturity, risk_free_rate, volatility, 100)["option_price"][1]
        european_price = binomial_trees_pricing(option_type, "EUROPEAN", underlying_price, strike_price, 
                                                time_to_maturity, risk_free_rate, volatility, 100)["option_price"][1]
        
        spread = american_price - european_price
        
        return {
            "american_price": ("American Option Price :", round(american_price, 4)),
            "european_price": ("European Option Price :", round(european_price, 4)),
            "spread": ("American - European Spread :", round(spread, 4))
        }

    except Exception as e:
        return {"error": str(e)}, 400
