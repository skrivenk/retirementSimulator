# Retirement Simulation Predictor

### Overview
The **Retirement Simulation Predictor** is a **GUI-based interactive application** built using **Python (PyQt6)**. It helps users **simulate their retirement savings growth** using **Monte Carlo simulations** while accounting for **investment strategies, recessions, and salary growth over time**.

---

## Features
- **User-friendly GUI** built with PyQt6  
- **Monte Carlo Simulations** for realistic retirement forecasting  
- **Multiple Investment Strategies** (Aggressive, Moderate, Conservative)  
- **Recession Impact Simulation**  
- **Customizable Contribution Growth** (Increase savings over time)  
- **Annual Bonus Adjustments** (Including growth projections)  
- **Clear Fields Button** for resetting inputs  
- **Status Updates** during simulations  
- **Graphical Visualization of Results** using Matplotlib  
- **Formatted Financial Figures** (No scientific notation)  

---

## Technologies Used
- **Python 3.x**
- **PyQt6** (GUI framework)
- **Matplotlib** (Graph visualization)
- **NumPy & Pandas** (Data handling)
- **GitHub** (Version control)

---

## Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/skrivenk/retirementSimulator.git
   cd retirementSimulator

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # (Mac/Linux)
   .venv\Scripts\activate     # (Windows)

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Run the application:
   ```bash
   python main.py

## How to use
1. Enter your starting balance, monthly contributions, and annual bonuses.
2. Set your current age and desired retirement age.
3. Choose an investment strategy:
  Aggressive (Higher risk, higher reward)
  Moderate (Balanced growth)
  Conservative (Low risk, stable returns)
4. Enable "Include Recession Impact" if you want market downturns to be factored in.
5. Adjust salary growth & bonuses over time.
6. Click "Simulate Retirement" and wait for the graph & final projections.
7. View the Final Balance and Total Contributions at the top of the results tab.
