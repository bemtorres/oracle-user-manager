import cx_Oracle
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser

from config.config import DB_SERVICE_NAMES, ICON_PATH, YOUTUBE_CHANNEL_URL

def open_youtube_channel():
    webbrowser.open(YOUTUBE_CHANNEL_URL)

def display_text_status(msg, color):
    connection_status_label.config(text=msg, fg=color)
    
def create_user(drop_user = False):
    sys_password = sys_password_entry.get()
    # sys_password = 'sys'
    sys_user = sys_user_entry.get()
    
    new_user = new_user_entry.get().upper()
    new_user_password = new_user_password_entry.get()
    service_name = service_combobox.get()

    if not sys_password or not new_user or not new_user_password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    dsn = cx_Oracle.makedsn('localhost', 1521, service_name=service_name)
    connection = None

    try:
        connection = cx_Oracle.connect(user=sys_user, password=sys_password, dsn=dsn, mode=cx_Oracle.SYSDBA)
        cursor = connection.cursor()
        
        cursor.execute(f"alter session set \"_ORACLE_SCRIPT\"=true")
        
        if drop_user:
            cursor.execute(f"DROP USER {new_user} CASCADE")
            messagebox.showinfo("DROP USER", f'Usuario {new_user} eliminado exitosamente.')
        
        cursor.execute(f"CREATE USER {new_user} IDENTIFIED BY \"{new_user_password}\" DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE TEMP")
        cursor.execute(f"ALTER USER {new_user} QUOTA UNLIMITED ON USERS")
        cursor.execute(f"GRANT CREATE SESSION TO {new_user}")
        cursor.execute(f"GRANT RESOURCE TO {new_user}")
        cursor.execute(f"ALTER USER {new_user} DEFAULT ROLE RESOURCE")

        messagebox.showinfo("Éxito", f'Usuario {new_user} creado exitosamente.')
        display_text_status(f"Usuario creado exitosamente. \n\n USUARIO: {new_user} \n\n PASSWORD: {new_user_password}", "blue")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        messagebox.showerror("Error", f'Error al crear el usuario {new_user}: {error.message}')
        display_text_status(f"Error al crear el usuario \n\n  {new_user}","red")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def test_connection(service_name, username, password):
    dsn = cx_Oracle.makedsn('localhost', 1521, service_name=service_name)
    connection = None

    try:
        # https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        return True, "Conexión exitosa a la base de datos."
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return False, f'Error de conexión: {error.message}'
    finally:
        if connection:
            connection.close()
    
def on_test_connection():
    username = new_user_entry.get().upper()
    password = new_user_password_entry.get()
    service_name = service_combobox.get()

    if not username or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    success, msg = test_connection(service_name, username, password)
    
    if success:
        display_text_status(msg, "green")
        messagebox.showinfo("Éxito", msg)
    else:
        display_text_status(msg, "red")
        messagebox.showerror("Error", msg)


def load_sql_file():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo SQL", filetypes=[("SQL files", "*.txt")])
    if not file_path:
        return
    
    new_user = new_user_entry.get().upper()
    new_user_password = new_user_password_entry.get()
    service_name = service_combobox.get()

    if not new_user or not new_user_password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    dsn = cx_Oracle.makedsn('localhost', 1521, service_name=service_name)
    connection = None

    try:
        connection = cx_Oracle.connect(user=new_user, password=new_user_password, dsn=dsn)
        cursor = connection.cursor()
        
        # solucion de error ORA-00933: sql command not properly ended
        cursor.execute(f"UPDATE DATABASECHANGELOGLOCK SET LOCKED=0, LOCKGRANTED=null, LOCKEDBY=null where ID=1")
        # 
        
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read()

        cursor.execute(sql_commands)
        messagebox.showinfo("Éxito", "El archivo SQL se ha ejecutado exitosamente.")
        display_text_status("El archivo SQL se ha ejecutado exitosamente.", "green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        messagebox.showerror("Error", f'Error al ejecutar el archivo SQL: {error.message}')
        display_text_status(error.message, "red")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Crear la ventana principal
root = tk.Tk()
root.title("代码库 CODE&CODE | Oracle User Manager v0.1.0 | PROFE BENJA")

# Añadir un ícono
icon_path = 'icono.ico'
root.iconbitmap(icon_path)
# root.iconbitmap(ICON_PATH)

# Establecer el tamaño de la ventana
window_width = 500
window_height = 350
center_window(root, window_width, window_height)


# Crear y ubicar los widgets
tk.Label(root, text="Servicio de Base de Datos:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
service_combobox = ttk.Combobox(root, values=DB_SERVICE_NAMES, width=45)
service_combobox.grid(row=0, column=1, padx=10, pady=5)
service_combobox.current(0)  # Establecer valor predeterminado

tk.Label(root, text="Nombre del nuevo usuario:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
sys_user_entry = tk.Entry(root, width=45)
sys_user_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña del usuario SYS:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
sys_password_entry = tk.Entry(root, show='*', width=45)
sys_password_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre del nuevo usuario:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
new_user_entry = tk.Entry(root, width=45)
new_user_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña del nuevo usuario:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
new_user_password_entry = tk.Entry(root, show='*', width=45)
new_user_password_entry.grid(row=4, column=1, padx=10, pady=5)


sys_password_entry.insert(0, 'sys')
sys_user_entry.insert(0, 'sys')
new_user_entry.insert(0, 'MDY3131_NOMBRE_APELLIDO_EJERCICIO_1')
new_user_password_entry.insert(0, 'MDY3131.practica_2')


tk.Button(root, text="Cargar Archivo SQL", command=load_sql_file).grid(row=5, column=0, pady=10)
tk.Button(root, text="Crear Usuario", command=create_user).grid(row=5, column=1, pady=10)

tk.Button(root, text="Probar Conexión", command=on_test_connection).grid(row=6, column=0, columnspan=1, pady=10)
tk.Button(root, text="REINICIAR USUARIO", command=lambda: create_user(drop_user=True)).grid(row=6, column=1, columnspan=1, pady=10)


tk.Button(root, text="Ir a Canal de YouTube", command=open_youtube_channel).grid(row=7, column=0, columnspan=2, pady=10)

connection_status_label = tk.Label(root, text="Estado de la conexión no comprobado", fg="blue")
connection_status_label.grid(row=9, column=0, columnspan=2, pady=10)
# Iniciar el bucle principal de la GUI
root.mainloop()
