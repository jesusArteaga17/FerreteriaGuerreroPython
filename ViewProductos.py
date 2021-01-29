from PyQt5.QtWidgets import  QApplication,QTableWidgetItem,QShortcut,QMainWindow
from PyQt5 import uic,QtWidgets,QtGui
from pymsgbox import *
from datetime import datetime
import sys

class ViewProductos(QMainWindow):
    formValid=False
    def __init__(self,parametros={}, *args, **kwargs):
        super(ViewProductos, self).__init__(*args, **kwargs)
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        #instanciamiento de mi clase Valida
        self.valida=parametros['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #Declaramos la variable de productos
        self.productos=[]
        uic.loadUi("productos.ui",self)
        #Inicialización para los eventos de los botones
        self.botonagregar.clicked.connect(self.agrega)
        self.botoneditar.clicked.connect(self.edita)
        self.botoneliminar.clicked.connect(self.elimina)
        self.botonayudaadd.clicked.connect(self.ayudaAgregar)
        self.botonayudaedit.clicked.connect(self.ayudaeditar)
        self.botonayudadelete.clicked.connect(self.ayudaeliminar)
        self.botonbuscar.clicked.connect(self.enterBuscar)
        self.anterior.clicked.connect(self.ShowAnterior)
        self.siguiente.clicked.connect(self.ShowSiguiente)
        #Inicialización de los eventos para los inputs
        self.codigo.textChanged.connect(self.valCodigo)
        self.codigo.returnPressed.connect(self.agrega)
        self.producto.textChanged.connect(self.valProducto)
        self.producto.returnPressed.connect(self.agrega)
        self.grupo.textChanged.connect(self.validaGrupo)
        self.grupo.returnPressed.connect(self.agrega)
        self.utilidades.textChanged.connect(self.valIncremento)
        self.utilidades.returnPressed.connect(self.agrega)
        self.preciocompra.textChanged.connect(self.valPreciocompra)
        self.preciocompra.returnPressed.connect(self.agrega)
        self.stock.textChanged.connect(self.valExistencia)
        self.stock.returnPressed.connect(self.agrega)
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.setFocus()
        self.pagina.returnPressed.connect(self.ShowPage)
        self.pagina.textChanged.connect(self.valPagina)
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
        #lista de los inputs disponibles en la vista de productos
        self.inputs = [self.codigo, self.producto, self.grupo, self.utilidades,self.preciocompra,self.stock]
        #hacemos la paginacion de la tabla
        numproducts = self.con.GetNumProducts()
        pagina = 1
        if numproducts != 0:
            pagina = int(numproducts / 50)
            if numproducts % 50 > 0:
                pagina += 1
        if pagina<=1:
            self.anterior.setEnabled(False)
        self.pagina.setText(str(pagina))
        self.total_paginas.setText(str(pagina))
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
            opc = confirm(text="Desea agregar " + str(self.producto.text()) + "?", title="Agregar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                producto = {}
                producto['codigo'] = self.codigo.text()
                producto['producto'] = self.producto.text()
                producto['grupo'] = self.grupo.text()
                if self.utilidades.text()!="":
                    producto['utilidades'] = self.utilidades.text()
                else:
                    producto['utilidades']="0"
                if self.preciocompra.text()!="":
                    producto['preciocompra'] = self.preciocompra.text()
                else:
                    producto['preciocompra']="0"
                if self.stock.text()!="":
                    producto['stock'] = self.stock.text()
                else:
                    producto['stock']="0"
                producto['preciopublico'] =str(float(producto["preciocompra"])+float(producto["utilidades"]))
                if self.codigo.text() != "":
                    productoexist = self.con.GetProductByCode(self.codigo.text())
                    if productoexist != False:
                        if len(productoexist) == 0:
                            if self.con.AddProduct(producto)!=False:
                                for i in range(len(self.inputs)):
                                    self.inputs[i].setText("")
                                #Actualizamos los datos de la paginacion a ultima pagina
                                numproducts = self.con.GetNumProducts()
                                pagina = int(numproducts / 50)
                                if numproducts % 50 > 0:
                                    pagina += 1
                                self.pagina.setText(str(pagina))
                                self.total_paginas.setText(str(pagina))
                                self.RefreshTableData()
                                self.RefreshTableStockmin()
                                self.siguiente.setEnabled(False)
                                self.botoneditar.setEnabled(False)
                                self.botoneliminar.setEnabled(False)
                                #alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
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
                        numproducts = self.con.GetNumProducts()
                        pagina = int(numproducts / 50)
                        if numproducts % 50 > 0:
                            pagina += 1
                        self.pagina.setText(str(pagina))
                        self.total_paginas.setText(str(pagina))
                        self.RefreshTableData()
                        for i in range(len(self.inputs)):
                            self.inputs[i].setText("")
                        self.RefreshTableStockmin()
                        self.siguiente.setEnabled(False)
                        self.botoneditar.setEnabled(False)
                        self.botoneliminar.setEnabled(False)
                        #alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
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
                    #recojemos los datos del formulario
                    codigo_ant=self.tablaproductos.item(row, 0).text()
                    producto = {}
                    producto['codigo'] = self.codigo.text()
                    producto['producto'] = self.producto.text()
                    producto['grupo'] = self.grupo.text()
                    producto['utilidades'] = self.utilidades.text()
                    producto['preciocompra'] = self.preciocompra.text()
                    producto['stock'] = self.stock.text()
                    producto['preciopublico'] = str(float(producto["preciocompra"])+float(producto["utilidades"]))
                    if self.codigo.text()!=codigo_ant:
                        productexist = self.con.GetProductByCode(self.codigo.text())
                        if productexist != False:
                            if len(productexist) == 0:
                                self.con.UpdateProduct(codigo_ant, producto)
                                index=self.tablaproductos.currentRow()
                                self.tablaproductos.setItem(index, 0, QTableWidgetItem(str(producto['codigo'])))
                                self.tablaproductos.setItem(index, 1, QTableWidgetItem(str(producto['producto'])))
                                self.tablaproductos.setItem(index, 2, QTableWidgetItem(str(producto['grupo'])))
                                self.tablaproductos.setItem(index, 3, QTableWidgetItem(str(producto['utilidades'])))
                                self.tablaproductos.setItem(index, 4, QTableWidgetItem(str(producto['preciocompra'])))
                                self.tablaproductos.setItem(index, 5, QTableWidgetItem(str(producto['preciopublico'])))
                                self.RefreshTableStockmin()
                                self.botoneditar.setEnabled(False)
                                self.botoneliminar.setEnabled(False)
                                for i in range(len(self.inputs)):
                                    self.inputs[i].setText("")
                            else:
                                alert(title="Código en uso!", text="El codigo que ingresó ya existe", button="OK")
                        else:
                            alert(title="Error en el servidor!", text="Revise que el servidor XAMPP este activo",
                                  button="OK")
                    else:
                        if self.con.UpdateProduct(codigo_ant,producto)!=False:
                            index = self.tablaproductos.currentRow()
                            self.tablaproductos.setItem(index, 0, QTableWidgetItem(str(producto['codigo'])))
                            self.tablaproductos.setItem(index, 1, QTableWidgetItem(str(producto['producto'])))
                            self.tablaproductos.setItem(index, 2, QTableWidgetItem(str(producto['grupo'])))
                            self.tablaproductos.setItem(index, 3, QTableWidgetItem(str(producto['utilidades'])))
                            self.tablaproductos.setItem(index, 4, QTableWidgetItem(str(producto['preciocompra'])))
                            self.tablaproductos.setItem(index, 5, QTableWidgetItem(str(producto['preciopublico'])))
                            self.RefreshTableStockmin()
                            self.botoneditar.setEnabled(False)
                            self.botoneliminar.setEnabled(False)
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
            opc=confirm(text="Desea eliminar "+str(self.tablaproductos.item(row,1).text())+"?",title="Eliminar?",buttons=["OK","CANCEL"])
            if opc=="OK":
                codigo=self.tablaproductos.item(row, 0).text()
                if self.con.DeleteProduct(codigo)!=False:
                    #alert(title="Listo!",text="Se eliminó correctamente",button="OK")
                    for i in range(len(self.inputs)):
                        self.inputs[i].setText("")
                    try:
                        numproducts = self.con.GetNumProducts()
                        total_paginas = int(numproducts / 50)
                        if numproducts % 50 > 0:
                            total_paginas += 1
                        self.total_paginas.setText(str(total_paginas))
                        if int(self.pagina.text())>int(self.total_paginas.text()):
                            self.pagina.setText(self.total_paginas.text())
                            self.siguiente.setEnabled(False)
                        elif int(self.pagina.text())==int(self.total_paginas.text()):
                            self.siguiente.setEnabled(False)
                        self.RefreshTableData()
                        self.botoneditar.setEnabled(False)
                        self.botoneliminar.setEnabled(False)
                    except:
                        pass

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
            self.inputs[-1].setText(str(self.productos[row]["stock"]))
            self.botoneditar.setEnabled(True)
            self.botoneliminar.setEnabled(True)
        except:
            pass
    def valida_formulario(self,accion):
        if accion=="agrega":
            if self.codigo.text()!="":
                if self.valCodigo() and self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
            else:
                if  self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
        else:
            if self.codigo.text()!="":
                if self.valCodigo()  and self.valExistencia() and self.valPreciocompra() and self.valProducto() and self.valIncremento():
                    return True
                else:
                    return False
            else:
                return False
    def valCodigo(self):
        input=self.codigo
        res=False
        try:
            text=input.text()
            int(text)
            if len(text)<21:
                input.setStyleSheet(self.trueValidate)
                res=True
        except:
            input.setStyleSheet(self.falseValidate)
        #res=self.valida.validaNumero(input.text())
        return res
    def valProducto(self):
        input = self.producto
        validacion=self.valida.valida50Caracteres(input.text())
        if validacion and self.producto.text()!="":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def validaGrupo(self):
        input = self.grupo
        validacion = self.valida.valida50Caracteres(input.text())
        if validacion:
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valExistencia(self):
        input = self.stock
        res = self.valida.valida20Caracteres(input.text())
        if res:
            res = self.valida.validaDecimal(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valIncremento(self):
        input = self.utilidades
        res = self.valida.valida20Caracteres(input.text())
        if res:
            res = self.valida.validaDecimal(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valPreciocompra(self):
        input = self.preciocompra
        res = self.valida.valida20Caracteres(input.text())
        if res:
            res = self.valida.validaDecimal(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
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
        productos=self.productos
        if productos!=False:
            rowCount = self.tablaproductos.rowCount()
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(productos)):
                self.tablaproductos.insertRow(0)
                self.tablaproductos.setItem(0,0, QTableWidgetItem( str(productos[i]['codigo'])))
                self.tablaproductos.setItem(0, 1, QTableWidgetItem(str(productos[i]['producto'])))
                self.tablaproductos.setItem(0, 2, QTableWidgetItem(str(productos[i]['grupo'])))
                self.tablaproductos.setItem(0, 3, QTableWidgetItem(str(productos[i]['utilidades'])))
                self.tablaproductos.setItem(0, 4, QTableWidgetItem(str(productos[i]['preciocompra'])))
                self.tablaproductos.setItem(0, 5, QTableWidgetItem(str(productos[i]['preciopublico'])))
            self.RefreshTableStockmin()
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def ShowSiguiente(self):
        self.anterior.setEnabled(True)
        pagina=int(self.pagina.text())+1
        self.pagina.setText(str(pagina))
        if pagina==int(self.total_paginas.text()):
            self.siguiente.setEnabled(False)
        self.RefreshTableData()
        self.botoneditar.setEnabled(False)
        self.botoneliminar.setEnabled(False)
    def ShowAnterior(self):
        self.siguiente.setEnabled(True)
        pagina = int(self.pagina.text()) - 1
        self.pagina.setText(str(pagina))
        if pagina ==1:
            self.anterior.setEnabled(False)
        self.RefreshTableData()
        self.botoneditar.setEnabled(False)
        self.botoneliminar.setEnabled(False)
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
            self.botoneditar.setEnabled(False)
            self.botoneliminar.setEnabled(False)
        else:
            input.setText(str(self.total_paginas.text()))
            self.anterior.setEnabled(True)
            self.siguiente.setEnabled(False)
    def RefreshTableStockmin(self):
        productos = self.con.AllStockMinimo()
        rowCount=self.tablestockminimo.rowCount()
        for i in range(rowCount):
            self.tablestockminimo.removeRow(0)
        for i in range(len(productos)-1,-1,-1):
            self.tablestockminimo.insertRow(i)
            self.tablestockminimo.setItem(i, 0, QTableWidgetItem(str(productos[i]['producto'])))
            self.tablestockminimo.setItem(i, 1, QTableWidgetItem(str(productos[i]['stockminimo'])))
            self.tablestockminimo.setItem(i, 2, QTableWidgetItem(str(productos[i]['stock'])))
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
        if self.busqueda.text()!="" and len(self.busqueda.text())>3:
            busqueda=self.busqueda.text()
            self.productos=self.con.FindProducts(busqueda)
            coincidencias=self.productos
            rowCount = self.tablaproductos.rowCount()
            for i in range(rowCount):
                self.tablaproductos.removeRow(0)
            for i in range(len(coincidencias)):
                self.tablaproductos.insertRow(0)
                self.tablaproductos.setItem(0, 0, QTableWidgetItem(str(coincidencias[i]['codigo'])))
                self.tablaproductos.setItem(0, 1, QTableWidgetItem(str(coincidencias[i]['producto'])))
                self.tablaproductos.setItem(0, 2, QTableWidgetItem(str(coincidencias[i]['grupo'])))
                self.tablaproductos.setItem(0, 3, QTableWidgetItem(str(coincidencias[i]['utilidades'])))
                self.tablaproductos.setItem(0, 4, QTableWidgetItem(str(coincidencias[i]['preciocompra'])))
                self.tablaproductos.setItem(0, 5, QTableWidgetItem(str(coincidencias[i]['preciopublico'])))
            self.botoneditar.setEnabled(False)
            self.botoneliminar.setEnabled(False)
        elif len(self.busqueda.text())<4 and self.busqueda.text()!='':
            pass
        else:
            self.botoneditar.setEnabled(False)
            self.botoneliminar.setEnabled(False)
            self.RefreshTableData()
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()
if __name__=="__main__":
    from validaciones import Valida
    from conexion import Conexion
    parametros={'conexion':Conexion(),'valida':Valida()}
    app = QApplication(sys.argv)
    gui = ViewProductos(parametros)
    gui.show()
    sys.exit(app.exec())
