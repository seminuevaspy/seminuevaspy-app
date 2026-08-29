import streamlit as st
import database as db
import sync
import pandas as pd

st.set_page_config(
    page_title="Seminuevaspy · Caja",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #FFFFFF;
        --surface: #F7F7F7;
        --surface-2: #FFFFFF;
        --border: #E3E3E3;
        --ink: #111111;
        --ink-soft: #2E2E2E;
        --muted: #767676;
        --sage: #4C7A5A;
        --rust: #B03A2E;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background: var(--bg);
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ---- Encabezado con sello ---- */
    .marca-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 28px 8px 20px 8px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 28px;
    }
    .sello {
        width: 60px;
        height: 60px;
        min-width: 60px;
        border-radius: 50%;
        border: 1.5px solid var(--ink);
        display: flex;
        align-items: center;
        justify-content: center;
        background: #0A0A0A;
    }
    .sello span {
        font-family: 'Fraunces', serif;
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
    }
    .marca-titulo h1 {
        font-family: 'Fraunces', serif;
        font-size: 32px;
        font-weight: 600;
        margin: 0;
        color: var(--ink);
        letter-spacing: 0.2px;
    }
    .marca-titulo p {
        font-family: 'Inter', sans-serif;
        font-size: 12.5px;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--muted);
        margin: 2px 0 0 0;
    }

    /* ---- Tabs como pills ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: var(--surface);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        color: var(--muted);
        font-weight: 600;
        font-size: 14px;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: var(--ink) !important;
        color: #FFFFFF !important;
    }

    /* ---- Tarjetas ---- */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
    }
    .card-title {
        font-family: 'Fraunces', serif;
        font-size: 19px;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 4px;
    }
    .card-sub {
        font-size: 12.5px;
        color: var(--muted);
        margin-bottom: 18px;
    }

    /* ---- Métricas ---- */
    .metrica {
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--ink);
        border-radius: 12px;
        padding: 16px 18px;
    }
    .metrica .num {
        font-family: 'Fraunces', serif;
        font-size: 24px;
        font-weight: 600;
        color: var(--ink);
    }
    .metrica .label {
        font-size: 11.5px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: var(--muted);
    }

    /* ---- Desglose de costos ---- */
    .linea-costo {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px dashed var(--border);
        font-size: 14px;
        color: var(--ink-soft);
    }
    .linea-costo.total {
        border-bottom: none;
        border-top: 1.5px solid var(--ink);
        margin-top: 4px;
        padding-top: 12px;
        font-weight: 700;
        color: var(--ink);
    }
    .linea-costo span.valor { font-weight: 600; }

    /* ---- Inputs ---- */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--ink) !important;
    }
    label, .stMarkdown p { color: var(--ink-soft) !important; }

    /* ---- Botones ---- */
    .stButton > button {
        background: var(--ink);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 14.5px;
        transition: background 0.15s ease;
    }
    .stButton > button:hover {
        background: var(--ink-soft);
        color: #FFFFFF;
    }
    .boton-sync button {
        background: var(--ink) !important;
        color: #FFFFFF !important;
        width: 100%;
    }
    .boton-sync button:hover {
        background: var(--ink-soft) !important;
    }
    .boton-peligro button {
        background: transparent !important;
        border: 1px solid var(--rust) !important;
        color: var(--rust) !important;
    }
    .boton-peligro button:hover {
        background: var(--rust) !important;
        color: #FFFFFF !important;
    }

    /* ---- Dataframe ---- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    hr { border-color: var(--border); }
    </style>
    """,
    unsafe_allow_html=True,
)

db.init_db()

# ---------------------------------------------------------------------------
# CONSTANTES DE NEGOCIO
# ---------------------------------------------------------------------------
VENDEDORAS = ["Romina", "Pamela", "Mama"]

COMISION_ROMINA = 0.07
COMISION_PAMELA = 0.07
COMISION_DAMIAN = 0.03
PORCENTAJE_BRUTO_DUENA = 0.60  # parte de las ventas totales que corresponde a la dueña antes de restar sueldos y costos fijos

COSTOS_FIJOS = {
    "Alquiler de la tienda": 2_300_000,
    "Internet": 100_000,
    "Agua y camión de basura": 110_000,
    "Luz": 150_000,
}

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


def etiqueta_mes(periodo: str) -> str:
    anio, mes = periodo.split("-")
    return f"{MESES_ES[int(mes)]} {anio}"


# ---------------------------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="marca-header">
        <div class="sello"><span>SN</span></div>
        <div class="marca-titulo">
            <h1>Seminuevaspy</h1>
            <p>Sistema de caja &amp; ventas</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(["Nueva venta", "Historial", "Resumen financiero", "Sincronización"])

# ---------------------------------------------------------------------------
# TAB 1 · NUEVA VENTA
# ---------------------------------------------------------------------------
with tab1:
    col_form, col_ayuda = st.columns([2, 1])

    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Registrar venta</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Completá los datos y guardá — se sincroniza sola con Sheets.</div>', unsafe_allow_html=True)

        with st.form("form_nueva_venta", clear_on_submit=True):
            monto = st.number_input(
                "Precio de la prenda (₲)", min_value=0, step=10000, format="%d",
                value=None, placeholder="Ej: 150000",
            )
            descripcion = st.text_input("Descripción de la prenda", placeholder="Ej: Campera de cuero negra")

            c1, c2 = st.columns(2)
            with c1:
                metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "QR"])
            with c2:
                vendedora = st.selectbox("Vendedora", VENDEDORAS)

            clienta = st.text_input("Nombre de la clienta", placeholder="Opcional")

            enviar = st.form_submit_button("Guardar venta", use_container_width=True)

            if enviar:
                if monto is not None and monto > 0:
                    nombre_final = clienta.strip() if clienta and clienta.strip() else "Cliente casual"
                    db.agregar_venta(
                        monto_gs=monto,
                        metodo_pago=metodo,
                        descripcion_prenda=descripcion,
                        nombre_clienta=nombre_final,
                        vendedora=vendedora,
                    )
                    mensaje_sync = sync.sincronizar_pendientes()
                    st.success(f"Venta de ₲ {monto:,.0f} guardada.")
                    st.caption(mensaje_sync)
                else:
                    st.warning("Ingresá un monto válido antes de guardar.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_ayuda:
        df_resumen = pd.DataFrame(db.obtener_todas_las_ventas())
        total_ventas = len(df_resumen) if not df_resumen.empty else 0
        pendientes = int((df_resumen["sync_status"] == 0).sum()) if not df_resumen.empty else 0
        anuladas = int((df_resumen["estado"] == "anulada").sum()) if not df_resumen.empty else 0

        st.markdown(
            f"""
            <div class="metrica" style="margin-bottom:14px;">
                <div class="num">{total_ventas}</div>
                <div class="label">Ventas totales</div>
            </div>
            <div class="metrica" style="margin-bottom:14px; border-left-color: var(--rust);">
                <div class="num">{pendientes}</div>
                <div class="label">Pendientes de subir</div>
            </div>
            <div class="metrica" style="border-left-color: var(--sage);">
                <div class="num">{anuladas}</div>
                <div class="label">Anuladas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# TAB 2 · HISTORIAL
# ---------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Historial de ventas</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Estado y sincronización de cada movimiento.</div>', unsafe_allow_html=True)

    df_hist = pd.DataFrame(db.obtener_todas_las_ventas())

    if not df_hist.empty:
        df_vista = df_hist.copy()
        df_vista["Estado"] = df_vista["estado"].map(
            {"activa": "🟢 Activa", "anulada": "🔴 Anulada"}
        ).fillna(df_vista["estado"])
        df_vista["Nube"] = df_vista["sync_status"].map(
            {1: "☁️ Sincronizada", 0: "⏳ Pendiente"}
        ).fillna("⏳ Pendiente")
        df_vista["Monto (₲)"] = df_vista["monto_gs"].map(lambda x: f"₲ {x:,.0f}")

        columnas = {
            "id": "ID",
            "fecha_hora": "Fecha",
            "descripcion_prenda": "Prenda",
            "Monto (₲)": "Monto (₲)",
            "metodo_pago": "Método",
            "nombre_clienta": "Clienta",
            "vendedora": "Vendedora",
            "Estado": "Estado",
            "Nube": "Nube",
        }
        df_final = df_vista.rename(columns=columnas)[list(columnas.values())]

        st.dataframe(df_final, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="font-size:16px;">Anular una venta</div>', unsafe_allow_html=True)

        col_id, col_btn = st.columns([3, 1])
        with col_id:
            id_anular = st.text_input("ID de la venta (UUID)", placeholder="Pegá el ID acá", label_visibility="collapsed")
        with col_btn:
            st.markdown('<div class="boton-peligro">', unsafe_allow_html=True)
            if st.button("Anular venta", use_container_width=True):
                if id_anular.strip():
                    id_limpio = id_anular.strip()
                    existe = (df_hist["id"] == id_limpio).any()
                    if existe:
                        db.anular_venta(id_limpio)
                        st.success("Venta anulada.")
                        st.rerun()
                    else:
                        st.error("No se encontró esa venta.")
                else:
                    st.warning("Pegá un ID válido.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Todavía no hay ventas registradas.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 3 · RESUMEN FINANCIERO
# ---------------------------------------------------------------------------
with tab3:
    df_fin = pd.DataFrame(db.obtener_todas_las_ventas())

    if df_fin.empty:
        st.info("Todavía no hay ventas registradas para calcular un resumen.")
    else:
        df_fin["fecha_dt"] = pd.to_datetime(df_fin["fecha_hora"], errors="coerce")
        df_fin["periodo"] = df_fin["fecha_dt"].dt.to_period("M").astype(str)

        # Solo ventas activas cuentan para la facturación real
        df_activas = df_fin[df_fin["estado"] == "activa"]

        periodos_disponibles = sorted(df_fin["periodo"].dropna().unique(), reverse=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Resumen financiero</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Elegí el mes para ver la facturación, los sueldos y la ganancia neta de mamá.</div>', unsafe_allow_html=True)

        opciones_labels = [etiqueta_mes(p) for p in periodos_disponibles]
        seleccion_label = st.selectbox("Mes", opciones_labels)
        periodo_seleccionado = periodos_disponibles[opciones_labels.index(seleccion_label)]

        df_mes = df_activas[df_activas["periodo"] == periodo_seleccionado]
        total_mes = float(df_mes["monto_gs"].sum())

        comision_romina = total_mes * COMISION_ROMINA
        comision_pamela = total_mes * COMISION_PAMELA
        comision_damian = total_mes * COMISION_DAMIAN
        total_sueldos = comision_romina + comision_pamela + comision_damian

        bruto_duena = total_mes * PORCENTAJE_BRUTO_DUENA
        total_costos_fijos = sum(COSTOS_FIJOS.values())
        ganancia_neta_duena = bruto_duena - total_sueldos - total_costos_fijos

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.markdown(
            f"""<div class="metrica"><div class="num">₲ {total_mes:,.0f}</div>
            <div class="label">Venta bruta del mes ({len(df_mes)} ventas)</div></div>""",
            unsafe_allow_html=True,
        )
        c2.markdown(
            f"""<div class="metrica"><div class="num">₲ {total_sueldos:,.0f}</div>
            <div class="label">Total sueldos (17%)</div></div>""",
            unsafe_allow_html=True,
        )
        c3.markdown(
            f"""<div class="metrica" style="border-left-color: var(--sage);"><div class="num">₲ {ganancia_neta_duena:,.0f}</div>
            <div class="label">Ganancia neta de mamá</div></div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col_sueldos, col_duena = st.columns(2)

        with col_sueldos:
            st.markdown('<div class="card-title" style="font-size:16px;">Sueldos del mes</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="linea-costo"><span>Romina (7%)</span><span class="valor">₲ {comision_romina:,.0f}</span></div>
                <div class="linea-costo"><span>Pamela (7%)</span><span class="valor">₲ {comision_pamela:,.0f}</span></div>
                <div class="linea-costo"><span>Damián (3%)</span><span class="valor">₲ {comision_damian:,.0f}</span></div>
                <div class="linea-costo total"><span>Total sueldos</span><span class="valor">₲ {total_sueldos:,.0f}</span></div>
                """,
                unsafe_allow_html=True,
            )

        with col_duena:
            st.markdown('<div class="card-title" style="font-size:16px;">Ganancia neta de mamá</div>', unsafe_allow_html=True)
            filas_costos = "".join(
                f'<div class="linea-costo"><span>{nombre}</span><span class="valor">− ₲ {valor:,.0f}</span></div>'
                for nombre, valor in COSTOS_FIJOS.items()
            )
            st.markdown(
                f"""
                <div class="linea-costo"><span>60% de venta bruta</span><span class="valor">₲ {bruto_duena:,.0f}</span></div>
                <div class="linea-costo"><span>Sueldos (17% de venta bruta)</span><span class="valor">− ₲ {total_sueldos:,.0f}</span></div>
                {filas_costos}
                <div class="linea-costo total"><span>Ganancia neta</span><span class="valor">₲ {ganancia_neta_duena:,.0f}</span></div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="font-size:16px;">Todos los meses</div>', unsafe_allow_html=True)

        resumen_todos = (
            df_activas.groupby("periodo")["monto_gs"]
            .sum()
            .reindex(periodos_disponibles)
            .fillna(0)
        )
        df_todos = pd.DataFrame({
            "Mes": [etiqueta_mes(p) for p in resumen_todos.index],
            "Venta bruta (₲)": [f"₲ {v:,.0f}" for v in resumen_todos.values],
            "Ganancia neta de mamá (₲)": [
                f"₲ {(v * PORCENTAJE_BRUTO_DUENA - v * (COMISION_ROMINA + COMISION_PAMELA + COMISION_DAMIAN) - total_costos_fijos):,.0f}"
                for v in resumen_todos.values
            ],
        })
        st.dataframe(df_todos, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 4 · SINCRONIZACIÓN
# ---------------------------------------------------------------------------
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Sincronización manual</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-sub">Si se cortó internet, las ventas quedan pendientes localmente. '
        'Usá este botón cuando vuelva la conexión para subir todo lo pendiente a Sheets.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="boton-sync">', unsafe_allow_html=True)
    if st.button("🔄 Sincronizar ahora", use_container_width=True):
        with st.spinner("Subiendo ventas pendientes a Google Sheets..."):
            mensaje_sync = sync.sincronizar_pendientes()
        st.success(mensaje_sync)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)