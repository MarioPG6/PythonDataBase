# Python y Bases de Datos con SQLite

Este proyecto muestra cómo trabajar con **SQLite** en Python para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos.

## Instalación y Preparación

SQLite es un motor de base de datos ligero y sin servidor. En Ubuntu, normalmente ya viene incluido el módulo `sqlite3` en Python.

Para comprobar que SQLite está instalado en tu sistema, ejecuta:

```sh
sqlite3 --version
```

Si no está instalado, puedes hacerlo con:

```sh
sudo apt install sqlite3
```

## Estructura del Programa

El programa realiza las siguientes operaciones:

1. Conectar (o crear) una base de datos SQLite.
2. Crear una tabla si no existe.
3. Realizar operaciones CRUD:
   - Crear: Insertar nuevos registros.
   - Leer: Consultar los registros existentes.
   - Actualizar: Modificar un registro.
   - Eliminar: Borrar un registro.

## Código

Puedes encontrar el código del proyecto en **crud.py**. También puedes copiarlo desde el siguiente enlace y pegarlo en VSCode:

[Enlace al Código CRUD en SQLite](https://1drv.ms/u/c/f5a0e6d62543b390/EYDLYqdKrEBMhqpL8pYeCJwBXfSgAuel3ydchgCoR-auVw?e=4pPay7)

## Ejecución del Proyecto

1. Clona este repositorio en tu máquina:
   ```sh
   git clone git@github.com:MarioPG6/PythonDataBase.git
   cd PythonDataBase
   ```
2. Asegúrate de tener Python instalado (versión 3.x recomendada).
3. Ejecuta el script:
   ```sh
   python crud.py
   ```

## Notas Adicionales

- SQLite almacena la base de datos en un solo archivo `.db`, lo que facilita su portabilidad.
- Puedes inspeccionar la base de datos con herramientas como **DB Browser for SQLite**.
- Asegúrate de cerrar la conexión a la base de datos después de cada operación para evitar bloqueos.

Para dudas o mejoras, contacta al autor o contribuye al proyecto.
