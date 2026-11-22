# 🐍 Entrega Final - Curso de Iniciación a la Programación con Python | Talento Tech - Año 2026 - Comisión 26209 

Sistema de gestión de productos con base de datos SQLite, desarrollado como proyecto final del curso de iniciación a la programación con Python. 

## 📋 Descripción

Aplicación de terminal que permite administrar un inventario de productos alojado en una base de datos inventario.db (SQLite). Incluye operaciones CRUD completas, búsqueda por ID y por nombre o categoría, y un reporte de productos con límite máximo de stock.

## ✨ Funcionalidades

- ➕ Guardar nuevos productos
- 📄 Visualizar todos los productos guardados
- 🔍 Buscar productos por ID, nombre o categoría
- ✏️ Actualizar productos por ID
- 🗑️ Eliminar productos por ID
- ⚠️ Reporte de productos con cantidad igual o inferior a un límite indicado de stock
- 🔄 Resetear la base de datos con opción de recargar desde productos.json un listado por defecto

## 🗄️ Base de datos

El programa utiliza SQLite y crea automáticamente el archivo inventario.db la primera vez que se ejecuta, junto con la tabla productos:

| Columna       | Tipo    | Restricciones              |
|---------------|---------|----------------------------|
| id            | INTEGER | PRIMARY KEY AUTOINCREMENT  |
| nombre        | TEXT    | NOT NULL                   |
| descripcion   | TEXT    | —                          |
| cantidad      | INTEGER | NOT NULL                   |
| precio        | REAL    | NOT NULL                   |
| categoria     | TEXT    | —                          |

💡 Si la base está vacía y existe productos.json, el programa intenta precargarla automáticamente desde ese archivo json.

## 📁 Estructura del proyecto

├── main.py              
├── conexiones.py       
├── funciones_sql.py     
├── funciones_generales.py         
├── productos.json       
├── inventario.db        
└── README.md

## 💻 Sistemas testeados

- 🪟 Windows 10
- 🐧 Linux (Arch y derivados)

## 📥 Descargar el proyecto

Clonar el repositorio:

    git clone https://github.com/jmp-software/python-entrega-final-jmp.git

Ingresar al directorio del proyecto:

    cd python-entrega-final-jmp

## ▶️ Cómo ejecutar


### 🪟 Windows o 🐧 Linux  


    python main.py


## 🧭 Menú principal

| Opción | Acción                                            |
|:------:|---------------------------------------------------|
|   1    | Agregar producto                                  |
|   2    | Mostrar productos                                 |
|   3    | Buscar producto (por ID, nombre o categoría)      |
|   4    | Actualizar producto (por ID)                      |
|   5    | Eliminar producto (por ID)                        |
|   6    | Reporte de bajo stock                             |
|   7    | Resetear base de datos                            |
|   8    | Salir                                             |

## 🛠️ Tecnologías utilizadas

- Python 3.10+ (usa match/case)
- SQLite (módulo sqlite3 de la biblioteca estándar)
- JSON (módulo json de la biblioteca estándar)

## 👤 Autor

jmp-software — Comisión 26209, Talento Tech