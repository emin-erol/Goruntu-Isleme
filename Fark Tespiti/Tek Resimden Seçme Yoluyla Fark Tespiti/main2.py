from PyQt5.QtWidgets import QApplication
import fark_tespiti
import sys

app = QApplication(sys.argv)
window = fark_tespiti.Window()
window.show()

sys.exit(app.exec_())

