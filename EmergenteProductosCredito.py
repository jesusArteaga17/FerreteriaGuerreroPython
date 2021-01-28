from PyQt5.QtWidgets import QDialog,QTableWidgetItem,QHeaderView
from PyQt5 import uic
from pymsgbox import *
class EmergenteProductosCredito(QDialog):
    def __init__(self, datos={},*args, **kwargs):
        super(EmergenteProductosCredito, self).__init__(*args, **kwargs)
        uic.loadUi("ViewProductosCredito.ui", self)
        self.nombrecliente.setText(datos['nombrecliente'])
        self.fechainicio.setText(datos['fechainicio'])
        self.fechavencimiento.setText(datos['fechavencimiento'])
        self.adeudo.setText(str(datos['adeudo']))
        self.id_credito=datos['id_credito']
        self.con=datos['conexion']
        self.montototal.setText('0')
        self.productos=self.con
        self.RefreshTableData()
        montototal=0
        numRows=self.tableProductsInCredit.rowCount()
        for i in range(numRows):
            montototal+=float(self.tableProductsInCredit.item(i,4).text())
        self.montototal.setText(str(montototal))
    def RefreshTableData(self):
        productos = self.con.AllProductsInCredit(self.id_credito)
        for i in range(len(productos)):
            self.tableProductsInCredit.insertRow(i)
            self.tableProductsInCredit.setItem(i, 0, QTableWidgetItem(str(productos[i]['producto'])))
            self.tableProductsInCredit.setItem(i, 1, QTableWidgetItem(str(productos[i]['fecha'])))
            self.tableProductsInCredit.setItem(i, 2, QTableWidgetItem(str(productos[i]['cantidad'])))
            self.tableProductsInCredit.setItem(i, 3, QTableWidgetItem(str(productos[i]['precio'])))
            self.tableProductsInCredit.setItem(i, 4, QTableWidgetItem(
                str(float(productos[i]['cantidad']) * float(productos[i]['precio']))))
            header = self.tableProductsInCredit.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    datos={}
    datos['nombrecliente']='juan'
    datos['fechainicio']='11-42-2020'
    datos['fechavencimiento']='355-256-3'
    gui = EmergenteProductosCredito(datos)
    gui.show()
    sys.exit(app.exec())