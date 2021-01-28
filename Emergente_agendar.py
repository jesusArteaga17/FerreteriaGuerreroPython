from PyQt5.QtWidgets import  QDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate
from pymsgbox import *
from datetime import datetime

class EmergenteAgendar(QDialog):
    def __init__(self, parametros,*args, **kwargs):
        super(EmergenteAgendar, self).__init__(*args, **kwargs)
        uic.loadUi("emergente_agendar.ui", self)
        #inicializamos el objeto conexion y el de datetime
        self.con=parametros['conexion']
        self.date=datetime.now()
        #conectamos a los botones aceptar con su funcion
        self.buttonBox.accepted.connect(self.aceptar)
        #Mandamos al campo fecha la fecha correspondiente al sistema
        today=QDate(self.date.year,self.date.month,self.date.day)
        self.dia_agendar.setDate(today)
        self.proveedor=parametros['proveedor']
        self.registro=None
    def aceptar(self):
        if self.validaFormulario():
            fecha="%s-%s-%s" % ( self.dia_agendar.date().year(), self.dia_agendar.date().month(),self.dia_agendar.date().day())
            hora="%s:%s"%(self.hora_agendar.time().hour(),self.hora_agendar.time().minute())
            evento={}
            evento['proveedor']=self.proveedor
            evento['dia']=fecha
            evento['hora']=hora
            evento['descripcion']=self.descripcion_agendar.toPlainText()
            if self.con.AddEvent(evento):
                self.registro=True
            else:
                self.registro=False
        else:
            #print ('no se cumplieron con los requisitos')
            alert(title="Error",text="No se puede ingresar una fecha que ya pasó \nNo se puede ingresar más de 200 caracteres en la descripción",button="OK")
    def validaFormulario(self):
        ban=True
        if len(self.descripcion_agendar.toPlainText())>200:
            ban=False
        dia_agendar=self.dia_agendar.date()
        if dia_agendar.year()<self.date.year:
            ban=False
        elif dia_agendar.year()==self.date.year:
            if dia_agendar.month()<self.date.month:
                ban=False
            elif dia_agendar.month()==self.date.month:
                if dia_agendar.day()<self.date.day:
                    ban=False
        return ban
if __name__=="__main__":
    from PyQt5.QtWidgets import QApplication
    from conexion import Conexion
    app = QApplication(sys.argv)
    gui = EmergenteAgendar(parametros={'proveedor':"nommscompa",'conexion':Conexion()})
    gui.show()
    sys.exit(app.exec())