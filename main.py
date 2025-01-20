from repositorio import Repositorio

"""
    Por: Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Main: Código principal para testear el sistema.
"""

# Crear el repositorio.
repo = Repositorio()

# Añadir archivos y ejecutar un commit en la rama 'main'.
repo.git_commit(input("\ngit commit -m "))

# Mostrar el historial de commits.
repo.git_log()

# Crear una nueva rama ('develop').
repo.git_branch_create(input("\ngit branch "))

# Mostrar la lista de ramas del repositorio.
repo.git_branch()

# Cambiar a la rama ('develop').
repo.git_switch(input("\ngit switch "))

# Añadir archivos y ejecutar un commit en la rama ('develop').
repo.git_commit(input("\ngit commit -m "))

# Mostrar el historial de commits.
repo.git_log()

# Cambiar a la rama 'main'.
repo.git_switch(input("\ngit switch "))

# Añadir archivos y ejecutar un commit en la rama 'main'.
repo.git_commit(input("\ngit commit -m "))

# Mostrar el historial de commits.
repo.git_log()

# Crear una nueva rama ('alternative').
repo.git_branch_create(input("\ngit branch "))

# Mostrar la lista de ramas del repositorio.
repo.git_branch()

# Cambiar a la rama ('alternative')
repo.git_switch(input("\ngit switch "))

# Añadir archivos y ejecutar un commit en la rama ('alternative').
repo.git_commit(input("\ngit commit -m "))

# Mostrar el historial de commits.
repo.git_log()

# Cambiar a la rama ('develop').
repo.git_switch(input("\ngit switch "))

# Fusionar la rama ('alternative') con la rama ('develop') - Merge.
repo.git_merge(input("\ngit merge "))

# Mostrar el historial de commits.
repo.git_log()

# Cambiar a la rama 'main'.
repo.git_switch(input("\ngit switch "))

# Fusionar la rama ('develop') con la rama 'main' - Merge.
repo.git_merge(input("\ngit merge "))

# Mostrar el historial de commits.
repo.git_log()