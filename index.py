from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton, QLabel, QWidget,QTableWidgetItem
from PyQt5 import uic
from ViewProductos import ViewProductos
import sys
class AdminView(QMainWindow):
    formValid=False

    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindowAdmin.ui",self)
        self.botonProductos.clicked.connect(self.showProductos)
    def showProductos(self):
        view=ViewProductos(self)
        view.show()
if __name__=="__main__":
    app=QApplication(sys.argv)
    gui = AdminView()
    gui.show()
    sys.exit(app.exec())