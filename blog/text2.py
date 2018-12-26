import sys
from PyQt5 import QtCore, QtWidgets

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(400, 1400)
widget.setWindowTitle("This is a demo for PyQt Widget.")
widget.show()

exit(app.exec_())
