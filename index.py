from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from pymsgbox import *
from ViewProductos import ViewProductos
from ViewInventario import ViewInventario
from ViewProveedores import ViewProveedores
from ViewClientes import ViewClientes
from ViewUsuarios import ViewUsuarios
from ViewVentas import ViewVentas
from validaciones import Valida
import sys
class Index(QMainWindow):
    formValid=False
    def __init__(self,parametros={},*args, **kwargs):
        self.user=parametros['user']
        super().__init__(*args, **kwargs)
        loadUi("MainWindowAdmin.ui",self)
        self.botonProductos.setEnabled(int(self.user['productos']))
        self.botonInventario.setEnabled(int(self.user['inventario']))
        self.botonProveedores.setEnabled(int(self.user['proveedores']))
        self.botonClientes.setEnabled(int(self.user['clientes'])or int(self.user['creditos']))
        if self.user['nombre_usuario']=="Administrador":
            self.botonUsuarios.setEnabled(True)
        else:
            self.botonUsuarios.setEnabled(False)
        self.botonVentas.setEnabled(int(self.user['ventas']))
        self.botonProductos.clicked.connect(self.showProductos)
        self.botonInventario.clicked.connect(self.showInventario)
        self.botonProveedores.clicked.connect(self.showProveedores)
        self.botonClientes.clicked.connect(self.showClientes)
        self.botonUsuarios.clicked.connect(self.showUsuarios)
        self.botonVentas.clicked.connect(self.showVentas)
        self.botonSalir.clicked.connect(self.close)
        self.parametros=parametros
        #self.parametros['conexion']=Conexion()
        self.parametros['valida']=Valida()
        self.parametros['usuario']=self.user['nombre_usuario']
        #print (user)
        self.firstCloseEvent=False
    def closeEvent(self, event):
        if self.firstCloseEvent:
            opc=confirm(title='Salir?',text='Desea cerrar la ventana?',buttons=['Si','No'])
            if opc=='Si':
                self.parametros['conexion'].close()
                event.accept()
            else: event.ignore()
        else:
            self.firstCloseEvent=True
            event.ignore()
    def showProductos(self):
        view=ViewProductos(self.parametros,self)
        view.show()
    def showInventario(self):
        view = ViewInventario(self.parametros,self)
        view.show()
    def showProveedores(self):
        view = ViewProveedores(self.parametros,self)
        view.show()
    def showClientes(self):

        permisos={'clientes':self.user['clientes'],'creditos':self.user['creditos']}
        permisos['conexion']=self.parametros['conexion']
        permisos['valida']=self.parametros['valida']
        view = ViewClientes(permisos,self)
        view.show()
    def showUsuarios(self):
        view = ViewUsuarios(self.parametros,self)
        view.show()
    def showVentas(self):
        view = ViewVentas(self.parametros,self)
        view.show()
if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from conexion import Conexion
    usuario={'nombre_usuario':'Administrador', 'contrasena':'777777', 'productos':'1', 'inventario':'1','proveedores':'1','clientes':'1','creditos':'1','ventas':'1'}
    app = QApplication(sys.argv)
    argumentos={}
    argumentos['user']=usuario
    argumentos['conexion']=Conexion()
    gui = Index(argumentos)
    gui.show()
    sys.exit(app.exec())
