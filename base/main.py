import cx_Oracle
import getpass

_SERVICE_NAME = 'orcl'

def main():
    # Pedir las credenciales
    new_user = input('Ingrese el nombre del nuevo usuario: ').upper()
    new_user_password = getpass.getpass(prompt='Ingrese la contraseña del nuevo usuario: ')
    
    if not new_user:
        new_user = 'MDY3131_NOMBRE_APELLIDO_EJERCICIO_1'
        
    if not new_user_password:
        new_user_password = 'MDY3131.practica_2'

    # Conectar a la base de datos como SYSDBA
    dsn = cx_Oracle.makedsn('localhost', 1521, service_name=_SERVICE_NAME)
    connection = None

    try:
        connection = cx_Oracle.connect(user='sys', password='sys', dsn=dsn, mode=cx_Oracle.SYSDBA)
        cursor = connection.cursor()

        # Crear el nuevo usuario
        cursor.execute(f"alter session set \"_ORACLE_SCRIPT\"=true")
        cursor.execute(f"CREATE USER \"{new_user}\" IDENTIFIED BY \"{new_user_password}\"")
        
        # DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE TEMP
        cursor.execute(f"ALTER USER \"{new_user}\" DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE TEMP")
        cursor.execute(f"ALTER USER \"{new_user}\" QUOTA UNLIMITED ON USERS")
        cursor.execute(f"GRANT CREATE SESSION TO \"{new_user}\"")
        cursor.execute(f"GRANT \"RESOURCE\" TO \"{new_user}\"")
        cursor.execute(f"ALTER USER \"{new_user}\" DEFAULT ROLE \"RESOURCE\"")
        print(f'Usuario \"{new_user}\" creado exitosamente.')
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f'Error al crear el usuario {new_user}: {error.message}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    main()
