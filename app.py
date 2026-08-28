import streamlit as st
import pandas as pd
from datetime import datetime

import database
import sync


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Seminuevaspy · POS",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ESTILOS — UI PREMIUM
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f6f7f9;
        color: #171717;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- OCULTAR ELEMENTOS STREAMLIT ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- HEADER ---------- */

    .brand-wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    .brand-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: #171717;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        box-shadow: 0 8px 20px rgba(0,0,0,.10);
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #111111;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #858585;
        margin-top: 4px;
        font-weight: 500;
    }

    .online-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 8px 13px;
        border-radius: 999px;
        background: #ecfdf3;
        color: #087443;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #c9f2db;
    }

    .online-dot {
        width: 7px;
        height: 7px;
        background: #16a34a;
        border-radius: 50%;
    }

    /* ---------- CARDS ---------- */

    .section-card {
        background: white;
        border: 1px solid #e9eaec;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 5px 22px rgba(20,20,20,.035);
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 17px;
        font-weight: 750;
        color: #171717;
        margin-bottom: 4px;
        letter-spacing: -.25px;
    }

    .section-description {
        font-size: 12px;
        color: #8a8d91;
        margin-bottom: 20px;
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 11px !important;
        border: 1px solid #dedfe2 !important;
        background: #ffffff !important;
        min-height: 44px;
        transition: all .15s ease;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #171717 !important;
        box-shadow: 0 0 0 2px rgba(23,23,23,.06) !important;
    }

    label {
        font-size: 12px !important;
        font-weight: 650 !important;
        color: #454545 !important;
        margin-bottom: 5px !important;
    }

    /* ---------- BOTONES ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 11px;
        min-height: 44px;
        border: 1px solid #dedfe2;
        background: white;
        color: #171717;
        font-weight: 700;
        font-size: 13px;
        transition: all .15s ease;
    }

    .stButton > button:hover {
        border-color: #171717;
        background: #fafafa;
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(0,0,0,.07);
    }

    .stButton > button[kind="primary"] {
        background: #171717 !important;
        color: white !important;
        border-color: #171717 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #303030 !important;
        border-color: #303030 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,.15);
    }

    /* ---------- MÉTRICAS ---------- */

    .metric-card {
        background: white;
        border: 1px solid #e9eaec;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 18px rgba(20,20,20,.025);
    }

    .metric-label {
        color: #85878b;
        font-size: 11px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .5px;
    }

    .metric-value {
        color: #171717;
        font-size: 24px;
        font-weight: 800;
        margin-top: 5px;
        letter-spacing: -.7px;
    }

    /* ---------- TABLA ---------- */

    .history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .history-count {
        background: #f1f2f4;
        color: #676a6e;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #e7e8ea;
        border-radius: 13px;
        overflow: hidden;
    }

    /* ---------- BADGES ---------- */

    .status-active {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        background: #ecfdf3;
        color: #087443;
        font-size: 11px;
        font-weight: 700;
    }

    .status-cancelled {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        background: #fff1f2;
        color: #be123c;
        font-size: 11px;
        font-weight: 700;
    }

    .sync-ok {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        background: #eff6ff;
        color: #1d4ed8;
        font-size: 11px;
        font-weight: 700;
    }

    .sync-pending {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        background: #fff7ed;
        color: #c2410c;
        font-size: 11px;
        font-weight: 700;
    }

    /* ---------- EMERGENCY SYNC ---------- */

    .sync-banner {
        background: #171717;
        border-radius: 17px;
        padding: 19px 22px;
        color: white;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    .sync-banner-title {
        font-weight: 750;
        font-size: 14px;
    }

    .sync-banner-text {
        color: #bcbcbc;
        font-size: 11px;
        margin-top: 3px;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border: none !important;
        border-top: 1px solid #ededed !important;
        margin: 26px 0 !important;
    }

    /* ---------- ALERTAS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #e6e7e9;
    }

    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .brand-name {
            font-size: 21px;
        }

        .metric-value {
            font-size: 20px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_gs(valor):
    try:
        return f"Gs. {int(valor):,}".replace(",", ".")
    except Exception:
        return "Gs. 0"


def cargar_ventas():
    try:
        ventas = database.obtener_todas_las_ventas()

        if not ventas:
            return pd.DataFrame()

        # Compatible con listas de diccionarios
        if isinstance(ventas, list) and isinstance(ventas[0], dict):
            return pd.DataFrame(ventas)

        # Compatible con listas de tuplas
        columnas = [
            "monto_gs",
            "metodo_pago",
            "descripcion_prenda",
            "nombre_clienta",
            "vendedora",
            "id",
            "fecha_hora",
            "estado",
            "sync_status",
        ]

        try:
            return pd.DataFrame(ventas, columns=columnas)
        except Exception:
            return pd.DataFrame(ventas)

    except Exception as e:
        st.error(f"No se pudo cargar el historial: {e}")
        return pd.DataFrame()


def normalizar_columnas(df):
    if df.empty:
        return df

    df = df.copy()

    # En caso de que la base devuelva nombres ligeramente distintos
    aliases = {
        "monto": "monto_gs",
        "monto": "monto_gs",
        "descripcion": "descripcion_prenda",
        "cliente": "nombre_clienta",
        "vendedora": "vendedora",
        "fecha": "fecha_hora",
        "estado": "estado",
        "sync": "sync_status",
    }

    for origen, destino in aliases.items():
        if origen in df.columns and destino not in df.columns:
            df.rename(columns={origen: destino}, inplace=True)

    return df


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-wrapper">
        <div class="brand-left">
            <div class="brand-icon">🛍️</div>
            <div>
                <div class="brand-name">seminuevaspy</div>
                <div class="brand-subtitle">Sistema de ventas · Punto de venta</div>
            </div>
        </div>

        <div class="online-badge">
            <span class="online-dot"></span>
            Sistema operativo
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CARGAR DATOS
# ============================================================

df = normalizar_columnas(cargar_ventas())


# ============================================================
# MÉTRICAS
# ============================================================

ventas_activas = pd.DataFrame()

if not df.empty:
    if "estado" in df.columns:
        ventas_activas = df[df["estado"].astype(str).str.lower() == "activa"].copy()
    else:
        ventas_activas = df.copy()

total_facturado = 0

if not ventas_activas.empty and "monto_gs" in ventas_activas.columns:
    total_facturado = pd.to_numeric(
        ventas_activas["monto_gs"],
        errors="coerce"
    ).fillna(0).sum()

cantidad_ventas = len(ventas_activas)

ticket_promedio = (
    total_facturado / cantidad_ventas
    if cantidad_ventas > 0
    else 0
)

pendientes = 0

if not df.empty and "sync_status" in df.columns:
    pendientes = (
        pd.to_numeric(df["sync_status"], errors="coerce")
        .fillna(0)
        .eq(0)
        .sum()
    )


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Facturación activa</div>
            <div class="metric-value">{formatear_gs(total_facturado)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Ventas</div>
            <div class="metric-value">{cantidad_ventas}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Ticket promedio</div>
            <div class="metric-value">{formatear_gs(ticket_promedio)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Pendientes de nube</div>
            <div class="metric-value">{pendientes}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# NUEVA VENTA
# ============================================================

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Nueva venta</div>
        <div class="section-description">
            Registrá una nueva operación. Los datos se guardarán localmente
            y luego se sincronizarán con la nube.
        </div>
    """,
    unsafe_allow_html=True,
)

with st.form("form_nueva_venta", clear_on_submit=True):

    col1, col2 = st.columns([1.6, 1])

    with col1:
        descripcion = st.text_input(
            "Descripción de la prenda",
            placeholder="Ej.: Vestido negro Zara",
        )

    with col2:
        monto = st.number_input(
            "Monto en Gs.",
            min_value=0,
            step=1000,
            format="%d",
        )

    col3, col4, col5 = st.columns([1, 1, 1])

    with col3:
        metodo_pago = st.selectbox(
            "Método de pago",
            ["Efectivo", "Transferencia", "QR"],
        )

    with col4:
        nombre_clienta = st.text_input(
            "Nombre de clienta",
            placeholder="Opcional",
        )

    with col5:
        vendedora = st.selectbox(
            "Vendedora",
            ["Romina", "Otra"],
        )

    st.markdown("<br>", unsafe_allow_html=True)

    guardar = st.form_submit_button(
        "✓  Registrar venta",
        type="primary",
        use_container_width=True,
    )

    if guardar:

        if not descripcion.strip():
            st.error("Ingresá la descripción de la prenda.")
        elif monto <= 0:
            st.error("El monto debe ser mayor a 0.")
        else:

            clienta_final = nombre_clienta.strip() or "Cliente casual"

            try:
                # Mantener intacta la lógica del backend.
                database.agregar_venta(
                    monto_gs=int(monto),
                    metodo_pago=metodo_pago,
                    descripcion_prenda=descripcion.strip(),
                    nombre_clienta=clienta_final,
                    vendedora=vendedora,
                )

                try:
                    sync.sincronizar_pendientes()
                except Exception:
                    # La venta ya quedó guardada localmente.
                    # Si no hay internet, seguirá pendiente.
                    pass

                st.success(
                    "Venta registrada correctamente."
                )

                st.rerun()

            except TypeError:
                # Compatibilidad con funciones que reciben argumentos
                # posicionales en lugar de argumentos nombrados.
                try:
                    database.agregar_venta(
                        int(monto),
                        metodo_pago,
                        descripcion.strip(),
                        clienta_final,
                        vendedora,
                    )

                    try:
                        sync.sincronizar_pendientes()
                    except Exception:
                        pass

                    st.success("Venta registrada correctamente.")
                    st.rerun()

                except Exception as e:
                    st.error(f"No se pudo registrar la venta: {e}")

            except Exception as e:
                st.error(f"No se pudo registrar la venta: {e}")


st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SINCRONIZACIÓN
# ============================================================

st.markdown(
    """
    <div class="sync-banner">
        <div class="sync-banner-title">☁️ Sincronización con la nube</div>
        <div class="sync-banner-text">
            Si hubo un corte de internet, podés intentar subir nuevamente
            todas las ventas pendientes.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

sync_col1, sync_col2 = st.columns([3, 1])

with sync_col1:
    st.caption(
        f"{pendientes} venta(s) pendiente(s) de sincronización."
        if pendientes != 1
        else "1 venta pendiente de sincronización."
    )

with sync_col2:
    if st.button(
        "☁️ Sincronizar ahora",
        type="primary",
        use_container_width=True,
    ):
        try:
            sync.sincronizar_pendientes()
            st.success("Sincronización ejecutada correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"No se pudo sincronizar: {e}")


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# HISTORIAL
# ============================================================

st.markdown(
    """
    <div class="section-card">
        <div class="history-header">
            <div>
                <div class="section-title">Historial de ventas</div>
                <div class="section-description" style="margin-bottom:0;">
                    Todas las operaciones registradas en el sistema.
                </div>
            </div>
        """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="history-count">{len(df)} registros</div></div>',
    unsafe_allow_html=True,
)

if df.empty:

    st.info("Todavía no hay ventas registradas.")

else:

    tabla = df.copy()

    # Ordenar por fecha si existe
    if "fecha_hora" in tabla.columns:
        try:
            tabla["_fecha_sort"] = pd.to_datetime(
                tabla["fecha_hora"],
                errors="coerce"
            )
            tabla = tabla.sort_values(
                "_fecha_sort",
                ascending=False
            )
            tabla.drop(columns=["_fecha_sort"], inplace=True)
        except Exception:
            pass

    # Estado amigable
    if "estado" in tabla.columns:
        tabla["estado"] = tabla["estado"].apply(
            lambda x:
            "🟢 Activa"
            if str(x).lower() == "activa"
            else "🔴 Anulada"
        )

    # Sincronización amigable
    if "sync_status" in tabla.columns:
        tabla["sync_status"] = tabla["sync_status"].apply(
            lambda x:
            "☁️ Sí"
            if str(x) == "1"
            else "⏳ Pendiente"
        )

    # Formato de monto
    if "monto_gs" in tabla.columns:
        tabla["monto_gs"] = pd.to_numeric(
            tabla["monto_gs"],
            errors="coerce"
        ).fillna(0).apply(formatear_gs)

    # Renombrar para mostrar nombres amigables
    nombres_columnas = {
        "fecha_hora": "Fecha y hora",
        "descripcion_prenda": "Prenda",
        "monto_gs": "Monto",
        "metodo_pago": "Método",
        "nombre_clienta": "Clienta",
        "vendedora": "Vendedora",
        "estado": "Estado",
        "sync_status": "Nube",
        "id": "ID",
    }

    tabla.rename(
        columns={
            k: v
            for k, v in nombres_columnas.items()
            if k in tabla.columns
        },
        inplace=True,
    )

    # Orden visual
    orden = [
        "Fecha y hora",
        "Prenda",
        "Monto",
        "Método",
        "Clienta",
        "Vendedora",
        "Estado",
        "Nube",
        "ID",
    ]

    columnas_finales = [
        c for c in orden
        if c in tabla.columns
    ]

    tabla = tabla[columnas_finales]

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
        height=430,
    )


st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ANULACIÓN
# ============================================================

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Anular una venta</div>
        <div class="section-description">
            Utilizá el ID de la venta para anularla. La operación no se
            elimina del historial.
        </div>
    """,
    unsafe_allow_html=True,
)

col_id, col_button = st.columns([3, 1])

with col_id:
    id_venta = st.text_input(
        "ID de venta",
        placeholder="Pegá aquí el UUID de la venta",
        label_visibility="collapsed",
    )

with col_button:
    anular = st.button(
        "Anular venta",
        use_container_width=True,
    )

if anular:

    id_limpio = id_venta.strip()

    if not id_limpio:
        st.warning("Ingresá el ID de la venta.")
    else:
        try:
            resultado = database.anular_venta(id_limpio)

            if resultado is False:
                st.warning(
                    "No se encontró la venta o no pudo ser anulada."
                )
            else:
                st.success("Venta anulada correctamente.")
                st.rerun()

        except Exception as e:
            st.error(f"No se pudo anular la venta: {e}")


st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#a0a2a5;
        font-size:11px;
        padding-top:18px;
    ">
        seminuevaspy · Sistema POS
    </div>
    """,
    unsafe_allow_html=True,
)