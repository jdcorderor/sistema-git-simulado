from rama import Rama
from commit import Commit
from archivo import Archivo

""" 
    Por. Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Repositorio.
    Atributos: lista de Commits (historial), lista de Ramas existentes y puntero a la Rama Activa. 
"""

class Repositorio:
    # Constructor de la clase Repositorio:
    def __init__(self):
        self.repo_commits = None # Atributo (lista de Commits) inicializado "None" debido a que no se ha ejecutado un Commit.
        self.repo_ramas = [Rama("main", None)] # Automáticamente se crea la rama "main" (por default) al crear el Repositorio.
        self.rama_activa = self.repo_ramas[0] # Automáticamente se selecciona la rama "main" como Rama Activa.

    # Método encargado de crear un objeto del tipo de la clase Commit, almacenarlo en el historial ("repo_commits") y en el atributo "commit_reciente" del objeto del tipo de la clase Rama:
    def git_commit(self, identificador: str):
        ultimo_commit = self.rama_activa.commit_reciente # Variable que almacena el último Commit registrado en la Rama Activa.
        lista = self.listar_archivos_commit() # Invoca al método auxiliar "listar_archivos_commit".
        if confirmacion_commit(): # Invoca a la función auxiliar "confirmacion_commit".
            if self.rama_activa.commit_reciente != None: # Filtra el caso en que no se haya ejecutado un Commit previamente.
                lista = lista + self.rama_activa.commit_reciente.lista_archivos
            commit_nuevo = Commit(identificador, lista, ultimo_commit) # Construye el objeto del tipo de la clase Commit. 
            if self.repo_commits == None:
                self.repo_commits = [commit_nuevo] # Si se ejecuta el primer Commit en el sistema, se crea la lista ("repo_commits") que almacenará los objetos de dicha clase (historial de Commits).
            else:
                self.repo_commits.append(commit_nuevo) # Si han sido ejecutados Commits previamente, se agrega el objeto creado a la lista.
            self.rama_activa.set_commit_reciente(commit_nuevo) # Se modifica el atributo "commit_reciente" del objeto de la clase Rama que almacena el Commit.
            print("\nCommit '%s' done. Files:"%(identificador), end=" ") # Mensaje de confirmación.
            self.imprimir_nombres_archivos() # Invoca al método auxiliar "imprimir_nombres_archivos".
            
    # Método encargado de crear un objeto del tipo de la clase Rama y almacenarlo en la lista de Ramas existentes ("repo_ramas"):
    def git_branch_create(self, identificador: str):
        rama_nueva = Rama(identificador, self.rama_activa.commit_reciente) # Construye el objeto del tipo de la clase Rama. Invoca al getter del Commit más reciente ("commit_reciente") de la Rama Activa.
        self.repo_ramas.append(rama_nueva) # Agrega el objeto creado a la lista de Ramas existentes ("repo_ramas").
        print("\nBranch '%s' created succesfully"%(identificador)) # Mensaje de confirmación.

    # Método encargado de cambiar la Rama Activa, permitiendo trabajar en todas las Ramas del Repositorio: 
    def git_switch(self, rama_objetivo: str):
        self.rama_activa = self.repo_ramas[self.index_ramas(rama_objetivo)] # Modifica el atributo "rama_activa" del Repositorio. Invoca al método auxiliar "index_ramas".
        print("\nSwitched to '%s' branch succesfully"%(rama_objetivo)) # Mensaje de confirmación.

    # Método encargado de fusionar (Merge) dos Ramas del Repositorio:
    def git_merge(self, rama_merge: str):
        index_rama_merge = self.index_ramas(rama_merge) # Invoca al método auxiliar "index_ramas" y almacena el índice (respectivo en la lista "repo_ramas") de la rama a fusionar con la Rama Activa.
        merge_commit_id = f"Merge {rama_merge} into {self.rama_activa.nombre_rama}" # Crea el mensaje del Commit asociado al Merge.
        lista_archivos_merge = self.rama_activa.commit_reciente.lista_archivos + self.repo_ramas[index_rama_merge].commit_reciente.lista_archivos # Fusiona las listas de Archivos de los Commits más recientes de ambas Ramas. 
        self.rama_activa.set_commit_reciente(Commit(merge_commit_id, lista_archivos_merge, self.rama_activa.commit_reciente)) # Actualiza el Commit más reciente de la Rama Activa.
        self.repo_ramas[index_rama_merge].set_commit_reciente(Commit(merge_commit_id, lista_archivos_merge, self.repo_ramas[index_rama_merge].commit_reciente)) # Actualiza el Commit más reciente de la Rama fusionada.
        self.repo_commits.append(self.rama_activa.commit_reciente) # Agrega el Commit (asociado al Merge) al historial de Commits ("repo_commits").
        print("\n'%s' completed. Files:"%(merge_commit_id), end=" ") # Mensaje de confirmación.
        self.imprimir_nombres_archivos() # Invoca al método auxiliar "imprimir_nombres_archivos".

    # Método encargado de mostrar por consola el historial de Commits del Repositorio:
    def git_log(self):
        print("\n--- Commit Record ---") # Imprime un encabezado.
        i = len(self.repo_commits) - 1
        while (i >= 0):
            print("%s"%(self.repo_commits[i].commit_id)) # Ciclo que imprime el "commit_id" de todos los objetos del tipo de la clase Commit registrados en el historial ("repo_commits").
            i -= 1

    # Método encargado de mostrar por consola la lista de Ramas del Repositorio:
    def git_branch(self):
        print("\n--- Branches ---") # Imprime un encabezado.
        i = len(self.repo_ramas) - 1
        while (i >= 0):
            print("%s"%(self.repo_ramas[i].nombre_rama)) # Ciclo que imprime el "nombre_rama" de todos los objetos del tipo de la clase Rama registrados en "repo_ramas".
            i -= 1

    # Método auxiliar encargado de listar los archivos implicados en un Commit:
    def listar_archivos_commit(self):
        band = 0
        archivos = []
        while (band == 0):
            print("\n--- Carga de Archivo ---")
            nombre = input("Ingrese el nombre del archivo: ")
            contenido = input("Ingrese el contenido del archivo: ")
            archivos.append(Archivo(nombre, contenido))
            band = int(input("Ingrese 0 para agregar un nuevo archivo; cualquier otro valor para ejecutar el Commit: "))
        return archivos
    
    # Método auxiliar encargado de filtrar la lista de Ramas existentes según el atributo "nombre_rama":
    def index_ramas(self, clave_rama: str):
        for i in range (len(self.repo_ramas)):
            if self.repo_ramas[i].nombre_rama == clave_rama: # Recorre los elementos de la lista del tipo de la clase Rama en busca de una coincidencia del atributo "nombre_rama" con la cadena "clave_rama".
                return i # Retorna el índice al encontrar una coincidencia, permitiendo acceder a objetos del tipo de la clase Rama con facilidad.
            
    # Método auxiliar para imprimir los nombres de los objetos de la clase Archivo pertenecientes a la Rama Activa:
    def imprimir_nombres_archivos(self):
        nombres_archivos = set()
        commit = self.rama_activa.commit_reciente
        for archivo in commit.lista_archivos:
            nombres_archivos.add(archivo.nombre_archivo)
        print(", ".join(nombres_archivos))

# Método para confirmar el Commit:
def confirmacion_commit():
    band = (int(input("\n¿Desea ejecutar el Commit? Ingrese 0: ")))
    if band == 0:
        return True