import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()
        
        
        print("===========================")
        print("   Bienvenido al Manager   ")
        print("===========================")
        print("[1] Listar Clientes        ")
        print("[2] Buscar Cliente         ")
        print("[3] Añadir Cliente         ")
        print("[4] Modificar Cliente      ")
        print("[5] Borrar Cliente         ")
        print("[6] Cerrar Manager         ")
        print("===========================")
        
        opcion = input("> ")
        helpers.limpiar_pantalla()
        
        if opcion == '1':
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
                
        elif opcion == '2':
            print("Buscando Clientes...\n")
            dni = helpers.leer_texto(3, 3, "DNI(2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado")
            
        elif opcion == '3':
            print("Añadiendo Cliente...\n")
            
            dni = None
            while True:
                dni = helpers.leer_texto(3, 3, "DNI(2 int y 1 char)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break
                
            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 chars)").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 chars)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente")
            
        elif opcion == '4':
            print("Modificando Cliente...\n")
            dni = helpers.leer_texto(3, 3 , "DNI(2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre (de 2 a 30 chars) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (de 2 a 30 chars) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encontrado")
            
            
        elif opcion == '5':
            print("Borrando Cliente...\n")
            dni = helpers.leer_texto(3, 3 , "DNI(2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente.dni == dni:
                db.Clientes.borrar(dni)
                print(f"El Cliente [{cliente.nombre},{cliente.apellido}] fue borrado")
            else:
                print("Cliente no Enontrado")
            
        
        elif opcion == '6':
            print("Saliendo...\n")
            break

        input("\nPresiona ENTER para continuar...")