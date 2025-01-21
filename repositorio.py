from rama import Rama
from commit import Commit
from archivo import Archivo

""" 
    Por: Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Clase Repositorio.
    Atributos: lista de commits (historial), lista de ramas existentes y puntero a la rama activa. 
"""

class Repositorio:
    # Constructor de la clase Repositorio:
    def __init__(self):
        self.lista_repo_commits = None # Se inicializa con 'None' ya que no se han ejecutado commits.
        self.lista_repo_ramas = [Rama("main", None)] # Se inicializa automáticamente con una lista que almacena un puntero a la rama 'main'.
        self.rama_activa = self.lista_repo_ramas[0] # Se inicializa automáticamente con un puntero a la rama "main".
        print("\ngit init") # Se imprime el comando Git que inicializa un repositorio.

    # Método encargado de crear un objeto del tipo de la clase Commit:
    def git_commit(self, identificador: str): # Recibe como parámetro el identificador del commit ingresado por el usuario.
        if self.validacion_identificador_commit(identificador): # Invoca al método 'validacion_identificador_commit', que verifica la unicidad del identificador.
            ultimo_commit = self.rama_activa.commit_reciente # Asigna el puntero al commit más reciente de la rama activa a la variable 'ultimo_commit'.
            lista_archivos_commit = self.listar_archivos_commit() # Invoca al método 'listar_archivos_commit', para agregar los archivos y almacenarlos en 'lista_archivos_commit'.
            imprimir_stage_area(lista_archivos_commit)
            if confirmacion_commit(identificador): # Invoca a la función 'confirmacion_commit', en la que el usuario debe confirmar la ejecución del commit.
                if ultimo_commit: # Evalúa si existe un commit predecesor en la rama activa.
                    lista_archivos_commit = self.rama_activa.commit_reciente.lista_archivos + lista_archivos_commit # Los archivos preexistentes se añaden a 'lista_archivos_commit'.
                    lista_archivos_commit = self.validacion_actualizacion_archivos(lista_archivos_commit) # Se invoca al método 'validación_actualizacion_archivos', que garantiza la actualización del contenido.
                commit_nuevo = Commit(identificador, lista_archivos_commit, ultimo_commit) # Crea el objeto de la clase Commit y asigna el puntero a la variable 'commit_nuevo'.
                if self.lista_repo_commits: # Evalúa si 'lista_repo_commits' existe.
                    self.lista_repo_commits.append(commit_nuevo) # Agrega el puntero al historial de commits: 'lista_repo_commits'.
                else: # En caso de que 'lista_repo_commits' no exista, es decir, sea 'None'.
                    self.lista_repo_commits = [commit_nuevo] # Crea una lista del tipo de la clase Commit, que almacena un puntero al objeto commit creado.
                self.rama_activa.commit_reciente = commit_nuevo # Asigna el objeto commit creado al atributo 'commit_reciente' de la rama activa.
                print("\nCommit '%s' ejecutado exitosamente. Archivos:"%(identificador), end=" ") # Se imprime el mensaje de confirmación.
                self.imprimir_atributos_archivos() # Invoca al método 'imprimir_atributos_archivos', que muestra en pantalla los archivos almacenados por el objeto commit.
            else: # En caso de que el usuario no confirme la ejecución del commit.
                self.git_commit(identificador) # Invoca nuevamente al método 'git_commit', enviando como argumento el mismo identificador.
        else: # En caso de que el identificador ya exista.
            self.git_commit(input("\nError: Identificador existente. Por favor, ingrese otro identificador para el commit\n\ngit commit -m ")) # Invoca nuevamente al método 'git_commit', y solicita al usuario el ingreso de un nuevo identificador.
            
    # Método encargado de crear un objeto del tipo de la clase Rama:
    def git_branch_create(self, identificador: str): # Recibe como parámetro el nombre de la rama ingresado por el usuario.
        if self.validacion_identificador_rama(identificador): # Invoca al método 'validacion_identificador_rama', que verifica la unicidad del nombre.
            rama_nueva = Rama(identificador, self.rama_activa.commit_reciente) # Crea el objeto de la clase Rama y asigna el puntero a la variable 'rama_nueva'. Envía como argumento el puntero al commit más reciente de la rama activa.
            self.lista_repo_ramas.append(rama_nueva) # Agrega el puntero a la lista de ramas: 'lista_repo_ramas'.
            print("\nRama '%s' creada exitosamente"%(identificador)) # Se imprime el mensaje de confirmación.
        else: # En caso de que el nombre ya exista.
            self.git_branch_create(input("\nError: Nombre existente. Por favor, ingrese otro identificador para la rama\n\ngit branch ")) # Invoca nuevamente al método 'git_branch', y solicita al usuario el ingreso de un nuevo nombre.

    # Método encargado de cambiar la rama activa, permitiendo acceder y trabajar en todas las ramas del repositorio: 
    def git_switch(self, nombre_rama_objetivo: str): # Recibe como parámetro el nombre del objeto de la clase Rama al que se desea acceder.
        if self.validacion_identificador_rama(nombre_rama_objetivo) is False: # Invoca al método 'validacion_identificador_rama', que verifica la existencia del nombre: 'nombre_rama_objetivo'.
            self.rama_activa = self.lista_repo_ramas[self.get_index_ramas(nombre_rama_objetivo)] # Invoca al método 'get_index_ramas', que retorna el índice del objeto rama en 'lista_repo_ramas'. Asigna al atributo 'rama_activa' el puntero a la rama seleccionada.
            print("\nCambio exitoso a la rama '%s'"%(nombre_rama_objetivo)) # Se imprime el mensaje de confirmación.
        else: # En caso de que el nombre no exista.
            self.git_switch(input("\nError: Rama no existente. Por favor, ingrese un identificador de rama válido\n\ngit switch ")) # Invoca nuevamente al método 'git_switch', y solicita al usuario el ingreso de un nuevo nombre.
            
    # Método encargado de fusionar (Merge) dos ramas del repositorio:
    def git_merge(self, nombre_rama_merge: str): # Recibe como parámetro el nombre del objeto de la clase Rama que se desea fusionar con la rama activa.
        if self.validacion_identificador_rama(nombre_rama_merge) is False: # Invoca al método 'validacion_identificador_rama', que verifica la existencia del nombre: 'nombre_rama_merge'.
            index_rama_merge = self.get_index_ramas(nombre_rama_merge) # Invoca al método 'get_index_ramas', que retorna el índice del objeto rama en 'lista_repo_ramas'; y lo asigna a la variable 'index_rama_merge'.
            merge_commit_id = f"Merge {nombre_rama_merge} into {self.rama_activa.nombre_rama}" # Formatea y asigna a la variable 'merge_commit_id' el identificador de la fusión.
            if confirmacion_merge(merge_commit_id): # Invoca a la función 'confirmacion_merge', en la que el usuario debe confirmar la ejecución de la fusión.
                lista_archivos_merge = self.validacion_archivos_merge(index_rama_merge) # Invoca al método 'validacion_archivos_merge', que retorna una lista que se asigna a la variable 'lista_archivos_merge'.
                self.rama_activa.commit_reciente = Commit(merge_commit_id, lista_archivos_merge, self.rama_activa.commit_reciente) # Crea el objeto del tipo Commit y asigna el puntero al atributo 'commit_reciente' de la rama activa.
                self.lista_repo_ramas[index_rama_merge].commit_reciente = Commit(merge_commit_id, lista_archivos_merge, self.lista_repo_ramas[index_rama_merge].commit_reciente) # Crea el objeto del tipo Commit y asigna el puntero al atributo 'commit_reciente' de la rama fusionada.
                self.lista_repo_commits.append(self.rama_activa.commit_reciente) # Agrega el puntero al historial de commits: 'lista_repo_commits'.
                print("\n'%s' completado. Archivos:"%(merge_commit_id), end=" ") # Se imprime el mensaje de confirmación.
                self.imprimir_atributos_archivos() # Invoca al método 'imprimir_atributos_archivos', que muestra en pantalla los archivos almacenados por el objeto commit.
        else: # En caso de que el nombre no exista.
            self.git_merge(input("\nError: Rama no existente. Por favor, ingrese un identificador de rama válido\n\ngit merge ")) # Invoca nuevamente al método 'git_merge', y solicita al usuario el ingreso de un nuevo nombre.

    # Método encargado de mostrar por consola el historial de commits del repositorio:
    def git_log(self):
        if self.lista_repo_commits: # Evalúa si 'lista_repo_commits' existe.
            print("\n--- Historial de Commits ---") # Se imprime un encabezado.
            i = len(self.lista_repo_commits) - 1 # Almacena en la variable 'i' el mayor índice de 'lista_repo_commits'.
            while (i >= 0): # Evalúa que el índice sea mayor o igual que cero.
                print("%s"%(self.lista_repo_commits[i].commit_id)) # Se imprime el identificador del commit apuntado por la posición 'i' de la lista.
                i -= 1 # La variable 'i' disminuye en 1, para recorrer toda la lista en orden (del más al menos reciente).

    # Método encargado de mostrar por consola la lista de ramas del repositorio:
    def git_branch(self):
        print("\n--- Ramas ---") # Se imprime un encabezado.
        i = len(self.lista_repo_ramas) - 1 # Almacena en la variable 'i' el mayor índice de 'lista_repo_ramas'.
        while (i >= 0): # Evalúa que el índice sea mayor o igual que cero.
            print("%s"%(self.lista_repo_ramas[i].nombre_rama)) # Se imprime el nombre de la rama apuntada por la posición 'i' de la lista.
            i -= 1 # La variable 'i' disminuye en 1, para recorrer toda la lista en orden (del más al menos reciente).

    # Método auxiliar encargado de comprobar la unicidad del identificador del commit:
    def validacion_identificador_commit(self, identificador_commit: str): # Recibe como parámetro el identificador del commit ingresado por el usuario.
        if self.lista_repo_commits: # Evalúa si 'lista_repo_commits' existe.
            for commit in self.lista_repo_commits: # Recorre la lista de commits, guardando en 'commit' el puntero al objeto del tipo Commit (referenciado por cada posición de la lista).
                if commit.commit_id == identificador_commit: # Evalúa si el identificador coincide con un identificador preexistente.
                    return False # Retorna 'False', rechazando el identificador.
            return True # Retorna 'True', validando el identificador.
        else: # En caso de que 'lista_repo_commits' no exista.
            return True # Retorna 'True', validando el identificador.

    # Método auxiliar encargado de comprobar la unicidad / existencia del nombre de la rama:
    def validacion_identificador_rama(self, identificador_rama: str): # Recibe como parámetro el nombre de la rama ingresado por el usuario.
        for rama in self.lista_repo_ramas: # Recorre la lista de ramas, guardando en 'rama' el puntero al objeto del tipo Rama (referenciado por cada posición de la lista).
            if rama.nombre_rama == identificador_rama: # Evalúa si el nombre coincide con un nombre preexistente.
                return False # Retorna 'False', rechazando el nombre / validando la existencia.
        return True # Retorna 'True', validando el nombre / descartando la existencia.
    
    # Método auxiliar encargado de validar la actualización del contenido de los archivos implicados en un commit:
    def validacion_actualizacion_archivos(self, archivos: list[Archivo]): # Recibe como parámetro una lista de la clase Archivo.
        archivos_actualizados = [archivos[-1]] # Asigna a la variable 'archivos_actualizados' una lista que almacena el puntero al último objeto del tipo Archivo agregado a la lista 'archivos'.
        i = len(archivos) - 2 # Almacena en la variable 'i' el segundo mayor índice de 'archivos'.
        while i >= 0: # Evalúa que el índice sea mayor o igual que cero.
            band = 0 # Inicializa la variable 'band' en cero.
            for elemento in archivos_actualizados: # Recorre la lista 'archivos_actualizados', guardando en 'elemento' el puntero al objeto del tipo Archivo (referenciado por cada posición de la lista).
                if elemento.nombre_archivo == archivos[i].nombre_archivo: # Evalúa si el nombre de cada archivo de la lista 'archivos' coincide con un nombre de archivo existente en la lista 'archivos_actualizados'.
                    band = 1 # Asigna 1 a la variable 'band'.
            if band == 0: # Evalúa si la variable 'band' preserva el valor inicial (implica que no se han hallado coincidencias).
                archivos_actualizados.append(archivos[i]) # Agrega el objeto archivo de la lista 'archivos' a la lista 'archivos_actualizados'.   
            i -= 1 # La variable 'i' disminuye en 1, para recorrer toda la lista en orden (del más al menos reciente).
        return archivos_actualizados # Retorna la lista 'archivos_actualizados'.
    
    # Método auxiliar encargado de validar la actualización de los archivos implicados en un merge:
    def validacion_archivos_merge(self, rama_merge_indice: int): # Recibe como parámetro el índice del objeto rama a fusionar (en 'lista_repo_ramas').
        rama_activa_indice = self.get_index_ramas(self.rama_activa.nombre_rama) # Invoca al método 'get_index_ramas'. El índice del objeto rama (rama activa) en 'lista_repo_ramas' se almacena en la variable 'rama_activa_indice'.
        archivos_merge = [] # Se crea una lista vacía, y se asigna a la variable 'archivos_merge'.
        i = len(self.lista_repo_commits) - 1 # Almacena en la variable 'i' el mayor índice de 'lista_repo_commits'.
        while i >= 0: # Evalúa que el índice sea mayor o igual que cero.
            if self.lista_repo_commits[i].commit_id == self.lista_repo_ramas[rama_activa_indice].commit_reciente.commit_id: # Evalúa si el identificador de algún commit de 'lista_repo_commits' coincide con el identificador del commit más reciente de la rama activa.
                indice1 = rama_activa_indice # Se asigna el índice de la rama activa a la variable 'indice1' (implica que su commit actual es más reciente que el de la otra rama).
                indice2 = rama_merge_indice # Se asigna el índice de la rama a fusionar a la variable 'indice2' (implica que su commit actual es menos reciente que el de la otra rama).
                break
            elif self.lista_repo_commits[i].commit_id == self.lista_repo_ramas[rama_merge_indice].commit_reciente.commit_id: # Evalúa si el identificador de algún commit de 'lista_repo_commits' coincide con el identificador del commit más reciente de la rama a fusionar.
                indice1 = rama_merge_indice # Se asigna el índice de la rama a fusionar a la variable 'indice1' (implica que su commit actual es más reciente que el de la otra rama).
                indice2 = rama_activa_indice # Se asigna el índice de la rama activa a la variable 'indice2' (implica que su commit actual es menos reciente que el de la otra rama).
                break
            i -= 1 # La variable 'i' disminuye en 1, para recorrer toda la lista en orden (del más al menos reciente).
            break
        archivos_merge = self.validacion_actualizacion_archivos(self.lista_repo_ramas[indice2].commit_reciente.lista_archivos + self.lista_repo_ramas[indice1].commit_reciente.lista_archivos) # Invoca al método 'validacion_actualizacion_archivos', que valida la lista que se pasa como argumento, y luego se almacena en la variable 'archivos_merge'.
        return archivos_merge # Retorna la lista 'archivos_merge'.

    # Método auxiliar encargado de agregar por teclado los archivos implicados en un commit:
    def listar_archivos_commit(self):
        band = "0" # Se inicializa la variable 'band' en '0'.
        archivos = [] # Se crea una lista vacía, y se asigna a la variable 'archivos'.
        while (band == "0"): # Evalúa si el valor de la variable 'band' es '0'.
            print("\n--- Carga de Archivo ---") # Se imprime un encabezado.
            nombre = input("Ingrese el nombre del archivo: ") # Se solicita el ingreso del nombre del archivo.
            contenido = input("Ingrese el contenido del archivo: ") # Se solicita el ingreso del contenido del archivo.
            validacion_add_archivos(nombre, contenido, archivos) # Invoca a la función 'validacion_add_archivos', que valida la unicidad de los nombres de los archivos agregados.
            band = input("Ingrese 0 para agregar un nuevo archivo, y cualquier otro valor para proceder al commit: ") # Se emite la consulta de confirmación (permite al usuario acceder al teclado).
        return archivos # Retorna la lista 'archivos'.
    
    # Método auxiliar para imprimir los atributos de los objetos archivo implicados en un commit:
    def imprimir_atributos_archivos(self):
        i = len(self.rama_activa.commit_reciente.lista_archivos) - 1 # Almacena en la variable 'i' el mayor índice de 'lista_archivos', correspondiente al commit más reciente de la rama activa.
        for archivo in self.rama_activa.commit_reciente.lista_archivos: # Recorre 'lista_archivos', guardando en la variable 'archivo' los punteros a los objetos archivo (referenciados por las posiciones de la lista).
            if i == 0: # Evalúa si el índice es igual a cero (último elemento en orden inverso).
                print("%s: %s"%(archivo.nombre_archivo, archivo.contenido_archivo)) # Se imprimen los atributos del último objeto archivo, sin evitar el salto de línea.
            else: # En caso de que el índice sea distinto de cero.
                print("%s: %s,"%(archivo.nombre_archivo, archivo.contenido_archivo), end=" ") # Se imprimen los atributos de los objetos archivo, agregando una coma y evitando el salto de línea.
            i -= 1 # La variable 'i' disminuye en 1, para recorrer toda la lista en orden (del más al menos reciente).
        
    # Método auxiliar encargado de filtrar la lista de ramas existentes (según el nombre), retornando el índice del objeto rama en 'lista_repo_ramas':
    def get_index_ramas(self, nombre_clave_rama: str): # Recibe como parámetro el nombre de la rama cuyo índice se quiere identificar.
        for i in range (len(self.lista_repo_ramas)): # Recorre las posiciones de 'lista_repo_ramas'.
            if self.lista_repo_ramas[i].nombre_rama == nombre_clave_rama: # Evalúa si el nombre del objeto rama apuntado por cada posición de la lista coincide con el argumento 'nombre_clave_rama'.
                return i # Retorna el índice de la posición que apunta al objeto rama seleccionado.
    
