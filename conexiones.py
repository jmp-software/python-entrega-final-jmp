######################################
# Conexión a la base de datos SQLite #
######################################

import sqlite3

# Archivo de base de datos
RUTA_BD = "inventario.db"


def obtiene_conexion():
    
    # Crear y devolver conexión a la base de datos tipo SQLite.
    # Activar claves foráneas y brindar filas como sqlite3.Row para acceder a columnas por nombre.
    
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


def crea_tabla():
    
    # Crea la tabla 'productos' si no existe.
    # Columnas:
    #    id          -> entero, PK se incrementa automáticamente
    #    nombre      -> texto, NOT NULL
    #    descripcion -> texto
    #    cantidad    -> entero, NOT NULL
    #    precio      -> real, NOT NULL
    #    categoria   -> texto
    
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT    NOT NULL,
                descripcion TEXT,
                cantidad    INTEGER NOT NULL,
                precio      REAL    NOT NULL,
                categoria   TEXT
            )
        """)
        conexion.commit()


def inicia_bd():
    
    # Inicializa la base de datos creando la tabla al arrancar el programa
    
    crea_tabla()