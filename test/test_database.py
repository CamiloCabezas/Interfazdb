import unittest
import config
import csv 
import copy
import database as db
import helpers

class TestDatabase(unittest.TestCase):
     
     
    def setUp(self):
         db.Clientes.lista = [
             db.Cliente('22J', 'Sofia', 'Jimenez'),
             db.Cliente('17C', 'Camilo', 'Lopez'),
             db.Cliente('11S', 'Ana', 'Perilla'),
         ]
    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('22J')
        cliente_inexistente = db.Clientes.buscar('414K')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
    
    def test_crear_clientes(self):
        nuevo_cliente = db.Clientes.crear('12D', 'Pablo', 'Enriquez')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '12D')
        self.assertEqual(nuevo_cliente.nombre, 'Pablo')
        self.assertEqual(nuevo_cliente.apellido, 'Enriquez')
        
    def modificar_cliente(self):
        cliente_a_modificar = copy.copy (db.Clientes.buscar('22J'))
        cliente_modificado = db.Clientes.modificar('22J', 'Sofi', 'Jimenez')
        self.assertEqual(cliente_a_modificar.nombre, 'Sofia')
        self.assertEqual(cliente_modificado.nombre, 'Sofi')
       
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('11S')
        cliente_rebuscado = db.Clientes.buscar('11S')
        self.assertEqual(cliente_borrado.dni , '11S')
        self.assertIsNone(cliente_rebuscado)
        
    def test_dni_valido(self):
        self.assertFalse(helpers.dni_valido('12311531531C',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('fafaf34',db.Clientes.lista))
        self.assertTrue(helpers.dni_valido('00S', db.Clientes.lista))
        


        
    
        