# Función auxiliar encargada de validar la unicidad de los nombres de los archivos agregados en el método "listar_archivos_commit":
def validacion_add_archivos(archivo_nombre: str, archivo_contenido: str, archivos_agregados: list[Archivo]): # Recibe como parámetros el nombre y el contenido del archivo a ingresar, y la lista de archivos agregados anteriormente.
    if len(archivos_agregados) > 0: # Evalúa si la lista 'archivos_agregados' tiene elementos.
        for archivo in archivos_agregados: # Recorre la lista 'archivos_agregados', guardando en la variable 'archivo' los punteros a los objetos archivo (referenciados por las posiciones de la lista).
            if archivo.nombre_archivo == archivo_nombre: # Evalúa si el nombre del archivo a ingresar coincide con el nombre de un archivo preexistente.
                archivo.contenido_archivo = archivo_contenido # Modifica el contenido del archivo previamente agregado (actualización).
                return 
        archivos_agregados.append(Archivo(archivo_nombre, archivo_contenido)) # Crea el objeto archivo y lo agrega a la lista 'archivos_agrupados'.
    else: # En caso de que la lista 'archivos_agregados' no tenga elementos.
        archivos_agregados.append(Archivo(archivo_nombre, archivo_contenido)) # Crea el objeto archivo y lo agrega a la lista 'archivos_agrupados'.

