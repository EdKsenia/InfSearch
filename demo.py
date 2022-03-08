import sys

from PyQt5.QtWidgets import QApplication

# from form.MainMenu import MainMenuWidget
from TestForm import TestFormWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = MainMenuWidget()
    ex = TestFormWidget()
    ex.show()
    sys.exit(app.exec_())