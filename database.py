import sqlite3
import uuid
from datetime import datetime

DB_NAME = "seminuevaspy.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Tabla adaptada a tus columnas exactas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id TEXT PRIMARY KEY,
            fecha_hora TEXT,
            monto_gs REAL,
            metodo_pago TEXT,
            descripcion_prenda TEXT,
            nombre_clienta TEXT,
            vendedora TEXT,
            estado TEXT,      
            sync_status INTEGER 
        )
    ''')
    conn.commit()
    conn.close()

def agregar_venta(monto_gs, metodo_pago, descripcion_prenda, nombre_clienta, vendedora):
    conn = get_connection()
    cursor = conn.cursor()
    
    venta_id = str(uuid.uuid4()) 
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "activa"
    sync_status = 0 
    
    cursor.execute('''
        INSERT INTO ventas (id, fecha_hora, monto_gs, metodo_pago, descripcion_prenda, nombre_clienta, vendedora, estado, sync_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (venta_id, fecha_actual, monto_gs, metodo_pago, descripcion_prenda, nombre_clienta, vendedora, estado, sync_status))
    
    conn.commit()
    conn.close()
    return venta_id

def anular_venta(venta_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ventas SET estado = 'anulada', sync_status = 0 WHERE id = ?", (venta_id,))
    conn.commit()
    conn.close()

def obtener_ventas_pendientes_sync():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas WHERE sync_status = 0")
    columnas = [column[0] for column in cursor.description]
    resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
    conn.close()
    return resultados

def marcar_como_sincronizada(venta_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ventas SET sync_status = 1 WHERE id = ?", (venta_id,))
    conn.commit()
    conn.close()

def obtener_todas_las_ventas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas ORDER BY fecha_hora DESC")
    columnas = [column[0] for column in cursor.description]
    resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
    conn.close()
    return resultados

if __name__ == "__main__":
    init_db()
    print("Base de datos SQLite inicializada con tus columnas personalizadas.")