import sys
from PyQt6.QtWidgets import QApplication
from gui import TradingBotGUI  # Import the class, not a function

if __name__ == "__main__":
    app = QApplication(sys.argv)   # Create the Qt application
    window = TradingBotGUI()       # Instantiate your GUI class
    window.show()                  # Show the window
    sys.exit(app.exec())           # Start the Qt event loop
