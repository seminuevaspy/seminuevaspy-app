import sqlite3
from datetime import datetime
import pandas as pd

def crear_conexion():
    try:
        conn = sqlite3.connect('seminuevaspy.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar: {e}")
        return None

def inicializar_db():
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora DATETIME NOT NULL,
                    monto_gs INTEGER NOT NULL,
                    metodo_pago TEXT NOT NULL,
                    nombre_clienta TEXT,
                    vendedora TEXT NOT NULL,
                    descripcion_prenda TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conn.close()

def registrar_venta(monto, metodo_pago, nombre_clienta, vendedora, descripcion_prenda):
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO ventas (fecha_hora, monto_gs, metodo_pago, nombre_clienta, vendedora, descripcion_prenda)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (fecha_actual, monto, metodo_pago, nombre_clienta, vendedora, descripcion_prenda))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar venta: {e}")
            return False
        finally:
            conn.close()

def obtener_datos_ventas():
    conn = crear_conexion()
    if conn is not None:
        df = pd.read_sql_query("SELECT * FROM ventas ORDER BY id DESC", conn)
        conn.close()
        return df
    return pd.DataFrame()

def eliminar_venta(id_venta):
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas WHERE id = ?", (id_venta,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            conn.close()