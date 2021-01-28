from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from pymsgbox import *
class EmergenteAgendar2(QDialog):
    def __init__(self, parametros,*args, **kwargs):
        super(EmergenteAgendar2, self).__init__(*args, **kwargs)
        uic.loadUi("Emergente_agendar2.ui", self)
        #inicializamos el objeto conexion
        self.con=parametros['conexion']
        #conectamos a los botones aceptar con su funcion
        self.buttonBox.accepted.connect(self.aceptar)
        self.dia=parametros['dia']
        res=self.con.AllProveedores()
        proveedores=[]
        for proveedor in res:
            proveedores.append(proveedor['nombre'])
        self.proveedores.addItems(proveedores)
        self.registro=None
    def aceptar(self):
        descripcion=self.descripcion.toPlainText()
        if len(descripcion)<200:
            evento={}
            evento['proveedor']=str(self.proveedores.currentText())
            evento['dia']=self.dia
            evento['hora']="%s:%s"%(self.hora.time().hour(),self.hora.time().minute())
            evento['descripcion']=self.descripcion.toPlainText()
            #print (evento)
            if not self.con.AddEvent(evento):
                alert(title="Error", text="Asegurese que el servidor XAMPP esté encendido", button="OK")
                self.registro=False
            else:
                self.registro=True
        else:
            alert(title="Error",text="No se puede ingresar más de 200 caracteres en la descripción",button="OK")
if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from conexion import Conexion
    app = QApplication(sys.argv)
    gui = EmergenteAgendar2(parametros={'dia':'2020-10-10','conexion':Conexion()})
    gui.show()
    sys.exit(app.exec())