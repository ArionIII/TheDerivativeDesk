import numpy as np
### Chapitre 4 - Interest Rates

def convert_nominal_to_continuous(m, R_m):
    """
    Convert nominal return to continuous return.

    Formula:
        R_c = m * ln(1 + R_m / m)

    Args:
        m (float): Frequency of compounding (e.g., 12 for monthly, 1 for annual).
        R_m (float): Nominal return.

    Returns:
        float: Continuous return (R_c).

    Raises:
        ValueError: If m is non-positive or if inputs are not numeric.
    """
    if not isinstance(m, (int, float)) or not isinstance(R_m, (int, float)):
        raise ValueError("Both inputs must be numeric (int or float).")
    if m <= 0:
        raise ValueError("Frequency of compounding (m) must be positive.")

    return m * np.log(1 + R_m / m)

def convert_continuous_to_nominal(m, R_c):
    """
    Convert continuous return to nominal return.

    Formula:
        R_m = m * (e^(R_c / m) - 1)

    Args:
        m (float): Frequency of compounding (e.g., 12 for monthly, 1 for annual).
        R_c (float): Continuous return.

    Returns:
        float: Nominal return (R_m).

    Raises:
        ValueError: If m is non-positive or if inputs are not numeric.
    """
    if not isinstance(m, (int, float)) or not isinstance(R_c, (int, float)):
        raise ValueError("Both inputs must be numeric (int or float).")
    if m <= 0:
        raise ValueError("Frequency of compounding (m) must be positive.")

    return m * (np.exp(R_c / m) - 1)

def compute_zero_coupon_price_continuous(R, t):
    """
    Compute the price of a zero-coupon bond using continuous compounding.

    Formula:
        P = 100 * e^(-R * t)

    Args:
        R (float): Zero-coupon rate (continuous compounding).
        t (float): Time to maturity in years.

    Returns:
        float: Price of the zero-coupon bond (P).

    Raises:
        ValueError: If inputs are invalid (negative or non-numeric).
    """
    if not isinstance(R, (int, float)) or not isinstance(t, (int, float)):
        raise ValueError("Both inputs must be numeric (int or float).")
    if t < 0:
        raise ValueError("Time to maturity (t) must be non-negative.")

    return 100 * np.exp(-R * t)

def compute_zero_coupon_bond_price_discrete(F, r, m, n):
    """
    Compute the price of a zero-coupon bond using discrete compounding.

    Formula:
        P = F / (1 + r/m)^(m * n)

    Args:
        F (float): Face value of the bond.
        r (float): Annual nominal interest rate.
        m (int): Compounding frequency per year.
        n (int): Total number of years to maturity.

    Returns:
        float: Price of the zero-coupon bond.

    Raises:
        ValueError: If inputs are invalid (negative or non-numeric values).
    """
    if not all(isinstance(val, (int, float)) for val in [F, r]):
        raise ValueError("Face value and interest rate must be numeric (int or float).")
    if not all(isinstance(val, int) for val in [m, n]) or m <= 0 or n <= 0:
        raise ValueError("Compounding frequency and number of years must be positive integers.")
    if F <= 0 or r < 0:
        raise ValueError("Face value must be positive, and interest rate must be non-negative.")

    return F / (1 + r / m) ** (m * n)

def compute_zero_coupon_rate(P, t):
    """
    Compute the zero-coupon rate given the price and time to maturity.

    Formula:
        R = -(1/t) * ln(P / 100)

    Args:
        P (float): Price of the zero-coupon bond.
        t (float): Time to maturity in years.

    Returns:
        float: Zero-coupon rate (R) with continuous compounding.

    Raises:
        ValueError: If inputs are invalid (non-positive price, negative or zero time).
    """
    if not isinstance(P, (int, float)) or not isinstance(t, (int, float)):
        raise ValueError("Both inputs must be numeric (int or float).")
    if P <= 0:
        raise ValueError("Price (P) must be positive.")
    if t <= 0:
        raise ValueError("Time to maturity (t) must be positive.")

    return -(1 / t) * np.log(P / 100)

