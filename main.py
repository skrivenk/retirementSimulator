import sys
from PyQt6.QtWidgets import QApplication
from ui import RetirementSimulatorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RetirementSimulatorApp()
    window.show()
    sys.exit(app.exec())
