from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QCheckBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from simulation import run_simulation


class RetirementSimulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input Fields
        self.label_starting_balance = QLabel('Starting Balance ($):')
        self.input_starting_balance = QLineEdit()

        self.label_monthly_contribution = QLabel('Monthly Contribution ($):')
        self.input_monthly_contribution = QLineEdit()

        self.label_bonus = QLabel('Annual Bonus ($):')
        self.input_bonus = QLineEdit()

        self.label_retirement_age = QLabel('Retirement Age:')
        self.input_retirement_age = QLineEdit()

        # Investment Strategy Dropdown
        self.label_strategy = QLabel('Investment Strategy:')
        self.combo_strategy = QComboBox()
        self.combo_strategy.addItems(['Aggressive', 'Moderate', 'Conservative'])

        # Recession Checkbox
        self.checkbox_recession = QCheckBox('Include Recession Impact')

        # Simulate Button
        self.simulate_button = QPushButton('Simulate Retirement')
        self.simulate_button.clicked.connect(self.run_simulation)

        # Graph Canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Add Widgets to Layout
        layout.addWidget(self.label_starting_balance)
        layout.addWidget(self.input_starting_balance)
        layout.addWidget(self.label_monthly_contribution)
        layout.addWidget(self.input_monthly_contribution)
        layout.addWidget(self.label_bonus)
        layout.addWidget(self.input_bonus)
        layout.addWidget(self.label_retirement_age)
        layout.addWidget(self.input_retirement_age)
        layout.addWidget(self.label_strategy)
        layout.addWidget(self.combo_strategy)
        layout.addWidget(self.checkbox_recession)
        layout.addWidget(self.simulate_button)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setWindowTitle('Retirement Simulation Predictor')
        self.setGeometry(100, 100, 600, 600)

    def run_simulation(self):
        try:
            start_balance = float(self.input_starting_balance.text())
            monthly_contrib = float(self.input_monthly_contribution.text())
            bonus = float(self.input_bonus.text())
            retirement_age = int(self.input_retirement_age.text())

            strategy = self.combo_strategy.currentText()
            recession = self.checkbox_recession.isChecked()

            results = run_simulation(start_balance, monthly_contrib, bonus, retirement_age, strategy, recession)

            # Plot the results
            self.ax.clear()
            self.ax.plot(results['Age'], results['Balance'], label='Projected Balance')
            self.ax.set_xlabel('Age')
            self.ax.set_ylabel('Balance ($)')
            self.ax.set_title('Retirement Savings Growth')
            self.ax.legend()
            self.canvas.draw()

        except ValueError:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 'Invalid Input!', ha='center', va='center', fontsize=12, color='red')
            self.canvas.draw()
