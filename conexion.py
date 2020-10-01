import pymysql
class Conexion():
    def conect(self):
        try:
            con = pymysql.connect(
                host="localhost", port=3306, user="root",
                passwd="", db="ferreteria_guerrero"
            )
            return con
        except:
            print ("Algo salio mal al tratar de conectar a base de datos")
            return False
    def AllProducts(self):
        con=self.conect()
        if con!=False:
            cursor=con.cursor()
            cursor.execute("select * from productos")
            resultado=[]
            for producto in cursor.fetchall():
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','existencia'], producto)))
            con.close()
            return (resultado)
        else:
            return False
    def GetProductByCode(self,code):
        con = self.conect()
        if con!=False:
            cursor = con.cursor()
            cursor.execute("select * from productos where codigo="+str(code))
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','existencia'], producto)))
            con.close()
            return (resultado)
        else:
            return False
    def AddProduct(self,producto):
        con=self.conect()
        if con != False:
            cursor=con.cursor()
            cursor.execute(
                "INSERT  INTO productos (codigo,producto,grupo,utilidades,preciocompra,stock,preciopublico)VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (producto['codigo'],producto['producto'],producto['grupo'],producto['utilidades'],
                 producto['preciocompra'],producto['stock'],producto['preciopublico']))
            # Guardar cambios.
            con.commit()
            id=cursor.lastrowid
            con.close()
            return id
        else:
            return False
    def UpdateProduct(self,codigo,producto):
        con=self.conect()
        if con!=False:
            cursor=con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `codigo` = %s, `producto` = %s, `grupo` = %s, `utilidades` = %s, `preciocompra` = %s, `stock` = %s, `preciopublico` = %s WHERE `productos`.`codigo` = "+str(codigo),
                (producto['codigo'], producto['producto'], producto['grupo'], producto['utilidades'],producto['preciocompra'], producto['stock'], producto['preciopublico']))
            con.commit()
            con.close()
            return True
        else:
            return False
    def UpdateCodigoProduct(self,id,codigo):
        con=self.conect()
        if con !=False:
            cursor=con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `codigo` = %s WHERE id = " + str(
                    id),
                (codigo)
                )
            con.commit()
            con.close()
            return True
        else:
            return False
    def DeleteProduct(self,codigo):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("DELETE FROM `productos` WHERE `productos`.`codigo` = "+str(codigo))
            # Guardar cambios.
            con.commit()
            return True
        else:
            return False
    def AllStockMinimo(self):
        con = self.conect()
        if con!=False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `productos` WHERE stock<=stockminimo")
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock'], producto)))
            con.close()
            return (resultado)
        else:
            return False
    def AllUsers(self):
        con = self.conect()
        cursor = con.cursor()
        cursor.execute("select * from usuarios")
        resultado = []
        for producto in cursor.fetchall():
            resultado.append(dict(zip(
                ['id', 'nombre', 'apellidos', 'numcontrol', 'telefono', 'correo'], producto)))
        con.close()
        return (resultado)
    def GetUserById(self,id):
        con = self.conect()
        cursor = con.cursor()
        cursor.execute("select * from usuarios where id="+str(id))
        resultado = []
        for producto in cursor.fetchall():
            resultado.append(dict(zip(
                ['id', 'nombre', 'apellidos', 'numcontrol', 'telefono', 'correo'], producto)))
        con.close()
        return (resultado)
if __name__=="__main__":
    con=Conexion()
    #producto={'codigo':'26749433','producto':"basinilla",'descuento':'7','stockminimo':'23','stockmaximo':'50','precio':'67.7','existencia':'24','grupo':'basinillas'       }
    #p=con.AddProduct(producto)
    producto={'codigo': '3827', 'producto': 'yanobandera', 'grupo': '', 'utilidades': '0.0', 'preciocompra': '0.0', 'stock': '0.0', 'preciopublico': '0.0'}
    print (con.AddProduct(producto))