def compute_bond_price_continuous(C, r, n, F):
    """
    Compute the price of a bond with coupons using continuous compounding.

    Formula:
        P = sum(C * e^(-r * t)) + F * e^(-r * n)

    Args:
        C (float): Coupon payment per period.
        r (float): Continuous compounding interest rate.
        n (int): Total number of periods.
        F (float): Face value of the bond.

    Returns:
        float: Price of the bond.

    Raises:
        ValueError: If inputs are invalid (negative or non-numeric values).
    """
    if not all(isinstance(val, (int, float)) for val in [C, r, F]):
        raise ValueError("Coupon, interest rate, and face value must be numeric.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Number of periods (n) must be a positive integer.")
    if C < 0 or r < 0 or F < 0:
        raise ValueError("Coupon, interest rate, and face value must be non-negative.")

    coupon_sum = sum(C * np.exp(-r * t) for t in range(1, n + 1))
    face_value_discounted = F * np.exp(-r * n)
    return coupon_sum + face_value_discounted

def compute_bond_price_discrete(C, r, m, n, F):
    """
    Compute the price of a bond with coupons using discrete compounding.

    Formula:
        P = sum(C / (1 + r/m)^(mt)) + F / (1 + r/m)^(mn)

    Args:
        C (float): Coupon payment per period.
        r (float): Annual nominal interest rate.
        m (int): Compounding frequency per year.
        n (int): Total number of periods.
        F (float): Face value of the bond.

    Returns:
        float: Price of the bond.

    Raises:
        ValueError: If inputs are invalid (negative or non-numeric values).
    """
    if not all(isinstance(val, (int, float)) for val in [C, r, F]):
        raise ValueError("Coupon, interest rate, and face value must be numeric.")
    if not all(isinstance(val, int) for val in [m, n]) or m <= 0 or n <= 0:
        raise ValueError("Compounding frequency and number of periods must be positive integers.")
    if C < 0 or r < 0 or F < 0:
        raise ValueError("Coupon, interest rate, and face value must be non-negative.")

    coupon_sum = sum(C / (1 + r / m) ** (m * t) for t in range(1, n + 1))
    face_value_discounted = F / (1 + r / m) ** (m * n)
    return coupon_sum + face_value_discounted

def compute_forward_rate(R1, T1, R2, T2):
    """
    Compute the forward interest rate implied by two zero rates.

    Formula:
        R_F = (R2 * T2 - R1 * T1) / (T2 - T1)

    Args:
        R1 (float): Zero rate for maturity T1.
        T1 (float): Time to maturity for the first rate (in years).
        R2 (float): Zero rate for maturity T2.
        T2 (float): Time to maturity for the second rate (in years).

    Returns:
        float: Forward interest rate for the period between T1 and T2.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or T2 <= T1).
    """
    if not all(isinstance(val, (int, float)) for val in [R1, T1, R2, T2]):
        raise ValueError("All inputs must be numeric (int or float).")
    if T1 < 0 or T2 < 0:
        raise ValueError("Times to maturity (T1, T2) must be non-negative.")
    if T2 <= T1:
        raise ValueError("T2 must be greater than T1.")

    return (R2 * T2 - R1 * T1) / (T2 - T1)

