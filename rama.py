from commit import Commit

"""
    Por: Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Rama.
    Atributos: nombre de la rama y puntero al commit más reciente (actual). 
"""

class Rama:
    # Constructor de la clase Rama:
    def __init__(self, nombre_rama: str, commit_reciente: Commit):
        self.nombre_rama = nombre_rama
        self.commit_reciente = commit_reciente