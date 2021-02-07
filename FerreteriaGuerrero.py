from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.uic import loadUi
from index import Index
from pymsgbox import alert
from conexion import Conexion
import sys
class Login(QMainWindow):
    def __init__(self,conexion,*args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        loadUi("Login.ui", self)
        #inicializamos el objeto conexion
        self.con=conexion
        #conectamos a los botones aceptar con su funcion
        self.loguear.clicked.connect(self.aceptar)
        self.usuario.returnPressed.connect(self.aceptar)
        self.contrasena.returnPressed.connect(self.aceptar)
    def aceptar(self):
        usuario=self.usuario.text()
        contrasena=self.contrasena.text()
        try:
            user=self.con.GetUserByName(usuario)
            if len(user)==1:
                #no borrar esta linea ya que agarra el primer elemento de la consulta anterior
                user=user[0]
                #print(user)
                if user['contrasena']==contrasena:
                    self.usuario.setText('')
                    self.contrasena.setText('')
                    argumentos={}
                    argumentos['user']=user
                    argumentos['conexion']=self.con
                    view = Index(argumentos, self)
                    view.show()
                    self.close()
                else:
                    alert(title="Error",text="Contraseña incorrecta")
            else:
                alert(title="Error!",text='Usuario no registrado')
        except:
            alert(title='Error!',text='Revise que el servidor XAMPP esté activo')
            self.close()
if __name__=='__main__':
    acceso=False
    con=Conexion()
    if con.conexion:
        app = QApplication(sys.argv)
        gui = Login(con)
        gui.show()
        sys.exit(app.exec())
    else:
        alert(title='Error!', text='Revise que el servidor XAMPP esté activo y que la configuración\n'
                                   'de el archivo de la carpeta config "db.tx" este correcto')
