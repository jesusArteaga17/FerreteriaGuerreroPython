from PyQt5.QtWidgets import  QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from conexion import Conexion
from pymsgbox import *
from datetime import datetime

class EmergenteCreditos(QDialog):
    def __init__(self, id_cliente=None,*args, **kwargs):
        super(EmergenteCreditos, self).__init__(*args, **kwargs)
        loadUi("Emergente_creditos.ui", self)
        #inicializamos el objeto conexion y el de datetime
        self.con=Conexion()
        self.date=datetime.now()
        #conectamos a los botones aceptar con su funcion
        self.botonok.clicked.connect(self.aceptar)
        self.botoncancelar.clicked.connect(self.close)
        #Mandamos al campo fecha la fecha correspondiente al sistema
        today=QDate(self.date.year,self.date.month,self.date.day)
        self.fechainicio.setDate(today)
        self.fechavencimiento.setDate(today)
        self.id_cliente=id_cliente
    def aceptar(self):
        if self.validaFormulario():
            fechainicio="%s-%s-%s" % ( self.fechainicio.date().year(), self.fechainicio.date().month(),self.fechainicio.date().day())
            fechavencimiento= "%s-%s-%s" % (self.fechavencimiento.date().year(), self.fechavencimiento.date().month(), self.fechavencimiento.date().day())
            credito={}
            credito['id_cliente']=str(self.id_cliente)
            credito['fecha_inicio']=fechainicio
            credito['fecha_vencimiento']=fechavencimiento
            credito['descripcion_productos']=self.descripcionproductos.toPlainText()
            credito['adeudo']="0"
            if self.con.AddCredit(credito):
                alert(title="Correcto!",text="La transacción ha sido exitosa!")
                self.close()
            else:
                alert(title="Error!",text="La operación no se pudo realizar correctamente")
        else:
            #print ('no se cumplieron con los requisitos')
            alert(title="Error",text="Revise coherencia con las fechas \nNo se puede ingresar más de 500 caracteres en la descripción",button="OK")
    def validaFormulario(self):
        ban=True
        if len(self.descripcionproductos.toPlainText())>=500:
            ban=False
        fechainicio=self.fechainicio.date()
        if fechainicio.year()<self.date.year:
            ban=False
        elif fechainicio.year()==self.date.year:
            if fechainicio.month()<self.date.month:
                ban=False
            elif fechainicio.month()==self.date.month:
                if fechainicio.day()<self.date.day:
                    ban=False
        fechavencimiento=self.fechavencimiento.date()
        if int(fechavencimiento.year())<int(fechainicio.year()):
            ban=False
        elif int(fechavencimiento.year())==int(fechainicio.year()):
            if int(fechavencimiento.month())<int(fechainicio.month()):
                ban=False
            elif int(fechavencimiento.month())==int(fechainicio.month()):
                if int(fechavencimiento.day())<int(fechainicio.day()):
                    ban=False
        return ban
if __name__=="__main__":
    app = QApplication(sys.argv)
    gui = EmergenteCreditos(id_cliente="3")
    gui.show()
    sys.exit(app.exec())