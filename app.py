import streamlit as st
import database as db
import sync
import pandas as pd

st.set_page_config(
    page_title="Seminuevaspy · Caja",
    page_icon="👗",
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
        --bg: #15111C;
        --surface: #211A2B;
        --surface-2: #2A2136;
        --border: #362A44;
        --wine: #7A2E3D;
        --wine-light: #9C4257;
        --gold: #C9A227;
        --cream: #F3EAE0;
        --muted: #A99BB0;
        --sage: #7C9473;
        --rust: #B5533C;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: var(--cream);
    }

    .stApp {
        background: linear-gradient(180deg, #15111C 0%, #1A1522 100%);
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ---- Encabezado con sello ---- */
    .marca-header {
        display: flex;
        align-items: center;
        gap: 22px;
        padding: 28px 8px 20px 8px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 28px;
    }
    .sello {
        width: 64px;
        height: 64px;
        min-width: 64px;
        border-radius: 50%;
        border: 2px solid var(--gold);
        display: flex;
        align-items: center;
        justify-content: center;
        transform: rotate(-8deg);
        background: radial-gradient(circle at 35% 30%, #2A2136, #1A1522);
        box-shadow: 0 0 0 4px rgba(201, 162, 39, 0.08);
    }
    .sello span {
        font-family: 'Fraunces', serif;
        font-size: 22px;
        font-weight: 700;
        color: var(--gold);
    }
    .marca-titulo h1 {
        font-family: 'Fraunces', serif;
        font-size: 34px;
        font-weight: 600;
        margin: 0;
        color: var(--cream);
        letter-spacing: 0.3px;
    }
    .marca-titulo p {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
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
        background: var(--wine) !important;
        color: var(--cream) !important;
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
        color: var(--cream);
        margin-bottom: 4px;
    }
    .card-sub {
        font-size: 12.5px;
        color: var(--muted);
        margin-bottom: 18px;
    }

    /* ---- Métricas ---- */
    .metrica {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 3px solid var(--gold);
        border-radius: 12px;
        padding: 16px 18px;
    }
    .metrica .num {
        font-family: 'Fraunces', serif;
        font-size: 26px;
        font-weight: 600;
        color: var(--cream);
    }
    .metrica .label {
        font-size: 11.5px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: var(--muted);
    }

    /* ---- Inputs ---- */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--cream) !important;
    }
    label, .stMarkdown p { color: var(--muted) !important; }

    /* ---- Botones ---- */
    .stButton > button {
        background: var(--wine);
        color: var(--cream);
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 14.5px;
        transition: background 0.15s ease;
    }
    .stButton > button:hover {
        background: var(--wine-light);
        color: var(--cream);
    }
    .boton-sync button {
        background: var(--gold) !important;
        color: #1A1522 !important;
        width: 100%;
    }
    .boton-sync button:hover {
        background: #DDB84A !important;
    }
    .boton-peligro button {
        background: transparent !important;
        border: 1px solid var(--rust) !important;
        color: var(--rust) !important;
    }
    .boton-peligro button:hover {
        background: var(--rust) !important;
        color: var(--cream) !important;
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
# ENCABEZADO
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="marca-header">
        <div class="sello"><span>SP</span></div>
        <div class="marca-titulo">
            <h1>Seminuevaspy</h1>
            <p>Sistema de caja &amp; ventas</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["Nueva venta", "Historial", "Sincronización"])

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
            descripcion = st.text_input("Descripción de la prenda", placeholder="Ej: Campera de cuero negra")

            c1, c2 = st.columns(2)
            with c1:
                monto = st.number_input(
                    "Monto (₲)", min_value=0, step=10000, format="%d",
                    value=None, placeholder="Ej: 150000",
                )
            with c2:
                metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "QR"])

            c3, c4 = st.columns(2)
            with c3:
                clienta = st.text_input("Nombre de la clienta", placeholder="Opcional")
            with c4:
                vendedora = st.selectbox("Vendedora", ["Romina", "Otra"])

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
# TAB 3 · SINCRONIZACIÓN
# ---------------------------------------------------------------------------
with tab3:
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