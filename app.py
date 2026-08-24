import streamlit as st
import database as db

st.set_page_config(page_title="Seminuevaspy - Sistema", page_icon="👗", layout="wide")

st.markdown("<h1 style='text-align: center;'>👗 Sistema Seminuevaspy</h1>", unsafe_allow_html=True)
st.markdown("---")

db.inicializar_db()

tab1, tab2, tab3 = st.tabs(["📝 Registrar Venta", "📊 Tablero Financiero", "⚙️ Administrar"])

# --- PESTAÑA 1: FORMULARIO ---
with tab1:
    st.subheader("Nueva Venta")
    with st.form("formulario_ventas", clear_on_submit=True):
        # value=None hace que el campo empiece vacío
        monto = st.number_input("Monto de la venta (₲)", min_value=0, step=10000, format="%d", value=None, placeholder="Ej: 150000")
        
        col1, col2 = st.columns(2)
        with col1:
            metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "QR"])
        with col2:
            vendedora = st.selectbox("Vendedora", ["Romina", "Pamela"]) 
            
        descripcion = st.text_input("Descripción de la prenda (Opcional)", placeholder="Ej: Blusa negra Zara")
        clienta = st.text_input("Nombre de la clienta (Opcional)")
        
        submit = st.form_submit_button("Guardar Venta", use_container_width=True)
        
        if submit:
            if monto is not None and monto > 0:
                exito = db.registrar_venta(monto, metodo, clienta, vendedora, descripcion)
                if exito:
                    st.success(f"✅ Venta de ₲ {monto:,} guardada correctamente.")
                else:
                    st.error("❌ Hubo un error al guardar la venta.")
            else:
                st.warning("⚠️ Por favor, ingresa un monto válido.")

# --- PESTAÑA 2: TABLERO ULTRA PRO ---
with tab2:
    st.subheader("Resumen del Mes")
    df_ventas = db.obtener_datos_ventas()

    if not df_ventas.empty:
        total_bruto = df_ventas['monto_gs'].sum()
        costo_ropa = total_bruto * 0.50 
        comision_romina = total_bruto * 0.07
        comision_pamela = total_bruto * 0.07
        comision_damian = total_bruto * 0.03
        ganancia_duena = costo_ropa - comision_romina - comision_pamela - comision_damian 

        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Venta Bruta (100%)", f"₲ {total_bruto:,.0f}")
        c2.warning(f"📦 Capital Reposición Ropa (50%)\n\n₲ {costo_ropa:,.0f}")
        c3.success(f"👑 Ganancia Neta Dueña (33%)\n\n₲ {ganancia_duena:,.0f}")
        
        st.markdown("---")
        st.markdown("### 🤝 Reparto de Comisiones (17%)")
        
        c4, c5, c6 = st.columns(3)
        c4.markdown(f"""<div style="background-color: rgba(155, 89, 182, 0.15); border: 1px solid rgba(155, 89, 182, 0.5); padding: 15px; border-radius: 8px;"><p style="margin:0px; font-size: 14px; font-weight: 500;">Comisión Romina (7%)</p><h3 style="margin:0px; margin-top:10px; color: #D7BDE2;">₲ {comision_romina:,.0f}</h3></div>""", unsafe_allow_html=True)
        c5.markdown(f"""<div style="background-color: rgba(232, 67, 147, 0.15); border: 1px solid rgba(232, 67, 147, 0.5); padding: 15px; border-radius: 8px;"><p style="margin:0px; font-size: 14px; font-weight: 500;">Comisión Pamela (7%)</p><h3 style="margin:0px; margin-top:10px; color: #FF9EE2;">₲ {comision_pamela:,.0f}</h3></div>""", unsafe_allow_html=True)
        c6.markdown(f"""<div style="background-color: rgba(52, 152, 219, 0.15); border: 1px solid rgba(52, 152, 219, 0.5); padding: 15px; border-radius: 8px;"><p style="margin:0px; font-size: 14px; font-weight: 500;">Comisión Damián (3%)</p><h3 style="margin:0px; margin-top:10px; color: #AED6F1;">₲ {comision_damian:,.0f}</h3></div>""", unsafe_allow_html=True)

    else:
        st.info("Aún no hay ventas registradas.")

# --- PESTAÑA 3: ADMINISTRACIÓN ---
with tab3:
    st.subheader("Historial y Correcciones")
    df_ventas_admin = db.obtener_datos_ventas()
    
    if not df_ventas_admin.empty:
        # Reordenamos las columnas para que la descripción se vea bien
        columnas_ordenadas = ['id', 'fecha_hora', 'monto_gs', 'metodo_pago', 'descripcion_prenda', 'nombre_clienta', 'vendedora']
        df_mostrar = df_ventas_admin[columnas_ordenadas]
        
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        
        st.markdown("### 🗑️ Borrar una venta incorrecta")
        col_del1, col_del2 = st.columns([2, 1])
        with col_del1:
            id_a_borrar = st.number_input("ID de la venta a eliminar:", min_value=1, step=1, format="%d")
        with col_del2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Eliminar Registro", type="primary"):
                if db.eliminar_venta(id_a_borrar):
                    st.success(f"Venta eliminada. Recarga la página.")
                else:
                    st.error("No se pudo eliminar.")
    else:
        st.info("La base de datos está vacía.")