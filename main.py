from repositorio import Repositorio

"""
    Por. Juan Diego Cordero Román | 31.115.188 | Sección 305C1

    Main: Código principal para testear el sistema.
"""

# Creamos un nuevo Repositorio.
repo = Repositorio()

# Agregamos Archivos y ejecutamos un Commit.
repo.git_commit("Initial commit")
repo.git_log()

# Creamos una nueva Rama ("develop").
repo.git_branch_create("develop")
repo.git_branch()

# Cambiamos a la Rama "develop".
repo.git_switch("develop")

# Agregamos Archivos y ejecutamos un Commit.
repo.git_commit("Added new feature")
repo.git_log()

# Cambiamos a la Rama "main".
repo.git_switch("main")

# Fusionamos la Rama "develop" con la Rama "main" (MERGE).
repo.git_merge("develop")
repo.git_log()


