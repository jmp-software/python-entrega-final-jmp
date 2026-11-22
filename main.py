#################################################
# Entrega Final - Talento Tech - Comisión 26209 #
#################################################

"""
Programa de gestión de productos con SQLite:

 - Base de datos 'inventario.db' y tabla 'productos'
 - Guardar, visualizar, modifgicar y borrar productos (por ID)
 - Buscar por ID y opcionalmente por nombre / categoría
 - Listar productos con cantidad igual o menor al un límite de stock
 - Proyecto modularizado en diferente archivos y funciones
"""

from conexiones import inicia_bd
from funciones_generales import (
    limpia_pantalla, pausa, imprime_menu,
    normaliza_texto, valida_precio, valida_entero_positivo,
    imprime_producto, imprime_lista_productos, resetea_bd_interfaz
)
from funciones_sql import (
    inserta_producto, obtiene_todos, obtiene_por_id,
    busca_por_nombre_o_categoria, productos_bajo_stock,
    actualiza_producto, elimina_producto, carga_desde_json 
)

PRECARGAR_DESDE_JSON = True # Poner en False para que no haga la pregarga automática desde el JSON al iniciar el programa (en True solo la hace si la lista está vacía)


### 1) AGREGA DE PRODUCTO ###
def alta_producto():
    print("\n░▒▓█ Agregar producto █▓▒░\n")

    nombre = input("Ingresá el nombre del producto: ").strip()
    if not nombre:
        print("❌ ¡El nombre ingresado es incorrecto!")
        pausa(); return

    descripcion = input("Ingresá una descripción (opcional): ").strip()

    categoria = input("Ingrese la categoría del producto: ").strip()
    if not categoria:
        print("❌ ¡La categoría ingresada es incorrecta!")
        pausa(); return

    cantidad_texto = input("Ingresá la cantidad disponible: ").strip()
    cantidad = valida_entero_positivo(cantidad_texto, permitir_cero=True)
    if cantidad is None:
        print("❌ ¡La cantidad ingresada es incorrecta!")
        pausa(); return

    precio_texto = input("Ingresá el precio (puede usar '.' o ','): ").strip()
    precio = valida_precio(precio_texto)
    if precio is None:
        print("❌ ¡El precio ingresado es incorrecto!")
        pausa(); return

    nuevo_id = inserta_producto(nombre, descripcion, cantidad, precio, categoria)
    print(f"✔️  Producto '{nombre}' agregado con ID {nuevo_id}.")
    pausa()


### 2) LISTAR PRODUCTOS ###
def lista_productos():
    print("\n░▒▓█ Listar productos █▓▒░")
    productos = obtiene_todos()
    imprime_lista_productos(productos)
    pausa()


### 3) BUSCAR PRODUCTOS ###
def busca_producto():
    limpia_pantalla()
    imprime_menu("3")
    print("░▒▓█ Búsqueda de productos █▓▒░\n")
    print("a) Buscar por ID")
    print("b) Buscar por nombre o categoría")
    opcion = input("> ").strip().lower()

    if opcion == "a":
        id_texto = input("Ingresá el ID del producto: ").strip()
        id_producto = valida_entero_positivo(id_texto, permitir_cero=False)
        if id_producto is None:
            print("❌ ¡ID inválido!")
            pausa(); return
        producto = obtiene_por_id(id_producto)
        if producto:
            print("\nProducto encontrado:\n")
            imprime_producto(producto)
        else:
            print("❌ ¡No se encontró un producto con ese ID!")

    elif opcion == "b":
        texto = normaliza_texto(input("Ingresá nombre o categoría a buscar: "))
        if not texto:
            print("❌ ¡La búsqueda no puede estar vacía!")
            pausa(); return
        resultados = busca_por_nombre_o_categoria(texto)
        if resultados:
            print("\nResultados encontrados:\n")
            for p in resultados:
                imprime_producto(p)
        else:
            print("❌ ¡No se encontraron resultados!")

    else:
        print("❌ Opción errónea.")

    pausa()