def compute_instantaneous_forward_rate(R, T, dR_dT):
    """
    Compute the instantaneous forward rate for a maturity T.

    Formula:
        R_F = R + T * (dR/dT)

    Args:
        R (float): Zero rate for a maturity T.
        T (float): Time to maturity (in years).
        dR_dT (float): Derivative of the zero rate with respect to time (dR/dT).

    Returns:
        float: Instantaneous forward rate for the given maturity.

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [R, T, dR_dT]):
        raise ValueError("All inputs must be numeric (int or float).")
    if T < 0:
        raise ValueError("Time to maturity (T) must be non-negative.")

    return R + T * dR_dT

def compute_fra_cashflow_lender(L, RK, RM, T1, T2):
    """
    Company X lends money to company Y for the period between T1 and T2.
    Compute the cash flow to Company X under a Forward Rate Agreement (FRA).

    Formula:
        Cash Flow = L * (RK - RM) * (T2 - T1)

    Args:
        L (float): Principal underlying the contract.
        RK (float): Rate of interest agreed to in the FRA.
        RM (float): Actual observed LIBOR interest rate.
        T1 (float): Start time of the period (in years).
        T2 (float): End time of the period (in years).

    Returns:
        float: Cash flow to Company X.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or T2 <= T1).
    """
    if not all(isinstance(val, (int, float)) for val in [L, RK, RM, T1, T2]):
        raise ValueError("All inputs must be numeric (int or float).")
    if L <= 0 or T1 < 0 or T2 <= T1:
        raise ValueError("Principal (L) must be positive, T1 must be non-negative, and T2 must be greater than T1.")

    return (L * (RK - RM) * (T2 - T1)) / (1 + RM * (T2 - T1))

def compute_fra_cashflow_borrower(L, RM, RK, T1, T2):
    """
    Company X lends money to company Y for the period between T1 and T2.
    Compute the cash flow to Company Y under a Forward Rate Agreement (FRA).

    Formula:
        Cash Flow = L * (RM - RK) * (T2 - T1)

    Args:
        L (float): Principal underlying the contract.
        RM (float): Actual observed LIBOR interest rate.
        RK (float): Rate of interest agreed to in the FRA.
        T1 (float): Start time of the period (in years).
        T2 (float): End time of the period (in years).

    Returns:
        float: Cash flow to Company Y.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or T2 <= T1).
    """
    if not all(isinstance(val, (int, float)) for val in [L, RM, RK, T1, T2]):
        raise ValueError("All inputs must be numeric (int or float).")
    if L <= 0 or T1 < 0 or T2 <= T1:
        raise ValueError("Principal (L) must be positive, T1 must be non-negative, and T2 must be greater than T1.")

    return (L * (RM - RK) * (T2 - T1)) / (1 + RM * (T2 - T1))

def value_fra_receive_RK(L, RK, RF, T1, T2, R2):
    """
    Compute the value of a Forward Rate Agreement (FRA) where RK is received.

    Formula:
        V_FRA = L * (RK - RF) * (T2 - T1) * e^(-R2 * T2)

    Args:
        L (float): Principal underlying the contract.
        RK (float): Rate of interest agreed to in the FRA (received).
        RF (float): Forward LIBOR interest rate (paid).
        T1 (float): Start time of the period (in years).
        T2 (float): End time of the period (in years).
        R2 (float): Continuously compounded riskless zero rate for maturity T2.

    Returns:
        float: Value of the FRA where RK is received.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or T2 <= T1).
    """
    if not all(isinstance(val, (int, float)) for val in [L, RK, RF, T1, T2, R2]):
        raise ValueError("All inputs must be numeric (int or float).")
    if L <= 0 or T1 < 0 or T2 <= T1 or R2 < 0:
        raise ValueError("Principal (L) must be positive, T1 must be non-negative, T2 must be greater than T1, and R2 must be non-negative.")

    return L * (RK - RF) * (T2 - T1) * np.exp(-R2 * T2)

def value_fra_pay_RK(L, RF, RK, T1, T2, R2):
    """
    Compute the value of a Forward Rate Agreement (FRA) where RK is paid.

    Formula:
        V_FRA = L * (RF - RK) * (T2 - T1) * e^(-R2 * T2)

    Args:
        L (float): Principal underlying the contract.
        RF (float): Forward LIBOR interest rate (received).
        RK (float): Rate of interest agreed to in the FRA (paid).
        T1 (float): Start time of the period (in years).
        T2 (float): End time of the period (in years).
        R2 (float): Continuously compounded riskless zero rate for maturity T2.

    Returns:
        float: Value of the FRA where RK is paid.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or T2 <= T1).
    """
    if not all(isinstance(val, (int, float)) for val in [L, RF, RK, T1, T2, R2]):
        raise ValueError("All inputs must be numeric (int or float).")
    if L <= 0 or T1 < 0 or T2 <= T1 or R2 < 0:
        raise ValueError("Principal (L) must be positive, T1 must be non-negative, T2 must be greater than T1, and R2 must be non-negative.")

    return L * (RF - RK) * (T2 - T1) * np.exp(-R2 * T2)

def compute_bond_price_from_cash_flows(cash_flows, times, yield_rate):
    """
    Compute the price of a bond using continuous compounding.

    Formula:
        B = sum(c_i * e^(-y * t_i))

    Args:
        cash_flows (list of float): Cash flows of the bond.
        times (list of float): Times at which cash flows are received (in years).
        yield_rate (float): Continuously compounded yield.

    Returns:
        float: Price of the bond.

    Raises:
        ValueError: If inputs are invalid (non-numeric or mismatched lengths).
    """
    if not isinstance(yield_rate, (int, float)) or yield_rate < 0:
        raise ValueError("Yield rate must be a non-negative numeric value.")
    if len(cash_flows) != len(times):
        raise ValueError("Cash flows and times must have the same length.")
    if not all(isinstance(val, (int, float)) for val in cash_flows + times):
        raise ValueError("Cash flows and times must be numeric.")

    return sum(c * np.exp(-yield_rate * t) for c, t in zip(cash_flows, times))

def compute_macaulay_duration(cash_flows, times, yield_rate):
    """
    Compute the Macaulay Duration of a bond.

    Formula:
        D = (sum(t_i * c_i * e^(-y * t_i)) / B)

    Args:
        cash_flows (list of float): Cash flows of the bond.
        times (list of float): Times at which cash flows are received (in years).
        yield_rate (float): Continuously compounded yield.

    Returns:
        float: Macaulay Duration of the bond.

    Raises:
        ValueError: If inputs are invalid (non-numeric or mismatched lengths).
    """
    bond_price = compute_bond_price_from_cash_flows(cash_flows, times, yield_rate)
    if bond_price == 0:
        raise ValueError("Bond price cannot be zero.")

    numerator = sum(t * c * np.exp(-yield_rate * t) for c, t in zip(cash_flows, times))
    return numerator / bond_price

def compute_change_in_bond_price(cash_flows, times, yield_rate, delta_y):
    """
    Approximate the change in bond price due to a small change in yield.

    Formula:
        ΔB = -Δy * sum(t_i * c_i * e^(-y * t_i))

    Args:
        cash_flows (list of float): Cash flows of the bond.
        times (list of float): Times at which cash flows are received (in years).
        yield_rate (float): Continuously compounded yield.
        delta_y (float): Small change in yield.

    Returns:
        float: Approximate change in bond price.

    Raises:
        ValueError: If inputs are invalid (non-numeric or mismatched lengths).
    """
    if not isinstance(delta_y, (int, float)):
        raise ValueError("Delta_y must be numeric.")

    numerator = sum(t * c * np.exp(-yield_rate * t) for c, t in zip(cash_flows, times))
    return -delta_y * numerator

def compute_change_in_bond_price_from_duration(bond_price, duration, delta_y):
    """
    Compute the change in bond price using its duration and a change in yield.

    Formula:
        ΔB = -B * D * Δy

    Args:
        bond_price (float): Current price of the bond (B).
        duration (float): Macaulay Duration of the bond (D).
        delta_y (float): Small change in yield (Δy).

    Returns:
        float: Change in bond price (ΔB).

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [bond_price, duration, delta_y]):
        raise ValueError("All inputs must be numeric (int or float).")
    if bond_price <= 0 or duration < 0:
        raise ValueError("Bond price must be positive and duration must be non-negative.")

    return -bond_price * duration * delta_y

