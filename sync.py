import requests
import database

# Tu URL oficial conectada a Seminuevaspy
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyKe-suHpsnCkBL7qtbHbqSwExrSB3tYfrHBtbJINjLMNezq5dUZjoR1hobVg-fZkzFvA/exec"

def sincronizar_pendientes():
    """Busca ventas no sincronizadas en SQLite y las envía a Google Sheets."""
    ventas_pendientes = database.obtener_ventas_pendientes_sync()
    
    if not ventas_pendientes:
        return "Todo está al día. No hay ventas pendientes de subir."

    exitos = 0
    errores = 0

    for venta in ventas_pendientes:
        try:
            payload = {
                "accion": "guardar_venta",
                "datos": venta
            }
            
            respuesta = requests.post(URL_APPS_SCRIPT, json=payload, timeout=10)
            
            if respuesta.status_code == 200 and respuesta.json().get("estatus") == "exito":
                database.marcar_como_sincronizada(venta['id'])
                exitos += 1
            else:
                errores += 1
                
        except requests.exceptions.RequestException:
            errores += 1
    
    return f"Sincronización finalizada: {exitos} subidas con éxito, {errores} fallidas (quedan en espera)."

if __name__ == "__main__":
    resultado = sincronizar_pendientes()
    print(resultado)