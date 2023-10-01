import re
import os
import platform

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')
    # La primera parte es lo que se quiere si se cumple la condicion
    # la segunda parte es lo que se cumple si no se cumple la condicion
    
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato.")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente.")
            return False
    return True

