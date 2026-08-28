import streamlit as st
import pandas as pd
import database
import sync

# Configuración inicial de la página
st.set_page_config(page_title="Seminuevaspy - Caja", page_icon="👗", layout="wide")

# Asegurarnos de que la base de datos existe al abrir la app
database.init_db()

st.title("👗 Sistema de Ventas - Seminuevaspy")
st.markdown("---")

# Dividimos la pantalla en dos columnas (Izquierda: Formulario | Derecha: Historial)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Registrar Nueva Venta")
    
    # Creamos el formulario de carga
    with st.form("formulario_ventas", clear_on_submit=True):
        descripcion_prenda = st.text_input("Descripción de la prenda *", placeholder="Ej: Vestido rojo fiesta")
        monto_gs = st.number_input("Monto en Guaraníes (Gs) *", min_value=0, step=5000)
        metodo_pago = st.selectbox("Método de Pago *", ["Efectivo", "Transferencia", "QR"])
        nombre_clienta = st.text_input("Nombre de la Clienta (Opcional)", placeholder="Dejar en blanco para 'Cliente casual'")
        vendedora = st.selectbox("Vendedora *", ["Romina", "Otra"])
        
        btn_guardar = st.form_submit_button("💰 Registrar Venta", use_container_width=True)
        
        if btn_guardar:
            if descripcion_prenda and monto_gs > 0:
                # Si el nombre está vacío, asigna "Cliente casual" por defecto
                cliente_final = nombre_clienta if nombre_clienta else "Cliente casual"
                
                # 1. Guardar en disco duro local (Súper rápido y seguro)
                database.agregar_venta(monto_gs, metodo_pago, descripcion_prenda, cliente_final, vendedora)
                st.success("✅ Venta guardada localmente.")
                
                # 2. Intentar subir a Google Sheets en segundo plano
                resultado_sync = sync.sincronizar_pendientes()
                st.info(resultado_sync)
                
                # Recargar la página para actualizar la tabla
                st.rerun()
            else:
                st.error("⚠️ La descripción y el monto son obligatorios.")

    st.markdown("---")
    st.subheader("🔄 Sincronización Manual")
    st.write("Usa este botón si se cortó el internet y querés forzar la subida de datos a la planilla.")
    if st.button("Subir datos pendientes a la nube", use_container_width=True):
        with st.spinner("Sincronizando con Google Sheets..."):
            resultado = sync.sincronizar_pendientes()
            st.success(resultado)
            st.rerun()

with col2:
    st.subheader("📊 Historial Reciente")
    
    # Traemos todas las ventas de la base de datos local
    ventas = database.obtener_todas_las_ventas()
    
    if ventas:
        # Convertimos los datos en una tabla de Pandas para que se vea lindo en Streamlit
        df = pd.DataFrame(ventas)
        
        # Le damos un formato más amigable a las columnas para leerlo mejor
        df_mostrar = df[['fecha_hora', 'descripcion_prenda', 'monto_gs', 'metodo_pago', 'estado', 'sync_status', 'id']]
        df_mostrar.columns = ['Fecha y Hora', 'Prenda', 'Monto (Gs)', 'Pago', 'Estado', 'Subido a Nube', 'ID Venta']
        
        # Cambiamos el 1 y 0 por emojis para que sea más visual
        df_mostrar['Subido a Nube'] = df_mostrar['Subido a Nube'].apply(lambda x: "✅ Sí" if x == 1 else "⏳ Pendiente")
        
        # Mostramos la tabla interactiva
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("❌ Anular una Venta")
        st.write("Si te equivocaste al cargar, copiá el 'ID Venta' de la tabla de arriba, pegalo acá y anulá el registro. (No se borra, cambia su estado a 'anulada').")
        
        col_anular1, col_anular2 = st.columns([3, 1])
        with col_anular1:
            id_a_anular = st.text_input("Pegar el ID Venta completo aquí", label_visibility="collapsed")
        with col_anular2:
            if st.button("Anular Venta", type="primary"):
                if id_a_anular:
                    database.anular_venta(id_a_anular)
                    sync.sincronizar_pendientes() # Avisa a Sheets que se anuló
                    st.success("Venta anulada correctamente.")
                    st.rerun()
                else:
                    st.warning("Ingresa un ID primero.")
    else:
        st.info("No hay ventas registradas todavía. ¡Cargá tu primera venta a la izquierda!")