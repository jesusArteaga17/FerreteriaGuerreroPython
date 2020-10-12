from PyQt5.QtWidgets import  QApplication, QDialog,QTableWidgetItem,QSlider
from PyQt5 import uic,QtWidgets
from validaciones import Valida
from conexion import *
from pymsgbox import *
from datetime import datetime
import sys
#QSlider.val
class ViewInventario(QDialog):
    formValid=False
    def __init__(self, *args, **kwargs):
        self.date = datetime.now()
        super(ViewInventario, self).__init__(*args, **kwargs)
        #todos los productos
        self.productos=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=Conexion()
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #bandera para saber cuando esta habilitada la opcion de editar un producto
        #instanciamiento de mi clase Valida (sirve para validar cadenas)
        self.valida=Valida()
        uic.loadUi("inventarioUI.ui",self)
        #Inicialización para los eventos de los botones
        self.botoneditar.clicked.connect(self.edita)
        self.botoneditar.setDisabled(True)
        self.ayudaeditar.clicked.connect(self.ayudaEditar)
        self.botonsurtirstock.clicked.connect(self.surtirStock)
        self.botonsurtirstock.setDisabled(True)
        self.ayudasurtirstock.clicked.connect(self.ayudaSurtirStock)
        self.botonsurtir.clicked.connect(self.surtir)
        self.botonsurtir.setDisabled(True)
        self.ayudasurtir.clicked.connect(self.ayudaSurtir)
        #los botones para las consultas de inventario
        self.botstockmin.clicked.connect(self.showStockMin)
        self.ayudastockminimo.clicked.connect(self.ayudaStockminimo)
        self.botbodega.clicked.connect(self.showBodega)
        self.ayudabodega.clicked.connect(self.ayudaBodega)
        self.botontodos.clicked.connect(self.RefreshTableData)
        self.ayudatodos.clicked.connect(self.ayudaTodos)
        #Inicialización de los eventos para los inputs
        self.stockminimo.textChanged.connect(self.valStockminimo)
        self.stockminimo.returnPressed.connect(self.edita)
        self.stockmaximo.textChanged.connect(self.valStockmaximo)
        self.stockmaximo.returnPressed.connect(self.edita)
        self.stock.textChanged.connect(self.valStock)
        self.stock.returnPressed.connect(self.edita)
        self.bodega.textChanged.connect(self.valBodega)
        self.bodega.returnPressed.connect(self.edita)
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.returnPressed.connect(self.enterBuscar)

        self.preciocompra.textChanged.connect(self.valPreciocompra)
        self.preciocompra.returnPressed.connect(self.surtir)
        self.cantidadadquirida.textChanged.connect(self.valCantidadadquirida)
        self.cantidadadquirida.returnPressed.connect(self.surtir)
        #Inicialización de los eventos de las tablas
        self.tablaproductos.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        tablaProductos = self.tablaproductos.horizontalHeader()
        tablaProductos.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        tablaProductos.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        tablaProductos.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        #lista de los inputs disponibles en la vista de productos
        self.inputs = [self.stockminimo,self.stockmaximo,self.stock,self.bodega]
        #desactivamos el slider
        self.horizontalSlider.valueChanged.connect(self.mandaBodega)
        self.horizontalSlider.setDisabled(True)

        #Refrescamos por primera vez las tablas
        self.RefreshTableData()
        """
        shortcut1 = QShortcut(QtGui.QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        shortcut3 = QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QtGui.QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.elimina)
        shortcut5 = QShortcut(QtGui.QKeySequence("Esc"), self)
        shortcut5.activated.connect(self.close)"""
    def mandaBodega(self):
        slider=int(self.horizontalSlider.value())
        self.labelbodega.setText("En bodega: " + str(self.cantidad_bodega-slider))
        self.labelstock.setText("En stock: " + str(self.cantidad_stock+slider))
        self.labelcantidad.setText('Cantidad: '+str(slider))
    def surtirStock(self):
        slider = int(self.horizontalSlider.value())
        opc=confirm(text="Desea surtir " +str(slider)+ " en stock?", title="Surtir?",
                buttons=["OK", "CANCEL"])
        if opc=="OK":
            row=self.tablaproductos.currentRow()
            bodega=self.cantidad_bodega - slider
            stock=self.cantidad_stock + slider
            codigo=self.tablaproductos.item(row,0).text()
            if self.con.SurtirStock(codigo,stock,bodega):
                alert(text="Operación exitosa",title="Correcto")
                self.clean()
                self.horizontalSlider.setDisabled(True)
                self.botonsurtir.setDisabled(True)
                self.botonsurtirstock.setDisabled(True)
                self.botoneditar.setDisabled(True)
                self.RefreshTableData()
            else:
                alert(title="Error",text="Hubo algún error")
    def surtir(self):
        if self.valCantidadadquirida() and self.valPreciocompra():
            row=self.tablaproductos.currentRow()
            codigo=self.tablaproductos.item(row,0).text()
            opc = confirm(text="Desea surtir " +self.cantidadadquirida.text()+" productos?", title="Surtir?",
                          buttons=["OK", "CANCEL"])
            if opc=="OK":
                if self.con.Surtir(codigo,preciocompra=self.preciocompra.text(),bodega=str(float(self.tablaproductos.item(row,6).text())+float(self.cantidadadquirida.text()))):
                    alert(title="Correcto",text="Operación exitosa")
                    self.clean()
                    self.horizontalSlider.setDisabled(True)
                    self.botonsurtir.setDisabled(True)
                    self.botonsurtirstock.setDisabled(True)
                    self.botoneditar.setDisabled(True)
                    self.RefreshTableData()
                else:
                    alert(title="Error",text="Revise que el servidor XAMPP este activo")
        else:
            alert (title="Error",text="Revise el formulario")
    def edita(self):
        if self.valida_formulario():
            row = self.tablaproductos.currentRow()
            opc = confirm(text="Desea editar " + str(self.tablaproductos.item(row, 1).text()) + "?", title="Editar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                producto = {}
                producto['stockminimo'] = self.stockminimo.text()
                producto['stockmaximo'] = self.stockmaximo.text()
                producto['stock'] = self.stock.text()
                producto['bodega']=self.bodega.text()
                codigo = self.tablaproductos.item(row, 0).text()
                if self.con.UpdateInventario(codigo, producto) != False:
                    self.clean()
                    self.RefreshTableData()
                    self.botoneditar.setDisabled(True)
                    self.botonsurtirstock.setDisabled(True)
                    self.botonsurtir.setDisabled(True)
                    self.horizontalSlider.setDisabled(True)
                else:
                    alert(title="Error en el servidor!", text="Revise que el servidor XAMPP este activo",
                          button="OK")
        else:
            alert(title="Error en formulario!", text="Revise el formulario", button='OK')
    def rowClicked(self):
        try:
            row= self.tablaproductos.currentRow()
            #col=self.tablaproductos.currentColumn()
            self.stockminimo.setText(self.tablaproductos.item(row,3).text())
            self.stockmaximo.setText(self.tablaproductos.item(row,4).text())
            self.stock.setText(self.tablaproductos.item(row,5).text())
            self.bodega.setText(self.tablaproductos.item(row,6).text())
            self.botoneditar.setDisabled(False)
            self.botonsurtir.setDisabled(False)
            self.cantidad_bodega=float(self.tablaproductos.item(row,6).text())
            self.cantidad_stock=float(self.tablaproductos.item(row,5).text())
            if self.cantidad_bodega>0:
                self.botonsurtirstock.setDisabled(False)
                self.horizontalSlider.setDisabled(False)
                self.horizontalSlider.setRange(0,int(self.cantidad_bodega))
                self.labelmaximun.setText(str(int(self.cantidad_bodega)))
                self.labelbodega.setText("En bodega: "+str(int(self.cantidad_bodega)))
                self.labelstock.setText("En stock: "+str(self.cantidad_stock))
            else:
                self.botonsurtirstock.setDisabled(True)
                self.horizontalSlider.setDisabled(True)
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
        if len(str(input.text())) < 12:
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
    def valBodega(self):
        input = self.bodega
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valCantidadadquirida(self):
        input = self.cantidadadquirida
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valPreciocompra(self):
        input = self.preciocompra
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valida_formulario(self):
        if self.valStockminimo() and self.valStockmaximo() and self.valStock() and self.valBodega():
            return True
        else:
            return False
    def RefreshTableData(self):
        self.productos=self.con.AllProducts()
        if self.productos!=False:
            rowCount=self.tablaproductos.rowCount()
            self.tablaproductos.clearContents()
            productos=self.productos
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(productos)):
                self.tablaproductos.insertRow(i)
                self.tablaproductos.setItem(i,0, QTableWidgetItem( str(productos[i]['codigo'])))
                self.tablaproductos.setItem(i, 1, QTableWidgetItem(str(productos[i]['producto'])))
                self.tablaproductos.setItem(i, 2, QTableWidgetItem(str(productos[i]['grupo'])))
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(productos[i]['stockminimo'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(productos[i]['stockmaximo'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(productos[i]['stock'])))
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(productos[i]['bodega'])))
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def clean(self):
        #for i in len(self.inputs):
            #self.inputs[i].setText('')
        self.preciocompra.setText('')
        self.cantidadadquirida.setText('')
        self.labelmaximun.setText("0")
        self.labelbodega.setText('En bodega:')
        self.labelstock.setText('En stock:')
        self.labelcantidad.setText('Cantidad:')
        self.horizontalSlider.setValue(0)
    def showStockMin(self):
        productos = self.con.AllStockMinimo()
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
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(productos[i]['bodega'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def showBodega(self):
        productos = self.con.AllBodega()
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
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(productos[i]['bodega'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def ayudaSurtirStock(self):
        alert(title="Ayuda", text="Proceso por el cual se lleva una cantidad de producto\nde la bodega a Stock\n"
                                  "1.-Seleccione el producto en la tabla.\n"
                                  "2.-Deslice la barra de la derecha hasta obtener\n"
                                  "la cantidad deseada.\n"
                                  "3.-Hacer click en el boton'Surtir stock'")
    def ayudaSurtir(self):
        alert(title="Ayuda", text="Para surtir un producto del proveedor:\n"
                                  "1.- Seleccione el producto a surtir en la tabla \n"
                                  "2.- Ingrese los datos solicitados (precio de \ncompra y cantidad adquirida)\n"
                                  "3.- Hacer click en el boton 'surtir'" )
    def ayudaStockminimo(self):
        alert(title="ayuda",text="Muestra todos los productos que estan por debajo del stock mínimo")
    def ayudaBodega(self):
        alert(title="Ayuda",text="Muestra todos los productos que se encuentran \nen cantidad bajos y que posiblemente necesiten\nser surtidos")
    def ayudaTodos(self):
        alert(title="Ayuda",text="Muestra todos los produtos registrados")
    def ayudaEditar(self):
        alert(title="Ayuda",text="Para editar la información de un proveedor: \n"
                                 "1.- Seleccione el proveedor a editar en la tabla \n"
                                 "2.- Modifique los datos"
                                 "3.- Hacer click en el boton 'Editar' o precionar 'Ctrl + e'",button=
              "OK")
    def buscar(self):
        if self.busqueda.text()!="":
            coincidencias=[]
            keys=[]
            busqueda=self.busqueda.text().lower()
            for i in range(len(self.productos)):
                keys.append([])
                producto=list(self.productos[i].values())
                for j in range(len(producto)):
                    keys[i].append(str(producto[j]).lower())
                for j in range(len(keys[i])):
                    if keys[i][j].find(busqueda)!=-1:
                        if i not in coincidencias:
                            coincidencias.append(i)
            for i in range(self.tablaproductos.rowCount()):
                self.tablaproductos.removeRow(0)
            for i in range(len(coincidencias)):
                self.tablaproductos.insertRow(i)
                self.tablaproductos.setItem(i, 0, QTableWidgetItem(str(self.productos[coincidencias[i]]['codigo'])))
                self.tablaproductos.setItem(i, 1, QTableWidgetItem(str(self.productos[coincidencias[i]]['producto'])))
                self.tablaproductos.setItem(i, 2, QTableWidgetItem(str(self.productos[coincidencias[i]]['grupo'])))
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(self.productos[coincidencias[i]]['stockminimo'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(self.productos[coincidencias[i]]['stockmaximo'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(self.productos[coincidencias[i]]['stock'])))
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(self.productos[coincidencias[i]]['bodega'])))

        else:
            self.RefreshTableData()
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()

if __name__=="__main__":
    app = QApplication(sys.argv)
    gui = ViewInventario()
    gui.show()
    sys.exit(app.exec())