def compute_relative_change_in_bond_price(duration, delta_y):
    """
    Compute the relative change in bond price using its duration and a change in yield.

    Formula:
        ΔB / B = -D * Δy

    Args:
        duration (float): Macaulay Duration of the bond (D).
        delta_y (float): Small change in yield (Δy).

    Returns:
        float: Relative change in bond price (ΔB / B).

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [duration, delta_y]):
        raise ValueError("All inputs must be numeric (int or float).")
    if duration < 0:
        raise ValueError("Duration must be non-negative.")

    return -duration * delta_y

def compute_modified_duration(macaulay_duration, yield_rate, m=1):
    """
    Compute the modified duration of a bond.

    Formula:
        D* = D / (1 + y / m)

    Args:
        macaulay_duration (float): Macaulay Duration of the bond (D).
        yield_rate (float): Yield rate (y) expressed with compounding frequency m.
        m (int): Compounding frequency per year (default is 1 for annual compounding).

    Returns:
        float: Modified duration (D*).

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or m <= 0).
    """
    if not isinstance(macaulay_duration, (int, float)) or not isinstance(yield_rate, (int, float)):
        raise ValueError("Macaulay duration and yield rate must be numeric.")
    if not isinstance(m, int) or m <= 0:
        raise ValueError("Compounding frequency (m) must be a positive integer.")
    if macaulay_duration < 0 or yield_rate < 0:
        raise ValueError("Macaulay duration and yield rate must be non-negative.")

    return macaulay_duration / (1 + yield_rate / m)


def compute_change_in_bond_price_from_modified_duration(bond_price, modified_duration, delta_y):
    """
    Compute the change in bond price using modified duration.

    Formula:
        ΔB = -B * D* * Δy

    Args:
        bond_price (float): Current price of the bond (B).
        modified_duration (float): Modified duration of the bond (D*).
        delta_y (float): Small change in yield (Δy).

    Returns:
        float: Change in bond price (ΔB).

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [bond_price, modified_duration, delta_y]):
        raise ValueError("All inputs must be numeric (int or float).")
    if bond_price <= 0 or modified_duration < 0:
        raise ValueError("Bond price must be positive and modified duration must be non-negative.")

    return -bond_price * modified_duration * delta_y

