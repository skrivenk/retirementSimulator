import matplotlib.pyplot as plt


def plot_simulation(results):
    """
    Plots the retirement savings simulation results.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(results["Age"], results["Balance"], marker='o', linestyle='-')
    plt.xlabel("Age")
    plt.ylabel("Balance ($)")
    plt.title("Retirement Savings Projection")
    plt.grid(True)
    plt.show()
