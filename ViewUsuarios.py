from PyQt5.QtWidgets import  QShortcut ,QTableWidgetItem,QDialog,QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QKeySequence
from pymsgbox import *
import sys
class ViewUsuarios(QDialog):
    formValid=False
    def __init__(self,parametros={}, *args, **kwargs):
        super(ViewUsuarios, self).__init__(*args, **kwargs)
        #todos los usuarios
        self.Usuarios=[]
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        #instanciamiento de mi clase Valida
        self.valida=parametros['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"

        loadUi("Usuarios.ui",self)
        #Inicialización para los eventos de los botones
        self.boteditar.setDisabled(True)
        self.boteliminar.setDisabled(True)
        self.botagregar.clicked.connect(self.agrega)
        self.boteditar.clicked.connect(self.edita)
        self.boteliminar.clicked.connect(self.elimina)
        self.botbusqueda.clicked.connect(self.enterBuscar)
        #botones de ayuda
        self.ayudaproductos.clicked.connect(self.Ayudaproductos)
        self.ayudainventario.clicked.connect(self.Ayudainventario)
        self.ayudaproveedores.clicked.connect(self.Ayudaproveedores)
        self.ayudaclientes.clicked.connect(self.Ayudaclientes)
        self.ayudacreditos.clicked.connect(self.Ayudacreditos)
        self.ayudaventas.clicked.connect(self.Ayudaventas)
        self.ayudaagregar.clicked.connect(self.Ayudaagregar)
        self.ayudaeditar.clicked.connect(self.Ayudaeditar)
        self.ayudaeliminar.clicked.connect(self.Ayudaeliminar)
        #Inicialización de los eventos para los inputs
        self.busqueda.textChanged.connect(self.buscar)
        self.busqueda.returnPressed.connect(self.enterBuscar)
        #validación de los campos
        self.usuario.textChanged.connect(self.valUsuario)
        self.contrasena.textChanged.connect(self.valContrasena)
        #inicialización de arreglo de campos de formulario
        self.inputs=[self.usuario,self.contrasena,self.productos, self.inventario,self.proveedores,self.clientes,self.creditos,self.ventas]
        #mandamos a selección el campo de busqueda
        self.busqueda.setFocus()
        #Inicialización de los eventos de la tabla
        self.tableUsuarios.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        header = self.tableUsuarios.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        #Definiendo los atajos
        shortcut1 = QShortcut(QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        shortcut3 = QShortcut(QKeySequence("Ctrl+e"), self)
        shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.elimina)
        shortcut5 = QShortcut(QKeySequence("Ctrl+Enter"), self)
        shortcut5.activated.connect(self.agrega)
        #shortcut5 = QShortcut(QtGui.QKeySequence("Esc"), self)
        #shortcut5.activated.connect(self.close)
        self.RefreshTableData()
    def agrega(self):
        if self.valida_formulario():
            opc = confirm(text="Desea agregar " + str(self.usuario.text()) + "?", title="Agregar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                if len(self.con.GetUserByName(self.usuario.text()))<1:
                    usuario = {}
                    usuario['nombre_usuario'] = self.usuario.text()
                    usuario['contrasena'] = self.contrasena.text()
                    usuario['productos'] = self.productos.isChecked()
                    usuario['inventario']=self.inventario.isChecked()
                    usuario['proveedores']=self.proveedores.isChecked()
                    usuario['clientes']=self.clientes.isChecked()
                    usuario['creditos']=self.creditos.isChecked()
                    usuario['ventas']=self.ventas.isChecked()
                    if self.con.AddUser(usuario):
                        #alert(title="Correcto!",text="Operación correcta!")
                        for i in range(len(self.inputs)):
                            try:
                                self.inputs[i].setChecked(False)
                            except:
                                self.inputs[i].setText("")
                            self.RefreshTableData()
                    else:
                        alert(title="Error",text="Revise que el servicdor XAMPP este activo")
                else:
                    alert(title="Error!",text=('El nombre de usuario ya esta registrado'))
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def edita(self):
        if self.valida_formulario():
            row=self.tableUsuarios.currentRow()
            id=self.tableUsuarios.item(row,0).text()
            nombre_usuario=self.tableUsuarios.item(row,1).text()
            opc = confirm(text="Desea editar " + str(nombre_usuario) + "?", title="Editar?",
                          buttons=["OK", "CANCEL"])
            if opc == "OK":
                agregar=True
                if str(nombre_usuario)!=str(self.usuario.text()):
                    try:
                        if len(self.con.GetUserByName(self.usuario.text())) < 1:
                            agregar=True
                        else:
                            agregar=False
                    except:
                        pass
                if agregar:
                    usuario = {}
                    usuario['nombre_usuario'] = self.usuario.text()
                    usuario['contrasena'] = self.contrasena.text()
                    usuario['productos'] = self.productos.isChecked()
                    usuario['inventario'] = self.inventario.isChecked()
                    usuario['proveedores'] = self.proveedores.isChecked()
                    usuario['clientes'] = self.clientes.isChecked()
                    usuario['creditos'] = self.creditos.isChecked()
                    usuario['ventas'] = self.ventas.isChecked()
                    if self.con.UpdateUser(id,usuario):
                        #alert(title="Correcto!", text="Operación correcta!")
                        for i in range(len(self.inputs)):
                            try:
                                self.inputs[i].setChecked(False)
                            except:
                                self.inputs[i].setText("")
                        self.boteditar.setDisabled(True)
                        self.boteliminar.setDisabled(True)
                        self.RefreshTableData()
                    else:
                        alert(title="Error", text="Revise que el servicdor XAMPP este activo")
                else:
                    alert(title='Error!',text='Nombre de usuario ya registrado')
        else:
            alert(text='Revise el formulario', title='Error en formulario!', button='OK')
    def elimina(self):
        try:
            row = self.tableUsuarios.currentRow()
            opc=confirm(text="Desea eliminar "+str(self.tableUsuarios.item(row,1).text())+"?",title="Eliminar?",buttons=["OK","CANCEL"])
            if opc=="OK":
                id=self.tableUsuarios.item(row, 0).text()
                if self.con.DeleteUser(id)!=False:
                    #alert(title="Listo!",text="Se eliminó correctamente",button="OK")
                    for i in range(len(self.inputs)):
                        try:
                            self.inputs[i].setChecked(False)
                        except:
                            self.inputs[i].setText("")
                    self.RefreshTableData()
                    self.boteditar.setDisabled(True)
                    self.boteliminar.setDisabled(True)
                else:
                    alert(title="Error en el servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
        except:
            alert(title="Error!",text="Primero debes seleccionar una fila en la tabla", button='OK')
    def rowClicked(self):
        try:
            row= self.tableUsuarios.currentRow()
            self.inputs[0].setText(self.tableUsuarios.item(row,1).text())
            self.inputs[1].setText(self.tableUsuarios.item(row,2).text())
            for i in range(2,len(self.inputs)):
                if self.tableUsuarios.item(row,i+1).text()=="1":
                    self.inputs[i].setChecked(True)
                else:
                    self.inputs[i].setChecked(False)
            self.boteditar.setDisabled(False)
            if not(self.tableUsuarios.item(row,1).text() == "Administrador"):
                self.boteliminar.setDisabled(False)
                self.botagregar.setEnabled(True)
                self.usuario.setEnabled(True)
                self.productos.setEnabled(True)
                self.inventario.setEnabled(True)
                self.proveedores.setEnabled(True)
                self.clientes.setEnabled(True)
                self.creditos.setEnabled(True)
                self.ventas.setEnabled(True)
            else:
                self.botagregar.setEnabled(False)
                self.boteliminar.setDisabled(True)
                self.usuario.setEnabled(False)
                self.productos.setEnabled(False)
                self.inventario.setEnabled(False)
                self.proveedores.setEnabled(False)
                self.clientes.setEnabled(False)
                self.creditos.setEnabled(False)
                self.ventas.setEnabled(False)
        except:
            pass
    def valUsuario(self):
        input = self.usuario
        if len(input.text())<=100 and input.text() != "":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valContrasena(self):
        input = self.contrasena
        if len(input.text()) <= 100 and input.text() != "":
            input.setStyleSheet(self.trueValidate)
            return True
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def valida_formulario(self):
        if self.valUsuario() and self.valContrasena():
            return True
        else:
            return False
    def RefreshTableData(self):
        self.Usuarios=self.con.AllUsers()
        if self.Usuarios!=False:
            rowCount=self.tableUsuarios.rowCount()
            self.tableUsuarios.clearContents()
            usuarios=self.Usuarios
            for i in range(rowCount):
                self.tableUsuarios.removeRow(0)
            for i in range(len(usuarios)):
                self.tableUsuarios.insertRow(i)
                self.tableUsuarios.setItem(i,0, QTableWidgetItem( str(usuarios[i]['id'])))
                self.tableUsuarios.setItem(i, 1, QTableWidgetItem(str(usuarios[i]['nombre_usuario'])))
                self.tableUsuarios.setItem(i, 2, QTableWidgetItem(str(usuarios[i]['contrasena'])))
                self.tableUsuarios.setItem(i, 3, QTableWidgetItem(str(usuarios[i]['productos'])))
                self.tableUsuarios.setItem(i, 4, QTableWidgetItem(str(usuarios[i]['inventario'])))
                self.tableUsuarios.setItem(i, 5, QTableWidgetItem(str(usuarios[i]['proveedores'])))
                self.tableUsuarios.setItem(i, 6, QTableWidgetItem(str(usuarios[i]['clientes'])))
                self.tableUsuarios.setItem(i, 7, QTableWidgetItem(str(usuarios[i]['creditos'])))
                self.tableUsuarios.setItem(i, 8, QTableWidgetItem(str(usuarios[i]['ventas'])))
        else:
            alert(title="Error de servidor!",text="Asegurese que el servidor XAMPP este activo",button="OK")
    def Ayudaproductos(self):
        alert(title='Ayuda',text='El usuario con este permiso podrá acceder a la ventana de productos\n'
                                 '1.- Agregar un producto\n'
                                 '2.- Editar la información de un producto\n'
                                 '3.- Eliminar el registro de un producto')
    def Ayudainventario(self):
        alert(title='Ayuda', text='El usuario con este permiso podrá acceder a la ventana de inventario\n'
                                  '1.- Editar la información del inventario de un producto\n'
                                  '2.- Surtir stock\n'
                                  '3.- Surtir bodega')
    def Ayudaproveedores(self):
        alert(title='Ayuda', text='El usuario con este permiso podrá acceder a la ventana de proveedores\n'
                                  '1.- Agregar un proveedor\n'
                                  '2.- Editar la información de un proveedor\n'
                                  '3.- Eliminar el registro de un proveedor\n'
                                  '4.- Agendar un evento con proveedor\n'
                                  '5.- Eliminar un evento con proveedor')
    def Ayudaclientes(self):
        alert(title='Ayuda', text='El usuario con este permiso podrá acceder a la ventana de clientes\n'
                                      '1.- Agregar un cliente\n'
                                      '2.- Editar la información de un cliente\n'
                                      '3.- Eliminar el registro de un cliente\n')
    def Ayudacreditos(self):
        alert(title='Ayuda', text='El usuario con este permiso podrá acceder a la ventana de clientes\n'
                                  '1.- Asignar creditos a clientes')
    def Ayudaventas(self):
        alert(title='Ayuda', text='El usuario con este permiso podrá acceder a la ventana de ventas')
    def Ayudaagregar(self):
        alert(title="Ayuda",text='Para poder agregar un usuario nuevo y asignarle privilegios:\n'
                                 '1.- Llenar el formulario correctamente\n'
                                 '2.- Seleccionar los privilegios que el usuario tendrá'
                                 '3.- Presionar el boton "Agregar"\n'
                                 '4.- Aceptar la ventana emergente')
    def Ayudaeditar(self):
        alert(title="Ayuda", text='Para poder editar la información de un usuario nuevo junto con sus privilegios:\n'
                                  '1.- Seleccionar el usuario a editar de la tabla\n'
                                  '2.- Editar la información del usuario"\n'
                                  '3.- Seleccionar los nuevos privilegios que el usuario tendrá\n'
                                  '4.- Presionar el botón "Editar"\n'
                                  '5.- Aceptar la ventana emergente')
    def Ayudaeliminar(self):
        alert(title='ayuda',text='Para poder eliminar un usuario:\n'
                                 '1.- Seleccionar el usuario a eliminar de la tabla\n'
                                 '2.- Presionar el botón "Eliminar"\n'
                                 '3.- Aceptar la ventana emergente')
    def buscar(self):
        if self.busqueda.text()!="":
            coincidencias = []
            keys = []
            busqueda = self.busqueda.text().lower()
            for i in range(len(self.Usuarios)):
                keys.append([])
                usuario = list(self.Usuarios[i].values())
                for j in range(len(usuario)):
                    keys[i].append(str(usuario[j]).lower())
                for j in range(len(keys[i])):
                    if keys[i][j].find(busqueda) != -1:
                        if i not in coincidencias:
                            coincidencias.append(i)
            for i in range(self.tableUsuarios.rowCount()):
                self.tableUsuarios.removeRow(0)
            for i in range(len(coincidencias)):
                self.tableUsuarios.insertRow(i)
                self.tableUsuarios.setItem(i, 0, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['id'])))
                self.tableUsuarios.setItem(i, 1, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['nombre_usuario'])))
                self.tableUsuarios.setItem(i, 2, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['contrasena'])))
                self.tableUsuarios.setItem(i, 3, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['productos'])))
                self.tableUsuarios.setItem(i, 4, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['inventario'])))
                self.tableUsuarios.setItem(i, 5, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['proveedores'])))
                self.tableUsuarios.setItem(i, 6, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['clientes'])))
                self.tableUsuarios.setItem(i, 7, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['creditos'])))
                self.tableUsuarios.setItem(i, 8, QTableWidgetItem(str(self.Usuarios[coincidencias[i]]['ventas'])))
            self.boteliminar.setEnabled(False)
            self.boteditar.setEnabled(False)
        else:
            self.RefreshTableData()
            self.boteliminar.setEnabled(False)
            self.boteditar.setEnabled(False)
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()

if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from validaciones import Valida
    from conexion import *
    parametros={'conexion':Conexion(),'valida':Valida()}
    app = QApplication(sys.argv)
    gui = ViewUsuarios(parametros)
    gui.show()
    sys.exit(app.exec())
