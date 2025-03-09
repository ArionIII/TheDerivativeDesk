from flask import Blueprint, render_template

tool_category_options_routes = Blueprint("tool_category_options_routes", __name__)

OPTIONS_TOOL_CATEGORIES = {
    # Option Pricing Techniques
    "binomial-trees": {
        "title": "Binomial Trees",
        "description": "Price options using step-by-step binomial tree models.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Cox Ross Rubinstein Model",
                "description": "Adjust binomial trees to account for dividend payments.",
                "url": "/tools/options/option-pricing/binomial-dividend"
            }
        ]
    },

    "black-scholes": {
        "title": "Black-Scholes",
        "description": "Calculate option prices using the Black-Scholes formula.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Black-Scholes (Call & Put)",
                "description": "Compute the price of European options using the Black-Scholes model.",
                "url": "/tools/options/option-pricing/black-scholes-option"
            },
            {
                "title": "Implied Volatility",
                "description": "Estimate implied volatility from market prices using the Black-Scholes model.",
                "url": "/tools/options/option-pricing/black-scholes-implied-volatility"
            }
        ]
    },

    "monte-carlo": {
        "title": "Monte Carlo",
        "description": "Simulate option prices using Monte Carlo methods.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Monte Carlo (European & Asian Options)",
                "description": "Price European and Asian options using Monte Carlo simulation.",
                "url": "/tools/options/option-pricing/monte-carlo-option"
            },
            # {
            #     "title": "Monte Carlo (Path-Dependent Options)",
            #     "description": "Use Monte Carlo to price path-dependent options like lookbacks.",
            #     "url": "/tools/options/option-pricing/monte-carlo-path-dependent"
            # }
        ]
    },


    # Greeks
    "greeks": {
        "title": "Greeks",
        "description": "Measure the sensitivity of option prices to changes in market variables.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Delta",
                "description": "Measure the sensitivity of the option price to changes in the underlying asset price.",
                "url": "/tools/options/greeks/delta"
            },
            {
                "title": "Gamma",
                "description": "Measure the rate of change of Delta with respect to the underlying price.",
                "url": "/tools/options/greeks/gamma"
            },
            {
                "title": "Theta",
                "description": "Measure the sensitivity of the option price to the passage of time.",
                "url": "/tools/options/greeks/theta"
            },
            {
                "title": "Vega",
                "description": "Measure the sensitivity of the option price to changes in volatility.",
                "url": "/tools/options/greeks/vega"
            },
            {
                "title": "Rho",
                "description": "Measure the sensitivity of the option price to changes in the risk-free interest rate.",
                "url": "/tools/options/greeks/rho"
            }
        ]
    },

    # Trading Strategies
    "trading-strategies": {
        "title": "Trading Strategies",
        "description": "Implement different option trading strategies to manage risk and optimize returns.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Bull Spread",
                "description": "Set up a bullish strategy using call or put options.",
                "url": "/tools/options/trading-strategies/bull-spread"
            },
            {
                "title": "Bear Spread",
                "description": "Set up a bearish strategy using call or put options.",
                "url": "/tools/options/trading-strategies/bear-spread"
            },
            {
                "title": "Straddle",
                "description": "Set up a neutral strategy using a call and put with the same strike price.",
                "url": "/tools/options/trading-strategies/straddle"
            },
            {
                "title": "Strangle",
                "description": "Set up a neutral strategy using a call and put with different strike prices.",
                "url": "/tools/options/trading-strategies/strangle"
            }
        ]
    },

    # Exotic Options
    "exotic-options": {
        "title": "Exotic Options",
        "description": "Analyze and price exotic options such as barrier and lookback options.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Barrier Options",
                "description": "Price knock-in and knock-out options.",
                "url": "/tools/options/exotic-options/barrier"
            },
            {
                "title": "Lookback Options",
                "description": "Price options based on the maximum or minimum underlying price during the option's life.",
                "url": "/tools/options/exotic-options/lookback"
            },
            {
                "title": "Asian Options",
                "description": "Price options based on the average underlying price over a period.",
                "url": "/tools/options/exotic-options/asian"
            }
        ]
    },

    # Visualization and Analysis
    "graphs": {
        "title": "Graphs",
        "description": "Visualize option behavior and strategy performance.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Profit and Loss Diagrams",
                "description": "Visualize the profit/loss profile of an option strategy.",
                "url": "/tools/options/graphs/profit-loss"
            },
            {
                "title": "Greek Sensitivity Charts",
                "description": "Analyze how the Greeks change with the underlying asset price and time.",
                "url": "/tools/options/graphs/greek-sensitivity"
            }
        ]
    },

    # Scenario Analysis
    "scenario-analysis": {
        "title": "Scenario Analysis",
        "description": "Analyze how option strategies perform under different market scenarios.",
        "parent_category": "options",
        "tools": [
            {
                "title": "Stress Testing",
                "description": "Simulate how option portfolios react under extreme market conditions.",
                "url": "/tools/options/scenario-analysis/stress-testing"
            },
            {
                "title": "Interest Rate Changes",
                "description": "Evaluate how changes in interest rates impact option values.",
                "url": "/tools/options/scenario-analysis/interest-rate"
            },
            {
                "title": "Volatility Shocks",
                "description": "Analyze the impact of sudden changes in market volatility.",
                "url": "/tools/options/scenario-analysis/volatility-shock"
            }
        ]
    }
}

@tool_category_options_routes.route("/tools/options/<category_key>")
def render_tool_category(category_key):
    category = OPTIONS_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)
