from PyQt5.QtWidgets import   QDialog,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QHeaderView
from pymsgbox import *
import sys
class ViewAbonar(QDialog):
    def __init__(self,parametros, *args, **kwargs):

        super(ViewAbonar, self).__init__(*args, **kwargs)
        #todos los creditos en los que se debe dinero
        self.creditos=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        # instanciamiento de mi clase Valida
        self.valida = parametros['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        loadUi("Abonar.ui",self)
        #Inicialización para los eventos de los botones
        self.botabonar.clicked.connect(self.abonar)
        self.botcancelar.clicked.connect(self.cancelar)
        self.tablecreditos.clicked.connect(self.rowClicked)
        self.tablecreditos.doubleClicked.connect(self.doubleRowClicked)
        self.abono.returnPressed.connect(self.abonar)
        self.abono.textChanged.connect(self.validaAbono)
        #configuracion de la cabecera de mi tabla
        header = self.tablecreditos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.RefreshTableData()
        self.creditosview=True
        self.adeudo=0
        self.deudor=''
        self.id_credito=''
    def abonar(self):
        if self.validaAbono():
            if float(self.abono.text())<=self.adeudo:
                texto='Desea abonar $'+str(self.abono.text())+' al credito de '+self.deudor+'?'
                opc=confirm(title='Abonar?',text=texto,buttons=['OK','CANCEL'])
                if opc=='OK':
                    self.con.Abonar(self.id_credito,self.abono.text())
                    self.botabonar.setEnabled(False)
                    self.RefreshTableData()
            else:
                alert(title='Atención',text='El monto a abonar excede el adeudo')
        else:
            alert(title='Error!',text='Entrada no válida')
    def cancelar(self):
        if self.creditosview:
            self.close()
        else:
            self.creditosview=True
            self.botabonar.setEnabled(True)
            self.tablecreditos.setColumnCount(6)
            index = self.tablecreditos.rowCount()
            for i in range(index):
                self.tablecreditos.removeRow(0)
            labels = ('ID', 'Cliente', 'Fecha inicio', 'Fecha vencimiento', 'Descripción','Adeudo')
            self.tablecreditos.setHorizontalHeaderLabels(labels)
            header = self.tablecreditos.horizontalHeader()
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.RefreshTableData()
    def validaAbono(self):
        input = self.abono
        if self.valida.validaDecimal(input.text()) and len(input.text())>0:
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def rowClicked(self):
        if self.creditosview:
            self.botabonar.setEnabled(True)
            row=self.tablecreditos.currentRow()
            self.adeudo=float(self.tablecreditos.item(row,5).text())
            self.id_credito=self.tablecreditos.item(row,0).text()
            self.abono.setText(self.tablecreditos.item(row,5).text())
            self.deudor=self.tablecreditos.item(row,1).text()
            self.abono.setSelection(0,9999)
            self.abono.setFocus()
    def doubleRowClicked(self):
        if self.creditosview:
            self.botabonar.setEnabled(False)
            self.creditosview=False
            row=self.tablecreditos.currentRow()
            idcredito=self.tablecreditos.item(row,0).text()
            self.tablecreditos.setColumnCount(5)
            index=self.tablecreditos.rowCount()
            for i in range(index):
                self.tablecreditos.removeRow(0)
            labels=('Producto','Cantidad','Precio','Fecha','Importe')
            self.tablecreditos.setHorizontalHeaderLabels(labels)
            productos=self.con.AllProductsInCredit(idcredito)
            for i in range(len(productos)):
                self.tablecreditos.insertRow(i)
                self.tablecreditos.setItem(i, 0, QTableWidgetItem(str(productos[i]['producto'])))
                self.tablecreditos.setItem(i, 1, QTableWidgetItem(str(productos[i]['cantidad'])))
                self.tablecreditos.setItem(i, 2, QTableWidgetItem(str(productos[i]['precio'])))
                self.tablecreditos.setItem(i, 3, QTableWidgetItem(str(productos[i]['fecha'])))
                self.tablecreditos.setItem(i, 4, QTableWidgetItem(str(float(productos[i]['cantidad'])*float(productos[i]['precio']))))
                header = self.tablecreditos.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
    def RefreshTableData(self):
        self.creditos=self.con.AllCreditsSinpagar()
        index = self.tablecreditos.rowCount()
        for i in range(index):
            self.tablecreditos.removeRow(0)
        for i in range(len(self.creditos)):
            self.tablecreditos.insertRow(i)
            cliente=self.con.GetClientById(self.creditos[i]['idcliente'])
            self.tablecreditos.setItem(i, 0, QTableWidgetItem(str(self.creditos[i]['id'])))
            self.tablecreditos.setItem(i, 1, QTableWidgetItem(cliente[0]['nombre']+' '+cliente[0]['apellidos']))
            self.tablecreditos.setItem(i, 2, QTableWidgetItem(str(self.creditos[i]['fechainicio'])))
            self.tablecreditos.setItem(i, 3, QTableWidgetItem(str(self.creditos[i]['fechavencimiento'])))
            self.tablecreditos.setItem(i, 4, QTableWidgetItem(str(self.creditos[i]['descripcionproductos'])))
            self.tablecreditos.setItem(i, 5, QTableWidgetItem(str(self.creditos[i]['adeudo'])))

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from validaciones import Valida
    from conexion import Conexion
    app = QApplication(sys.argv)
    gui = ViewAbonar(parametros={'conexion':Conexion(),'valida':Valida()})
    gui.show()
    sys.exit(app.exec())