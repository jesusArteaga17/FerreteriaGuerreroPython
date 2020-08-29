from PyQt5.QtWidgets import  QApplication, QDialog,QTableWidgetItem,QShortcut
from PyQt5 import uic,QtWidgets,QtGui
from validaciones import Valida
from conexion import *
from pymsgbox import *
from datetime import datetime
import sys
class ViewProductos(QDialog):
    formValid=False
    def __init__(self, *args, **kwargs):
        super(ViewProductos, self).__init__(*args, **kwargs)
        #todos los productos
        self.productos=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=Conexion()
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #bandera para saber cuando esta habilitada la opcion de editar un producto
        #instanciamiento de mi clase Valida
        self.valida=Valida()
        uic.loadUi("productos.ui",self)
        #Inicialización para los eventos de los botones
        self.botonagregar.clicked.connect(self.agrega)
        self.botoneditar.clicked.connect(self.edita)
        self.botoneliminar.clicked.connect(self.elimina)
        self.botonayudaadd.clicked.connect(self.ayudaAgregar)
        self.botonayudaedit.clicked.connect(self.ayudaeditar)
        self.botonayudadelete.clicked.connect(self.ayudaeliminar)
        self.botonbuscar.clicked.connect(self.enterBuscar)
        #Inicialización de los eventos para los inputs
        self.codigo.textChanged.connect(self.valCodigo)
        self.codigo.returnPressed.connect(self.agrega)
        self.producto.textChanged.connect(self.valProducto)
        self.producto.returnPressed.connect(self.agrega)
        self.descuento.textChanged.connect(self.valDescuento)
        self.descuento.returnPressed.connect(self.agrega)
        self.incremento.textChanged.connect(self.valIncremento)
        self.incremento.returnPressed.connect(self.agrega)
        self.preciocompra.textChanged.connect(self.valPreciocompra)
        self.preciocompra.returnPressed.connect(self.agrega)
        self.existencia.textChanged.connect(self.valExistencia)
        self.existencia.returnPressed.connect(self.agrega)
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.setFocus()
        #Inicialización de los eventos de la tabla
        self.tablaproductos.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        header = self.tablaproductos.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        #lista de los inputs disponibles en la vista de productos
        self.inputs = [self.codigo, self.producto, self.grupo, self.descuento, self.incremento,self.preciocompra,self.existencia]
        self.RefreshTableData()
        #Definiendo los atajos
        shortcut1 = QShortcut(QtGui.QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        shortcut3 = QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QtGui.QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.elimina)
        shortcut5 = QShortcut(QtGui.QKeySequence("Esc"), self)
        shortcut5.activated.connect(self.close)
    def agrega(self):
        if self.valida_formulario("agrega"):
            opc = confirm(text="Desea agregar " + str(self.producto.text()) + "?", title="Agregar)",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                producto = {}
                producto['codigo'] = self.codigo.text()
                producto['producto'] = self.producto.text()
                producto['grupo'] = self.grupo.text()
                producto['descuento'] = self.descuento.text()
                producto['incremento'] = self.incremento.text()
                producto['preciocompra'] = self.preciocompra.text()
                producto['existencia'] = self.existencia.text()
                preciopublico=float(self.preciocompra.text())+float(self.preciocompra.text())*(float(self.incremento.text())/100)
                producto['preciopublico'] = str(preciopublico -float(self.descuento.text())/100*preciopublico)
                if self.codigo.text() != "":
                    productoexist = self.con.GetProductByCode(self.codigo.text())
                    if productoexist != False:
                        if len(productoexist) == 0:
                            if self.con.AddProduct(producto)!=False:
                                for i in range(len(self.inputs)):
                                    self.inputs[i].setText("")
                                self.RefreshTableData()
                                self.RefreshTableStockmin()
                                alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
                            else:
                                alert(title="Error de servidor",text="Ocurrió un error en el servidor",button="OK")
                        else:
                            alert(text='El código que ingresó ya existe', title='Código existente!', button='OK')
                    else:
                        alert(text="Revisa que el servidor XAMPP este activado", title="Error de servidor!",
                              button="OK")
                else:
                    id = self.con.AddProduct(producto)
                    if id!=False:
                        now = datetime.now()
                        second = str(now.second)
                        micro = str(now.microsecond)[3]
                        newcode = str(id) + second + micro
                        self.con.UpdateCodigoProduct(id, newcode)
                        rowPosition = self.tablaproductos.rowCount()
                        self.tablaproductos.insertRow(rowPosition)
                        self.tablaproductos.setItem(rowPosition, 0, QTableWidgetItem(newcode))
                        self.tablaproductos.setItem(rowPosition, 1, QTableWidgetItem(producto["producto"]))
                        self.tablaproductos.setItem(rowPosition, 2, QTableWidgetItem(producto["grupo"]))
                        self.tablaproductos.setItem(rowPosition, 3, QTableWidgetItem(producto["descuento"]))
                        self.tablaproductos.setItem(rowPosition, 4, QTableWidgetItem(producto["incremento"]))
                        self.tablaproductos.setItem(rowPosition, 5, QTableWidgetItem(producto["preciocompra"]))
                        self.tablaproductos.setItem(rowPosition, 6, QTableWidgetItem(producto["preciopublico"]))
                        for i in range(len(self.inputs)):
                            self.inputs[i].setText("")
                        self.RefreshTableStockmin()
                        alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
                    else:
                        alert(title="Error en servidor!", text="Revise que el servidor XAMPP este activo", button="OK")
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def edita(self):
        if self.valida_formulario("edita"):
            try:
                row = self.tablaproductos.currentRow()
                opc=confirm(text="Desea editar "+str(self.tablaproductos.item(row,1).text())+"?",title="Editar?",buttons=["OK","CANCEL"])
                if opc=="OK":
                    codigo_ant=self.tablaproductos.item(row, 0).text()
                    producto = {}
                    producto['codigo'] = self.codigo.text()
                    producto['producto'] = self.producto.text()
                    producto['grupo'] = self.grupo.text()
                    producto['descuento'] = self.descuento.text()
                    producto['incremento'] = self.incremento.text()
                    producto['preciocompra'] = self.preciocompra.text()
                    producto['existencia'] = self.existencia.text()
                    preciopublico = float(self.preciocompra.text()) + float(self.preciocompra.text()) * (
                    float(self.incremento.text()) / 100)
                    producto['preciopublico'] = str(preciopublico - float(self.descuento.text()) / 100 * preciopublico)
                    if self.codigo.text()!=codigo_ant:
                        productexist = self.con.GetProductByCode(self.codigo.text())
                        if productexist != False:
                            if len(productexist) == 0:
                                self.con.UpdateProduct(codigo_ant, producto)
                                self.RefreshTableData()
                                self.RefreshTableStockmin()
                                for i in range(len(self.inputs)):
                                    self.inputs[i].setText("")
                            else:
                                alert(title="Código en uso!", text="El codigo que ingresó ya existe", button="OK")
                        else:
                            alert(title="Error en el servidor!", text="Revise que el servidor XAMPP este activo",
                                  button="OK")
                    else:
                        if self.con.UpdateProduct(codigo_ant,producto)!=False:
                            self.RefreshTableData()
                            self.RefreshTableStockmin()
                            for i in range(len(self.inputs)):
                                self.inputs[i].setText("")
                        else:
                            alert(title="Error en el servidor!",text="Revise que el servidor XAMPP este activo",button="OK")
            except:
                alert(title="Error!",text="Primero debes seleccionar una fila en la tabla", button='OK')
        else:
            alert(title="Error en formulario!", text="Revise el formulario", button='OK')
    def elimina(self):
        try:
            row = self.tablaproductos.currentRow()
            opc=confirm(text="Desea Eliminar "+str(self.tablaproductos.item(row,1).text())+"?",title="Eliminar??",buttons=["OK","CANCEL"])
            if opc=="OK":
                codigo=self.tablaproductos.item(row, 0).text()
                if self.con.DeleteProduct(codigo)!=False:
                    alert(title="Listo!",text="Se eliminó correctamente",button="OK")
                    for i in range(len(self.inputs)):
                        self.inputs[i].setText("")
                    try:
                        self.RefreshTableData()
                    except:
                        print ("Hubo un error")

                else:
                    alert(title="Error en el servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")

        except:
            alert(title="Error!",text="Primero debes seleccionar una fila en la tabla", button='OK')
    def rowClicked(self):
        try:
            row= self.tablaproductos.currentRow()
            #col=self.tablaproductos.currentColumn()
            for i in range(len(self.inputs)-1):
                self.inputs[i].setText(self.tablaproductos.item(row,i).text())
            self.inputs[-1].setText(str(self.productos[row]["existencia"]))
        except:
            pass
    def valida_formulario(self,accion):
        if accion=="agrega":
            if self.codigo.text()!="":
                if self.valCodigo()and  self.valDescuento() and self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
            else:
                if self.valDescuento() and self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
        else:
            if self.codigo.text()!="":
                if self.valCodigo() and self.valDescuento() and self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
            else:
                return False
    def valCodigo(self):
        input=self.codigo
        res=self.valida.validaNumero(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valProducto(self):
        input = self.producto
        if input.text()!="":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valDescuento(self):
        input = self.descuento
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valStockminimo(self):
        input = self.stockminimo
        res = self.valida.validaNumero(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valStockmaximo(self):
        input = self.stockmaximo
        res = self.valida.validaNumero(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valExistencia(self):
        input = self.existencia
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valPrecio(self):
        input = self.precio
        res = self.valida.validaDecimal(input.text())
        if res:
            input.setStyleSheet(self.trueValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valIncremento(self):
        input = self.incremento
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
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(productos[i]['descuento'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(productos[i]['incremento'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(productos[i]['preciocompra'])))
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(productos[i]['preciopublico'])))
            self.RefreshTableStockmin()
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def RefreshTableStockmin(self):
        self.tablestockminimo.clearContents()
        productos = self.con.AllStockMinimo()
        rowCount=self.tablestockminimo.rowCount()
        for i in range(rowCount):
            self.tablestockminimo.removeRow(0)
        for i in range(len(productos)):
            self.tablestockminimo.insertRow(i)
            self.tablestockminimo.setItem(i, 0, QTableWidgetItem(str(productos[i]['producto'])))
            self.tablestockminimo.setItem(i, 1, QTableWidgetItem(str(productos[i]['stockminimo'])))
            self.tablestockminimo.setItem(i, 2, QTableWidgetItem(str(productos[i]['existencia'])))
    def ayudaAgregar(self):
        alert(title="Ayuda",text="Para agregar un producto \n"
                                 "1.- Llenar el formulario (basta con agregar solo el producto\n"
                                 "2.- Hacer click en el boton 'Agregar', precionar 'Enter' o precionar 'Ctrl + a'",button="OK")
    def ayudaeditar(self):
        alert(title="Ayuda",text="Para editar la información de un producto: \n"
                                 "1.- Seleccione el producto a editar en la tabla \n"
                                 "2.- Modifique los datos"
                                 "3.- Hacer click en el boton 'Editar' o precionar 'Ctrl + e'",button=
              "OK")
    def ayudaeliminar(self):
        alert(title="Ayuda",text="Para eliminar un producto: \n"
                                 "1.- Seleccione el producto a eliminar de la tabla \n"
                                 "2.- Hacer click en el boton 'Eliminar' o precionar 'Ctrl + d'")
    def buscar(self):
        if self.busqueda.text()!="":
            coincidencias=[]
            for j in range(1,4):
                keys=[]
                busqueda=self.busqueda.text().lower()
                for i in range(len(self.productos)):
                    producto=list(self.productos[i].values())
                    keys.append(str(producto[j]).lower())
                for i in range(len(keys)):
                    if keys[i].find(busqueda)!=-1:
                        if i not in coincidencias:
                            coincidencias.append(i)
                for i in range(self.tablaproductos.rowCount()):
                    self.tablaproductos.removeRow(0)
            for i in range(len(coincidencias)):
                self.tablaproductos.insertRow(i)
                self.tablaproductos.setItem(i, 0, QTableWidgetItem(str(self.productos[coincidencias[i]]['codigo'])))
                self.tablaproductos.setItem(i, 1, QTableWidgetItem(str(self.productos[coincidencias[i]]['producto'])))
                self.tablaproductos.setItem(i, 2, QTableWidgetItem(str(self.productos[coincidencias[i]]['grupo'])))
                self.tablaproductos.setItem(i, 3, QTableWidgetItem(str(self.productos[coincidencias[i]]['descuento'])))
                self.tablaproductos.setItem(i, 4, QTableWidgetItem(str(self.productos[coincidencias[i]]['incremento'])))
                self.tablaproductos.setItem(i, 5, QTableWidgetItem(str(self.productos[coincidencias[i]]['preciocompra'])))
                self.tablaproductos.setItem(i, 6, QTableWidgetItem(str(self.productos[coincidencias[i]]['preciopublico'])))
        else:
            self.RefreshTableData()
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()
if __name__=="__main__":
    app = QApplication(sys.argv)
    gui = ViewProductos()
    gui.show()
    sys.exit(app.exec())