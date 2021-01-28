import unittest
from conexion import Conexion

class Probador(unittest.TestCase):
    def setUp(self):
        self.con=Conexion()
        self.producto={'codigo':'89787','producto':'Pruebaunitaria',
                       'grupo':'Fabrica de software','utilidades':'10','preciocompra':'15','stock':'100','preciopublico':'17'}
        self.producto2={'codigo':'867743','producto':'Pruebaunitaria2',
                        'grupo':'itzas','utilidades':'11','preciocompra':'20','stock':'100','preciopublico':'17'}
        self.producto3= {'codigo': '85788', 'producto': 'Pruebaunitaria3',
                          'grupo': '', 'utilidades': '14', 'preciocompra': '20', 'stock': '100',
                          'preciopublico': '50'}
        self.user={'nombre_usuario':'Rafael','contrasena':'122','productos':True,'inventario':True,'proveedores':True,'clientes':True,'creditos':True,'ventas':True}
        self.user2= {'nombre_usuario': 'Raudel', 'contrasena': '122', 'productos': False, 'inventario': False,'proveedores': False,'clientes': False, 'creditos': False, 'ventas': False}
        self.user3= {'nombre_usuario': 'Roberto', 'contrasena': '1245', 'productos': False, 'inventario': True,
                     'proveedores': False,
                     'clientes': False, 'creditos': True, 'ventas': True}
        self.proveedor={'nombre':'proveedor de prueba','telefono':'3788822334','direccion':'Col Las moritas'}
        self.proveedor2={'nombre':'proveedor de prueba2','telefono':'3689444','direccion':'Esq. sur las americas #23'}
        self.proveedor3={'nombre':'proveedor de prueba3','telefono':'2gg38392','direccion':'Tlaltenango sanches'}
        self.event={'proveedor':3, 'dia':'2020-03-14', 'hora':'15:00','descripcion':'Unitest'}
        self.event2={'proveedor':4, 'dia':'2020-11-18', 'hora':'23:50','descripcion':'Unitest2'}
        self.event3={'proveedor':6, 'dia':'2021-03-14', 'hora':'02:00','descripcion':'Unitest3'}
        self.cliente={'nombre':'Lorena','apellidos':'Rodriguez','rfc':'ADDE24545566','correo':'Lore@gmail.com','telefono':'346878243','direccion':''}
        self.cliente2={'nombre':'Monche','apellidos':'Perez','rfc':'AEDR3445566',
                      'correo':'Monche@gmail.com','telefono':'346878243','direccion':''}
        self.credit={'id_cliente':'34','fecha_inicio':'2020-12-12','fecha_vencimiento':'2021-12-12','descripcion_productos':'descripcion', 'adeudo':500}
        self.carrito=[self.producto,self.producto2,self.producto3]

    def test_agregaProducto(self):
        #aqui se prueba que se retorna True en caso de hacer el registro exitoso
        self.assertTrue(self.con.AddProduct(self.producto))
    def test_editaProducto(self):
        #Aqui se prueba que retorna True cuando se edita correctamente el codigo
        self.assertTrue(self.con.UpdateProduct(89787,self.producto2))
    def test_eliminaProducto(self):
        #Aqui se prueba que retorna True cuando se elimina el registro
        self.assertTrue(self.con.DeleteProduct(867743))
    def test_todosLosProductos(self):
        #aqui se prueba que se obtiene un valor no nulo y que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllProducts())
        self.assertEqual(list,type(self.con.AllProducts()))
    def test_todosLosProductosStockMinimo(self):
        # aqui se prueba que se obtiene un valor no nulo y que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllStockMinimo())
        self.assertEqual(list, type(self.con.AllStockMinimo()))
    def test_GetProductByCode(self):
        # aqui se prueba que se obtiene un valor no nulo y que el objeto es de tipo lista
        self.assertIsNotNone(self.con.GetProductByCode(667743))
        self.assertEqual(list, type(self.con.GetProductByCode(667743)))
    def test_AllProductsInCredit(self):
        # aqui se prueba que se obtiene un valor no nulo y que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllProductsInCredit(idCredit=34))
        self.assertEqual(list, type(self.con.AllProductsInCredit(idCredit=34)))
    def test_addUser(self):
        # aqui se prueba que se retorna True en caso de hacer el registro exitoso
        self.assertTrue(self.con.AddUser(self.user))
    def test_AllUsers(self):
        # aqui se prueba que se obtiene un valor no nulo y que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllUsers())
        self.assertEqual(list, type(self.con.AllUsers()))
    def test_GetUserByName(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.GetUserByName('Administrador'))
        self.assertEqual(list, type(self.con.GetUserByName('Administrador')))
    def test_UptadeUser(self):
        #se valida que retorne True en caso de que si se editó correctamente el registro
        self.assertTrue(self.con.UpdateUser(id=1,usuario=self.user3))
    def test_DeleteUser(self):
        #valida que si el registro es eliminado correctamente la función retorna True
        self.assertTrue(self.con.DeleteUser(2))
    def test_AllBodega(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllBodega())
        self.assertEqual(list, type(self.con.AllBodega()))
    def test_AllProveedores(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllProveedores())
        self.assertEqual(list, type(self.con.AllProveedores()))
    def test_AddProveedor(self):
        #se prueba que se retorna True en caso de un registro exitoso
        self.assertTrue(self.con.AddProveedor(proveedor=self.proveedor))
    def test_UpdateProveedor(self):
        # se valida que retorne True en caso de que si se editó correctamente el registro
        self.assertTrue(self.con.UpdateProveedor(id=1,proveedor=self.proveedor2))
    def test_DeleteProveedor(self):
        # valida que si el registro es eliminado correctamente la función retorna True
        self.assertTrue(self.con.DeleteProveedor(5))
    def test_AllVentas(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllVentas())
        self.assertEqual(list, type(self.con.AllVentas()))
    def test_TodayEvents(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.TodayEvents())
        self.assertEqual(list, type(self.con.TodayEvents()))
    def test_FutureEvents(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.FutureEvents())
        self.assertEqual(list, type(self.con.FutureEvents()))
    def test_DeleteEvent(self):
        #se valida que retorne True si es que se elimina el registro de evento correctamente
        self.assertTrue(self.con.DeleteEvent(id=5))
    def test_DeleteEventProveedor(self):
        # se valida que retorne True si es que se elimina el registro de evento correctamente
        self.assertTrue(self.con.DeleteEventProveedor(proveedor='Trupper'))
    def test_DeletePastEvent(self):
        #Validación que retorna True si es que se eliimina el registro de los eventos pasados correctamente
        self.assertTrue(self.con.DeletePastEvents())
    def test_AddEvent(self):
        #valida que retorna True si es que se realizó el registro correcto de un nuevo registro
        self.assertTrue(self.con.AddEvent(self.event2))
    def test_UptdateInventario(self):
        #valida que retorna True si es que se realizó la modificación de un registro
        self.assertTrue(self.con.UpdateInventario(23,self.producto3))
    def test_SurtirStock(self):
        self.assertTrue(self.con.SurtirStock(23,45,87))
    def test_Surtir(self):
        self.assertTrue(self.con.Surtir(2,43,53,16))
    def test_AllClients(self):
        # aqui se prueba que se obtiene un valor no nulo, que el objeto es de tipo lista
        self.assertIsNotNone(self.con.AllClients())
        self.assertEqual(list, type(self.con.AllClients()))
    def test_AddClient(self):
        #valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.AddClient(self.cliente2))
    def test_UpdateClient(self):
        self.assertTrue(self.con.UpdateClient(4,self.cliente))
    def test_DeleteClient(self):
        self.assertTrue(self.con.DeleteClient(4))
    def test_GetClientByID(self):
        #validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.GetClientById(4))
        self.assertEqual(list, type(self.con.GetClientById(4)))
    def test_AllCredits(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllCredits())
        self.assertEqual(list, type(self.con.AllCredits()))
    def test_AllCreditsSinPagar(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllCreditsSinpagar())
        self.assertEqual(list, type(self.con.AllCreditsSinpagar()))
    def test_AllCreditsPagados(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllCreditsPagados())
        self.assertEqual(list, type(self.con.AllCreditsPagados()))
    def test_AllCreditsVencidos(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllCreditsVencidos())
        self.assertEqual(list, type(self.con.AllCreditsVencidos()))
    def test_AllCreditsVigentes(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllCreditsVigentes())
        self.assertEqual(list, type(self.con.AllCreditsVigentes()))
    def test_AddCredit(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.AddCredit(self.credit))
    def test_Abonar(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.Abonar(id_credito=5,abono=100))
    def test_SacarProductosCredito(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.SacarProductosCredito(id_credito=5,monto=500))
    def test_AllPruebas(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.AllVentas())
        self.assertEqual(list, type(self.con.AllVentas()))
    def test_GetProductosVenta(self):
        # validamos que  retorne algo no vacio y que sea de tipo lista
        self.assertIsNotNone(self.con.GetProductosVenta(id_venta=34))
        self.assertEqual(list, type(self.con.GetProductosVenta(id_venta=34)))
    def test_Vender(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.Vender(venta=self.venta,productos=self.carrito))
    def test_GuardarProductosInCredit(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.GuardarProductsInCredit(id_credit=34,productos=self.carrito))
    def test_ReducirStock(self):
        # valida que se retorna True si es que el registro fue registrado correctamente
        self.assertTrue(self.con.reducirStock(self.carrito))
if __name__=='__main__':
    unittest.main()