### 4) ACTUALIZA/MODIFICA PRODUCTO ###
def actualiza_producto_interfaz():
    limpia_pantalla()
    imprime_menu("4")
    print("░▒▓█ Actualizar producto █▓▒░\n")

    id_texto = input("Ingresá el ID del producto a actualizar: ").strip()
    id_producto = valida_entero_positivo(id_texto, permitir_cero=False)
    if id_producto is None:
        print("❌ ¡ID inválido!")
        pausa(); return

    producto = obtiene_por_id(id_producto)
    if not producto:
        print("❌ ¡No existe un producto con ese ID!")
        pausa(); return

    print("\nProducto actual:\n")
    imprime_producto(producto)
    print("\nIngresá los nuevos valores (dejá vacío para conservar el actual):\n")

    nombre = input(f"Nombre [{producto['nombre']}]: ").strip() or producto["nombre"]

    descripcion = input(f"Descripción [{producto['descripcion'] or ''}]: ").strip()
    if descripcion == "":
        descripcion = producto["descripcion"] or ""

    categoria = input(f"Categoría [{producto['categoria'] or ''}]: ").strip()
    if categoria == "":
        categoria = producto["categoria"] or ""

    cantidad_texto = input(f"Cantidad [{producto['cantidad']}]: ").strip()
    if cantidad_texto == "":
        cantidad = producto["cantidad"]
    else:
        cantidad = valida_entero_positivo(cantidad_texto, permitir_cero=True)
        if cantidad is None:
            print("❌ ¡Cantidad inválida! Se cancela la actualización.")
            pausa(); return

    precio_texto = input(f"Precio [{producto['precio']:.2f}]: ").strip()
    if precio_texto == "":
        precio = producto["precio"]
    else:
        precio = valida_precio(precio_texto)
        if precio is None:
            print("❌ ¡Precio inválido! Se cancela la actualización.")
            pausa(); return

    if actualiza_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
        print(f"✔️  Producto ID {id_producto} actualizado correctamente.")
    else:
        print("❌ No se pudo actualizar el producto.")
    pausa()


### 5) BORRA PRODUCTO ###
def elimina_producto_interfaz():
    limpia_pantalla()
    imprime_menu("5")
    print("░▒▓█ Eliminar producto █▓▒░\n")

    productos = obtiene_todos()
    if not productos:
        print("❌ No hay productos para eliminar.")
        pausa(); return

    print("Productos disponibles:\n")
    for p in productos:
        print(f"   {p['id']}. {p['nombre']}")

    id_texto = input("\nIngresá el ID del producto a eliminar: ").strip()
    id_producto = valida_entero_positivo(id_texto, permitir_cero=False)
    if id_producto is None:
        print("❌ ¡ID inválido!")
        pausa(); return

    producto = obtiene_por_id(id_producto)
    if not producto:
        print("❌ ¡No existe un producto con ese ID!")
        pausa(); return

    confirmacion = input(f"¿Eliminar '{producto['nombre']}' (ID {id_producto})? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("↩️  Eliminación cancelada.")
        pausa(); return

    if elimina_producto(id_producto):
        print(f"✔️  Producto '{producto['nombre']}' eliminado.")
    else:
        print("❌ No se pudo eliminar el producto.")
    pausa()


### 6) LISTA CON POR LÍMITE DE STOCK ###
def lista_con_limite_de_stock():
    print("\n░▒▓█ Reporte de bajo stock █▓▒░\n")

    limite_texto = input("Ingresá el límite de cantidad (inclusive): ").strip()
    limite = valida_entero_positivo(limite_texto, permitir_cero=True)
    if limite is None:
        print("❌ ¡Límite inválido!")
        pausa(); return

    resultados = productos_bajo_stock(limite)
    if resultados:
        print(f"\nProductos con cantidad <= {limite}:\n")
        for p in resultados:
            imprime_producto(p)
    else:
        print(f"✔️  No hay productos con cantidad igual o menor a {limite}.")
    pausa()


### MENÚ PRINCIPAL ###
def main():
    inicia_bd()
    
    # Intenta cargar automáticamente la primera vez desde el JSON si la base de datos está vacía y existe el JSON
    if PRECARGAR_DESDE_JSON and not obtiene_todos():
        
        insertados = carga_desde_json()
        if insertados > 0:
            limpia_pantalla()   
            print(f"ℹ️  Se precargaron {insertados} productos desde 'productos.json'.")
            pausa()
    
    salir = False

    while not salir:
        limpia_pantalla()
        imprime_menu()
        opcion = input("> ").strip()

        match opcion:
            case "1":
                alta_producto()
            case "2":
                lista_productos()
            case "3":
                busca_producto()
            case "4":
                actualiza_producto_interfaz()
            case "5":
                elimina_producto_interfaz()
            case "6":
                lista_con_limite_de_stock()
            case "7":
                resetea_bd_interfaz()
            case "8":
                print("\n¡Saliste del sistema! 🏃🚪")
                salir = True
            case _:
                print("❌ Opción errónea")
                pausa()


if __name__ == "__main__":
    main()