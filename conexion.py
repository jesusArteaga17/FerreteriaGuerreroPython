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
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock','bodega'], producto)))
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
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock','bodega'], producto)))
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
    def AllBodega(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `productos` WHERE bodega<stockminimo")
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'codigo', 'producto', 'grupo', 'utilidades', 'preciocompra', 'preciopublico', 'stockminimo',
                     'stockmaximo', 'stock', 'bodega'], producto)))
            con.close()
            return (resultado)
        else:
            return False
    def AllProveedores(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from proveedores")
            resultado = []
            for proveedor in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'nombre', 'telefono', 'direccion'], proveedor)))
            con.close()
            return (resultado)
        else:
            return False
    def AddProveedor(self,proveedor):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO proveedores (nombre,telefono,direccion)VALUES (%s,%s,%s)",
                (proveedor['nombre'],proveedor['telefono'],proveedor['direccion']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid
            con.close()
            return id
        else:
            return False
    def UpdateProveedor(self,id,proveedor):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `proveedores` SET `nombre` = %s, `telefono` = %s, `direccion` = %s WHERE `proveedores`.`id` = " + str(
                    id),
                (proveedor['nombre'],proveedor['telefono'],proveedor['direccion']))
            con.commit()
            con.close()
            return True
        else:
            return False
    def DeleteProveedor(self,id):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("DELETE FROM `proveedores` WHERE `proveedores`.`id` = " + str(id))
            # Guardar cambios.
            con.commit()
            return True
        else:
            return False

    def AllEvents(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos`")
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'],evento)))
            con.close()
            return (resultado)
        else:
            return False
    def TodayEvents(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos` where eventos.dia=CURDATE()")
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'], evento)))
            con.close()
            return (resultado)
        else:
            return False
    def FutureEvents(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos` where eventos.dia>CURDATE()")
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'], evento)))
            con.close()
            return (resultado)
        else:
            return False
    def DeleteEvent(self,id):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`id` = " + str(id))
            except:
                return None
            # Guardar cambios.
            con.commit()
            con.close()
            return True
        else:
            return False
    def DeleteEventProveedor(self,proveedor):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`proveedor` = " + str(proveedor))
            except:
                return None
            # Guardar cambios.
            con.commit()
            con.close()
            return True
        else:
            return False
    def DeletePastEvents(self):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            result =cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`dia` <CURDATE()")
            con.commit()
            con.close()
        else:
            return False
    def AddEvent(self,evento):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO eventos (proveedor,dia,hora,descripcion)VALUES (%s,%s,%s,%s)",
                (evento['proveedor'], evento['dia'], evento['hora'],evento['descripcion']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid
            con.close()
            return id
        else:
            return False

    def UpdateInventario(self,codigo,producto):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `stockminimo` = %s, `stockmaximo` = %s, `stock` = %s, `bodega` = %s WHERE `productos`.`codigo` = " + str(
                    codigo),
                (producto['stockminimo'], producto['stockmaximo'], producto['stock'], producto['bodega']))
            con.commit()
            con.close()
            return True
        else:
            return False
    def SurtirStock(self,codigo,stock,bodega):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `stock` = %s, `bodega` = %s WHERE `productos`.`codigo` = " + str(
                    codigo),
                (stock,bodega))
            con.commit()
            con.close()
            return True
        else:
            return False
    def Surtir(self,codigo,preciocompra,bodega):
        con = self.conect()
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `preciocompra` = %s, `bodega` = %s WHERE `productos`.`codigo` = " + str(
                    codigo),
                (preciocompra, bodega))
            con.commit()
            con.close()
            return True
        else:
            return False
if __name__=="__main__":
    con=Conexion()
    #producto={'codigo':'26749433','producto':"basinilla",'descuento':'7','stockminimo':'23','stockmaximo':'50','precio':'67.7','existencia':'24','grupo':'basinillas'       }
    #p=con.AddProduct(producto)
    #producto={'codigo': '3827', 'producto': 'yanobandera', 'grupo': '', 'utilidades': '0.0', 'preciocompra': '0.0', 'stock': '0.0', 'preciopublico': '0.0'}
    #proveedor={'nombre':'hola','telefono':'3456789','direccion':'simona la mona'}
    #eventos=con.FutureEvents()
    #for evento in eventos:
    #    print (evento)
    #print (res)
    #evento={'proveedor': 'jejes', 'dia': "2020-10-02", 'hora': "0", 'descripcion': 'otra2'}
    #con.AddEvent(evento)
    print (con.AllBodega())