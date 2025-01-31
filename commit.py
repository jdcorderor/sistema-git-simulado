from archivo import Archivo
from random import randint
from string import ascii_lowercase

"""
    Por: Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Commit.
    Atributos: identificador del commit, lista de archivos, hash del commit y puntero al commit anterior. 
"""

class Commit:
    # Constructor de la clase Commit.
    def __init__(self, commit_id: str, lista_archivos: list[Archivo], commit_anterior, lista_commits): 
        self.commit_id = commit_id
        self.commit_hash = self.crear_commit_hash(lista_commits) # Invoca al método 'crear_commit_hash', encargado de crear un código SHA-1 para el commit.
        self.lista_archivos = lista_archivos
        self.commit_anterior = commit_anterior

    # Método auxiliar encargado de crear y asignar un hash / SHA-1 al commit.
    def crear_commit_hash(self, lista_commits): # Recibe como parámetro la lista de commits del repositorio (historial).
        caracteres = list(ascii_lowercase) + list(str(i) for i in range (10)) # Crea una lista de caracteres, que contiene letras en minúsculas (ASCII) y los dígitos del sistema decimal (0-9).
        hash = "" # Inicializa la variable 'hash' como una cadena vacía.
        for i in range(40): # Ciclo encargado de controlar la adición de caracteres al hash.
            hash += caracteres[randint(0, len(caracteres) - 1)] # Invoca a la función 'randint', que retornará un índice aleatorio de la lista de caracteres. El caracter seleccionado por índice se adiciona al hash.
        if self.validacion_commit_hash(hash, lista_commits): # Invoca al método 'validacion_commit_hash', que verifica la unicidad del hash.
            return hash # Retorna el hash.
        else: # En caso de que el hash ya exista.
            self.crear_commit_hash(lista_commits) # Invoca nuevamente al método 'crear_commit_hash'.

    # Método auxiliar encargado de comprobar la unicidad del hash del commit:
    def validacion_commit_hash(self, hash_commit: str, lista_commits): # Recibe como parámetros el hash generado y la lista de commits del repositorio (historial).
        if lista_commits: # Evalúa si 'lista_commits' existe.
            for commit in lista_commits: # Recorre la lista de commits, guardando en 'commit' el puntero al objeto del tipo Commit (referenciado por cada posición de la lista).
                if commit.commit_hash == hash_commit: # Evalúa si el hash coincide con un hash preexistente.
                    return False # Retorna 'False', rechazando el hash.
            return True # Retorna 'True', validando el hash.
        else: # En caso de que 'lista_commits' no exista, es decir, sea 'None'.
            return True # Retorna 'True', validando el hash.