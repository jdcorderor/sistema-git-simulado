from commit import Commit

"""
    Por. Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Rama.
    Atributos: nombre de la Rama y puntero al Commit más reciente. 
"""

class Rama:
    # Constructor de la clase Rama:
    def __init__(self, nombre_rama: str, commit_reciente: Commit):
        self.nombre_rama = nombre_rama
        self.commit_reciente = commit_reciente

    # Getters de la clase Rama:
    def get_nombre_rama(self):
        return self.nombre_rama

    def get_commit_reciente(self):
        return self.commit_reciente

    # Setter de la clase Rama:
    def set_commit_reciente(self, valor: Commit):
        self.commit_reciente = valor