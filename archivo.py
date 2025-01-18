""" 
    Por. Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Archivo.
    Atributos: nombre del Archivo y contenido del Archivo. 
"""
class Archivo:
    # Constructor de la clase Archivo.
    def __init__(self, nombre_archivo: str, contenido_archivo: str):
        self.nombre_archivo = nombre_archivo
        self.contenido_archivo = contenido_archivo

    # Getter de la clase Archivo:
    def get_nombre_archivo(self):
        return self.nombre_archivo