# Función para confirmar el commit:
def confirmacion_commit(identificador_commit: str): # Recibe como parámetro el identificador del commit.
    band = input(f"\nIngrese 0 para ejecutar el commit '{identificador_commit}', y cualquier otro valor para descartar: ") # Se emite la consulta de confirmación (permite al usuario acceder al teclado).
    if band == "0": # Evalúa si el usuario ingresó '0' (valor de confirmación).
        return True # Retorna 'True', confirmando la ejecución.
    else: # En caso de que el usuario haya ingresado un valor distinto de cero.
        return False # Retorna 'False', descartando la ejecución.

# Función para confirmar el merge:   
def confirmacion_merge(identificador_merge: str): # Recibe como parámetro el identificador de la fusión (merge).
    band = input(f"\nIngrese 0 para ejecutar el '{identificador_merge}', y cualquier otro valor para descartar: ") # Se emite la consulta de confirmación (permite al usuario acceder al teclado).
    if band == "0": # Evalúa si el usuario ingresó '0' (valor de confirmación).
        return True # Retorna 'True', confirmando la ejecución.
    else: # En caso de que el usuario haya ingresado un valor distinto de cero.
        return False # Retorna 'False', descartando la ejecución.
    
# Función encargada de imprimir los archivos agregados al stage:
def imprimir_stage_area(archivos: list[Archivo]): # Recibe como parámetro una lista del tipo de la clase Archivo, con los archivos agregados al stage area (previo al commit).
    print("\nStage area:", end=" ") # Se imprime un subtítulo.
    for i in range (len(archivos)): # Ciclo que recorre las posiciones de la lista de objetos del tipo Archivo.
        if i == (len(archivos) - 1): # Evalúa si la variable 'i' toma el valor del mayor índice de la lista.
            print("%s: %s"%(archivos[i].nombre_archivo, archivos[i].contenido_archivo)) # Se imprimen los atributos del último objeto archivo, sin evitar el salto de línea.
        else: # En caso de que 'i' no asuma el valor del mayor índice de la lista.
            print("%s: %s,"%(archivos[i].nombre_archivo, archivos[i].contenido_archivo), end=" ") # Se imprimen los atributos de los objetos archivo, agregando una coma y evitando el salto de línea.