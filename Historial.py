from PyQt5.QtWidgets import  QDialog,QTableWidgetItem,QHeaderView
from PyQt5 import uic,QtCore
from datetime import datetime
import sys,os
#QDateEdit.setDate()
class ViewHistorial(QDialog):
    def __init__(self,parametros={}, *args, **kwargs):
        #self.fecha.setDate()
        super(ViewHistorial, self).__init__(*args, **kwargs)
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        self.ventas = self.con.AllVentas()
        uic.loadUi("Historial.ui",self)
        #Inicialización para los eventos de los botones
        self.botcancelar.clicked.connect(self.cancelar)
        self.botonimprimir.clicked.connect(self.imprime)
        self.tableventas.doubleClicked.connect(self.doubleRowClicked)
        self.tableventas.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        header = self.tableventas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.ventasview=True

        self.folio_venta_selected=0
        date = datetime.now()
        self.fecha.setDate(QtCore.QDate(date.year,date.month,date.day))
        self.fecha.dateChanged.connect(self.RefreshTableData)
        self.RefreshTableData()
    def hacerTicket(self,num_venta,venta,carrito):
        ticket='Ferretería Guerrero\nNicolás Bravo #4 esq. Américas\nTepechitlán Zacatecas\n99750\n\n______________________________\n'
        ticket+='No. TICKET:'+str(num_venta)+'\n'
        date = datetime.now()
        hora=date.hour
        minute=date.minute
        if hora<9:
            hora='0'+str(hora)
        if minute<9:
            minute='0'+str(minute)
        ticket+='FECHA: '+str(venta['fecha'])+'\nHORA: '+str(hora)+':'+str(minute)+'\n______________________________\nCantidad       Precio           Importe\n______________________________\n'
        col_vacia = "                       "
        for producto in carrito:
            ticket+=producto['producto'][:34]+'\n'
            cantidad = str(round(float(producto['cantidad']), 2))
            precio = str(round(float(producto['precio']), 2))
            importe = str(round(float(producto['cantidad']) * float(producto['precio']), 2))
            ticket+=cantidad+col_vacia[len(cantidad)*2:]+precio+col_vacia[len(precio)*2:]+importe+'\n'
        ticket+='______________________________\n\n'
        ticket+='Total: '+str(venta['importe'])+'\nPago: '+str(venta['pago'])+'\nCambio: '+str(venta['cambio'])+'\nOperador: '+venta['usuario']+'\n'+'Cliente: '+venta['cliente']
        return str(ticket)
    def imprime(self):
        venta=self.con.GetVenta(self.folio_venta_selected)
        carrito=self.con.GetProductosVenta(venta['id'])
        texto = self.hacerTicket(venta['id'], venta, carrito)
        f = open('Ticket.txt', 'w+')
        f.write(texto)
        f.close()
        os.startfile('Ticket.txt','print')
    def rowClicked(self):
        if self.ventasview:
            row=self.tableventas.currentRow()
            self.folio_venta_selected=self.tableventas.item(row,0).text()
            self.botonimprimir.setEnabled(True)
            print('Folio seleccionado: '+str(self.folio_venta_selected))
    def cancelar(self):
        if self.ventasview:
            self.close()
        else:
            self.ventasview=True
            self.tableventas.setColumnCount(9)
            index = self.tableventas.rowCount()
            for i in range(index):
                self.tableventas.removeRow(0)
            labels = ('ID', 'Usuario', 'Cliente', 'Tipo/venta','Metodo/pago','Fecha','Importe','Pago','Cambio')
            self.tableventas.setHorizontalHeaderLabels(labels)
            header = self.tableventas.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
            self.RefreshTableData()
    def doubleRowClicked(self):
        if self.ventasview:
            self.ventasview=False
            row=self.tableventas.currentRow()
            id_venta=self.tableventas.item(row,0).text()
            self.tableventas.setColumnCount(4)
            index=self.tableventas.rowCount()
            for i in range(index):
                self.tableventas.removeRow(0)
            labels=('Producto','Cantidad','Precio','Importe')
            self.tableventas.setHorizontalHeaderLabels(labels)
            productos=self.con.GetProductosVenta(id_venta)
            for i in range(len(productos)):
                self.tableventas.insertRow(i)
                self.tableventas.setItem(i, 0, QTableWidgetItem(str(productos[i]['producto'])))
                self.tableventas.setItem(i, 1, QTableWidgetItem(str(productos[i]['cantidad'])))
                self.tableventas.setItem(i, 2, QTableWidgetItem(str(productos[i]['precio'])))
                self.tableventas.setItem(i, 3, QTableWidgetItem(str(round(float(productos[i]['cantidad'])*float(productos[i]['precio']),2))))
            header = self.tableventas.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            self.botonimprimir.setEnabled(True)
    def RefreshTableData(self):
        date=self.fecha.date()
        mes=date.month()
        if mes<10:
            mes='0'+str(mes)
        dia=date.day()
        if dia<10:
            dia='0'+str(dia)
        ventas=self.con.VentasByDate(str(date.year())+'-'+str(mes)+'-'+str(dia) )
        index = self.tableventas.rowCount()
        for i in range(index):
            self.tableventas.removeRow(0)
        for i in range(len(ventas)):
            self.tableventas.insertRow(0)
            self.tableventas.setItem(0, 0, QTableWidgetItem(str(ventas[i]['id'])))
            self.tableventas.setItem(0, 1, QTableWidgetItem(str(ventas[i]['usuario'])))
            self.tableventas.setItem(0, 2, QTableWidgetItem(str(ventas[i]['cliente'])))
            self.tableventas.setItem(0, 3, QTableWidgetItem(str(ventas[i]['tipodeventa'])))
            self.tableventas.setItem(0, 4, QTableWidgetItem(str(ventas[i]['metododepago'])))
            self.tableventas.setItem(0, 5, QTableWidgetItem(str(ventas[i]['fecha'])))
            self.tableventas.setItem(0, 6, QTableWidgetItem(str(ventas[i]['importe'])))
            self.tableventas.setItem(0, 7, QTableWidgetItem(str(ventas[i]['pago'])))
            self.tableventas.setItem(0, 8, QTableWidgetItem(str(ventas[i]['cambio'])))
        self.botonimprimir.setEnabled(False)

if __name__=="__main__":

    from PyQt5.QtWidgets import QApplication
    from conexion import Conexion
    app = QApplication(sys.argv)
    gui = ViewHistorial(parametros={'conexion':Conexion()})
    gui.show()
    sys.exit(app.exec())