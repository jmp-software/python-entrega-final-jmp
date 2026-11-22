##############################################
#                                            #
#  Utilidades de interfaz:                   #
#  - limpieza de pantalla                    #
#  - menú                                    # 
#  - pausas                                  # 
#  - normalización / validación de entradas  #
#  - impresión de tablas de productos        #
#                                            #
##############################################

import os
from funciones_sql import resetea_productos, carga_desde_json

### UTILIDADES DE PANTALLA ### 
def limpia_pantalla():
    # Limpia la terminal (compatible Windows / Linux / Mac)
    os.system("cls" if os.name == "nt" else "clear")


def pausa(mensaje="\nPresioná ENTER para continuar..."):
    # Pausa la ejecución hasta que el usuario presione ENTER
    input(mensaje)


def imprime_menu(tipo=""):
    # Muestra el menú principal del sistema
    print("\n░▒▒▓▓▓████ SISTEMA DE GESTIÓN DE PRODUCTOS ████▓▓▓▒▒░")
    print("")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto (por ID, nombre o categoría)")
    print("4. Actualizar producto (por ID)")
    print("5. Eliminar producto (por ID)")
    print("6. Reporte de bajo stock")
    print("7. Resetear la base de datos")
    print("8. Salir")
    print("")
    if tipo != "":
        print(">", tipo)
        print("")


### NORMALIZACIÓN / VALIDACIÓN ###
def normaliza_texto(texto):
    # Quita acentos, pasa a minúsculas y recorta espacios
    sustituciones = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U",
        "ü": "u", "Ü": "U",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "À": "A", "È": "E", "Ì": "I", "Ò": "O", "Ù": "U",
        "ñ": "n", "Ñ": "N",
    }
    for original, comun in sustituciones.items():
        texto = texto.replace(original, comun)
    return texto.strip().lower()


def valida_precio(precio_texto):
    
    # Valida y normaliza un precio ingresado por el usuario.
    # Acepta '.' o ',' como separador decimal.
    # Devuelve el precio como float, o None si es inválido.
    
    precio_texto = precio_texto.strip().replace(",", ".")
    # Solo permitimos un punto decimal
    if precio_texto.count(".") > 1:
        return None
    try:
        precio = float(precio_texto)
        if precio < 0:
            return None
        return precio
    except ValueError:
        return None


def valida_entero_positivo(texto, permitir_cero=True):
    
    # Valida un entero >= 0 (o > 0 si permitir_cero=False).
    # Devuelve el entero o None si es inválido.
    
    texto = texto.strip()
    if not texto.isdigit():
        return None
    valor = int(texto)
    if not permitir_cero and valor == 0:
        return None
    return valor


### IMPRESIÓN DE PRODUCTOS ###
def imprime_producto(producto):
    
    # Imprime un único producto con formato
    
    print(f"   ID: {producto['id']} | "
          f"Nombre: {producto['nombre']} | "
          f"Categoría: {producto['categoria']} | "
          f"Cantidad: {producto['cantidad']} | "
          f"Precio: ${producto['precio']:.2f}")
    if producto["descripcion"]:
        print(f"       Descripción: {producto['descripcion']}")


def imprime_lista_productos(lista):
    
    # Imprime lista de productos o un mensaje si está vacía

    if not lista:
        print("❌ No hay productos para mostrar.")
        return
    print("\nProductos registrados:\n")
    for producto in lista:
        imprime_producto(producto)

def resetea_bd_interfaz():
   
    # Interfaz para resetear la base de datos 
    
    print("\n░▒▓█ Resetear base de datos █▓▒░\n")
    print("⚠️  Esta acción eliminará TODOS los productos de la base de datos.")
    confirmacion = input("¿Estás seguro? Escribí 'SI' o 'S' para continuar: ").strip().upper()

    if confirmacion != "SI" and confirmacion != "S":
        print("↩️  Reseteo cancelado.")
        pausa()
        return

    cantidad_previa = resetea_productos()
    print(f"✔️  Se eliminaron {cantidad_previa} productos. La base quedó vacía.")

    recargar = input("\n¿Querés recargar los productos por defecto desde 'productos.json'? (s/n): ").strip().lower()
    if recargar == "s":
        insertados = carga_desde_json()
        if insertados > 0:
            print(f"✔️  Se cargaron {insertados} productos desde 'productos.json'.")
        else:
            print("⚠️  No se pudo cargar nada (archivo inexistente, vacío o con formato inválido).")
    else:
        print("ℹ️  La base quedó vacía.")

    pausa()



