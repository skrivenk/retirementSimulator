import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def run_simulation(start_balance, monthly_contrib, bonus, current_age, retirement_age, strategy, recession,
                   increase_frequency=5, increase_percent=5, bonus_increase_percent=5, num_simulations=10000):
    """
    Runs Monte Carlo simulation with increasing contributions and bonuses over time.

    Parameters:
    - start_balance: Initial savings balance
    - monthly_contrib: Monthly contribution amount
    - bonus: Annual bonus added to savings
    - current_age: User's current age
    - retirement_age: Target retirement age
    - strategy: Investment strategy ('Aggressive', 'Moderate', 'Conservative')
    - recession: Boolean indicating if recession impact should be included
    - increase_frequency: How often (in years) contributions increase.
    - increase_percent: Percentage increase in contributions.
    - bonus_increase_percent: Percentage increase in annual bonuses.
    - num_simulations: Number of Monte Carlo simulations to run

    Returns:
    - df_trajectories: DataFrame containing the simulated balances over time
    - percentiles: Dictionary containing 10th, 50th (median), and 90th percentile results
    """

    years = retirement_age - current_age

    strategy_returns = {
        "Aggressive": (0.07, 0.15),
        "Moderate": (0.05, 0.10),
        "Conservative": (0.03, 0.05)
    }

    avg_return, std_dev = strategy_returns[strategy]
    if recession:
        avg_return -= 0.02

    final_balances = []
    balance_trajectories = []

    for _ in range(num_simulations):
        balances = [start_balance]
        curr_monthly_contrib = monthly_contrib
        curr_bonus = bonus

        for year in range(years):
            annual_return = np.random.normal(avg_return, std_dev)
            new_balance = balances[-1] * (1 + annual_return) + (curr_monthly_contrib * 12) + curr_bonus
            balances.append(new_balance)

            # Apply contribution & bonus increases at the set frequency
            if (year + 1) % increase_frequency == 0:
                curr_monthly_contrib *= (1 + increase_percent / 100)
                curr_bonus *= (1 + bonus_increase_percent / 100)

        final_balances.append(balances[-1])
        balance_trajectories.append(balances)

    df_trajectories = pd.DataFrame(balance_trajectories).T
    df_trajectories.columns = [f"Sim {i+1}" for i in range(num_simulations)]
    df_trajectories["Age"] = list(range(current_age, retirement_age + 1))

    percentiles = {
        "10th Percentile": round(np.percentile(final_balances, 10)),
        "50th Percentile (Median)": round(np.percentile(final_balances, 50)),
        "90th Percentile": round(np.percentile(final_balances, 90))
    }

    return df_trajectories, percentiles


def plot_simulation(results):
    """
    Plots the Monte Carlo simulation results.
    """
    plt.figure(figsize=(8, 5))

    # Plot multiple simulation lines in gray
    for col in results.columns[:-1]:  # Exclude 'Age' column
        plt.plot(results["Age"], results[col], color='gray', alpha=0.1)

    # Highlight median projection
    plt.plot(results["Age"], results.median(axis=1), color='blue', label="Median Projection")

    plt.xlabel("Age")
    plt.ylabel("Balance ($)")
    plt.title("Retirement Savings Projection")
    plt.grid(True)
    plt.legend()

    # Format y-axis to show whole dollar amounts
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.show()
