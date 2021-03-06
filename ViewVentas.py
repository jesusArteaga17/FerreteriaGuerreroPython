from os import startfile
from PyQt5.QtWidgets import QTableWidgetItem,QMainWindow,QHeaderView,QShortcut,QMenu,QAction,QActionGroup,QAbstractItemView
from PyQt5.QtGui import QKeySequence
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from pymsgbox import *
from datetime import datetime
from Abonar import ViewAbonar
from Historial import ViewHistorial
import sys
class ViewVentas(QMainWindow):
    formValid=False
    def __init__(self,parametros={}, *args, **kwargs):
        self.parametros=parametros
        super(ViewVentas, self).__init__(*args, **kwargs)
        loadUi("Ventas.ui",self)
        #instanciamos el objeto de conexion a base de datos
        self.con=parametros['conexion']
        #instanciamiento de mi clase Valida
        self.valida=parametros['valida']
        #Características de los imputs cuando son validados
        self.trueValidate="border: 2px solid green; font-size: 15px;"
        self.falseValidate="border: 2px solid red; font-size: 15px;"
        #Inicialización para los eventos de los botones
        self.busqueda.returnPressed.connect(self.buscar)
        #inicialización del evento para returnpressed de cantidad
        self.cantidad.textChanged.connect(self.validaCantidad)
        self.cantidad.returnPressed.connect(self.enterCantidad)
        self.pago.textChanged.connect(self.validaPago)
        self.pago.returnPressed.connect(self.vender)
        #eventos para el cambio de modo de pago
        self.radiocredito.clicked.connect(self.clickedradiocredito)
        self.radioventaabierta.clicked.connect(self.clickedradioventaabierta)
        #evento de seleccion de carro
        self.carritos.currentIndexChanged.connect(self.elegirCarro)
        self.carritos.setEnabled(False)
        #Eventos de los botones
        self.botbusqueda.clicked.connect(self.buscar)
        self.botguardar.clicked.connect(self.guardar)
        self.botquitar.clicked.connect(self.quitarproducto)
        self.botabonar.clicked.connect(self.abonar)
        self.bothistorial.clicked.connect(self.historial)
        self.botvender.clicked.connect(self.vender)
        self.botcancelar.clicked.connect(self.cancelar)
        self.ayudaabonar.clicked.connect(self.ayudaAbonar)
        self.ayudaguardar.clicked.connect(self.ayudaGuardarCarro)
        self.ayudahistorial.clicked.connect(self.ayudaHistorial)
        self.ayudaquitar.clicked.connect(self.ayudaQuitarProducto)
        self.botimprimir.clicked.connect(self.imprime)
        #mandamos a selección el campo de busqueda
        self.busqueda.setFocus()
        #Inicialización de los eventos de la tabla
        #self.tableventas.itemSelectionChanged.connect(self.rowClicked)
        self.tableventas.clicked.connect(self.rowClicked)
        #configuracion de la cabecera de mi tabla
        self.usuario=parametros['usuario']
        self.labelusuario.setText(parametros['usuario'][0:20])
        header = self.tableventas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        # configuacion del manu contextual
        self.tableventas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableventas.customContextMenuRequested.connect(self.menuContextual)
        # Deshabilitar edición
        self.tableventas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tableventas.setDragDropOverwriteMode(False)
        # Seleccionar toda la fila
        self.tableventas.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tableventas.setSelectionMode(QAbstractItemView.SingleSelection)
        # Especifica dónde deben aparecer los puntos suspensivos "..." cuando se muestran
        # textos que no encajan
        self.tableventas.setTextElideMode(Qt.ElideRight)  # Qt.ElideNone
        # Establecer el ajuste de palabras del texto
        self.tableventas.setWordWrap(False)
        # Deshabilitar clasificación
        self.tableventas.setSortingEnabled(False)
        self.clientes=self.con.AllClients()
        for i in range(len(self.clientes)):
            self.cliente.insertItem(0,self.clientes[i]['nombre']+' '+self.clientes[i]['apellidos'])
        #verificando si existen creditos vigentes
        creditos=self.con.AllCreditsVigentes()
        if len(creditos)>0:
            self.radiocredito.setEnabled(True)
        #Definiendo los atajos
        shortcut1 = QShortcut(QKeySequence("Ctrl+b"), self)
        shortcut1.activated.connect(self.setFocusBuscar)
        #shortcut3 = QShortcut(QtGui.QKeySequence("Ctrl+e"), self)
        #shortcut3.activated.connect(self.edita)
        shortcut4 = QShortcut(QKeySequence("Ctrl+d"), self)
        shortcut4.activated.connect(self.quitarproducto)
        shortcut5 = QShortcut(QKeySequence("Ctrl+s"), self)
        shortcut5.activated.connect(self.guardar)
        shortcut6 = QShortcut(QKeySequence("Ctrl+h"), self)
        shortcut6.activated.connect(self.historial)
        shortcut7 = QShortcut(QKeySequence("Esc"), self)
        shortcut7.activated.connect(self.cancelar)
        self.carrito=[]
        self.colacarritos={}
        self.montototal=0
        self.estabuscando=False
    def menuContextual(self, posicion):
        indices = self.tableventas.selectedIndexes()
        if indices and not self.estabuscando:
            menu = QMenu()
            itemsGrupo = QActionGroup(self)
            itemsGrupo.setExclusive(True)
            menu.addAction(QAction("Eliminar", itemsGrupo))
            itemsGrupo.triggered.connect(self.quitarproducto)
            menu.exec_(self.tableventas.viewport().mapToGlobal(posicion))
    def imprime(self):
        """Funcion para imprimir un ticket de prueba"""
        venta = {}
        venta['tipoventa'] = ''
        venta['metodopago'] = ''
        venta['pago'] = '0'
        venta['cambio'] = '0'
        venta['cliente'] = ''
        venta['metodopago'] = ''
        venta['usuario'] = self.usuario
        venta['montototal'] = '0'
        texto = self.hacerTicket(0000000, venta, carrito=[])
        # print('imprimiendo ticket')
        f = open('Ticket.txt', 'w+')
        f.write(texto)
        f.close()
        startfile('Ticket.txt', 'print')
    def clickedradioventaabierta(self):
        self.cliente.clear()
        self.clientes = self.con.AllClients()
        self.cliente.insertItem(0,"Público en general")
        for i in range(len(self.clientes)):
            self.cliente.insertItem(0, self.clientes[i]['nombre'] + ' ' + self.clientes[i]['apellidos'])
    def clickedradiocredito(self):
        self.cliente.clear()
        credits = self.con.AllCreditsVigentes()
        self.clientes=[]
        for i in range(len(credits)):
            cliente=self.con.GetClientById(credits[i]['idcliente'])
            self.clientes.append(cliente[0])
        for i in range(len(self.clientes)):
            self.cliente.insertItem(0,str(credits[i]['id'])+'.-'+ self.clientes[i]['nombre'] + ' ' + self.clientes[i]['apellidos'])
    def cancelar(self):
        if self.botcancelar.isEnabled():
            self.botcancelar.setEnabled(False)
            self.tableventas.setRowCount(0)
            self.estabuscando=False
            self.tableventas.setColumnHidden(4, False)
            self.tableventas.setColumnHidden(6, False)
            self.tableventas.setStyleSheet('QTableView,QListView::section {Background-color:rgb(255, 255, 255);alternate-background-color:rgb(200, 167, 255);}')
            self.botcancelar.setEnabled(True)
            if self.carritos.count()>0:
                self.carritos.setEnabled(True)
            self.botvender.setEnabled(True)
            for i in range(len(self.carrito)-1,-1,-1):
                self.tableventas.insertRow(0)
                self.tableventas.setItem(0, 0, QTableWidgetItem(str(self.carrito[i]['codigo'])))
                self.tableventas.setItem(0, 1, QTableWidgetItem(str(self.carrito[i]['producto'])))
                self.tableventas.setItem(0, 2, QTableWidgetItem(str(self.carrito[i]['grupo'])))
                self.tableventas.setItem(0, 3, QTableWidgetItem(str(self.carrito[i]['stock'])))
                self.tableventas.setItem(0, 4, QTableWidgetItem(str(self.carrito[i]['cantidad'])))
                self.tableventas.setItem(0, 5, QTableWidgetItem(str(self.carrito[i]['preciopublico'])))
                self.tableventas.setItem(0, 6, QTableWidgetItem(str(self.carrito[i]['preciopublico'])))
    def guardar(self):
        if self.tableventas.rowCount()>0 and not self.estabuscando :
            self.montototal=0
            self.total.setText('0')
            self.date = datetime.now()
            self.carrito = []
            numrenglones = self.tableventas.rowCount()
            # ahora llenamos el carrito con los datos
            for i in range(numrenglones):
                producto = {}
                producto['codigo'] = self.tableventas.item(i, 0).text()
                producto['producto'] = self.tableventas.item(i, 1).text()
                producto['grupo'] = self.tableventas.item(i, 2).text()
                producto['stock'] = self.tableventas.item(i, 3).text()
                producto['cantidad'] = self.tableventas.item(i, 4).text()
                producto['preciopublico'] = self.tableventas.item(i, 5).text()
                producto['importe'] = self.tableventas.item(i, 6).text()
                self.carrito.append(producto)
            nombrecarro="Carrito "+str(self.date.minute)+":"+str(self.date.second)
            self.colacarritos[nombrecarro]=self.carrito
            self.carritos.insertItem(0,nombrecarro)
            self.carrito=[]
            self.total.setText('0')
            self.pago.setText('0')
            for i in range(self.tableventas.rowCount()):
                self.tableventas.removeRow(0)
            self.carritos.setCurrentIndex(-1)
            self.carritos.setEnabled(True)
    def elegirCarro(self):
        if self.carritos.isEnabled():
            opc='OK'
            self.carritos.setEnabled(False)
            if self.tableventas.rowCount()>0:
                opc=confirm(title="Precausión!", text='Ya existen productos en carro, desea desechar el carro actual?',
                    buttons=['OK', 'CANCEL'])
                if opc=='OK':
                    row=self.tableventas.rowCount()
                    for i in range(row):
                        self.tableventas.removeRow(0)
            if self.tableventas.rowCount()==0 and opc=="OK":
                index=self.carritos.currentIndex()
                text=self.carritos.currentText()
                self.carritos.removeItem(index)
                carrito=self.colacarritos[text]
                del self.colacarritos[text]
                for i in range(len(carrito)):
                    self.tableventas.insertRow(i)
                    self.tableventas.setItem(i, 0, QTableWidgetItem(carrito[i]['codigo']))
                    self.tableventas.setItem(i, 1, QTableWidgetItem(carrito[i]['producto']))
                    self.tableventas.setItem(i, 2, QTableWidgetItem(carrito[i]['grupo']))
                    self.tableventas.setItem(i, 3, QTableWidgetItem(carrito[i]['stock']))
                    self.tableventas.setItem(i, 4, QTableWidgetItem(carrito[i]['cantidad']))
                    self.tableventas.setItem(i, 5, QTableWidgetItem(carrito[i]['preciopublico']))
                    self.tableventas.setItem(i, 6, QTableWidgetItem(carrito[i]['importe']))
                self.calculaMontototal()
            if self.carritos.count()>0:
                self.carritos.setCurrentIndex(-1)
                self.carritos.setEnabled(True)
    def vender(self):
        index=self.tableventas.rowCount()
        #verificamos que hay productos en el carro
        if index>0:
            #codigo para cuando es a credito
            creditCheked=self.radiocredito.isChecked()
            validapago=True
            if  not creditCheked:
                validapago=self.validaPago()
            if validapago:
                opc = confirm(title='Confirmar', text='Desea realizar la venta?', buttons=['OK', 'CANCEL'])
                if opc=='OK':
                    self.carrito = []
                    for i in range(index):
                        producto = {}
                        producto['codigo'] = self.tableventas.item(i, 0).text()
                        producto['producto'] = self.tableventas.item(i, 1).text()
                        producto['cantidad'] = self.tableventas.item(i, 4).text()
                        producto['precio'] = self.tableventas.item(i, 5).text()
                        #se reduce la existencia del producto
                        producto['stock'] = str(float(self.tableventas.item(i, 3).text()) - float(self.tableventas.item(i, 4).text()))
                        #producto['codigo']['stock'] = str(float(self.tableventas.item(i, 3).text()) - float(self.tableventas.item(i, 4).text()))#aqui es donde se reduce la existencia
                        self.carrito.append(producto)
                    venta={}
                    if creditCheked:
                        #esto es para cuando se deja seleccionado que va a ser un retiro a credito
                        venta['tipoventa'] = 'Credito'
                        venta['metodopago'] = ''
                        venta['pago'] = ''
                        venta['cambio'] = ''
                        id_credit = ''
                        cliente=''
                        text = self.cliente.currentText()
                        b=False
                        for i in range(len(text)):
                            if text[i] == '.':
                                b=True
                            elif b==False:
                                id_credit += text[i]
                                # hacemos la consulta
                            else:
                                if text[i]!='-':
                                    cliente+=text[i]
                        venta['cliente']=cliente
                        self.con.GuardarProductsInCredit(id_credit, self.carrito)
                        self.con.SacarProductosCredito(id_credit, self.montototal)
                    #codigo para cuando es al contado
                    else:
                        venta['cliente'] = self.cliente.currentText()
                        venta['tipoventa'] = 'Al Contado'
                        if self.radioefectivo.isChecked():
                            venta['metodopago'] = 'Efectivo'
                        elif self.radiotarjetacredito.isChecked():
                            venta['metodopago'] = 'Tarjeta de crédito'
                        elif self.radiotarjetadebito.isChecked():
                            venta['metodopago'] = 'Tarjeta de débito'
                        venta['pago'] = float(self.pago.text())
                        venta['cambio'] = float(self.pago.text()) - self.montototal
                    venta['usuario']=self.usuario
                    venta['montototal'] = self.montototal
                    num_venta = self.con.Vender(venta, self.carrito)
                    # Limpiar formularios y variables
                    self.numeroventa.setText(str(num_venta))
                    self.total.setText('0')
                    self.cantidad.setText('0')
                    self.pago.setText('0')
                    self.montototal = 0
                    row = self.tableventas.rowCount()
                    for i in range(row):
                        self.tableventas.removeRow(0)
                    # Hacemos el ticket
                    if self.ticket.isChecked():
                        texto=self.hacerTicket(num_venta,venta,self.carrito)
                        #print('imprimiendo ticket')
                        f = open('Ticket.txt', 'w+')
                        f.write(texto)
                        f.close()
                        startfile('Ticket.txt', 'print')
                    self.carrito = []
                    self.setFocusBuscar()
            else:
                alert(title='Error!',text="Entrada no válida")

    def hacerTicket(self,num_venta,venta,carrito):
        ticket='Ferretería Guerrero\nNicolás Bravo #4 esq. Américas\nTepechitlán Zacatecas\n99750\n\n______________________________\n'

        ticket+='No. TICKET:'+str(num_venta)+'\n'
        date= datetime.now()
        hora=date.hour
        minute=date.minute
        if hora<9:
            hora='0'+str(hora)
        if minute<9:
            minute='0'+str(minute)
        ticket+='FECHA: '+str(date.date())+'\nHORA: '+str(hora)+':'+str(minute)+'\n______________________________\nCantidad       Precio           Importe\n______________________________\n'
        col_vacia="                       "
        for producto in carrito:
            ticket+=producto['producto'][:34]+'\n'
            cantidad=str(round(float(producto['cantidad']),2))
            precio=str(round(float(producto['precio']),2))
            importe=str(round(float(producto['cantidad'])*float(producto['precio']),2))
            ticket+=cantidad+col_vacia[len(cantidad)*2:]+precio+col_vacia[len(precio)*2:]+importe+'\n'
        ticket+='______________________________\n\n'
        ticket+='Total: '+str(venta['montototal'])+'\nPago: '+str(venta['pago'])+'\nCambio: '+str(venta['cambio'])+'\nOperador: '+venta['usuario']+'\n'+'Cliente: '+venta['cliente']
        #print (ticket)
        return str(ticket)
    def abonar(self):
        view = ViewAbonar(self.parametros,self)
        view.show()
    def historial(self):
        view = ViewHistorial(self.parametros,self)
        view.show()
    def quitarproducto(self):
        row=self.tableventas.currentRow()
        self.tableventas.removeRow(row)
        self.calculaMontototal()
        self.cantidad.setText("0")
        self.cantidad.setEnabled(False)
        self.botquitar.setEnabled(False)
        self.setFocusBuscar()
    def calculaMontototal(self):
        if not self.estabuscando:
            index=self.tableventas.rowCount()
            self.montototal=0
            for i in range(index):
                self.montototal+=float(self.tableventas.item(i,6).text())
            self.montototal=round(self.montototal,2)
            self.total.setText(str(self.montototal))
            self.pago.setText(str(self.montototal))
    def rowClicked(self):
        if self.estabuscando:
            #quiere decir que clickamos cuando el cuadro esta en modo seleccion de producto
            self.estabuscando =False
            self.botcancelar.setEnabled(False)
            if self.carritos.count()>0:
                self.carritos.setEnabled(True)
            self.botvender.setEnabled(True)
            self.tableventas.setStyleSheet('QTableView,QListView::section {Background-color:rgb(255, 255, 255);alternate-background-color:rgb(200, 167, 255);}')
            row=self.tableventas.currentRow()
            # ahumentamos el importe
            #obtenemos el producto seleccionado
            seleccion=[]
            for i in range(self.tableventas.columnCount()):
                seleccion.append(self.tableventas.item(row,i).text())
            #buscamos en el carrito si es que ya existe ese producto
            b=False
            for i in range(len(self.carrito)):
                if self.carrito[i]['codigo']==self.tableventas.item(row,0).text():#Aqui encontro una coincidencia con el producto buscado
                    #verificamos que existan los productos para hacer la venta
                    if (float(self.carrito[i]['stock']))>float(self.carrito[i]['cantidad']):
                        #si es que se puede simplemente se le suma una unidad a la cantidad y se vuelve a calcular el importe
                        self.carrito[i]['cantidad']=str(float(self.carrito[i]['cantidad'])+1)
                        self.carrito[i]['importe']=str(round(float(self.carrito[i]['cantidad'])*float(self.carrito[i]['preciopublico']),2))
                    else:
                        alert(title='Existencia agotada!', text="La cantidad solicitada del producto excede la\n"
                                                                "existencia total del producto")
                    # vaciamos el contenido de la tabla
                    self.tableventas.setRowCount(0)
                    #Reajustamos la tabla para que coincida con el modo carrito
                    self.tableventas.setColumnHidden(4, False)
                    self.tableventas.setColumnHidden(6, False)
                    # insertamos los productos que tenemos guardados en el carrito
                    for j in range(len(self.carrito)):
                        self.tableventas.insertRow(j)
                        self.tableventas.setItem(j, 0, QTableWidgetItem(str(self.carrito[j]['codigo'])))
                        self.tableventas.setItem(j, 1, QTableWidgetItem(str(self.carrito[j]['producto'])))
                        self.tableventas.setItem(j, 2, QTableWidgetItem(str(self.carrito[j]['grupo'])))
                        self.tableventas.setItem(j, 3, QTableWidgetItem(str(self.carrito[j]['stock'])))
                        self.tableventas.setItem(j, 4, QTableWidgetItem(str(self.carrito[j]['cantidad'])))
                        self.tableventas.setItem(j, 5, QTableWidgetItem(str(self.carrito[j]['preciopublico'])))
                        self.tableventas.setItem(j, 6, QTableWidgetItem(str(self.carrito[j]['importe'])))
                    #seteamos el current para saber a la hora de editar la cantidad a cual producto la estamos editando
                    self.tableventas.setCurrentCell(i,0)
                    self.botquitar.setEnabled(True)
                    self.cantidad.setEnabled(True)
                    self.cantidad.setText(self.tableventas.item(i,4).text())
                    self.cantidad.setSelection(0, 9999)
                    self.cantidad.setFocus()
                    b=True
                    break
            #si la bandera "b" no cambia a True quiere decir que no se encontro el producto repetido en el carrito
            if b==False:
                #vaciamos el contenido de la tabla
                self.tableventas.setRowCount(0)
                #reajustamos la tabla para que coincida con el modo carrito
                self.tableventas.setColumnHidden(4, False)
                self.tableventas.setColumnHidden(6,False)
                #insertamos los productos que tenemos guardados en el carrito
                for i in range(len(self.carrito)):
                    self.tableventas.insertRow(i)
                    self.tableventas.setItem(i, 0, QTableWidgetItem(str(self.carrito[i]['codigo'])))
                    self.tableventas.setItem(i, 1, QTableWidgetItem(str(self.carrito[i]['producto'])))
                    self.tableventas.setItem(i, 2, QTableWidgetItem(str(self.carrito[i]['grupo'])))
                    self.tableventas.setItem(i, 3, QTableWidgetItem(str(self.carrito[i]['stock'])))
                    self.tableventas.setItem(i, 4, QTableWidgetItem(str(self.carrito[i]['cantidad'])))
                    self.tableventas.setItem(i, 5, QTableWidgetItem(str(self.carrito[i]['preciopublico'])))
                    self.tableventas.setItem(i, 6, QTableWidgetItem(str(self.carrito[i]['importe'])))
                #insertamos el elemento seleccionado en caso de que exista una sola unidad del producto (ya que es la
                #  primera vez que se hace la insercción del producto)}
                if float(seleccion[3])>0:#Hace referencia a la existencia total del producto
                    row = self.tableventas.rowCount()
                    #Aqui diferencia un poquito por el tamaño de el producto seleccionado
                    self.tableventas.insertRow(row)
                    self.tableventas.setItem(row, 0, QTableWidgetItem(seleccion[0]))
                    self.tableventas.setItem(row, 1, QTableWidgetItem(seleccion[1]))
                    self.tableventas.setItem(row, 2, QTableWidgetItem(seleccion[2]))
                    self.tableventas.setItem(row, 3, QTableWidgetItem(seleccion[3]))
                    self.tableventas.setItem(row, 4, QTableWidgetItem('1'))
                    self.tableventas.setItem(row, 5, QTableWidgetItem(seleccion[5]))
                    self.tableventas.setItem(row, 6, QTableWidgetItem(seleccion[5]))
                    self.tableventas.setCurrentCell(row, 0)
                    self.botquitar.setEnabled(True)
                    self.cantidad.setEnabled(True)
                    self.cantidad.setText(self.tableventas.item(row, 4).text())
                    self.cantidad.setSelection(0, 9999)
                    self.cantidad.setFocus()
                else:
                    alert(title='Producto agotado',text=seleccion[1]+' necesita ser surtido!')
            self.calculaMontototal()
        else:
            row=self.tableventas.currentRow()
            self.cantidad.setEnabled(True)
            self.botquitar.setEnabled(True)
            self.cantidad.setText(self.tableventas.item(row,4).text())
            self.cantidad.setSelection(0,9999)
            self.cantidad.setFocus()
    def validaCantidad(self):
        input = self.cantidad
        res = self.valida.valida20Caracteres(input.text())
        if res and len(input.text())>0:
            res = self.valida.validaDecimal(input.text())
            if res:
                try:
                    if float(input.text())>0:
                        input.setStyleSheet(self.trueValidate)
                        return True
                    else:
                        input.setStyleSheet(self.falseValidate)
                        return  False
                except:
                    input.setStyleSheet(self.falseValidate)
                    return False
            else:
                input.setStyleSheet(self.falseValidate)
                return False
        else:
            input.setStyleSheet(self.falseValidate)
            return False
    def validaPago(self):
        input = self.pago
        res = self.valida.valida20Caracteres(input.text())
        if res and len(input.text())>0:
            res = self.valida.validaDecimal(input.text())
            if res:
                try:
                    if float(input.text())<self.montototal:
                        self.labelcambio.setText('0')
                        input.setStyleSheet(self.falseValidate)
                        return False
                    else:
                        input.setStyleSheet(self.trueValidate)
                        self.labelcambio.setText(str(round(float(input.text())-self.montototal,2)))
                        return True
                except:
                    self.labelcambio.setText('0')
                    input.setStyleSheet(self.falseValidate)
                    return False
            else:
                input.setStyleSheet(self.falseValidate)
                self.labelcambio.setText('0')
                return False
        else:
            input.setStyleSheet(self.falseValidate)
        return res
    def enterCantidad(self):
        if self.validaCantidad() and self.cantidad.isEnabled():
            row=self.tableventas.currentRow()
            cantidad=float(self.cantidad.text())
            existencia=float(self.tableventas.item(row,3).text())
            if cantidad>existencia:
                alert(title='Existencia agotada!',text="La cantidad solicitada del producto excede la\n"
                            "existencia total del producto")
            else:
                monto=round(cantidad*float(self.tableventas.item(row,5).text()),2)
                self.tableventas.setItem(row, 4, QTableWidgetItem(str(cantidad)))
                self.tableventas.setItem(row, 6, QTableWidgetItem(str(monto)))
                self.cantidad.setText('0')
                self.cantidad.setEnabled(False)
                self.botquitar.setEnabled(False)
                self.calculaMontototal()
                self.setFocusBuscar()
        else:
            alert(title='Error!',text='Entrada no válida')
    def enterBuscar(self):
        self.busqueda.setSelection(0, 9999)
    def setFocusBuscar(self):
        self.busqueda.setText("")
        self.busqueda.setFocus()
    def setFocusPago(self):
        self.pago.setSelection(0, 9999)
        self.pago.setFocus()
    def buscarCode(self,busqueda,index):
        productos=self.con.GetProductByCode(busqueda)
        try:
            index=len(productos)
            if index==0:
                self.buscarName(busqueda,index)
            else:
                if self.estabuscando:
                    ban=False#Bandera que cambiara a True en caso de encontrar una coincidencia en el carrito
                    for i in range(len(self.carrito)):
                        if busqueda==self.carrito[i]['codigo']:#buscamos coincidencias con el carrito
                            #aqui se encontro una coincidencia con el carrito
                            if float(self.carrito[i]['stock'])>float(self.carrito[i]['cantidad']):#Aqui verificamos si la cantidad a llevar es menor a la existencia
                                #Si se puede sumar uno a la cantidad a llevar
                                self.carrito[i]['cantidad']=str(float(self.carrito[i]['cantidad'])+1)#se suma una unidad
                                self.carrito[i]['importe']=str(float(self.carrito[i]['cantidad'])*float(self.carrito[i]['cantidad']))
                                ban=True
                            else:
                                alert(title='Producto insuficiente',text='La cantidad solicitada es mayor a la existencia')
                                self.cancelar()
                                return 0
                    if not ban:
                        #se ejecuta este codigo en caso de no encontrar coincidencias en el carrito
                        producto=productos[0]
                        if float(producto['stock'])>0:
                            producto['cantidad']="1"
                            producto['importe']=str(producto['preciopublico'])
                            self.carrito.append(producto)
                        else:
                            alert(title='Producto insuficiente',text="La cantidad solicitada es mayor a la existencia")
                            self.cancelar()
                            return 0
                    self.cancelar()                    
                    self.calculaMontototal()
                else:
                    ban=False
                    index=self.tableventas.rowCount()
                    for i in range(index):
                        if self.tableventas.item(i,0).text()==productos[0]['codigo']:
                            #aqui se encuentra una coincidencia en la tabla de ventas
                            print('Se encontro una cohincidencia')
                            if float(self.tableventas.item(i,3).text())> float(self.tableventas.item(i,4).text()):
                                print('Existe stock suficiente')
                                #verificamos que el stock sea mayo que la cantidad a vender
                                self.tableventas.setItem(i, 4, QTableWidgetItem(str(float(self.tableventas.item(i,4).text())+1)))
                                self.tableventas.setItem(i, 6, QTableWidgetItem(str(float(self.tableventas.item(i,4).text())*float(self.tableventas.item(i,5).text()))))
                                #self.tableventas.setItem(i, 0, QTableWidgetItem(carrito[i]['codigo']))
                                self.calculaMontototal()
                                return 0
                            else:
                                alert(title='Producto insuficiente',text='La cantidad solicitada es mayor a la existencia')
                                return 0
                    if not ban:
                        producto=productos[0]
                        if float(producto['stock'])>=1:
                            self.tableventas.insertRow(0)
                            self.tableventas.setItem(0, 0, QTableWidgetItem(str(producto['codigo'])))
                            self.tableventas.setItem(0, 1, QTableWidgetItem(str(producto['producto'])))
                            self.tableventas.setItem(0, 2, QTableWidgetItem(str(producto['grupo'])))
                            self.tableventas.setItem(0, 3, QTableWidgetItem(str(producto['stock'])))
                            self.tableventas.setItem(0, 4, QTableWidgetItem('1'))
                            self.tableventas.setItem(0, 5, QTableWidgetItem(str(producto['preciopublico'])))
                            self.tableventas.setItem(0, 6, QTableWidgetItem(str(producto['preciopublico'])))
                            return 0
                        else:
                            alert(title='Producto insuficiente',text='La cantidad solicitada es mayor a la existencia')
                            return 0
        except:
            alert(title='Error!',text='Revise la conexion con la red')
            return 0        
    def buscarName(self,busqueda,index):
        coincidencias=self.con.FindProducts2(busqueda)
        try:
            longitud=len(coincidencias)
            if longitud==0:
                alert(title='Sin resultados!',text='Producto no encontrado')
                return 0
            if not self.estabuscando:
                self.tableventas.setColumnHidden(4, True)
                self.tableventas.setColumnHidden(6, True)
                self.tableventas.setStyleSheet("border: 2px solid green; font-size: 15px;")
                self.estabuscando=True
                self.botcancelar.setEnabled(True)
                self.carritos.setEnabled(False)
                self.botvender.setEnabled(False)
            self.tableventas.setRowCount(0)
            for i in  range(longitud):
                self.tableventas.insertRow(0)
                self.tableventas.setItem(0, 0, QTableWidgetItem(str(coincidencias[i]['codigo'])))
                self.tableventas.setItem(0, 1, QTableWidgetItem(str(coincidencias[i]['producto'])))
                self.tableventas.setItem(0, 2, QTableWidgetItem(str(coincidencias[i]['grupo'])))
                self.tableventas.setItem(0, 3, QTableWidgetItem(str(coincidencias[i]['stock'])))
                self.tableventas.setItem(0, 4, QTableWidgetItem('0'))
                self.tableventas.setItem(0, 5, QTableWidgetItem(str(coincidencias[i]['preciopublico'])))
                self.tableventas.setItem(0, 6, QTableWidgetItem('0'))
        except:
            alert(title="Error!",text='Revisa la conexion a red')
    def save(self):
        
        if not self.estabuscando:
            index=self.tableventas.rowCount()
            self.carrito=[]
            for i in range(index):
                producto = {}
                producto['codigo'] = self.tableventas.item(i, 0).text()
                producto['producto'] = self.tableventas.item(i, 1).text()
                producto['grupo'] = self.tableventas.item(i, 2).text()
                producto['stock'] = self.tableventas.item(i, 3).text()
                producto['cantidad'] = self.tableventas.item(i, 4).text()
                producto['preciopublico'] = self.tableventas.item(i, 5).text()
                producto['importe'] = self.tableventas.item(i, 6).text()
                self.carrito.append(producto)
            print("Carrito")
            for pro in self.carrito:
                print (pro)
    def buscar(self):
        busqueda=str(self.busqueda.text())
        self.busqueda.setText('')
        if busqueda=="":
            self.pago.setSelection(0,9999)
            self.pago.setFocus()
            return True
        index=self.tableventas.rowCount()
        self.enterBuscar()
        self.busqueda.setFocus(True)
        self.save()
        try:
            a=int(busqueda)
            iscode=True
        except:
            iscode=False
           
        if iscode:
            self.buscarCode(busqueda,index)
        else:
            self.buscarName(busqueda,index)
        self.tableventas.scrollToItem(self.tableventas.item(self.tableventas.rowCount(),0))
    def ayudaAbonar(self):
        alert(title="Ayuda",text='Despliega una ventana en donde se muestra la información\n'
                                 'de los clientes con deudas en crédito.\n'
                                 'Dar doble click en una celda mostrará más a detalle\n'
                                 'la información de los productos que fueron sacados\n'
                                 'con ese mismo crédito.')
    def ayudaQuitarProducto(self):
        alert(title='Ayuda',text='Para quitar un producto de la lista del carro:\n'
                                 '1.- Seleccionar el producto de la lista\n'
                                 '2.- Presionar el botón "Quitar producto"')
    def ayudaGuardarCarro(self):
        alert(title='Ayuda',text='Para poner en cola un carrito de compra sólo presionar\n'
                                 'el botón de "Guardar carro", el carrito se guardará en el sistema,\n'
                                 'para posteriormente renaudar con el proceso de venta de ese carro\n'
                                 'basta con seleccionarlo de la lista en la parte inferior izquierda\n'
                                 'en donde dice "Carritos"')
    def ayudaHistorial(self):
        alert(title='Ayuda',text='Despliega una ventana en donde se muestra el historial de ventas.\n'
                                 'Al hacer doble click en una celda se mostrará los productos\n'
                                 'que fueron vendidos en esa venta.')
if __name__=="__main__":
    if True:
        from PyQt5.QtWidgets import QApplication
        from validaciones import Valida
        from conexion import *
        app = QApplication(sys.argv)
        parametros = {'conexion': Conexion(), 'valida': Valida()}
        parametros['usuario'] = "brenda123456"
        gui = ViewVentas(parametros)
        gui.show()
        sys.exit(app.exec())
