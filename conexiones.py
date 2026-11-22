######################################
# Conexión a la base de datos SQLite #
######################################

import sqlite3

# Archivo de base de datos
RUTA_BD = "inventario.db"


def obtiene_conexion():
    
    # Crea y retorna conexión a la base de datos tipo SQLite.
    # Activa claves foráneas y brindar acceso
    # Crea/traspasa función de normalización de texto para búsqueda por nombre y categoría (ignora tildes, díéreses, etc.)    
    from funciones_generales import normaliza_texto

    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.create_function("normaliza_texto", 1, normaliza_texto)

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