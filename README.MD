# oracle-user-manager

### English
A user-friendly application to manage Oracle database users and execute SQL files with a graphical interface.

## Español
Una aplicación fácil de usar para gestionar usuarios de la base de datos Oracle y ejecutar archivos SQL con una interfaz gráfica.

## 中文
一个用户友好的应用程序，用于管理 Oracle 数据库用户和通过图形界面执行 SQL 文件。


## Descripción del Proyecto

Este proyecto contiene un script en Python que permite crear un nuevo usuario en una base de datos Oracle. El script se conecta a la base de datos como `SYSDBA`, crea el usuario y le asigna los permisos básicos de `CONNECT` y `RESOURCE`.

## Requisitos

- Python 3.x
- Oracle Database
- Biblioteca `cx_Oracle` de Python

## Configuración del Entorno Virtual

1. **Clonar el repositorio** (opcional):
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. **Crear un entorno virtual**:
    ```sh
    python -m venv myenv
    ```

3. **Activar el entorno virtual**:
    - En Windows:
        ```sh
        myenv\Scripts\activate
        ```
    - En macOS y Linux:
        ```sh
        source myenv/bin/activate
        ```

4. **Instalar los requisitos**:
    ```sh
    pip install -r requirements.txt
    ```

## Uso del Script

1. **Ejecutar el script**:
    ```sh
    python main.py
    ```

2. **Proporcionar las credenciales**:
    - SID puede ser  `xe` o `orcl`.
    - El usuario `sys` y su contraseña `sys`.
    - El nombre del nuevo usuario.
    - La contraseña del nuevo usuario.

## Descripción del Script

El script `main.py` realiza las siguientes acciones:
1. Solicita al usuario las credenciales necesarias:
    - Servicio de la base de datos (SID) ->  (`xe` o `orcl`).
    - El usuario `sys` y su contraseña `sys`.
    - Nombre del nuevo usuario.
    - Contraseña del nuevo usuario.
2. Se conecta a la base de datos Oracle como `SYSDBA`.
3. Crea el nuevo usuario y le asigna los permisos `CONNECT` y `RESOURCE`.
4. Maneja los errores que puedan ocurrir durante la ejecución.

## Nota
Asegúrate de que el servicio de Oracle Database esté en funcionamiento y que cx_Oracle pueda conectarse a la base de datos.

## Compilar en exe
    https://pyinstaller.org/en/stable/usage.html

    ```sh
        pyinstaller --onefile --icon=icono.ico --name=oracle_user_manager main.py

        
    ```

    Limpiar Archivos: Después de la creación del ejecutable, puedes limpiar los archivos temporales generados por PyInstaller si no los necesitas:
   ```sh
        rm -rf build && rm -rf dist && rm -f *.spec
    ```



