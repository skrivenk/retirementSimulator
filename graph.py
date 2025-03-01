import matplotlib.pyplot as plt

def plot_simulation(results):
    plt.figure(figsize=(8, 5))
    for col in results.columns[:-1]:
        plt.plot(results["Age"], results[col], color='gray', alpha=0.1)
    plt.plot(results["Age"], results.median(axis=1), color='blue', label="Median Projection")
    plt.xlabel("Age")
    plt.ylabel("Balance ($)")
    plt.title("Retirement Savings Projection")
    plt.grid(True)
    plt.legend()
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.show()
