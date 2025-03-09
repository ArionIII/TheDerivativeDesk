from config import generate_input_from_file
import os
INTEREST_RATE_DERIVATIVES_TOOL_CONFIG = {
    # Payoff of FRA
    "payoff-of-fra": {
    "title": "Payoff of FRA",
    "description": "Calculate the total payoff of a forward rate agreement over multiple periods based on agreed rates and market conditions.",
    "url": "/tools/forward-rate-agreements/payoff-of-fra",
    "inputs": [
        {
            "label": "Contract Rate", 
            "id": "contract_rate", 
            "type": "number", 
            "placeholder": "0.02", 
            "optional": False
        },
        {
            "label": "Settlement Rates (comma-separated)", 
            "id": "settlement_rates", 
            "type": "array", 
            "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'settlement_rates.csv'))}",
            "optional": False
        },
        {
            "label": "Settlement Rates (CSV)", 
            "id": "file_settlement_rates", 
            "type": "file", 
            "accept": ".csv", 
            "data_target": "settlement_rates", 
            "template": "/static/templates/settlement_rates.csv", 
            "optional": True
        },
        {
            "label": "Notional Value", 
            "id": "notional_value", 
            "type": "number", 
            "placeholder": "1000000", 
            "optional": False
        },
        {
            "label": "Interval Between Payments (Years)", 
            "id": "interval_between_payments", 
            "type": "number", 
            "placeholder": "0.5", 
            "optional": False
        }
    ],
    "note": "The payoff is the net difference between Floating Leg & Fixed Leg. It is the payoff for the buyer of the FRA (aka the fix-leg payer / floating-leg receiver)",
    "outputs": ["Total FRA Payoff"],
    "graphs":[
        {
            "name" : "Payoff Evolution"
        },
        {
            "name" : "Fixed Leg vs Floating Leg"
        }
    ]
},  
    # Valuation of FRA
    "valuation-of-fra": {
        "title": "Valuation of FRA",
        "description": "Evaluate the value of a forward rate agreement using discount factors and market forward rates.",
        "url": "/tools/forward-rate-agreements/valuation-of-fra",
        "inputs": [
        {
            "label": "Contract Rate", 
            "id": "contract_rate", 
            "type": "number", 
            "placeholder": "0.02", 
            "optional": False
        },
        {
            "label": "Forward Rates (comma-separated)", 
            "id": "forward_rates", 
            "type": "array", 
            "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'settlement_rates.csv'))}",
            "optional": False
        },
        {
            "label": "Forward Rates (CSV)", 
            "id": "file_forward_rates", 
            "type": "file", 
            "accept": ".csv", 
            "data_target": "forward_rates", 
            "template": "/static/templates/settlement_rates.csv", 
            "optional": True
        },
        {
            "label": "Notional Value", 
            "id": "notional_value", 
            "type": "number", 
            "placeholder": "1000000", 
            "optional": False
        },
        {
            "label": "Interval Between Payments (Years)", 
            "id": "interval_between_payments", 
            "type": "number", 
            "placeholder": "0.5", 
            "optional": False
        }
    ],
        "note": "You can calculate the forward rate curve with the 'Forward Rate Calculation' tool",
        "outputs": ["FRA Valuation"],
        "graphs": [
            {
                "name": "FRA Payoff"
            },
            {
                "name": "FRA fixed vs floating"
            }
        ]
    },
    # Forward Rate Calculation
    "forward-rate-calculation": {
    "title": "Forward Rate Calculation",
    "description": "Calculate the forward curve from spot rates (zero rates).",
    "url": "/tools/forward-rate-agreements/forward-rate-calculation",
    "inputs": [
        {
            "label": "Spot Rates (comma-separated)", 
            "id": "spot_rates", 
            "type": "array", 
            "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'spot_rates_forward_rates.csv'))}",
            "optional": False
        },
        {
            "label": "Maturities (Years)", 
            "id": "maturities", 
            "type": "array", 
            "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'maturities_forward_rates.csv'))}",
            "optional": False
        },
        {
            "label": "Upload Spot Rate Data (CSV)", 
            "id": "file_spot_rates", 
            "type": "file", 
            "accept": ".csv", 
            "data_target": "spot_rates",
            "template": "/static/templates/spot_rates_forward_rates.csv", 
            "optional": True
        },
        {
            "label": "Upload Maturity Data (CSV)", 
            "id": "file_maturities", 
            "type": "file", 
            "accept": ".csv", 
            "data_target": "maturities",
            "template": "/static/templates/maturities_forward_rates.csv", 
            "optional": True
        }
    ],
    "graphs":[
        {
            "name": "Forward Rates Curve"
        },
        {
            "name": "Forward Rates vs Spot Rates"
        }
    ],
    "outputs": ["Forward Rate Curve CSV & XLSX files"],
},

    # FRA Break-Even Rate
    "fra-break-even-rate": {
        "title": "FRA Break-Even Rate",
        "description": "Determine the break-even interest rate for an FRA.",
        "url": "/tools/forward-rate-agreements/fra-break-even-rate",
        "inputs": [
        {
            "label": "Forward Rates (comma-separated)", 
            "id": "forward_rates", 
            "type": "array", 
            "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'settlement_rates.csv'))}",
            "optional": False
        },
        {
            "label": "Forward Rates (CSV)", 
            "id": "file_forward_rates", 
            "type": "file", 
            "accept": ".csv", 
            "data_target": "forward_rates", 
            "template": "/static/templates/settlement_rates.csv", 
            "optional": True
        },
        {
            "label": "Interval Between Payments (Years)", 
            "id": "interval_between_payments", 
            "type": "number", 
            "placeholder": "0.5", 
            "optional": False
        }
    ],
        # "graphs": [
        #     {"name" : "Break Even rate vs Forward rates"},
        #     {"name" : "Break Even rate vs Maturity"}
        # ],
        "note": "You can calculate the forward rate curve with the 'Forward Rate Calculation' tool",
        "outputs": ["Break-Even Rate"],
    },
    # Hedging with FRA
    "hedging-with-fra": {
    "title": "Hedging with FRA",
    "description": "Analyze hedging strategies using forward rate agreements to manage interest rate risks.",
    "url": "/tools/forward-rate-agreements/hedging-with-fra",
    "inputs": [
        {
            "label": "Current Position (Notional)", 
            "id": "current_position", 
            "type": "number", 
            "placeholder": "1000000", 
            "optional": False
        },
        {
            "label": "Target Rate", 
            "id": "target_rate", 
            "type": "number", 
            "placeholder": "0.025", 
            "optional": False
        },
        {
            "label": "Market Rate", 
            "id": "market_rate", 
            "type": "number", 
            "placeholder": "0.03", 
            "optional": False
        },
        {
            "label": "FRA Period (Years)", 
            "id": "fra_period", 
            "type": "number", 
            "placeholder": "0.5", 
            "optional": False
        },
        {
            "label": "Position Type (Payer/Receiver)", 
            "id": "position_type", 
            "type": "select", 
            "placeholder": "Select Payer or Receiver", 
            "options": ["Payer", "Receiver"], 
            "default": "Payer",
            "optional": False
        }
    ],
    "outputs": ["Hedging Strategy Analysis"],
},
    # Interest Rate Swap Cash Flows
    "interest-rate-swap-cash-flows": {
        "title": "Interest Rate Swap Cash Flows",
        "description": "Calculate the cash flows of fixed-for-floating interest rate swaps.",
        "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-cash-flows",
        "inputs": [
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
            {"label": "Fixed Rate", "id": "fixed_rate", "type": "number", "placeholder": "0.03", "optional": False},
            {"label": "Floating Rate", "id": "floating_rate", "type": "number", "placeholder": "0.025", "optional": False},
            {"label": "Periods (comma-separated)", "id": "periods", "type": "array", "placeholder": "[1, 2, 3]", "optional": False},
        ],
        "outputs": ["Cash Flows"],
    },
    # Interest Rate Swap Valuation
    "interest-rate-swap-valuation": {
        "title": "Interest Rate Swap Valuation",
        "description": "Compute the present value of interest rate swaps using market curves.",
        "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-valuation",
        "inputs": [
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
            {"label": "Fixed Rate", "id": "fixed_rate", "type": "number", "placeholder": "0.03", "optional": False},
            {"label": "Discount Factors (comma-separated)", "id": "discount_factors", "type": "array", "placeholder": "[0.95, 0.94, 0.93]", "optional": False},
            {"label": "Floating Cash Flows (comma-separated)", "id": "floating_cash_flows", "type": "array", "placeholder": "[30000, 30000, 30000]", "optional": False},
        ],
        "outputs": ["Swap Valuation"],
    },
    # Pricing Interest Rate Futures
    "pricing-interest-rate-futures": {
        "title": "Pricing Interest Rate Futures",
        "description": "Price interest rate futures such as Eurodollar futures based on market interest rates.",
        "url": "/tools/swaps-and-interest-rate-derivatives/pricing-interest-rate-futures",
        "inputs": [
            {"label": "Current Market Rate (%)", "id": "market_rate", "type": "number", "placeholder": "4", "optional": False},
            {"label": "Days to Maturity", "id": "days_to_maturity", "type": "number", "placeholder": "90", "optional": False},
        ],
        "outputs": ["Future Price"],
    },
    # Swap Spread Analysis
    "swap-spread-analysis": {
        "title": "Swap Spread Analysis",
        "description": "Analyze the spread between swap rates and government yields.",
        "url": "/tools/swaps-and-interest-rate-derivatives/swap-spread-analysis",
        "inputs": [
            {"label": "Swap Rate", "id": "swap_rate", "type": "number", "placeholder": "0.025", "optional": False},
            {"label": "Government Yield", "id": "government_yield", "type": "number", "placeholder": "0.02", "optional": False},
        ],
        "outputs": ["Swap Spread"],
    },
    # Swaption Valuation
    "swaption-valuation": {
        "title": "Swaption Valuation",
        "description": "Value options on interest rate swaps using Black’s model.",
        "url": "/tools/swaps-and-interest-rate-derivatives/swaption-valuation",
        "inputs": [
            {"label": "Strike Rate", "id": "strike_rate", "type": "number", "placeholder": "0.03", "optional": False},
            {"label": "Volatility (%)", "id": "volatility", "type": "number", "placeholder": "20", "optional": False},
            {"label": "Time to Maturity (Years)", "id": "time_to_maturity", "type": "number", "placeholder": "1", "optional": False},
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
        ],
        "outputs": ["Swaption Value"],
    },
    # Basis Swap Analysis
    "basis-swap-analysis": {
        "title": "Basis Swap Analysis",
        "description": "Evaluate basis swaps where both legs are floating rates with different benchmarks.",
        "url": "/tools/swaps-and-interest-rate-derivatives/basis-swap-analysis",
        "inputs": [
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
            {"label": "Benchmark 1 Rate", "id": "benchmark__rate_1", "type": "number", "placeholder": "0.02", "optional": False},
            {"label": "Benchmark 2 Rate", "id": "benchmark_rate_2", "type": "number", "placeholder": "0.025", "optional": False},
            {"label": "Periods (comma-separated)", "id": "periods", "type": "array", "placeholder": "[1, 2, 3]", "optional": False},
        ],
        "outputs": ["Basis Swap Analysis"],
    },
    # Interest Rate Swap Delta Hedging
    "interest-rate-swap-delta-hedging": {
        "title": "Interest Rate Swap Delta Hedging",
        "description": "Analyze hedging strategies for interest rate swaps.",
        "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-delta-hedging",
        "inputs": [
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
            {"label": "Fixed Rate", "id": "fixed_rate", "type": "number", "placeholder": "0.03", "optional": False},
            {"label": "Floating Rate", "id": "floating_rate", "type": "number", "placeholder": "0.025", "optional": False},
            {"label": "Hedge Ratio", "id": "hedge_ratio", "type": "number", "placeholder": "0.8", "optional": False},
        ],
        "outputs": ["Delta Hedging Strategy"],
    },
}
