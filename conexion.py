import pymysql
from random import randrange
class Conexion():
    def __init__(self):
        f = open('config/db.txt', 'r')
        config= f.read()
        host=''
        port=''
        user=''
        passwd=''
        if config.find('host='):
            for i in range(config.find('host=')+5,len(config)):
                if config[i]==' ':
                    pass
                elif config[i]=='\n':
                    break
                else:
                    host+=config[i]

        if config.find('port='):
            for i in range(config.find('port=')+5,len(config)):
                if config[i]==' ':
                    pass
                elif config[i]=='\n':
                    break
                else:
                    port+=config[i]
        if config.find('user='):
            for i in range(config.find('user=')+5,len(config)):
                if config[i]==' ':
                    pass
                elif config[i]=='\n':
                    break
                else:
                    user+=config[i]
        if config.find('passwd='):
            for i in range(config.find('passwd=')+7,len(config)):
                if config[i]==' ':
                    pass
                elif config[i]=='\n':
                    break
                else:
                    passwd+=config[i]
        f.close()
        print (host,port,user,passwd)
        self.conexion=False
        try:
            self.conexion = pymysql.connect(host=str(host), port=int(port), user=user, passwd=passwd,db="ferreteria_guerrero")
            if self.conexion:
                print('conectectado al host: ' + host)
        except:
            print ('no hubo conexion')
    def close(self):
        self.conexion.close()
    def AllProducts(self):
        con=self.conexion
        if con!=False:
            cursor=con.cursor()
            cursor.execute("select * from productos")
            con.commit()
            resultado=[]
            for producto in cursor.fetchall():
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock'], producto)))

            return (resultado)
        else:
            return False
    def GetProductByCode(self,code):
        con = self.conexion
        if con!=False:
            cursor = con.cursor()
            cursor.execute("select * from productos where codigo="+str(code))
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock'], producto)))

            return (resultado)
        else:
            return False
    def AddProduct(self,producto):
        con=self.conexion
        if con != False:
            cursor=con.cursor()
            cursor.execute(
                "INSERT  INTO productos (codigo,producto,grupo,utilidades,preciocompra,stock,preciopublico)VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (producto['codigo'],producto['producto'],producto['grupo'],producto['utilidades'],
                 producto['preciocompra'],producto['stock'],producto['preciopublico']))
            # Guardar cambios.
            con.commit()
            id=cursor.lastrowid

            return id
        else:
            return False
    def UpdateProduct(self,codigo,producto):
        con=self.conexion
        if con!=False:
            cursor=con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `codigo` = %s, `producto` = %s, `grupo` = %s, `utilidades` = %s, `preciocompra` = %s, `stock` = %s, `preciopublico` = %s WHERE `productos`.`codigo` = "+str(codigo),
                (producto['codigo'], producto['producto'], producto['grupo'], producto['utilidades'],producto['preciocompra'], producto['stock'], producto['preciopublico']))
            con.commit()

            return True
        else:
            return False
    def UpdateCodigoProduct(self,id,codigo):
        con=self.conexion
        if con !=False:
            cursor=con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `codigo` = %s WHERE id = " + str(
                    id),
                (codigo)
                )
            con.commit()

            return True
        else:
            return False
    def DeleteProduct(self,codigo):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("DELETE FROM `productos` WHERE `productos`.`codigo` = "+str(codigo))
            # Guardar cambios.
            con.commit()
            return True
        else:
            return False
    def AllStockMinimo(self):
        con = self.conexion
        if con!=False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `productos` WHERE stock<=stockminimo")
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(['id','codigo','producto','grupo','utilidades','preciocompra','preciopublico','stockminimo','stockmaximo','stock'], producto)))

            return (resultado)
        else:
            return False
    def AllProductsInCredit(self,idCredit):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from productos_credito where id_credito=" + str(idCredit))
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id_credito', 'producto', 'cantidad', 'precio', 'fecha'], producto)))

            return (resultado)
        else:
            return False
    def InsertProducts(self,n):
        producto={}
        for i in range(n):
            producto['codigo']=str(randrange(0,99999999999999999999))
            producto['producto']='product'+str(i)
            producto['grupo']='grupo'+str(i)
            producto['utilidades']=str(randrange(0,99999))
            producto['preciocompra']=str(randrange(0,99999))
            producto['stock']=str(randrange(0,99999))
            producto['preciopublico']=str(randrange(0,99999))
            self.AddProduct(producto)
        print ('Termine')
    def FindProducts(self,cadena):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM productos WHERE producto LIKE "%'+str(cadena)+'%" OR grupo LIKE"%'+str(cadena)+'%" OR codigo LIKE"%'+str(cadena)+'%"')
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'codigo', 'producto', 'grupo', 'utilidades', 'preciocompra', 'preciopublico', 'stockminimo',
                     'stockmaximo', 'stock'], producto)))
            return (resultado)
        else:
            return False
    def FindProducts2(self,cadena):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM productos WHERE producto LIKE "%'+str(cadena)+'%" OR grupo LIKE"%'+str(cadena)+'%"')
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'codigo', 'producto', 'grupo', 'utilidades', 'preciocompra', 'preciopublico', 'stockminimo',
                     'stockmaximo', 'stock'], producto)))
            return (resultado)
        else:
            return False
    def LastProducts(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from productos order by id desc limit 50")
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'codigo', 'producto', 'grupo', 'utilidades', 'preciocompra', 'preciopublico', 'stockminimo',
                     'stockmaximo', 'stock'], producto)))

            return (resultado)
        else:
            return False
    def GetPageProducts(self,numpage):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from productos limit "+str((int(numpage)-1)*50)+",50")
            con.commit()
            resultado = []
            for producto in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'codigo', 'producto', 'grupo', 'utilidades', 'preciocompra', 'preciopublico', 'stockminimo',
                     'stockmaximo', 'stock'], producto)))

            return (resultado)
        else:
            return False
    def GetNumProducts(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos;")
            con.commit()
            resultado=cursor.fetchall()
            return resultado[0][0]
        else:
            return False

    def AddUser(self,user):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO usuarios (nombre_usuario,contrasena,productos,inventario,proveedores,clientes,creditos,ventas)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (user['nombre_usuario'], user['contrasena'], user['productos'], user['inventario'],
                 user['proveedores'], user['clientes'], user['creditos'],user['ventas']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid

            return id
        else:
            return False
    def AllUsers(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from usuarios ORDER BY nombre_usuario ASC" )
            con.commit()
            resultado = []
            for user in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'nombre_usuario', 'contrasena', 'productos', 'inventario', 'proveedores', 'clientes',
                     'creditos', 'ventas'], user)))
            return (resultado)
        else:
            return False
    def GetUserByName(self,name):
        con = self.conexion
        if con!=False:
            cursor = con.cursor()
            cursor.execute("select * from usuarios where usuarios.nombre_usuario='"+str(name)+"'")
            con.commit()
            resultado = []
            for user in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'nombre_usuario', 'contrasena','productos','inventario','proveedores','clientes','creditos','ventas'], user)))

            return (resultado)
        else:
            return False
    def UpdateUser(self,id,usuario):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `usuarios` SET `nombre_usuario` = %s, `contrasena` = %s, `productos` = %s, `inventario` = %s, `proveedores` = %s, `clientes` = %s, `creditos` = %s, `ventas` = %s WHERE `usuarios`.`id` = " + str(
                    id),
                (usuario['nombre_usuario'], usuario['contrasena'], usuario['productos'], usuario['inventario'],
                 usuario['proveedores'], usuario['clientes'], usuario['creditos'],usuario['ventas']))
            con.commit()

            return True
        else:
            return False
    def DeleteUser(self,id):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("DELETE FROM `usuarios` WHERE `usuarios`.`id` = " + str(id))
            # Guardar cambios.
            con.commit()
            return True
        else:
            return False

    def AllProveedores(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("select * from proveedores ORDER BY nombre ASC")
            con.commit()
            resultado = []
            for proveedor in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'nombre', 'telefono', 'direccion'], proveedor)))

            return (resultado)
        else:
            return False
    def AddProveedor(self,proveedor):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO proveedores (nombre,telefono,direccion)VALUES (%s,%s,%s)",
                (proveedor['nombre'],proveedor['telefono'],proveedor['direccion']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid

            return id
        else:
            return False
    def UpdateProveedor(self,id,proveedor):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `proveedores` SET `nombre` = %s, `telefono` = %s, `direccion` = %s WHERE `proveedores`.`id` = " + str(
                    id),
                (proveedor['nombre'],proveedor['telefono'],proveedor['direccion']))
            con.commit()

            return True
        else:
            return False
    def DeleteProveedor(self,id):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("DELETE FROM `proveedores` WHERE `proveedores`.`id` = " + str(id))
            # Guardar cambios.
            con.commit()
            return True
        else:
            return False

    def AllEvents(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos`")
            con.commit()
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'],evento)))

            return (resultado)
        else:
            return False
    def TodayEvents(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos` where eventos.dia=CURDATE()")
            con.commit()
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'], evento)))

            return (resultado)
        else:
            return False
    def FutureEvents(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `eventos` where eventos.dia>CURDATE()")
            con.commit()
            resultado = []
            for evento in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'proveedor', 'dia', 'hora', 'descripcion'], evento)))

            return (resultado)
        else:
            return False
    def DeleteEvent(self,id):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`id` = " + str(id))
            except:
                return None
            # Guardar cambios.
            con.commit()

            return True
        else:
            return False
    def DeleteEventProveedor(self,proveedor):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`proveedor` = " + str(proveedor))
            except:
                return None
            # Guardar cambios.
            con.commit()

            return True
        else:
            return False
    def DeletePastEvents(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            result =cursor.execute("DELETE FROM `eventos` WHERE `eventos`.`dia` <CURDATE()")
            con.commit()

        else:
            return False
    def AddEvent(self,evento):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO eventos (proveedor,dia,hora,descripcion)VALUES (%s,%s,%s,%s)",
                (evento['proveedor'], evento['dia'], evento['hora'],evento['descripcion']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid

            return id
        else:
            return False

    def UpdateInventario(self,codigo,producto):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `stockminimo` = %s, `stockmaximo` = %s, `stock` = %s WHERE `productos`.`codigo` = " + str(
                    codigo),
                (producto['stockminimo'], producto['stockmaximo'], producto['stock']))
            con.commit()

            return True
        else:
            return False
    def Surtir(self,codigo,preciocompra,preciopublico,stock):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `productos` SET `preciocompra` = %s,`preciopublico`=%s, `stock` = %s WHERE `productos`.`codigo` = " + str(
                    codigo),
                (preciocompra,preciopublico, stock))
            con.commit()

            return True
        else:
            return False

    def AllClients(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `clientes` ORDER BY nombre ASC")
            con.commit()
            resultado = []
            for cliente in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'nombre', 'apellidos', 'rfc', 'correo','telefono','direccion'], cliente)))

            return (resultado)
        else:
            return False
    def AddClient(self,cliente):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO clientes (nombre,apellidos,rfc,correo,telefono,direccion)VALUES (%s,%s,%s,%s,%s,%s)",
                (cliente['nombre'], cliente['apellidos'], cliente['rfc'], cliente['correo'],cliente['telefono'],cliente['direccion']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid

            return id
        else:
            return False
    def UpdateClient(self,id,cliente):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `clientes` SET `nombre` = %s, `apellidos` = %s, `rfc` = %s, `correo` = %s, `telefono` = %s,`direccion` = %s  WHERE `clientes`.`id` = " + str(id),
                (cliente['nombre'], cliente['apellidos'], cliente['rfc'], cliente['correo'],cliente['telefono'],cliente['direccion']))
            con.commit()

            return True
        else:
            return False
    def DeleteClient(self,id):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `clientes` WHERE `clientes`.`id` = " + str(id))
            except:
                return None
            # Guardar cambios.
            con.commit()

            return True
        else:
            return False
    def GetClientById(self,id):
        con = self.conexion
        cursor = con.cursor()
        cursor.execute("select * from clientes where id=" + str(id))
        con.commit()
        resultado = []
        for client in cursor.fetchall():
            resultado.append(dict(zip(
                ['id', 'nombre', 'apellidos', 'rfc', 'correo', 'telefono','direccion'], client)))

        return (resultado)

    def AllCredits(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `creditos`")
            con.commit()
            resultado = []
            for credito in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'idcliente', 'fechainicio', 'fechavencimiento', 'descripcionproductos', 'adeudo'], credito)))

            return (resultado)
        else:
            return False
    def AllCreditsSinpagar(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `creditos` WHERE `adeudo`>0")
            con.commit()
            resultado = []
            for credito in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'idcliente', 'fechainicio', 'fechavencimiento', 'descripcionproductos', 'adeudo'],
                    credito)))

            return (resultado)
        else:
            return False
    def AllCreditsPagados(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `creditos` WHERE `adeudo`=0")
            con.commit()
            resultado = []
            for credito in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'idcliente', 'fechainicio', 'fechavencimiento', 'descripcionproductos', 'adeudo'],
                    credito)))

            return (resultado)
        else:
            return False
    def AllCreditsVencidos(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `creditos` WHERE fecha_vencimiento<CURDATE()")
            con.commit()
            resultado = []
            for credito in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'idcliente', 'fechainicio', 'fechavencimiento', 'descripcionproductos', 'adeudo'],
                    credito)))

            return (resultado)
        else:
            return False
    def AllCreditsVigentes(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `creditos` WHERE fecha_inicio<=CURDATE() AND CURDATE()<fecha_vencimiento")
            con.commit()
            resultado = []
            for credito in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'idcliente', 'fechainicio', 'fechavencimiento', 'descripcionproductos', 'adeudo'],
                    credito)))

            return (resultado)
        else:
            return False
    def AddCredit(self,credito):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "INSERT  INTO creditos (id_cliente,fecha_inicio,fecha_vencimiento,descripcion_productos,adeudo)VALUES (%s,%s,%s,%s,%s)",
                (credito['id_cliente'], credito['fecha_inicio'], credito['fecha_vencimiento'], credito['descripcion_productos'], credito['adeudo']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid

            return id
        else:
            return False
    def Abonar(self,id_credito,abono):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `creditos` SET `adeudo` = `adeudo`- %s  WHERE `creditos`.`id` = " + str(
                    id_credito),
                (str(abono)))
            con.commit()

            return True
        else:
            return False
    def SacarProductosCredito(self,id_credito,monto):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE `creditos` SET `adeudo` = `adeudo`+ %s  WHERE `creditos`.`id` = " + str(
                    id_credito),
                (str(monto)))
            con.commit()

            return True
        else:
            return False
    def DeleteCredits(self,id_cliente):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            try:
                cursor.execute("DELETE FROM `creditos` WHERE `creditos`.`id_cliente` = " + str(id_cliente))
            except:
                return None
            # Guardar cambios.
            con.commit()

            return True
        else:
            return False

    def AllVentas(self):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `ventas`")
            con.commit()
            resultado = []
            for venta in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'usuario', 'cliente', 'tipodeventa', 'metododepago', 'fecha','importe','pago','cambio'], venta)))

            return (resultado)
        else:
            return False
    def VentasByDate(self,date):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute('SELECT * FROM `ventas` WHERE fecha LIKE "'+str(date)+'"')
            con.commit()
            resultado = []
            for venta in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'usuario', 'cliente', 'tipodeventa', 'metododepago', 'fecha', 'importe', 'pago', 'cambio'],
                    venta)))

            return (resultado)
        else:
            return False
    def GetProductosVenta(self,id_venta):
        con = self.conexion
        cursor = con.cursor()
        cursor.execute("select * from productos_ventas where id_venta=" + str(id_venta))
        con.commit()
        resultado = []
        for producto in cursor.fetchall():
            resultado.append(dict(zip(
                ['id_venta', 'producto', 'cantidad', 'precio'], producto)))

        return (resultado)
    def GetVenta(self,id_venta):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `ventas` where id="+str(id_venta))
            con.commit()
            resultado = []
            for venta in cursor.fetchall():
                resultado.append(dict(zip(
                    ['id', 'usuario', 'cliente', 'tipodeventa', 'metododepago', 'fecha', 'importe', 'pago', 'cambio'],
                    venta)))

            return (resultado[0])
        else:
            return False

    def Vender(self,venta,productos):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            #hacemos el registro de la venta
            cursor.execute(
                "INSERT  INTO ventas (usuario,cliente,tipodeventa,metododepago,fecha,importe,pago,cambio)VALUES (%s,%s,%s,%s,CURDATE(),%s,%s,%s)",
                (venta['usuario'],venta['cliente'], venta['tipoventa'], venta['metodopago'], venta['montototal'], venta['pago'], venta['cambio']))
            # Guardar cambios.
            con.commit()
            id = cursor.lastrowid
            for producto in productos:
                #registramos los productos vendidos
                cursor.execute(
                    "INSERT  INTO productos_ventas (id_venta,producto,cantidad,precio)VALUES (%s,%s,%s,%s)",
                    (id, producto['producto'], producto['cantidad'], producto['precio']))
                # Guardar cambios.
                con.commit()
                #reducimos el stock de los productos vendidos
                cursor.execute(
                        "UPDATE `productos` SET `stock` = %s  WHERE `productos`.`codigo` = " + str(producto['codigo']),(str(producto['stock'])))
                con.commit()

            return id
        else:
            return False
    def GuardarProductsInCredit(self,id_credit,productos):
        con = self.conexion
        if con != False:
            cursor = con.cursor()
            for producto in productos:
                cursor.execute(
                    "INSERT  INTO productos_credito (id_credito,producto,cantidad,precio,fecha)VALUES (%s,%s,%s,%s,CURDATE())",
                    (id_credit, producto['producto'], producto['cantidad'], producto['precio']))
                # Guardar cambios.
                con.commit()

            return True
        else:
            return False

if __name__=="__main__":
    from datetime import datetime
    con=Conexion()
    #print (con.GetProductByCode(6675))
    users=con.AllClients()
    for user in users:
        print (user)
