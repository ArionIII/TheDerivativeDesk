from config import generate_input_from_file
import os

INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG = {
    "continuous-compounding-rate": {
        "title": "m-Compounding to Continuous Compounding Rate",
        "description": "Convert m-compounding rate to continuous compounding rate.",
        "url": "/tools/basic-interest-rates-analysis/continuous-compounding-rate",
        "inputs": [
            {
                "label": "Rate ",
                "id": "rate",
                "type": "number",
                "placeholder": "0.05",
                "optional": False,
            },
            {
                "label": "Compounding Frequency ",
                "id": "frequency",
                "type": "number",
                "placeholder": "4",
                "optional": False,
            },
        ],
        "outputs": ["Rate (Continuous Compounding)"],
    },
    "m-to-continuous-compounding-rate": {
        "title": "Continuous to m-Compounding Rate",
        "description": "Convert continuous compounding rate to m-compounding rate.",
        "url": "/tools/basic-interest-rates-analysis/m-to-continuous-compounding-rate",
        "inputs": [
            {
                "label": "Rate ",
                "id": "rate",
                "type": "number",
                "placeholder": "0.05",
                "optional": False,
            },
            {
                "label": "Compounding Frequency",
                "id": "frequency",
                "type": "number",
                "placeholder": "4",
                "optional": False,
            },
        ],
        "outputs": ["Rate (m-Compounding)"],
    },
    # "zero-rate-curve": {
    # "title": "Zero Rate Curve Construction",
    # "description": "Construct zero rate curves using market instruments.",
    # "url": "/tools/basic-interest-rates-analysis/zero-rate-curve",
    # "inputs": [
    #     {
    #         "label": "Input Rates (comma-separated)",
    #         "id": "input_rates",
    #         "type": "array",
    #         "placeholder": "[0.02, 0.025, 0.03]",
    #         "optional": False
    #     },
    #     {
    #         "label": "Rate Type (FRA, Swap)",
    #         "id": "rate_type",
    #         "type": "select",
    #         "placeholder": "Select Rate Type (FRA or Swap)",
    #         "options": ["FRA", "Swap"],
    #         "default": "FRA",
    #         "optional": False
    #     },
    #     {
    #         "label": "Maturities (comma-separated)",
    #         "id": "maturities",
    #         "type": "array",
    #         "placeholder": "[0.5, 1, 1.5]",
    #         "optional": False
    #     },
    #     {
    #         "label": "Space Between Payments (Years)",
    #         "id": "space_between_payments",
    #         "type": "number",
    #         "placeholder": "0.5 (Semi-annual)",
    #         "optional": True
    #     }
    # ],
    # "outputs": ["Zero Rate Curve"]
    # },
    "bond-pricing": {
        "title": "Bond Pricing",
        "description": "Calculate the price of a bond given its characteristics.",
        "url": "/tools/basic-interest-rates-analysis/bond-pricing",
        "inputs": [
            {
                "label": "Face Value",
                "id": "face_value",
                "type": "number",
                "placeholder": "1000",
                "optional": False,
            },
            {
                "label": "Coupon Rate (%)",
                "id": "coupon_rate",
                "type": "number",
                "placeholder": "5",
                "optional": False,
            },
            {
                "label": "Maturity (Years)",
                "id": "maturity",
                "type": "number",
                "placeholder": "10",
                "optional": False,
            },
            {
                "label": "Market Rate (%)",
                "id": "market_rate",
                "type": "number",
                "placeholder": "4",
                "optional": False,
            },
        ],
        "outputs": ["Bond Price"],
    },
    "determining-zero-rates": {
        "title": "Determining Zero Rates & Zero-Curve",
        "description": "Calculate zero rates from coupon bond prices and coupon rates.",
        "url": "/tools/basic-interest-rates-analysis/determining-zero-rates",
        "inputs": [
            {
                "label": "Bond Prices (comma-separated)",
                "id": "bond_prices",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'bond_prices_cloche.csv'))}",
            },
            {
                "label": "Bond Prices (CSV)",
                "id": "file_bond_prices",
                "type": "file",
                "accept": ".csv",
                "data_target": "bond_prices",
                "template": "/static/templates/bond_prices_cloche.csv",
                "optional": True,
            },
            {
                "label": "Face Values (comma-separated)",
                "id": "face_values",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'face_values_cloche.csv'))}",
            },
            {
                "label": "Face Values (CSV)",
                "id": "file_face_values",
                "type": "file",
                "accept": ".csv",
                "data_target": "face_values",
                "template": "/static/templates/face_values_cloche.csv",
                "optional": True,
            },
            {
                "label": "Maturities (Years)",
                "id": "maturities",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'maturities_cloche.csv'))}",
            },
            {
                "label": "Maturities (CSV)",
                "id": "file_maturities",
                "type": "file",
                "accept": ".csv",
                "data_target": "maturities",
                "template": "/static/templates/maturities_cloche.csv",
                "optional": True,
            },
            {
                "label": "Coupon Rates (comma-separated, in decimal form)",
                "id": "coupon_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'coupon_rates_cloche.csv'))}",
            },
            {
                "label": "Coupon Rates (CSV)",
                "id": "file_coupon_rates",
                "type": "file",
                "accept": ".csv",
                "data_target": "coupon_rates",
                "template": "/static/templates/coupon_rates_cloche.csv",
                "optional": True,
            },
            {
                "label": "Compounding Frequency per Year (comma-separated)",
                "id": "m_compoundings",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'm_compoundings_cloche.csv'))}",
            },
            {
                "label": "Compounding Frequencies (CSV)",
                "id": "file_m_compoundings",
                "type": "file",
                "accept": ".csv",
                "data_target": "m_compoundings",
                "template": "/static/templates/m_compoundings_cloche.csv",
                "optional": True,
            },
        ],
        "graphs": [
            {
                "name": "Zero Rates Curve",
            },
            {
                "name": "Zero Rates vs Bond Prices",
            },
        ],
        "outputs": ["CSV File with Zero Rates"],
        "note": """
To ensure accurate computations, the input data must satisfy the following conditions:

1. **All input lists must be complete and well-formatted**  
    Each list must have the **same length**.  

2. **The first bond should ideally be a zero-coupon bond**  
   Bootstrapping works best when the shortest-maturity bond is zero-coupon, ensuring a reliable starting point.  

3. **Maturities should align with coupon payment schedules**  
   Each maturity \( T \) should be a **multiple of \( 1/m \)** (where \( m \) is the compounding frequency).  
   Example: If coupons are paid **semi-annually** (\( m=2 \)), maturities must be at intervals like 0.5, 1.0, 1.5, 2.0, etc.

If these conditions are not met, the zero rates calculation may fail or produce inaccurate results.
""",
    },
    "extending-libor-curve-with-swap-rates": {
        "title": "Extend Zero-Rate Curve with Swap Rates",
        "description": "Use swap rates to extend the Zero-Rate curve.",
        "url": "/tools/term-structure-construction/extending-libor-curve-with-swap-rates",
        "inputs": [
            {
                "label": "Initial Zero-Rates (comma-separated)",
                "id": "libor_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'libor_rates.csv'))}",
                "optional": False,
            },
            {
                "label": "Initial Zero Rates (CSV)",
                "id": "file_libor_rates",
                "type": "file",
                "accept": ".csv",
                "data_target": "libor_rates",
                "template": "/static/templates/libor_rates.csv",
                "optional": True,
            },
            {
                "label": "Swap Rates (comma-separated)",
                "id": "swap_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'swap_rates.csv'))}",
                "optional": False,
            },
            {
                "label": "Swap Rates (CSV)",
                "id": "file_swap_rates",
                "type": "file",
                "accept": ".csv",
                "data_target": "swap_rates",
                "template": "/static/templates/swap_rates.csv",
                "optional": True,
            },
            {
                "label": "Zero-Rate Tenors (Years)",
                "id": "libor_tenors",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'libor_tenors.csv'))}",
                "optional": False,
            },
            {
                "label": "Zero-Rate Tenors (CSV)",
                "id": "file_libor_tenors",
                "type": "file",
                "accept": ".csv",
                "data_target": "libor_tenors",
                "template": "/static/templates/libor_tenors.csv",
                "optional": True,
            },
            {
                "label": "Swap Tenors (Years)",
                "id": "swap_tenors",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'swap_tenors.csv'))}",
                "optional": False,
            },
            {
                "label": "Swap Tenors (CSV)",
                "id": "file_swap_tenors",
                "type": "file",
                "accept": ".csv",
                "data_target": "swap_tenors",
                "template": "/static/templates/swap_tenors.csv",
                "optional": True,
            },
        ],
        "outputs": ["Extended Zero Curve"],
        "note": "We assume here for simplicity purpose : ACT/360 Day Count Convention, Annual Fixed Leg Frequency, and Semi-Annual Floating Leg Frequency. Also, we use CubicSpline Interpolation (solving of third-degrees polynomes), which allows bent curves instead of straight lines.",
        "graphs": [
            {
                "name": "Extended Zero Curve",
            },
        ],
    },
    "extending-zero-curve-with-fra": {
        "title": "Extend Zero-Rate Curve with FRA",
        "description": "Use FRA rates to extend the Zero-Rate curve.",
        "url": "/tools/term-structure-construction/extending-zero-curve-with-fra",
        "inputs": [
            {
                "label": "Initial Zero Rates (comma-separated)",
                "id": "libor_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'libor_rates_fra.csv'))}",
                "optional": False,
            },
            {
                "label": "Initial Zero Rates (CSV)",
                "id": "file_libor_rates",
                "type": "file",
                "accept": ".csv",
                "data_target": "libor_rates",
                "template": "/static/templates/libor_rates_fra.csv",
                "optional": True,
            },
            {
                "label": "FRA Rates (comma-separated)",
                "id": "fra_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'fra_rates.csv'))}",
                "optional": False,
            },
            {
                "label": "FRA Rates (CSV)",
                "id": "file_fra_rates",
                "type": "file",
                "accept": ".csv",
                "data_target": "fra_rates",
                "template": "/static/templates/fra_rates.csv",
                "optional": True,
            },
            {
                "label": "Zero-Rate Maturities (Years)",
                "id": "libor_tenors",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'libor_tenors_fra.csv'))}",
                "optional": False,
            },
            {
                "label": "Zero-Rate Maturities (CSV)",
                "id": "file_libor_tenors",
                "type": "file",
                "accept": ".csv",
                "data_target": "libor_tenors",
                "template": "/static/templates/libor_tenors_fra.csv",
                "optional": True,
            },
            {
                "label": "FRA Maturities (Years)",
                "id": "fra_tenors",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'fra_tenors.csv'))}",
                "optional": False,
            },
            {
                "label": "FRA Maturities (CSV)",
                "id": "file_fra_tenors",
                "type": "file",
                "accept": ".csv",
                "data_target": "fra_tenors",
                "template": "/static/templates/fra_tenors.csv",
                "optional": True,
            },
        ],
        "graphs": [
            {
                "name": "Extended Zero Curve",
            }
        ],
        "note": "We assume here for simplicity purpose : ACT/360 Day Count Convention, Annual Fixed Leg Frequency, and Semi-Annual Floating Leg Frequency. Also, we use CubicSpline Interpolation (solving of third-degrees polynomes), which allows bent curves instead of straight lines.",
        "outputs": ["Extended Zero Curve"],
    },
    # "payoff-of-fra": {
    #     "title": "Payoff of FRA",
    #     "description": "Calculate the payoff of a Forward Rate Agreement (FRA).",
    #     "url": "/tools/interest-rates/payoff-of-fra",
    #     "inputs": [
    #         {"label": "Contract Rate", "id": "contract_rate", "type": "number", "placeholder": "0.02", "optional": False},
    #         {"label": "Settlement Rate", "id": "settlement_rate", "type": "number", "placeholder": "0.025", "optional": False},
    #         {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "1000000", "optional": False},
    #         {"label": "Time (Years)", "id": "time", "type": "number", "placeholder": "0.5", "optional": False},
    #     ],
    #     "outputs": ["FRA Payoff"],
    # },
    "duration-and-convexity": {
        "title": "Duration and Convexity",
        "description": "Calculate the duration and convexity of a bond.",
        "url": "/tools/basic-interest-rates-analysis/duration-and-convexity",
        "inputs": [
            {
                "label": "Bond Cash Flows (comma-separated)",
                "id": "cash_flows",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'duration_cash_flows.csv'))}",
                "optional": False,
            },
            {
                "label": "Discount Rates (comma-separated)",
                "id": "discount_rates",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'duration_discount_rates.csv'))}",
                "optional": False,
            },
            {
                "label": "Time Periods (Years)",
                "id": "time_periods",
                "type": "array",
                "placeholder": f"{generate_input_from_file(os.path.join(os.getcwd(), 'static', 'templates', 'duration_time_periods.csv'))}",
                "optional": False,
            },
            {
                "label": "CSV for Cash Flows",
                "id": "cash_flows_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "cash_flows",
                "template": "/static/templates/duration_cash_flows.csv",
            },
            {
                "label": "CSV for Discount Rates",
                "id": "discount_rates_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "discount_rates",
                "template": "/static/templates/duration_discount_rates.csv",
            },
            {
                "label": "CSV for Time Periods",
                "id": "time_periods_file",
                "type": "file",
                "accept": ".csv",
                "data_target": "time_periods",
                "template": "/static/templates/duration_time_periods.csv",
            },
        ],
        "graphs": [
            {"name": "Duration Contribution (%)"},
            {"name": "Cash Flow Discounting"},
        ],
        "outputs": ["Duration", "Convexity"],
    },
}
