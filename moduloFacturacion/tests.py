from django.utils import unittest
from django.test.client import Client
from selenium.webdriver.chrome.webdriver import WebDriver
from django.test.testcases import LiveServerTestCase
from moduloFacturacion.models import OrdenPedido
from datetime import date
from moduloClientes.models import Cliente


class statusTest(unittest.TestCase):
    def test_get_crear_orden_Pedido_TC001(self):
        client = Client()
        response = client.get('/crearOrdenPedido/')
        self.assertEqual(response.status_code, 200)
        
    def test_post_crear_orden_Pedido_TC001(self):
        client = Client()
        response = client.post('/login/', {'codigo': ['001029'],
                                           'codigo_factura': ['001029'], 
                                            'fecha_compra_day': ['15'], 
                                            'fecha_facturacion_day': ['17'], 
                                            'item_ordenpedido_cantidad_set-2-item': [''], 
                                            'item_ordenpedido_cantidad_set-1-subtotal': [''], 
                                            'item_ordenpedido_cantidad_set-1-cantidad': [''], 
                                            'item_ordenpedido_cantidad_set-1-precio_venta_unitario': [''], 
                                            'fecha_compra_month': ['2'], 
                                            'items': ['LBP00124'], 
                                            'fecha_facturacion_year': ['2013'], 
                                            'item_ordenpedido_cantidad_set-1-item': [''], 
                                            'item_ordenpedido_cantidad_set-0-item': [''], 
                                            'item_ordenpedido_cantidad_set-2-cantidad': [''], 
                                            'fecha_facturacion_month': ['11'], 
                                            'item_ordenpedido_cantidad_set-0-precio_venta_unitario': [''], 
                                            'fecha_compra_year': ['2012'], 
                                            'item_ordenpedido_cantidad_set-2-precio_venta_unitario': [''], 
                                            'item_ordenpedido_cantidad_set-0-cantidad': [''], 
                                            'csrfmiddlewaretoken': ['2djaPSAJE8tsfLTgs03HoSwuMuomm0zt'], 
                                            'item_ordenpedido_cantidad_set-0-subtotal': [''], 
                                            'detalle': ['can'], 
                                            'cliente': ['1'], 
                                            'item_ordenpedido_cantidad_set-2-subtotal': ['']})
        self.assertEqual(response.status_code, 200)
        
    #codigos iguales
    def test_post_crear_orden_Pedido_TC002(self):
        client = Client()
        response = client.post('/login/', {'codigo': ['001029'],
                                           'codigo_factura': ['001029'], 
                                            'fecha_compra_day': ['15'], 
                                            'fecha_facturacion_day': ['17'], 
                                            'item_ordenpedido_cantidad_set-2-item': [''], 
                                            'item_ordenpedido_cantidad_set-1-subtotal': [''], 
                                            'item_ordenpedido_cantidad_set-1-cantidad': [''], 
                                            'item_ordenpedido_cantidad_set-1-precio_venta_unitario': [''], 
                                            'fecha_compra_month': ['2'], 
                                            'items': ['LBP00124'], 
                                            'fecha_facturacion_year': ['2013'], 
                                            'item_ordenpedido_cantidad_set-1-item': [''], 
                                            'item_ordenpedido_cantidad_set-0-item': [''], 
                                            'item_ordenpedido_cantidad_set-2-cantidad': [''], 
                                            'fecha_facturacion_month': ['11'], 
                                            'item_ordenpedido_cantidad_set-0-precio_venta_unitario': [''], 
                                            'fecha_compra_year': ['2012'], 
                                            'item_ordenpedido_cantidad_set-2-precio_venta_unitario': [''], 
                                            'item_ordenpedido_cantidad_set-0-cantidad': [''], 
                                            'csrfmiddlewaretoken': ['2djaPSAJE8tsfLTgs03HoSwuMuomm0zt'], 
                                            'item_ordenpedido_cantidad_set-0-subtotal': [''], 
                                            'detalle': ['can'], 
                                            'cliente': ['1'], 
                                            'item_ordenpedido_cantidad_set-2-subtotal': ['']})
        self.assertEqual(response.status_code, 501)
        
    def test_ordenes_pedido_TC001(self):
        client = Client()
        response = client.get('/ordenesDePedido/')
        self.assertEqual(response.status_code, 200)
        
class moduloFacturacion_SeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(moduloFacturacion_SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(moduloFacturacion_SeleniumTests, cls).tearDownClass()

    def test_editarOrdenPedido(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/editarOrdenPedido/?q=000824'))
        codigo_input = self.selenium.find_element_by_name("codigo")
        factura_input = self.selenium.find_element_by_name("codigo_factura")
        fecha_month_input = self.selenium.find_element_by_name("fecha_compra_month")
        fecha_day_input = self.selenium.find_element_by_name("fecha_compra_day")
        fecha_year_input = self.selenium.find_element_by_name("fecha_compra_year")        
        entrega_month_input = self.selenium.find_element_by_name("fecha_compra_month")
        entrega_day_input = self.selenium.find_element_by_name("fecha_compra_day")
        entrega_year_input = self.selenium.find_element_by_name("fecha_compra_year")
        cliente_input = self.selenium.find_element_by_name("cliente")
        #items_input_set = self.selenium.find_element_by_name("items")
        orden_to_test = OrdenPedido.objects.get(pk='000824')
        #assert input
        self.assertTrue(codigo_input == orden_to_test.codigo)   
        self.assertTrue(factura_input == orden_to_test.codigo_factura)            
        self.assertTrue(orden_to_test.fecha_compra == date(year=fecha_year_input,month=fecha_month_input,day=fecha_day_input))            
        self.assertTrue(orden_to_test.fecha_facturacion == date(year=entrega_year_input,month=entrega_month_input,day=entrega_day_input))           
        self.assertTrue(orden_to_test.cliente == Cliente.objects.get(pk=cliente_input))