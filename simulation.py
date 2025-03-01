import numpy as np
import pandas as pd


def run_simulation(start_balance, monthly_contrib, bonus, retirement_age, strategy, recession):
    """
    Simulates retirement savings growth based on user inputs.
    """
    current_age = 30  # Assumed starting age
    years = retirement_age - current_age

    # Define Investment Strategy Returns & Risks
    strategy_returns = {
        "Aggressive": (0.07, 0.15),   # Higher returns, higher risk
        "Moderate": (0.05, 0.10),     # Balanced risk
        "Conservative": (0.03, 0.05)  # Lower risk, stable returns
    }

    avg_return, std_dev = strategy_returns[strategy]

    # Apply recession impact
    if recession:
        avg_return -= 0.02

    # Simulate Retirement Savings Growth
    balances = [start_balance]
    ages = [current_age]

    for year in range(1, years + 1):
        new_balance = balances[-1] * (1 + np.random.normal(avg_return, std_dev)) + (monthly_contrib * 12) + bonus
        balances.append(new_balance)
        ages.append(current_age + year)

    return pd.DataFrame({"Age": ages, "Balance": balances})
