from archivo import Archivo

"""
    Por. Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Commit.
    Atributos: mensaje del commit, lista de Archivos involucrados y puntero al Commit anterior. 
"""

class Commit:
    # Constructor de la clase Commit.
    def __init__(self, commit_id: str, lista_archivos: list[Archivo], commit_anterior): 
        self.commit_id = commit_id
        self.lista_archivos = lista_archivos
        self.commit_anterior = commit_anterior