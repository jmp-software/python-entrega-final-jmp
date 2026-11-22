###################################
# CRUD sobre la tabla 'productos' #
###################################

import json
import os

ARCHIVO_JSON = "productos.json"

from conexiones import obtiene_conexion


### CREA PRODUCTO ###
def inserta_producto(nombre, descripcion, cantidad, precio, categoria):
    # Crea el producto y retorna el ID
    
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        return cursor.lastrowid


### LEE LISTADO DE PRODUCTOS ###
def obtiene_todos():
    
    # Retorna lista de todos los productos guardados
    # (sqlite3.Row, por nombre de columna)

    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id")
        return cursor.fetchall()


### LEE PRODUCTO POR ID ###
def obtiene_por_id(id_producto):
    
    # Retorna producto según ID o "NONE" si no existe
    
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        return cursor.fetchone()


### BUSCA PRODUCTO POR NOMBRE O CATEGORÍA ###
def busca_por_nombre_o_categoria(texto):
    
    # Búsqueda por nombre o categoría (no distinge mayúsculas/minúsculas, tíldes, ni diéresis, etc.)

    patron = f"%{texto}%"
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE normaliza_texto(nombre)LIKE ? COLLATE NOCASE
               OR normaliza_texto(categoria) LIKE ? COLLATE NOCASE
            ORDER BY id
        """, (patron, patron))
        return cursor.fetchall()


### BUSCA PRODUCTOS POR LÍMITE DE STOCK ###
def productos_bajo_stock(limite):
 
    # Retorna productos cuya cantidad sea igual o inferior al número ingresado
   
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE cantidad <= ?
            ORDER BY cantidad ASC
        """, (limite,))
        return cursor.fetchall()


### ACTUALIZA PRODUCTO ###
def actualiza_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
 
    # Actualiza todos los campos de un producto referenciado por ID
    # Devuelve VERDADERO si se modificó alguna fila, FALSO si el ID no existe
    
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos
               SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
             WHERE id = ?
        """, (nombre, descripcion, cantidad, precio, categoria, id_producto))
        conexion.commit()
        return cursor.rowcount > 0


### BORRA PRODUCTO ###
def elimina_producto(id_producto):

    # Elimina un producto por su ID
    # Devuelve VERDADERO si se eliminó, FALSO si el ID no existía

    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        return cursor.rowcount > 0


### RESETEAR LISTADO DE PRODUCTOS ###
def resetea_productos():
    
    # Borra TODOS los productos de la tabla y reinicia el contador de ID
    # Retorna la cantidad de productos que había antes de resetear
    
    with obtiene_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos")
        cantidad_previa = cursor.fetchone()[0]

        # Borra todas las filas
        cursor.execute("DELETE FROM productos")

        # Reinicia el AUTOINCREMENT para que el próximo id vuelva a 1
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'productos'")

        conexion.commit()
        return cantidad_previa


### REESTABLECER BASE DATOS POR DEFECTO ###
def carga_desde_json(ruta=ARCHIVO_JSON):
    
    # Lee el JSON con el formato nuevo e inserta todos los productos en la base de datos para completar el reseteo
    # Retorna la cantidad de productos insertados (0 si no había nada o hubo error)
   
    if not os.path.exists(ruta):
        return 0

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, ValueError):
        return 0

    insertados = 0
    for item in datos:
        # Validación de campos
        try:
            nombre = item["nombre"]
            descripcion = item.get("descripcion", "")
            cantidad = int(item["cantidad"])
            precio = float(item["precio"])
            categoria = item.get("categoria", "")
        except (KeyError, TypeError, ValueError):
            # Si hay alguno inválido, lo saltea
            continue

        inserta_producto(nombre, descripcion, cantidad, precio, categoria)
        insertados += 1

    return insertados
