""" 
    Por: Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Archivo.
    Atributos: nombre del archivo y contenido del archivo. 
"""
class Archivo:
    # Constructor de la clase Archivo.
    def __init__(self, nombre_archivo: str, contenido_archivo: str):
        self.nombre_archivo = nombre_archivo
        self.contenido_archivo = contenido_archivo