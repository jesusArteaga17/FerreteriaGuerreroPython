from PyQt5.QtWidgets import   QDialog,QTableWidgetItem,QShortcut,QMainWindow
from PyQt5 import uic,QtWidgets,QtGui

from pymsgbox import *
import sys
from emergente_creditos import EmergenteCreditos
from EmergenteProductosCredito import EmergenteProductosCredito
class ViewClientes(QMainWindow):
    formValid=False
    def __init__(self,privilegios={}, *args, **kwargs):
        self.permiso_clientes=int(privilegios['clientes'])
        self.permiso_creditos=int(privilegios['creditos'])
        super(ViewClientes, self).__init__(*args, **kwargs)
        #todos los Clientes
        self.Clientes=[]
        self.Creditos=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=privilegios['conexion']
        # instanciamiento de mi clase Valida
        self.valida = privilegios['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #bandera para saber cuando esta habilitada la opcion de editar un cliente
        uic.loadUi("Clientes.ui",self)
        #Inicialización para los eventos de los botones
        self.botagregar.clicked.connect(self.agrega)
        self.boteditar.clicked.connect(self.edita)
        self.boteliminar.clicked.connect(self.elimina)
        self.botcredito.clicked.connect(self.DarCredito)
        self.ayudaagregar.clicked.connect(self.ayudaAgregar)
        self.ayudaeditar.clicked.connect(self.ayudaEditar)
        self.ayudaeliminar.clicked.connect(self.ayudaEliminar)
        self.ayudacredito.clicked.connect(self.ayudaCredito)
        self.botbusqueda.clicked.connect(self.enterBuscar)
        self.botagregar.setEnabled(self.permiso_clientes)
        self.boteditar.setEnabled(False)
        self.boteliminar.setEnabled(False)
        self.botcredito.setEnabled(False)

        self.botvigentes.clicked.connect(self.Vigentes)
        self.botvencidos.clicked.connect(self.Vencidos)
        self.botpagados.clicked.connect(self.Pagados)
        self.botsinpagar.clicked.connect(self.Sinpagar)
        self.bottodos.clicked.connect(self.Todos)
        self.ayudavigentes.clicked.connect(self.ayudaVigentes)
        self.ayudavencidos.clicked.connect(self.ayudaVencidos)
        self.ayudapagados.clicked.connect(self.ayudaPagados)
        self.ayudasinpagar.clicked.connect(self.ayudaSinpagar)
        self.ayudatodos.clicked.connect(self.ayudaTodos)
        #Inicialización de los eventos para los inputs
        self.nombre.textChanged.connect(self.valNombre)
        self.nombre.returnPressed.connect(self.agrega)
        self.apellidos.textChanged.connect(self.valApellidos)
        self.apellidos.returnPressed.connect(self.agrega)
        self.rfc.textChanged.connect(self.valRfc)
        self.rfc.returnPressed.connect(self.agrega)
        self.telefono.textChanged.connect(self.valTelefono)
        self.telefono.returnPressed.connect(self.agrega)
        self.correo.textChanged.connect(self.valCorreo)
        self.correo.returnPressed.connect(self.agrega)
        self.direccion.textChanged.connect(self.valDireccion)
        self.direccion.returnPressed.connect(self.agrega)

        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.setFocus()
        #Inicialización de los eventos de la tabla
        self.tableClient.clicked.connect(self.rowClicked)
        self.tableCredit.clicked.connect(self.rowClicked2)
        #configuracion de la cabecera de mi tabla
        header = self.tableClient.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6,QtWidgets.QHeaderView.Stretch )

        header = self.tableCredit.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        #lista de los inputs disponibles en la vista de Clientes
        self.inputs = [self.nombre, self.apellidos, self.rfc, self.telefono,self.correo,self.direccion]
        self.RefreshTableData()
        #Definiendo los atajos
        shortcut1 = QShortcut(QtGui.QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        shortcut3 = QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QtGui.QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.elimina)
        #shortcut5 = QShortcut(QtGui.QKeySequence("Esc"), self)
        #shortcut5.activated.connect(self.close)
    def agrega(self):
        if self.valida_formulario():
            opc = confirm(text="Desea agregar " + str(self.nombre.text()) + "?", title="Agregar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                cliente = {}
                cliente['nombre'] = self.nombre.text()
                cliente['apellidos'] = self.apellidos.text()
                cliente['rfc'] = self.rfc.text()
                cliente['telefono']=self.telefono.text()
                cliente['correo']=self.correo.text()
                cliente['direccion']=self.direccion.text()
                if self.con.AddClient(cliente) != False:
                    for i in range(len(self.inputs)):
                        self.inputs[i].setText("")
                    self.RefreshTableData()
                    alert(text='Se agregó correctamente', title='Operación exitosa!', button='OK')
                    self.boteditar.setDisabled(True)
                    self.boteliminar.setDisabled(True)
                    self.botcredito.setDisabled(True)
                else:
                    alert(title="Error de servidor", text="Ocurrió un error en el servidor", button="OK")
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def edita(self):
        if self.valida_formulario():
            row=self.tableClient.currentRow()
            opc = confirm(text="Desea editar " + str(self.tableClient.item(row,1).text()) + "?", title="Editar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                id=self.tableClient.item(row,0).text()
                cliente = {}
                cliente['nombre'] = self.nombre.text()
                cliente['apellidos'] = self.apellidos.text()
                cliente['rfc'] = self.rfc.text()
                cliente['telefono']=self.telefono.text()
                cliente['correo']=self.correo.text()
                cliente['direccion']=self.direccion.text()
                if self.con.UpdateClient(id,cliente) != False:
                    for i in range(len(self.inputs)):
                        self.inputs[i].setText("")
                    self.RefreshTableData()
                    alert(text='Se editó correctamente', title='Operación exitosa!', button='OK')
                    self.boteditar.setDisabled(True)
                    self.boteliminar.setDisabled(True)
                    self.botcredito.setDisabled(True)
                else:
                    alert(title="Error de servidor", text="Ocurrió un error en el servidor", button="OK")
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def elimina(self):
        try:
            row = self.tableClient.currentRow()
            opc=confirm(text="Desea eliminar "+str(self.tableClient.item(row,1).text())+"?\n"
                                                                                        "Todos los creditos relacionados con este cliente\n"
                                                                                        "serán eliminados",title="Eliminar?",buttons=["OK","CANCEL"])
            if opc=="OK":
                id=self.tableClient.item(row, 0).text()
                if self.con.DeleteClient(id)!=False and self.con.DeleteCredits(id):
                    alert(title="Listo!",text="Se eliminó correctamente",button="OK")
                    for i in range(len(self.inputs)):
                        self.inputs[i].setText("")
                    try:
                        self.RefreshTableData()
                    except:
                        pass
                    self.boteditar.setDisabled(True)
                    self.boteliminar.setDisabled(True)
                    self.botcredito.setDisabled(True)
                else:
                    alert(title="Error en el servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
        except:
            alert(title="Error!",text="Primero debes seleccionar una fila en la tabla", button='OK')
    def DarCredito(self):
        self.boteditar.setDisabled(True)
        self.boteliminar.setDisabled(True)
        self.botcredito.setDisabled(True)
        row = self.tableClient.currentRow()
        id_cliente = self.tableClient.item(row, 0).text()
        view = EmergenteCreditos(id_cliente, self)
        view.show()
    def Vigentes(self):
        Creditos = self.con.AllCreditsVigentes()
        if Creditos != False:
            rowCount = self.tableCredit.rowCount()
            self.tableCredit.clearContents()
            for i in range(rowCount):
                self.tableCredit.removeRow(0)
            for i in range(len(Creditos)):
                self.tableCredit.insertRow(i)
                self.tableCredit.setItem(i, 0, QTableWidgetItem(str(Creditos[i]['id'])))
                cliente = self.con.GetClientById(str(Creditos[i]['idcliente']))
                self.tableCredit.setItem(i, 1, QTableWidgetItem(
                    str(cliente[0]['nombre']) + ' ' + str(cliente[0]['apellidos'])))
                self.tableCredit.setItem(i, 2, QTableWidgetItem(str(Creditos[i]['fechainicio'])))
                self.tableCredit.setItem(i, 3, QTableWidgetItem(str(Creditos[i]['fechavencimiento'])))
                self.tableCredit.setItem(i, 4, QTableWidgetItem(str(Creditos[i]['descripcionproductos'])))
                self.tableCredit.setItem(i, 5, QTableWidgetItem(str(Creditos[i]['adeudo'])))
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def Vencidos(self):
        Creditos = self.con.AllCreditsVencidos()
        if Creditos != False:
            rowCount = self.tableCredit.rowCount()
            self.tableCredit.clearContents()
            for i in range(rowCount):
                self.tableCredit.removeRow(0)
            for i in range(len(Creditos)):
                cliente = self.con.GetClientById(str(Creditos[i]['idcliente']))
                self.tableCredit.insertRow(i)
                self.tableCredit.setItem(i, 0, QTableWidgetItem(str(Creditos[i]['id'])))
                self.tableCredit.setItem(i, 1, QTableWidgetItem(
                    str(cliente[0]['nombre']) + ' ' + str(cliente[0]['apellidos'])))
                self.tableCredit.setItem(i, 2, QTableWidgetItem(str(Creditos[i]['fechainicio'])))
                self.tableCredit.setItem(i, 3, QTableWidgetItem(str(Creditos[i]['fechavencimiento'])))
                self.tableCredit.setItem(i, 4, QTableWidgetItem(str(Creditos[i]['descripcionproductos'])))
                self.tableCredit.setItem(i, 5, QTableWidgetItem(str(Creditos[i]['adeudo'])))
                # Aqui refrescaremos la otra tabla para los créditos
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def Pagados(self):
        Creditos = self.con.AllCreditsPagados()
        if Creditos != False:
            rowCount = self.tableCredit.rowCount()
            self.tableCredit.clearContents()
            for i in range(rowCount):
                self.tableCredit.removeRow(0)
            for i in range(len(Creditos)):
                cliente = self.con.GetClientById(str(Creditos[i]['idcliente']))
                self.tableCredit.insertRow(i)
                self.tableCredit.setItem(i, 0, QTableWidgetItem(str(Creditos[i]['id'])))
                self.tableCredit.setItem(i, 1, QTableWidgetItem(
                    str(cliente[0]['nombre']) + ' ' + str(cliente[0]['apellidos'])))
                self.tableCredit.setItem(i, 2, QTableWidgetItem(str(Creditos[i]['fechainicio'])))
                self.tableCredit.setItem(i, 3, QTableWidgetItem(str(Creditos[i]['fechavencimiento'])))
                self.tableCredit.setItem(i, 4, QTableWidgetItem(str(Creditos[i]['descripcionproductos'])))
                self.tableCredit.setItem(i, 5, QTableWidgetItem(str(Creditos[i]['adeudo'])))
                # Aqui refrescaremos la otra tabla para los créditos
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def Sinpagar(self):
        Creditos = self.con.AllCreditsSinpagar()
        if Creditos != False:
            rowCount = self.tableCredit.rowCount()
            self.tableCredit.clearContents()
            for i in range(rowCount):
                self.tableCredit.removeRow(0)
            for i in range(len(Creditos)):
                cliente = self.con.GetClientById(str(Creditos[i]['idcliente']))
                self.tableCredit.insertRow(i)
                self.tableCredit.setItem(i, 0, QTableWidgetItem(str(Creditos[i]['id'])))
                self.tableCredit.setItem(i, 1, QTableWidgetItem(
                    str(cliente[0]['nombre']) + ' ' + str(cliente[0]['apellidos'])))
                self.tableCredit.setItem(i, 2, QTableWidgetItem(str(Creditos[i]['fechainicio'])))
                self.tableCredit.setItem(i, 3, QTableWidgetItem(str(Creditos[i]['fechavencimiento'])))
                self.tableCredit.setItem(i, 4, QTableWidgetItem(str(Creditos[i]['descripcionproductos'])))
                self.tableCredit.setItem(i, 5, QTableWidgetItem(str(Creditos[i]['adeudo'])))
                # Aqui refrescaremos la otra tabla para los créditos
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def Todos(self):
        self.Creditos=[]
        self.Creditos =self.con.AllCredits()[:]
        if self.Creditos != False:
            rowCount = self.tableCredit.rowCount()
            self.tableCredit.clearContents()
            Creditos= self.Creditos
            for i in range(rowCount):
                self.tableCredit.removeRow(0)
            for i in range(len(Creditos)):
                cliente=self.con.GetClientById(str(Creditos[i]['idcliente']))
                self.tableCredit.insertRow(i)
                self.tableCredit.setItem(i, 0, QTableWidgetItem(str(Creditos[i]['id'])))
                self.tableCredit.setItem(i, 1, QTableWidgetItem(str(cliente[0]['nombre'])+' '+str(cliente[0]['apellidos'])))
                self.tableCredit.setItem(i, 2, QTableWidgetItem(str(Creditos[i]['fechainicio'])))
                self.tableCredit.setItem(i, 3, QTableWidgetItem(str(Creditos[i]['fechavencimiento'])))
                self.tableCredit.setItem(i, 4, QTableWidgetItem(str(Creditos[i]['descripcionproductos'])))
                self.tableCredit.setItem(i, 5, QTableWidgetItem(str(Creditos[i]['adeudo'])))
                # Aqui refrescaremos la otra tabla para los créditos
        else:
            alert(title="Error de servidor!", text="Asegurese que el servidor XAMPP este activo", button="OK")
    def rowClicked(self):
        if self.permiso_clientes:
            try:
                row= self.tableClient.currentRow()
                #col=self.tableClient.currentColumn()
                for i in range(len(self.inputs)):
                    self.inputs[i].setText(self.tableClient.item(row,i+1).text())
                #self.inputs[-1].setText(str(self.Clientes[row]["stock"]))
            except:
                pass
        self.boteditar.setEnabled(self.permiso_clientes)
        self.boteliminar.setEnabled(self.permiso_clientes)
        self.botcredito.setEnabled(self.permiso_creditos)
    def rowClicked2(self):
        if self.permiso_creditos:
            row = self.tableCredit.currentRow()
            id_credit = self.tableCredit.item(row, 0).text()
            datos={}
            datos['nombrecliente']=self.tableCredit.item(row, 1).text()
            datos['fechainicio']=self.tableCredit.item(row, 2).text()
            datos['fechavencimiento']=self.tableCredit.item(row, 3).text()
            datos['conexion']=self.con
            datos['id_credito']=id_credit
            datos['adeudo']=self.tableCredit.item(row, 5).text()
            view = EmergenteProductosCredito(datos, self)
            view.show()
    def valNombre(self):
        input = self.nombre
        if len(input.text())<=100 and input.text() != "":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valApellidos(self):
        input = self.apellidos
        if len(input.text()) <= 100 and input.text() != "":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valRfc(self):
        input = self.rfc
        if self.valida.validaRfc(input.text()) or input.text()!="":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valTelefono(self):
        input = self.telefono
        if len(input.text()) <=11 and self.valida.validaNumero(input.text()):
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valCorreo(self):
        input = self.correo
        if len(input.text()) <= 100 and self.valida.validaCorreo(input.text()):
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valDireccion(self):
        input = self.direccion
        if len(input.text()) <= 100:
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valida_formulario(self):
        if self.valNombre() and self.valApellidos() and self.valRfc() and self.valTelefono() and self.valCorreo() and self.valDireccion():
            return True
        else:
            return False
    def RefreshTableData(self):
        self.Clientes=self.con.AllClients()
        if self.Clientes!=False:
            rowCount=self.tableClient.rowCount()
            self.tableClient.clearContents()
            Clientes=self.Clientes[:]
            for i in range(rowCount):
                self.tableClient.removeRow(0)
            for i in range(len(Clientes)):
                self.tableClient.insertRow(i)
                self.tableClient.setItem(i,0, QTableWidgetItem( str(Clientes[i]['id'])))
                self.tableClient.setItem(i, 1, QTableWidgetItem(str(Clientes[i]['nombre'])))
                self.tableClient.setItem(i, 2, QTableWidgetItem(str(Clientes[i]['apellidos'])))
                self.tableClient.setItem(i, 3, QTableWidgetItem(str(Clientes[i]['rfc'])))
                self.tableClient.setItem(i, 4, QTableWidgetItem(str(Clientes[i]['telefono'])))
                self.tableClient.setItem(i, 5, QTableWidgetItem(str(Clientes[i]['correo'])))
                self.tableClient.setItem(i, 6, QTableWidgetItem(str(Clientes[i]['direccion'])))
            #Aqui refrescaremos la otra tabla para los créditos
            self.Todos()
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def ayudaAgregar(self):
        alert(title="Ayuda",text="Para agregar un cliente \n"
                                 "1.- Llenar el formulario\n"
                                 "2.- Hacer click en el boton 'Agregar', precionar 'Enter' o precionar 'Ctrl + a'",button="OK")
    def ayudaEditar(self):
        alert(title="Ayuda",text="Para editar la información de un cliente: \n"
                                 "1.- Seleccione el cliente a editar en la tabla \n"
                                 "2.- Modifique los datos"
                                 "3.- Hacer click en el boton 'Editar' o precionar 'Ctrl + e'",button=
              "OK")
    def ayudaEliminar(self):
        alert(title="Ayuda",text="Para eliminar un cliente: \n"
                                 "1.- Seleccione el cliente a eliminar de la tabla \n"
                                 "2.- Hacer click en el boton 'Eliminar' o precionar 'Ctrl + d'")
    def ayudaCredito(self):
        alert(title="Ayuda",text="Para otorgar un crédito a un cliente:\n"
                                 "1.- Seleccionar el cliente a otorgar el crédito de la tabla\n"
                                 "2.- Hacer click en el botón 'Crédito'\n"
                                 "3.- Llenar el formulario y dar en el botón 'OK'")
    def ayudaVigentes(self):
        alert(title='Ayuda',text='Mostrará los créditos que ahún se encuentran vigentes')
    def ayudaVencidos(self):
        alert(title='Ayuda', text='Mostrará los créditos que el periodo de vigencia ya venció')
    def ayudaPagados(self):
        alert(title='Ayuda', text='Mostrará los créditos que se encuentran con una deuda de cero pesos')
    def ayudaSinpagar(self):
        alert(title='Ayuda', text='Mostrará los créditos que tienen una deuda mayor de cero pesos')
    def ayudaTodos(self):
        alert(title='Ayuda', text='Mostrará todos los créditos que fueron otorgados')
    def buscar(self):
        if self.busqueda.text()!="":
            coincidencias = []
            keys = []
            busqueda = self.busqueda.text().lower()
            for i in range(len(self.Clientes)):
                keys.append([])
                cliente = list(self.Clientes[i].values())
                for j in range(len(cliente)):
                    keys[i].append(str(cliente[j]).lower())
                for j in range(len(keys[i])):
                    if keys[i][j].find(busqueda) != -1:
                        if i not in coincidencias:
                            coincidencias.append(i)
            for i in range(self.tableClient.rowCount()):
                self.tableClient.removeRow(0)
            for i in range(len(coincidencias)):
                self.tableClient.insertRow(i)
                self.tableClient.setItem(i, 0, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['id'])))
                self.tableClient.setItem(i, 1, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['nombre'])))
                self.tableClient.setItem(i, 2, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['apellidos'])))
                self.tableClient.setItem(i, 3, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['rfc'])))
                self.tableClient.setItem(i, 4, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['telefono'])))
                self.tableClient.setItem(i, 5, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['correo'])))
                self.tableClient.setItem(i, 6, QTableWidgetItem(str(self.Clientes[coincidencias[i]]['direccion'])))
            self.boteditar.setEnabled(False)
            self.boteliminar.setEnabled(False)
            self.botcredito.setEnabled(False)
        else:
            self.RefreshTableData()
            self.boteditar.setEnabled(False)
            self.boteliminar.setEnabled(False)
            self.botcredito.setEnabled(False)
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()
if __name__=="__main__":
    from validaciones import Valida
    from conexion import Conexion
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    gui = ViewClientes(privilegios={'clientes':'1','creditos':'1','conexion':Conexion(),'valida':Valida()})
    gui.show()
    sys.exit(app.exec())

