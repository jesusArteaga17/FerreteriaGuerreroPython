from PyQt5.QtWidgets import  QApplication, QDialog,QTableWidgetItem,QCalendarWidget
from PyQt5 import uic,QtWidgets
from validaciones import Valida
from conexion import *
from pymsgbox import *
from datetime import datetime
import time
import sys
from Emergente_agendar import EmergenteAgendar
from emergente_agendar2 import EmergenteAgendar2
#QPlainTextEdit.appendPlainText()
class ViewProveedores(QDialog):
    formValid=False
    def __init__(self, *args, **kwargs):
        self.date = datetime.now()
        super(ViewProveedores, self).__init__(*args, **kwargs)
        #todos los productos
        self.proveedores=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=Conexion()
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #bandera para saber cuando esta habilitada la opcion de editar un producto
        #instanciamiento de mi clase Valida (sirve para validar cadenas)
        self.valida=Valida()
        uic.loadUi("proveedores.ui",self)
        #Inicialización para los eventos de los botones
        self.botonagregar.clicked.connect(self.agrega)
        self.botoneditar.clicked.connect(self.edita)
        self.botoneliminar.clicked.connect(self.elimina)
        self.botonagendar.clicked.connect(self.agendar)
        self.botoneditar.setDisabled(True)
        self.botoneliminar.setDisabled(True)
        self.botonagendar.setDisabled(True)
        self.ayudaagregar.clicked.connect(self.ayudaAgregar)
        self.ayudaeditar.clicked.connect(self.ayudaEditar)
        self.ayudaeliminar.clicked.connect(self.ayudaEliminar)
        self.ayudaagendar.clicked.connect(self.ayudaAgendar)
        self.botonbuscar.clicked.connect(self.enterBuscar)
        self.botoneliminar_2.clicked.connect(self.eliminarEvento)
        self.botoneliminar_2.setDisabled(True)
        self.ayudaeliminar_2.clicked.connect(self.ayudaEliminar2)

        #aqui me falta agregar los botones que son para el calendario
        self.botonhoy.clicked.connect(self.showTodayEvents)
        self.botonfuturos.clicked.connect(self.showFutureEvents)
        self.botontodos.clicked.connect(self.RefreshTableEvents)
        self.ayudahoy.clicked.connect(self.ayudaHoy)
        self.ayudafuturos.clicked.connect(self.ayudaFuturos)
        self.ayudatodos.clicked.connect(self.ayudaTodos)
        #Inicialización de los eventos para los inputs
        self.nombre.textChanged.connect(self.valNombre)
        self.nombre.returnPressed.connect(self.agrega)
        self.telefono.textChanged.connect(self.valTelefono)
        self.telefono.returnPressed.connect(self.agrega)
        self.direccion.textChanged.connect(self.valDireccion)
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.returnPressed.connect(self.enterBuscar)
        #Inicialización de los eventos de las tablas
        self.tablaproveedores.clicked.connect(self.rowClicked)
        self.tablaeventos.clicked.connect(self.rowClicked2)
        #configuracion de la cabecera de mi tabla
        tablaProveedores = self.tablaproveedores.horizontalHeader()
        tablaProveedores.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        tablaProveedores.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        tablaProveedores.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        tablaProveedores.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        tablaEventos = self.tablaeventos.horizontalHeader()
        tablaEventos.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        tablaEventos.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        tablaEventos.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        tablaEventos.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        tablaEventos.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        #Enlazamos el evento clicked del calendario con su funcion
        self.calendario.clicked.connect(self.agregaEvento)
        #lista de los inputs disponibles en la vista de productos
        self.inputs = [self.nombre,self.telefono,self.direccion]
        #Refrescamos por primera vez las tablas
        self.RefreshTableData()
        self.RefreshTableEvents()
        #Definiendo los atajos
        """
        shortcut1 = QShortcut(QtGui.QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        shortcut3 = QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QtGui.QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.elimina)
        shortcut5 = QShortcut(QtGui.QKeySequence("Esc"), self)
        shortcut5.activated.connect(self.close)"""
    def agrega(self):
        if self.valida_formulario():
            opc = confirm(text="Desea agregar " + str(self.nombre.text()) + "?", title="Agregar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                proveedor = {}
                proveedor['nombre'] = self.nombre.text()
                proveedor['telefono'] = self.telefono.text()
                proveedor['direccion'] = self.direccion.toPlainText()
                if self.con.AddProveedor(proveedor) != False:
                    for i in range(len(self.inputs)):
                        try:
                            self.inputs[i].setText("")
                        except:
                            self.inputs[i].clear()
                    self.RefreshTableData()
                    self.botoneditar.setDisabled(True)
                    self.botoneliminar.setDisabled(True)
                    self.botonagendar.setDisabled(True)
                    alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
                else:
                    alert(title="Error de servidor", text="Ocurrió un error en el servidor", button="OK")
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def agregaEvento(self):
        year=self.calendario.selectedDate().year()
        month=self.calendario.selectedDate().month()
        day=self.calendario.selectedDate().day()
        ban=True
        dia_agendar = self.calendario.selectedDate()
        if dia_agendar.year() < self.date.year:
            ban = False
        elif dia_agendar.year() == self.date.year:
            if dia_agendar.month() < self.date.month:
                ban = False
            elif dia_agendar.month() == self.date.month:
                if dia_agendar.day() < self.date.day:
                    ban = False
        if ban:
            fecha="%s-%s-%s"%(year,month,day)
            view = EmergenteAgendar2(fecha, self)
            view.show()
            self.RefreshTableEvents()

    def edita(self):
        if self.valida_formulario():
            row = self.tablaproveedores.currentRow()
            opc = confirm(text="Desea editar " + str(self.tablaproveedores.item(row, 1).text()) + "?", title="Editar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                proveedor = {}
                proveedor['nombre'] = self.nombre.text()
                proveedor['telefono'] = self.telefono.text()
                proveedor['direccion'] = self.direccion.toPlainText()
                id = self.tablaproveedores.item(row, 0).text()
                if self.con.UpdateProveedor(id, proveedor) != False:
                    for i in range(len(self.inputs)):
                        try:
                            self.inputs[i].setText("")
                        except:
                            self.inputs[i].clear()
                    self.RefreshTableData()
                    self.botoneditar.setDisabled(True)
                    self.botoneliminar.setDisabled(True)
                    self.botonagendar.setDisabled(True)
                else:
                    alert(title="Error en el servidor!", text="Revise que el servidor XAMPP este activo",
                          button="OK")
        else:
            alert(title="Error en formulario!", text="Revise el formulario", button='OK')
    def elimina(self):
        row = self.tablaproveedores.currentRow()
        opc = confirm(text="Desea eliminar " + str(self.tablaproveedores.item(row, 1).text()) + "? \nSe eliminarán los eventos asociados con el proveedor", title="Eliminar?",
                      buttons=["OK", "CANCEL"])
        if opc == "OK":
            id = self.tablaproveedores.item(row, 0).text()
            nombre_proveedor= self.tablaproveedores.item(row, 1).text()

            if self.con.DeleteProveedor(id) != False:
                res=self.con.DeleteEventProveedor(nombre_proveedor)
                if res or res==None:
                    for i in range(len(self.inputs)):
                        try:
                            self.inputs[i].setText("")
                        except:
                            self.inputs[i].clear()
                    self.RefreshTableData()
                    self.RefreshTableEvents()
                    self.botoneditar.setDisabled(True)
                    self.botoneliminar.setDisabled(True)
                    self.botonagendar.setDisabled(True)
                    alert(title="Listo!", text="Se eliminó correctamente", button="OK")
                elif res==False:
                    alert(title="Error en el servidor!", text="Asegurese que el servidor XAMPP este activo",
                          button="OK")
            else:
                alert(title="Error en el servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def eliminarEvento(self):
        row = self.tablaeventos.currentRow()
        opc = confirm(text="Desea eliminar " + str(
            self.tablaeventos.item(row, 1).text()) + "?",
                      title="Eliminar?",
                      buttons=["OK", "CANCEL"])
        if opc == "OK":
            id = self.tablaeventos.item(row, 0).text()
            if self.con.DeleteEvent(id) != False:
                self.RefreshTableEvents()
                self.botoneliminar_2.setDisabled(True)
                alert(title="Listo!", text="Se eliminó correctamente", button="OK")
            else:
                alert(title="Error en el servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def agendar(self):
        self.botoneditar.setDisabled(True)
        self.botoneliminar.setDisabled(True)
        self.botonagendar.setDisabled(True)
        row=self.tablaproveedores.currentRow()
        proveedor=self.tablaproveedores.item(row, 1).text() #se obtiene el nombre del proveedor seleccionado
        view = EmergenteAgendar(proveedor,self)
        view.show()
        self.RefreshTableEvents()
    def rowClicked(self):
        try:
            row= self.tablaproveedores.currentRow()
            #col=self.tablaproveedores.currentColumn()
            for i in range(len(self.inputs)):
                try:
                    self.inputs[i].setText(self.tablaproveedores.item(row,i+1).text())
                except:
                    self.inputs[i].clear()
                    self.inputs[i].appendPlainText(self.tablaproveedores.item(row,i+1).text())
            self.botoneditar.setDisabled(False)
            self.botoneliminar.setDisabled(False)
            self.botonagendar.setDisabled(False)
        except:
            pass
    def rowClicked2(self):
        self.botoneliminar_2.setDisabled(False)
    def valNombre(self):
        input = self.nombre
        if len(input.text())<=100 and input.text()!="":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valTelefono(self):
        input = self.telefono
        res = self.valida.valida20Caracteres(input.text())
        if res:
            res = self.valida.validaNumero(input.text())
            if res:
                input.setStyleSheet(self.trueValidate)
            else:
                input.setStyleSheet(self.falseValidate)
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def valDireccion(self):
        input = self.direccion
        if len(input.toPlainText()) <= 200:
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valida_formulario(self):
        if self.valNombre() and self.valTelefono() and self.valDireccion():
            return True
        else:
            return False
    def RefreshTableData(self):
        self.proveedores=self.con.AllProveedores()
        if self.proveedores!=False:
            rowCount=self.tablaproveedores.rowCount()
            self.tablaproveedores.clearContents()
            proveedores=self.proveedores
            for i in range(rowCount):
                self.tablaproveedores.removeRow(0)
            for i in range(len(proveedores)):
                self.tablaproveedores.insertRow(i)
                self.tablaproveedores.setItem(i,0, QTableWidgetItem( str(proveedores[i]['id'])))
                self.tablaproveedores.setItem(i, 1, QTableWidgetItem(str(proveedores[i]['nombre'])))
                self.tablaproveedores.setItem(i, 2, QTableWidgetItem(str(proveedores[i]['telefono'])))
                self.tablaproveedores.setItem(i, 3, QTableWidgetItem(str(proveedores[i]['direccion'])))
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def RefreshTableEvents(self):
        eventos = self.con.AllEvents()
        if eventos != False:
            rowCount = self.tablaeventos.rowCount()
            self.tablaeventos.clearContents()
            for i in range(rowCount):
                self.tablaeventos.removeRow(0)
            for i in range(len(eventos)):
                self.tablaeventos.insertRow(i)
                self.tablaeventos.setItem(i, 0, QTableWidgetItem(str(eventos[i]['id'])))
                self.tablaeventos.setItem(i, 1, QTableWidgetItem(str(eventos[i]['proveedor'])))
                self.tablaeventos.setItem(i, 2, QTableWidgetItem(str(eventos[i]['dia'])))
                self.tablaeventos.setItem(i, 3, QTableWidgetItem(str(eventos[i]['hora'])))
                self.tablaeventos.setItem(i, 4, QTableWidgetItem(str(eventos[i]['descripcion'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def showTodayEvents(self):
        eventos = self.con.TodayEvents()
        if eventos != False:
            rowCount = self.tablaeventos.rowCount()
            self.tablaeventos.clearContents()
            for i in range(rowCount):
                self.tablaeventos.removeRow(0)
            for i in range(len(eventos)):
                self.tablaeventos.insertRow(i)
                self.tablaeventos.setItem(i, 0, QTableWidgetItem(str(eventos[i]['id'])))
                self.tablaeventos.setItem(i, 1, QTableWidgetItem(str(eventos[i]['proveedor'])))
                self.tablaeventos.setItem(i, 2, QTableWidgetItem(str(eventos[i]['dia'])))
                self.tablaeventos.setItem(i, 3, QTableWidgetItem(str(eventos[i]['hora'])))
                self.tablaeventos.setItem(i, 4, QTableWidgetItem(str(eventos[i]['descripcion'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def showFutureEvents(self):
        eventos = self.con.FutureEvents()
        if eventos != False:
            rowCount = self.tablaeventos.rowCount()
            self.tablaeventos.clearContents()
            for i in range(rowCount):
                self.tablaeventos.removeRow(0)
            for i in range(len(eventos)):
                self.tablaeventos.insertRow(i)
                self.tablaeventos.setItem(i, 0, QTableWidgetItem(str(eventos[i]['id'])))
                self.tablaeventos.setItem(i, 1, QTableWidgetItem(str(eventos[i]['proveedor'])))
                self.tablaeventos.setItem(i, 2, QTableWidgetItem(str(eventos[i]['dia'])))
                self.tablaeventos.setItem(i, 3, QTableWidgetItem(str(eventos[i]['hora'])))
                self.tablaeventos.setItem(i, 4, QTableWidgetItem(str(eventos[i]['descripcion'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def ayudaAgregar(self):
        alert(title="Ayuda",text="Para agregar un proveedor \n"
                                 "1.- Llenar el formulario \n"
                                 "2.- Hacer click en el boton 'Agregar', precionar 'Enter' o precionar 'Ctrl + a'",button="OK")
    def ayudaEditar(self):
        alert(title="Ayuda",text="Para editar la información de un proveedor: \n"
                                 "1.- Seleccione el proveedor a editar en la tabla \n"
                                 "2.- Modifique los datos"
                                 "3.- Hacer click en el boton 'Editar' o precionar 'Ctrl + e'",button=
              "OK")
    def ayudaEliminar(self):
        alert(title="Ayuda",text="Para eliminar un proveedor: \n"
                                 "1.- Seleccione el proveedor a eliminar de la tabla \n"
                                 "2.- Hacer click en el boton 'Eliminar' o precionar 'Ctrl + d'")
    def ayudaEliminar2(self):
        alert(title="Ayuda", text="Para eliminar un evento: \n"
                                  "1.- Seleccione el evento a eliminar de la tabla \n"
                                  "2.- Hacer click en el boton 'Eliminar' o precionar 'Ctrl + d'")
    def ayudaHoy(self):
        alert(title="Ayuda", text="Muestra todos los eventos programados para el día de hoy")
    def ayudaFuturos(self):
        alert(title="Ayuda", text="Muestra todos los eventos programados a partir de el día de mañana en adelante'")
    def ayudaTodos(self):
        alert(title="Ayuda", text="Muestra todos los eventos programados hasta el momento'")
    def ayudaAgendar(self):
        alert(title="Ayuda", text="Para agendar un evento con proveedor: \n"
                                  "1.- Seleccione el proveedor a agendar de la tabla \n"
                                  "2.- Hacer click en el boton 'Agendar'")
    def buscar(self):
        if self.busqueda.text()!="":
            coincidencias=[]
            keys=[]
            busqueda=self.busqueda.text().lower()
            for i in range(len(self.proveedores)):
                keys.append([])
                proveedor=list(self.proveedores[i].values())
                for j in range(len(proveedor)):
                    keys[i].append(str(proveedor[j]).lower())
                for j in range(len(keys[i])):
                    if keys[i][j].find(busqueda)!=-1:
                        if i not in coincidencias:
                            coincidencias.append(i)
            for i in range(self.tablaproveedores.rowCount()):
                self.tablaproveedores.removeRow(0)
            for i in range(len(coincidencias)):
                self.tablaproveedores.insertRow(i)
                self.tablaproveedores.setItem(i, 0, QTableWidgetItem(str(self.proveedores[coincidencias[i]]['id'])))
                self.tablaproveedores.setItem(i, 1, QTableWidgetItem(str(self.proveedores[coincidencias[i]]['nombre'])))
                self.tablaproveedores.setItem(i, 2, QTableWidgetItem(str(self.proveedores[coincidencias[i]]['telefono'])))
                self.tablaproveedores.setItem(i, 3, QTableWidgetItem(str(self.proveedores[coincidencias[i]]['direccion'])))
        else:
            self.RefreshTableData()
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()

if __name__=="__main__":
    app = QApplication(sys.argv)
    gui = ViewProveedores()
    gui.show()
    sys.exit(app.exec())

