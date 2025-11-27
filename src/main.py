import sys
from PyQt6.QtWidgets import QApplication
from gui import TradingBotGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingBotGUI()
    window.show()
    sys.exit(app.exec())