def compute_convexity(cash_flows, times, yield_rate):
    """
    Compute the convexity of a bond.

    Formula:
        C = (1 / B) * sum(c_i * t_i^2 * e^(-y * t_i))

    Args:
        cash_flows (list of float): Cash flows of the bond.
        times (list of float): Times at which cash flows are received (in years).
        yield_rate (float): Continuously compounded yield.

    Returns:
        float: Convexity of the bond.

    Raises:
        ValueError: If inputs are invalid (non-numeric, negative values, or mismatched lengths).
    """
    if not isinstance(yield_rate, (int, float)) or yield_rate < 0:
        raise ValueError("Yield rate must be a non-negative numeric value.")
    if len(cash_flows) != len(times):
        raise ValueError("Cash flows and times must have the same length.")
    if not all(isinstance(val, (int, float)) for val in cash_flows + times):
        raise ValueError("Cash flows and times must be numeric.")

    bond_price = sum(c * np.exp(-yield_rate * t) for c, t in zip(cash_flows, times))
    if bond_price == 0:
        raise ValueError("Bond price cannot be zero.")

    convexity = sum(c * t**2 * np.exp(-yield_rate * t) for c, t in zip(cash_flows, times))
    return convexity / bond_price

def compute_change_in_bond_price_with_convexity(bond_price, modified_duration, convexity, delta_y):
    """
    Compute the change in bond price using modified duration and convexity.

    Formula:
        ΔB = -B * D * Δy + 0.5 * B * C * (Δy)^2

    Args:
        bond_price (float): Current price of the bond (B).
        modified_duration (float): Modified duration of the bond (D).
        convexity (float): Convexity of the bond (C).
        delta_y (float): Small change in yield (Δy).

    Returns:
        float: Change in bond price (ΔB).

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [bond_price, modified_duration, convexity, delta_y]):
        raise ValueError("All inputs must be numeric (int or float).")
    if bond_price <= 0 or modified_duration < 0 or convexity < 0:
        raise ValueError("Bond price, modified duration, and convexity must be non-negative, with bond price positive.")

    return -bond_price * modified_duration * delta_y + 0.5 * bond_price * convexity * delta_y**2

def compute_relative_change_in_bond_price_with_convexity(modified_duration, convexity, delta_y):
    """
    Compute the relative change in bond price using modified duration and convexity.

    Formula:
        ΔB / B = -D * Δy + 0.5 * C * (Δy)^2

    Args:
        modified_duration (float): Modified duration of the bond (D).
        convexity (float): Convexity of the bond (C).
        delta_y (float): Small change in yield (Δy).

    Returns:
        float: Relative change in bond price (ΔB / B).

    Raises:
        ValueError: If inputs are invalid (non-numeric or negative values).
    """
    if not all(isinstance(val, (int, float)) for val in [modified_duration, convexity, delta_y]):
        raise ValueError("All inputs must be numeric (int or float).")
    if modified_duration < 0 or convexity < 0:
        raise ValueError("Modified duration and convexity must be non-negative.")

    return -modified_duration * delta_y + 0.5 * convexity * delta_y**2


