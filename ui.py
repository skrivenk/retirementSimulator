from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QCheckBox,
    QTabWidget, QGridLayout, QFrame, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # Import ticker for formatting
from simulation import run_simulation


class RetirementSimulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.input_tab = QWidget()
        self.result_tab = QWidget()

        self.tabs.addTab(self.input_tab, "Input Data")
        self.tabs.addTab(self.result_tab, "Results")

        self.setup_input_tab()
        self.setup_result_tab()  # ✅ FIXED: Function was missing

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.setWindowTitle('Retirement Simulation Predictor')
        self.setGeometry(100, 100, 700, 500)

    def setup_input_tab(self):
        """ Sets up the Input Tab with form layout. """
        layout = QGridLayout()

        # Labels and Inputs
        self.label_starting_balance = QLabel('Starting Balance ($):')
        self.input_starting_balance = QLineEdit()

        self.label_monthly_contribution = QLabel('Monthly Contribution ($):')
        self.input_monthly_contribution = QLineEdit()

        self.label_bonus = QLabel('Annual Bonus ($):')
        self.input_bonus = QLineEdit()

        self.label_current_age = QLabel('Current Age:')
        self.input_current_age = QLineEdit()

        self.label_retirement_age = QLabel('Retirement Age:')
        self.input_retirement_age = QLineEdit()

        self.label_strategy = QLabel('Investment Strategy:')
        self.combo_strategy = QComboBox()
        self.combo_strategy.addItems(['Aggressive', 'Moderate', 'Conservative'])

        self.checkbox_recession = QCheckBox('Include Recession Impact')

        # Contribution Growth Inputs
        self.label_increase_frequency = QLabel('Increase Every (Years):')
        self.input_increase_frequency = QLineEdit()

        self.label_increase_percent = QLabel('Increase by (%):')
        self.input_increase_percent = QLineEdit()

        self.label_bonus_increase = QLabel('Bonus Increase (%):')
        self.input_bonus_increase = QLineEdit()

        # Set fixed width for input fields
        input_field_width = 150
        self.input_starting_balance.setFixedWidth(input_field_width)
        self.input_monthly_contribution.setFixedWidth(input_field_width)
        self.input_bonus.setFixedWidth(input_field_width)
        self.input_current_age.setFixedWidth(input_field_width)
        self.input_retirement_age.setFixedWidth(input_field_width)
        self.input_increase_frequency.setFixedWidth(80)
        self.input_increase_percent.setFixedWidth(80)
        self.input_bonus_increase.setFixedWidth(80)

        # Simulate Button
        self.simulate_button = QPushButton('Simulate Retirement')
        self.simulate_button.setFixedWidth(200)  # Reduce button width
        self.simulate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.simulate_button.clicked.connect(self.run_simulation)

        # Clear Fields Button
        self.clear_button = QPushButton("Clear Fields")
        self.clear_button.setFixedWidth(200)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f; 
                color: white; 
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        self.clear_button.clicked.connect(self.clear_fields)

        # Center Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.simulate_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: blue;")

        # Adding elements to grid layout
        layout.addWidget(self.label_starting_balance, 0, 0)
        layout.addWidget(self.input_starting_balance, 0, 1)
        layout.addWidget(self.label_monthly_contribution, 1, 0)
        layout.addWidget(self.input_monthly_contribution, 1, 1)
        layout.addWidget(self.label_bonus, 2, 0)
        layout.addWidget(self.input_bonus, 2, 1)
        layout.addWidget(self.label_current_age, 3, 0)
        layout.addWidget(self.input_current_age, 3, 1)
        layout.addWidget(self.label_retirement_age, 4, 0)
        layout.addWidget(self.input_retirement_age, 4, 1)
        layout.addWidget(self.label_strategy, 5, 0)
        layout.addWidget(self.combo_strategy, 5, 1)
        layout.addWidget(self.checkbox_recession, 6, 0, 1, 2)
        layout.addWidget(self.label_increase_frequency, 7, 0)
        layout.addWidget(self.input_increase_frequency, 7, 1)
        layout.addWidget(self.label_increase_percent, 8, 0)
        layout.addWidget(self.input_increase_percent, 8, 1)
        layout.addWidget(self.label_bonus_increase, 9, 0)
        layout.addWidget(self.input_bonus_increase, 9, 1)
        layout.addLayout(button_layout, 10, 0, 1, 2)
        layout.addWidget(self.status_label, 11, 0, 1, 2)

        self.input_tab.setLayout(layout)

    def setup_result_tab(self):
        """ Sets up the Results Tab with a graph and summary. """
        layout = QVBoxLayout()

        # Summary Panel
        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray; padding: 10px;")
        self.summary_layout = QHBoxLayout()
        self.label_final_balance = QLabel("Final Balance: $0")
        self.label_total_contributions = QLabel("Total Contributions: $0")
        self.label_final_balance.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.label_total_contributions.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.summary_layout.addWidget(self.label_final_balance)
        self.summary_layout.addWidget(self.label_total_contributions)
        self.summary_frame.setLayout(self.summary_layout)

        # Graph Canvas
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.figure.tight_layout(pad=2.5)
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.summary_frame)
        layout.addWidget(self.canvas)
        self.result_tab.setLayout(layout)

    def clear_fields(self):
        """ Clears all input fields. """
        for widget in self.input_tab.findChildren(QLineEdit):
            widget.clear()

    def run_simulation(self):
        """ Runs the simulation and updates the UI with status messages. """
        try:
            self.status_label.setText("Running Simulation... Please wait.")
            QTimer.singleShot(100, self.execute_simulation)
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def execute_simulation(self):
        try:
            results, percentiles = run_simulation(
                float(self.input_starting_balance.text()),
                float(self.input_monthly_contribution.text()),
                float(self.input_bonus.text()),
                int(self.input_current_age.text()),
                int(self.input_retirement_age.text()),
                self.combo_strategy.currentText(),
                self.checkbox_recession.isChecked(),
                int(self.input_increase_frequency.text() or 5),
                float(self.input_increase_percent.text() or 5),
                float(self.input_bonus_increase.text() or 5)
            )

            # ✅ FIX: Update Summary Labels with Correct Values
            final_balance = percentiles["90th Percentile"]
            total_contributions = percentiles["50th Percentile (Median)"]

            self.label_final_balance.setText(f"Final Balance: ${final_balance:,.0f}")
            self.label_total_contributions.setText(f"Total Contributions: ${total_contributions:,.0f}")

            self.ax.clear()
            for col in results.columns[:-1]:
                self.ax.plot(results["Age"], results[col], color='gray', alpha=0.1)
            self.ax.plot(results["Age"], results.median(axis=1), color='blue', label="Median Projection", linewidth=2)
            self.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
            self.figure.tight_layout()
            self.canvas.draw()

            self.status_label.setText("Simulation Complete! Switch to Results Tab.")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
