from PyQt5.QtWidgets import   QTableWidgetItem,QShortcut,QMainWindow,QHeaderView
from PyQt5.QtGui import QKeySequence
from PyQt5.uic import loadUi
from pymsgbox import *
from datetime import datetime
import sys
#QSlider.val
class ViewInventario(QMainWindow):
    formValid=False
    def __init__(self,parametros, *args, **kwargs):
        self.date = datetime.now()
        super(ViewInventario, self).__init__(*args, **kwargs)
        #todos los productos
        self.productos=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        #instanciamiento de mi clase Valida (sirve para validar cadenas)
        self.valida=parametros['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #bandera para saber cuando esta habilitada la opcion de editar un producto
        loadUi("inventarioUI.ui",self)
        #Inicialización para los eventos de los botones
        self.botoneditar.clicked.connect(self.edita)
        self.botoneditar.setDisabled(True)
        self.ayudaeditar.clicked.connect(self.ayudaEditar)
        self.botonsurtir.clicked.connect(self.surtir)
        self.botonsurtir.setDisabled(True)
        self.ayudasurtir.clicked.connect(self.ayudaSurtir)
        #los botones para las consultas de inventario
        self.botstockmin.clicked.connect(self.showStockMin)
        self.ayudastockminimo.clicked.connect(self.ayudaStockminimo)
        self.anterior.clicked.connect(self.ShowAnterior)
        self.siguiente.clicked.connect(self.ShowSiguiente)
        #Inicialización de los eventos para los inputs
        self.stockminimo.textChanged.connect(self.valStockminimo)
        self.stockminimo.returnPressed.connect(self.edita)
        self.stockmaximo.textChanged.connect(self.valStockmaximo)
        self.stockmaximo.returnPressed.connect(self.edita)
        self.stock.textChanged.connect(self.valStock)
        self.stock.returnPressed.connect(self.edita)
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.returnPressed.connect(self.enterBuscar)
        self.preciopublico.textChanged.connect(self.valPreciopublico)
        self.preciopublico.returnPressed.connect(self.surtir)
        self.cantidadadquirida.textChanged.connect(self.valCantidadadquirida)
        self.cantidadadquirida.returnPressed.connect(self.surtir)
        self.pagina.returnPressed.connect(self.ShowPage)
        self.pagina.textChanged.connect(self.valPagina)
        #Inicialización de los eventos de las tablas
        self.tablaproductos.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        tablaProductos = self.tablaproductos.horizontalHeader()
        tablaProductos.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(2, QHeaderView.Stretch)
        tablaProductos.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #lista de los inputs disponibles en la vista de productos
        self.inputs = [self.stockminimo,self.stockmaximo,self.stock]

        #Refrescamos por primera vez las tablas
        numproducts = self.con.GetNumProducts()
        pagina=1
        if numproducts!=0:
            pagina = int(numproducts / 50)
            if numproducts % 50 > 0:
                pagina += 1
        if pagina<=1:
            self.anterior.setEnabled(False)
        self.pagina.setText(str(pagina))
        self.total_paginas.setText(str(pagina))
        self.RefreshTableData()
        shortcut3 = QShortcut(QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut5 = QShortcut(QKeySequence("Esc"), self)
        shortcut5.activated.connect(self.close)

    def surtir(self):
        if self.valCantidadadquirida() and self.valPreciopublico():
            row=self.tablaproductos.currentRow()
            codigo=self.tablaproductos.item(row,0).text()
            opc = confirm(text="Desea surtir " +self.cantidadadquirida.text()+" productos?", title="Surtir?",
                          buttons=["OK", "CANCEL"])
            if opc=="OK":
                preciopublico=self.preciopublico.text()
                stock=str(float(self.tablaproductos.item(row,5).text())+float(self.cantidadadquirida.text()))
                if self.con.Surtir(codigo,preciopublico,stock):
                    #alert(title="Correcto",text="Operación exitosa")
                    self.clean()
                    self.botonsurtir.setDisabled(True)
                    self.botoneditar.setDisabled(True)
                    self.tablaproductos.setItem(row, 5, QTableWidgetItem(str(stock)))
                else:
                    alert(title="Error",text="Revise que el servidor XAMPP este activo")
        else:
            alert (title="Error",text="Revise el formulario")
    def edita(self):
        if not self.botoneditar.isEnabled():
            return False
        if self.valida_formulario():
            row = self.tablaproductos.currentRow()
            opc = confirm(text="Desea editar " + str(self.tablaproductos.item(row, 1).text()) + "?", title="Editar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                producto = {}
                producto['stockminimo'] = self.stockminimo.text()
                producto['stockmaximo'] = self.stockmaximo.text()
                producto['stock'] = self.stock.text()
                codigo = self.tablaproductos.item(row, 0).text()
                if self.con.UpdateInventario(codigo, producto) != False:
                    self.clean()
                    self.tablaproductos.setItem(row, 3, QTableWidgetItem(str(producto['stockminimo'])))
                    self.tablaproductos.setItem(row, 4, QTableWidgetItem(str(producto['stockmaximo'])))
                    self.tablaproductos.setItem(row, 5, QTableWidgetItem(str(producto['stock'])))
                    self.botoneditar.setDisabled(True)
                    self.botonsurtir.setDisabled(True)
                else:
                    alert(title="Error en el servidor!", text="Revise que el servidor XAMPP este activo",
                          button="OK")
        else:
            alert(title="Error en formulario!", text="Revise el formulario", button='OK')
    def rowClicked(self):
        try:
            row= self.tablaproductos.currentRow()
            producto=self.con.GetProductByCode(self.tablaproductos.item(row,0).text())
            self.preciopublico.setText(str(producto[0]['preciopublico']))
            self.stockminimo.setText(self.tablaproductos.item(row,3).text())
            self.stockmaximo.setText(self.tablaproductos.item(row,4).text())
            self.stock.setText(self.tablaproductos.item(row,5).text())
            self.botoneditar.setDisabled(False)
            self.botonsurtir.setDisabled(False)
        except:
            pass
    def valStockminimo(self):
        input = self.stockminimo
        res=True
        if len(str(input.text()))<12:
            res = self.valida.validaNumero(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            res=False
            input.setStyleSheet(self.falseValidate)
        return res
    def valStockmaximo(self):
        input = self.stockmaximo
        res = True
        if len(str(input.text())) < 20:
            res = self.valida.validaNumero(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            res = False
            input.setStyleSheet(self.falseValidate)
        return res
    def valStock(self):
        input = self.stock
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valCantidadadquirida(self):
        input = self.cantidadadquirida
        if input.text()=='':
            input.setStyleSheet(self.falseValidate)
            return False
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valPreciopublico(self):
        input = self.preciopublico
        if input.text()=='':
            input.setStyleSheet(self.falseValidate)
            return False
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valida_formulario(self):
        return(self.valStockminimo() and self.valStockmaximo() and self.valStock())
    def valPagina(self):
        input = self.pagina
        valida=False
        if len(input.text())>0:
            valida = self.valida.validaNumero(input.text())
        if valida:
            if int(input.text()) > 0 and int(input.text()) <= int(self.total_paginas.text()):
                input.setStyleSheet(self.trueValidate)
                return True
            else:
                input.setStyleSheet(self.falseValidate)
                return False
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def RefreshTableData(self):
        page = int(self.pagina.text())
        self.productos = self.con.GetPageProducts(page)
        productos = self.productos
        if productos != False:
            rowCount = self.tablaproductos.rowCount()
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(productos)):
                self.tablaproductos.insertRow(0)
                self.tablaproductos.setItem(0, 0, QTableWidgetItem(str(productos[i]['codigo'])))
                self.tablaproductos.setItem(0, 1, QTableWidgetItem(str(productos[i]['producto'])))
                self.tablaproductos.setItem(0, 2, QTableWidgetItem(str(productos[i]['grupo'])))
                self.tablaproductos.setItem(0, 3, QTableWidgetItem(str(productos[i]['stockminimo'])))
                self.tablaproductos.setItem(0, 4, QTableWidgetItem(str(productos[i]['stockmaximo'])))
                self.tablaproductos.setItem(0, 5, QTableWidgetItem(str(productos[i]['stock'])))
            if int(self.pagina.text())<=1 and self.total_paginas.text()=='1':
                self.anterior.setEnabled(False)
                self.siguiente.setEnabled(False)
            elif int(self.pagina.text())<=1:
                self.anterior.setEnabled(False)
                self.siguiente.setEnabled(True)
            elif int(self.pagina.text())==int(self.total_paginas.text()) and int(self.pagina.text())>1:
                self.siguiente.setEnabled(False)
                self.anterior.setEnabled(True)
            else:
                self.siguiente.setEnabled(True)
                self.anterior.setEnabled(True)

        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def ShowSiguiente(self):
        self.anterior.setEnabled(True)
        pagina=int(self.pagina.text())+1
        self.pagina.setText(str(pagina))
        if pagina==int(self.total_paginas.text()):
            self.siguiente.setEnabled(False)
        self.RefreshTableData()
        self.clean()
    def ShowAnterior(self):
        self.siguiente.setEnabled(True)
        pagina = int(self.pagina.text()) - 1
        self.pagina.setText(str(pagina))
        if pagina ==1:
            self.anterior.setEnabled(False)
        self.RefreshTableData()
        self.clean()
    def ShowPage(self):
        input = self.pagina
        valida=self.valPagina()
        if valida:
            if input.text()==self.total_paginas.text():
                self.siguiente.setEnabled(False)
                self.anterior.setEnabled(True)
            elif input.text()=='1':
                self.anterior.setEnabled(False)
                self.siguiente.setEnabled(True)
            else:
                self.anterior.setEnabled(True)
                self.siguiente.setEnabled(True)
            self.RefreshTableData()
            self.clean()
        else:
            input.setText(str(self.total_paginas.text()))
            self.anterior.setEnabled(True)
            self.siguiente.setEnabled(False)

    def clean(self):
        #esta funcion es para limpiar el formulario
        self.stockminimo.setText('0')
        self.stockmaximo.setText('0')
        self.stock.setText('0')
        self.preciopublico.setText('')
        self.cantidadadquirida.setText('')
        self.botoneditar.setEnabled(False)
        self.botonsurtir.setEnabled(False)
    def showStockMin(self):
        productos = self.con.AllStockMinimo()
        self.clean()
        if self.productos != False:
            rowCount = self.tablaproductos.rowCount()
            self.tablaproductos.clearContents()
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(productos)):
                self.tablaproductos.insertRow(i)
                self.tablaproductos.setItem(i, 0, QTableWidgetItem(str(productos[i]['codigo'])))
                self.tablaproductos.setItem(i, 1, QTableWidgetItem(str(productos[i]['producto'])))
                self.tablaproductos.setItem(i, 2, QTableWidgetItem(str(productos[i]['grupo'])))
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(productos[i]['stockminimo'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(productos[i]['stockmaximo'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(productos[i]['stock'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def ayudaSurtir(self):
        alert(title="Ayuda", text="Para surtir un producto del proveedor:\n"
                                  "1.- Seleccione el producto a surtir en la tabla \n"
                                  "2.- Ingrese los datos solicitados (precio de \ncompra y cantidad adquirida)\n"
                                  "3.- Hacer click en el boton 'surtir'" )
    def ayudaStockminimo(self):
        alert(title="ayuda",text="Muestra todos los productos que estan por debajo del stock mínimo")
    def ayudaEditar(self):
        alert(title="Ayuda",text="Para editar la información de un proveedor: \n"
                                 "1.- Seleccione el proveedor a editar en la tabla \n"
                                 "2.- Modifique los datos"
                                 "3.- Hacer click en el boton 'Editar' o precionar 'Ctrl + e'",button=
              "OK")
    def buscar(self):
        if self.busqueda.text()!="" and len(self.busqueda.text())>3:
            busqueda=self.busqueda.text()
            coincidencias=self.con.FindProducts(busqueda)
            rowCount = self.tablaproductos.rowCount()
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(coincidencias)):
                self.tablaproductos.insertRow(i)
                self.tablaproductos.setItem(i, 0, QTableWidgetItem(str(coincidencias[i]['codigo'])))
                self.tablaproductos.setItem(i, 1, QTableWidgetItem(str(coincidencias[i]['producto'])))
                self.tablaproductos.setItem(i, 2, QTableWidgetItem(str(coincidencias[i]['grupo'])))
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(coincidencias[i]['stockminimo'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(coincidencias[i]['stockmaximo'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(coincidencias[i]['stock'])))
            self.clean()
        elif len(self.busqueda.text())<4 and self.busqueda.text()!='':
            pass
        else:
            self.RefreshTableData()
            self.clean()
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from validaciones import Valida
    from conexion import Conexion
    parametros={'conexion':Conexion(),'valida':Valida()}
    app = QApplication(sys.argv)
    gui = ViewInventario(parametros)
    gui.show()
    sys.exit(app.exec())

