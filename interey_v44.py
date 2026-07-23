import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="INTEREY | Dashboard Corporativo", layout="wide")

# ---------- ESTILO ----------
st.markdown("""
<style>
:root{
    --interey-blue:#123E70;
    --interey-blue-2:#0B1F4D;
    --interey-red:#D52B24;
    --interey-graphite:#344648;
    --interey-bg:#F5F7FB;
    --interey-card:#FFFFFF;
    --interey-green:#118C7E;
    --interey-yellow:#D97706;
    --interey-gray:#64748B;
}
.stApp {background: linear-gradient(180deg, #F7F9FC 0%, #FFFFFF 42%);}
.block-container {padding-top: 1.0rem; padding-bottom: 2rem; max-width: 1520px;}
[data-testid="stSidebar"] {background: #EEF3F8;}

/* Header INTEREY */
.hero-wrap{
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 6px 0 14px 0;
    box-shadow: none;
    margin-top: 0;
    margin-bottom: 10px;
}
.hero-title{font-size:2.25rem; font-weight:900; color:var(--interey-blue-2); letter-spacing:-.045em; line-height:1.02;}
.hero-kicker{font-size:.82rem; font-weight:800; color:var(--interey-red); letter-spacing:.13em; text-transform:uppercase; margin-bottom:4px;}
.hero-subtitle{font-size:1.04rem; color:var(--interey-graphite); margin-top:4px;}
.hero-pill{background:#FFFFFF; border:1px solid rgba(18,62,112,.16); border-radius:999px; padding:8px 12px; color:#334155; font-size:.82rem; display:inline-block; margin-top:8px;}
.hero-date{text-align:right; color:#475569; font-size:.83rem; padding-top:6px;}
.logo-box-premium img{max-height:74px; object-fit:contain;}

/* Cards */
.kpi-card {
    background: linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color: white;
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 8px 22px rgba(11,31,77,.14);
    height: 136px;
    min-height: 136px;
    max-height: 136px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,.18);
}
.kpi-card.green {background: linear-gradient(135deg, #0F766E 0%, var(--interey-green) 100%);}
.kpi-card.gray {background: linear-gradient(135deg, #334155 0%, #64748B 100%);}
.kpi-card.red {background: linear-gradient(135deg, #991B1B 0%, var(--interey-red) 100%);}
.kpi-card.yellow {background: linear-gradient(135deg, #92400E 0%, var(--interey-yellow) 100%);}
.kpi-card.orange {background: linear-gradient(135deg, #C2410C 0%, #EA580C 100%);}
.kpi-card.orange {background: linear-gradient(135deg, #9A3412 0%, #EA580C 100%);}
.kpi-label {font-size: .82rem; opacity: .94; line-height: 1.15; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight:700;}
.kpi-value {font-size: 1.62rem; font-weight: 900; margin-top: .10rem; line-height: 1.12; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing:-.02em;}
.kpi-sub {font-size: .72rem; opacity: .88; margin-top: .10rem; line-height: 1.22; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;}
.kpi-spacer{height:14px;}

.section-title {font-size: 1.18rem; font-weight: 850; color: var(--interey-blue-2); margin-top: 1.0rem; margin-bottom: .62rem; letter-spacing:-.01em;}
.small-note {font-size: .82rem; color: #6B7280;}
.exec-band {background: #FFFFFF; border: 1px solid rgba(18,62,112,.12); border-radius: 16px; padding: 10px 14px; margin-bottom: .9rem; box-shadow:0 4px 12px rgba(15,23,42,.04);}
.trend-note {font-size: .82rem; color: #475569; margin-top: .55rem; background: #F8FAFC; border-left: 4px solid var(--interey-blue); padding: 9px 11px; border-radius: 10px;}

/* Radar INTEREY 2.0 */
.radar-card{
    background:linear-gradient(135deg,#071A33 0%, #123E70 55%, #1D5C92 100%);
    border:1px solid rgba(255,255,255,.18);
    border-radius:24px;
    padding:20px 22px;
    margin:12px 0 18px 0;
    box-shadow:0 16px 36px rgba(11,31,77,.18);
    color:#FFFFFF;
    overflow:hidden;
    position:relative;
}
.radar-card:before{content:""; position:absolute; right:-70px; top:-90px; width:260px; height:260px; border-radius:50%; background:rgba(255,255,255,.08);}
.radar-card:after{content:""; position:absolute; right:34px; bottom:-78px; width:180px; height:180px; border-radius:50%; background:rgba(213,43,36,.13);}
.radar-head{display:flex; justify-content:space-between; gap:18px; align-items:flex-start; position:relative; z-index:2; margin-bottom:15px;}
.radar-title{font-size:1.32rem; font-weight:950; letter-spacing:-.02em; margin-bottom:3px; color:#FFFFFF;}
.radar-subtitle{font-size:.86rem; color:rgba(255,255,255,.78); line-height:1.32;}
.radar-badge{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.24); border-radius:999px; padding:8px 12px; font-size:.78rem; font-weight:850; color:#FFFFFF; white-space:nowrap;}
.radar2-grid{display:grid; grid-template-columns:1.25fr repeat(3, minmax(0, .9fr)); gap:12px; position:relative; z-index:2;}
.radar2-main{background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); border-radius:18px; padding:15px 16px; min-height:142px;}
.radar2-main-label{font-size:.76rem; font-weight:850; text-transform:uppercase; letter-spacing:.08em; color:rgba(255,255,255,.72);}
.radar2-main-value{font-size:1.45rem; line-height:1.12; font-weight:950; margin-top:7px; color:#FFFFFF; letter-spacing:-.025em;}
.radar2-main-sub{font-size:.83rem; line-height:1.33; color:rgba(255,255,255,.78); margin-top:9px;}
.radar2-tile{background:#FFFFFF; color:#0F172A; border-radius:18px; padding:14px 14px; box-shadow:0 10px 24px rgba(15,23,42,.13); min-height:142px; border-top:5px solid var(--interey-blue);}
.radar2-tile.green{border-top-color:var(--interey-green);}
.radar2-tile.red{border-top-color:var(--interey-red);}
.radar2-tile.yellow{border-top-color:var(--interey-yellow);}
.radar2-label{font-size:.74rem; font-weight:900; color:#64748B; text-transform:uppercase; letter-spacing:.06em;}
.radar2-value{font-size:1.22rem; font-weight:950; color:#0B1F4D; margin-top:6px; line-height:1.12;}
.radar2-text{font-size:.81rem; color:#475569; line-height:1.30; margin-top:8px;}
.radar2-list{margin:8px 0 0 0; padding-left:0; list-style:none;}
.radar2-list li{font-size:.80rem; color:#334155; line-height:1.32; margin:5px 0;}
.radar2-list li:before{content:"•"; color:var(--interey-blue); font-weight:950; margin-right:7px;}
.radar2-tile.green .radar2-list li:before{color:var(--interey-green);}
.radar2-tile.red .radar2-list li:before{color:var(--interey-red);}
.radar2-tile.yellow .radar2-list li:before{color:var(--interey-yellow);}
@media (max-width: 1200px){.radar2-grid{grid-template-columns:1fr 1fr;}}
@media (max-width: 760px){.radar-head{display:block;} .radar-badge{display:inline-block;margin-top:10px;} .radar2-grid{grid-template-columns:1fr;}}



/* Executive summary V43 */
.exec-summary-wrap{
    background: linear-gradient(135deg,#FFFFFF 0%,#F8FAFC 100%);
    border:1px solid rgba(18,62,112,.14);
    border-radius:22px;
    padding:18px 20px;
    margin:14px 0 18px 0;
    box-shadow:0 12px 30px rgba(15,23,42,.07);
}
.exec-summary-title{font-size:1.22rem;font-weight:950;color:var(--interey-blue-2);letter-spacing:-.02em;margin-bottom:4px;}
.exec-summary-sub{font-size:.85rem;color:#64748B;margin-bottom:14px;}
.exec-progress-card{
    background:linear-gradient(135deg,var(--interey-blue-2) 0%,var(--interey-blue) 100%);
    border-radius:20px;
    padding:18px 20px;
    color:#FFFFFF;
    box-shadow:0 10px 26px rgba(11,31,77,.16);
    overflow:hidden;
    position:relative;
}
.exec-progress-card:after{content:"";position:absolute;right:-40px;top:-60px;width:170px;height:170px;background:rgba(255,255,255,.08);border-radius:50%;}
.exec-progress-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-end;position:relative;z-index:2;}
.exec-progress-label{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:900;color:rgba(255,255,255,.75);}
.exec-progress-value{font-size:2.35rem;font-weight:950;letter-spacing:-.05em;line-height:1;}
.exec-progress-status{font-size:.88rem;font-weight:850;color:rgba(255,255,255,.88);text-align:right;}
.exec-progress-track{height:16px;background:rgba(255,255,255,.18);border-radius:999px;margin-top:16px;overflow:hidden;position:relative;z-index:2;}
.exec-progress-fill{height:16px;border-radius:999px;background:linear-gradient(90deg,#FFFFFF 0%,#DCEBFF 100%);}
.exec-progress-foot{font-size:.80rem;color:rgba(255,255,255,.78);margin-top:10px;position:relative;z-index:2;}
.exec-insights-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:14px;}
.exec-insight{background:#FFFFFF;border:1px solid #E2E8F0;border-radius:18px;padding:14px 14px;min-height:112px;box-shadow:0 8px 22px rgba(15,23,42,.05);border-left:5px solid var(--interey-blue);}
.exec-insight.green{border-left-color:var(--interey-green);} .exec-insight.red{border-left-color:var(--interey-red);} .exec-insight.yellow{border-left-color:var(--interey-yellow);} .exec-insight.gray{border-left-color:var(--interey-gray);}
.exec-insight-label{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:#64748B;font-weight:900;}
.exec-insight-value{font-size:1.05rem;line-height:1.20;font-weight:950;color:#0B1F4D;margin-top:7px;}
.exec-insight-text{font-size:.80rem;line-height:1.30;color:#475569;margin-top:7px;}
@media (max-width:1200px){.exec-insights-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media (max-width:760px){.exec-insights-grid{grid-template-columns:1fr;}}


/* Executive view selector */
.view-selector-card{
    background:linear-gradient(135deg,#FFFFFF 0%,#F8FAFC 100%);
    border:1px solid rgba(18,62,112,.14);
    border-radius:18px;
    padding:14px 18px 10px 18px;
    margin:12px 0 16px 0;
    box-shadow:0 8px 22px rgba(15,23,42,.05);
}
.view-selector-title{font-size:1.05rem;font-weight:900;color:var(--interey-blue-2);margin-bottom:2px;}
.view-selector-sub{font-size:.80rem;color:#64748B;margin-bottom:8px;}
div[role="radiogroup"] label{
    background:#FFFFFF;
    border:1px solid #D8E2EC;
    border-radius:999px;
    padding:8px 13px;
    margin-right:8px;
    box-shadow:0 3px 10px rgba(15,23,42,.04);
}
div[role="radiogroup"] label:hover{border-color:var(--interey-blue); transform: translateY(-1px); transition:.15s ease;}
div[role="radiogroup"] label:has(input:checked){
    background:linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color:#FFFFFF !important;
    border-color:var(--interey-blue-2);
    box-shadow:0 8px 18px rgba(18,62,112,.20);
}
div[role="radiogroup"] label:has(input:checked) p{color:#FFFFFF !important; font-weight:900;}

/* Streamlit tabs */
button[data-baseweb="tab"]{font-weight:700;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--interey-red);}



/* Premium tables */
.premium-table-wrap{
    background:#FFFFFF;
    border:1px solid rgba(18,62,112,.12);
    border-radius:16px;
    padding:10px 10px 8px 10px;
    box-shadow:0 8px 20px rgba(15,23,42,.05);
    overflow-x:auto;
    margin:8px 0 18px 0;
}
.premium-table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    font-size:.82rem;
    color:#1F2937;
}
.premium-table th{
    background:linear-gradient(135deg, var(--interey-blue-2) 0%, var(--interey-blue) 100%);
    color:#FFFFFF;
    padding:9px 10px;
    text-align:right;
    font-weight:850;
    border-right:1px solid rgba(255,255,255,.16);
    white-space:nowrap;
}
.premium-table th:first-child{
    text-align:left;
    border-top-left-radius:10px;
}
.premium-table th:last-child{
    border-top-right-radius:10px;
    border-right:none;
}
.premium-table td{
    padding:8px 10px;
    text-align:right;
    border-bottom:1px solid #E5EAF0;
    white-space:nowrap;
}
.premium-table td:first-child{
    text-align:left;
    font-weight:800;
    color:var(--interey-blue-2);
}
.premium-table tr:nth-child(even) td{background:#F8FAFC;}
.premium-table tr.highlight-row td{background:#EEF6FF; font-weight:850;}
.premium-table tr.risk-row td{background:#FFF7F7;}
.premium-table tr.warn-row td{background:#FFFBEB;}
.premium-table tr.attention-row td{background:#FFF7ED;}
.premium-table tr.critical-row td{background:#FEF2F2; font-weight:800;}
.backlog-alert{background:linear-gradient(135deg,#7F1D1D 0%,#DC2626 100%);color:#FFFFFF;border-radius:18px;padding:16px 18px;margin:12px 0 16px 0;box-shadow:0 10px 24px rgba(185,28,28,.18);border:1px solid rgba(255,255,255,.18);}
.backlog-alert-title{font-size:.80rem;text-transform:uppercase;letter-spacing:.08em;font-weight:900;opacity:.82;}
.backlog-alert-value{font-size:1.28rem;font-weight:950;margin-top:5px;line-height:1.18;}
.backlog-alert-sub{font-size:.82rem;opacity:.88;margin-top:5px;}
.premium-table tr.attention-row td{background:#FFF7ED;}
.premium-table tr.critical-row td{background:#FEE2E2; font-weight:850;}
.engineer-table td:nth-child(1), .engineer-table th:nth-child(1){text-align:left;}
.engineer-table td:nth-child(7), .engineer-table th:nth-child(7), .engineer-table td:nth-child(8), .engineer-table th:nth-child(8){text-align:left;}
.premium-table td.total-col{font-weight:900; color:var(--interey-blue-2); background:#EEF3F8;}
.status-good{color:#047857; font-weight:900;}
.status-warn{color:#B45309; font-weight:900;}
.status-bad{color:#B91C1C; font-weight:900;}
.table-caption-premium{font-size:.78rem; color:#64748B; margin-top:-8px; margin-bottom:8px;}

@media (max-width: 1100px){
    .radar-grid{grid-template-columns: repeat(2, minmax(0, 1fr));}
    .hero-date{text-align:left;}
}
</style>
""", unsafe_allow_html=True)

MONTHS_ES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
MONTH_ORDER = [MONTHS_ES[i] for i in range(1,13)]
MONTHS_FULL_TO_NUM = {"ENERO":1,"FEBRERO":2,"MARZO":3,"ABRIL":4,"MAYO":5,"JUNIO":6,"JULIO":7,"AGOSTO":8,"SEPTIEMBRE":9,"SETIEMBRE":9,"OCTUBRE":10,"NOVIEMBRE":11,"DICIEMBRE":12}
CUTOFF_DATE = pd.Timestamp("2026-05-31")
START_DATE = pd.Timestamp("2024-01-01")
VALID_YEARS = [2024, 2025, 2026]
PROJECT_TARGETS = {2024: 500000, 2025: 700000, 2026: 750000}
STORE_TARGETS = {2024: 150000, 2025: 250000, 2026: 275000}
ACTIVE_PROJECT_ENGINEERS_FOR_TARGET = 4
EXCLUDE_FROM_ENGINEER_ANALYSIS = {"ORLANDO MARTINEZ", "ANA MARGARITA SAHAGUN"}

DEFAULT_PROJECT_FILES = ["Proyectos 2024-2026.csv", "Reporte 2024-2026.csv", "Reporte 2024-2026.csv"]
DEFAULT_STORE_FILES = ["Tienda 2024-2026.csv", "reporte 2024-2026.csv"]
DEFAULT_EXPENSE_FILES = ["VENTAS INTEREY PROYECTOS Y TIENDA 2026.xlsx", "Gastos INTEREY 2026.xlsx", "Gastos 2026.xlsx"]
DEFAULT_BACKLOG_FILES = ["Proyectos en ejecucion.csv", "Proyectos%20en%20ejecucion.csv", "Proyectos en ejecución.csv"]


def fmt_money(x):
    try:
        if pd.isna(x):
            return "$0"
        return f"${float(x):,.0f}"
    except Exception:
        return "$0"


def fmt_pct(x):
    try:
        if pd.isna(x):
            return "0.0%"
        return f"{float(x):,.1f}%"
    except Exception:
        return "0.0%"


def parse_money(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if s == "" or s.lower() in ["nan", "none"]:
        return pd.NA
    # formato tipo ($ -494.61), (-6,484.63 %), $17.32
    neg = "(" in s and ")" in s
    s = s.replace("$", "").replace(",", "").replace("%", "").replace("(", "").replace(")", "").strip()
    s = s.replace(" ", "")
    try:
        val = float(s)
        return -abs(val) if neg else val
    except Exception:
        return pd.NA


def parse_date_project(series):
    dt = pd.to_datetime(series, format="%d/%m/%Y", errors="coerce")
    if dt.isna().all():
        dt = pd.to_datetime(series, dayfirst=True, errors="coerce")
    return dt


def parse_date_store(series):
    # Puede venir como "09:21 04/01/2024" o "04/01/2024"
    raw = series.astype(str).str.strip()
    extracted = raw.str.extract(r"(\d{1,2}/\d{1,2}/\d{4})", expand=False)
    candidate = extracted.fillna(raw)
    return pd.to_datetime(candidate, dayfirst=True, errors="coerce")


def add_time_cols(df):
    df["Año"] = df["Fecha"].dt.year
    df["Mes_Num"] = df["Fecha"].dt.month
    df["Mes"] = df["Mes_Num"].map(MONTHS_ES)
    df["Periodo"] = df["Fecha"].dt.strftime("%Y-%m")
    return df


def find_default_file(names):
    here = Path(__file__).resolve().parent
    for name in names:
        p = here / name
        if p.exists():
            return p
    return None


@st.cache_data
def load_projects(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        p = find_default_file(DEFAULT_PROJECT_FILES)
        if p is None:
            return pd.DataFrame()
        df = pd.read_csv(p)

    for col in ["Promotor", "Cliente", "Moneda", "Descripcion"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["TC", "Cotizado cliente", "Utilidad bruta", "Utilidad", "Utilidad después de indirectos"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    if "Fecha" not in df.columns:
        return pd.DataFrame()
    df["Fecha"] = parse_date_project(df["Fecha"])
    df = add_time_cols(df)

    # Regla de corte: solo 2024 en adelante y hasta 31/mayo/2026
    df = df[(df["Fecha"] >= START_DATE) & (df["Fecha"] <= CUTOFF_DATE) & (df["Año"].isin(VALID_YEARS))].copy()

    # Nota: Ana Margarita Sahagun y Orlando Martinez SÍ se incluyen en KPIs corporativos.
    # Solo se excluyen en los comparativos de desempeño por ingeniero/promotor.

    df["Moneda"] = df.get("Moneda", "MXN")
    df["Moneda"] = df["Moneda"].fillna("MXN").astype(str).str.upper()
    df["TC"] = df.get("TC", 1.0)
    df["TC"] = pd.to_numeric(df["TC"], errors="coerce").fillna(1.0)
    df["Tipo_Cambio_Aplicado"] = df.apply(lambda r: r["TC"] if r["Moneda"] == "USD" else 1.0, axis=1)

    df["Ventas_MXN"] = pd.to_numeric(df.get("Cotizado cliente", 0), errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]
    if "Utilidad bruta" not in df.columns:
        st.warning("El archivo de proyectos no trae la columna 'Utilidad bruta'. Se usará 'Utilidad después de indirectos' como respaldo.")
        util_source = "Utilidad después de indirectos" if "Utilidad después de indirectos" in df.columns else "Utilidad"
    else:
        util_source = "Utilidad bruta"
    df["Utilidad_Bruta_MXN"] = pd.to_numeric(df.get(util_source, 0), errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]
    df["Margen_Bruto_Pct"] = (df["Utilidad_Bruta_MXN"] / df["Ventas_MXN"].replace(0, pd.NA)) * 100
    df["Unidad"] = "Proyectos"
    return df


@st.cache_data
def load_backlog(uploaded_file):
    """Carga el snapshot vigente de proyectos con OC pendientes de facturar.

    Este archivo sustituye al anterior en cada corte mensual; no se acumula.
    """
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as exc:
            st.warning(f"No fue posible leer el archivo de ingresos comprometidos: {exc}")
            return pd.DataFrame()
    else:
        p = find_default_file(DEFAULT_BACKLOG_FILES)
        if p is None:
            return pd.DataFrame()
        try:
            df = pd.read_csv(p)
        except Exception as exc:
            st.warning(f"No fue posible leer el archivo base de ingresos comprometidos: {exc}")
            return pd.DataFrame()

    if df.empty:
        return pd.DataFrame()

    df.columns = [str(c).strip() for c in df.columns]
    required = ["Fecha", "Cliente", "Cotizado cliente"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.warning("El archivo de ingresos comprometidos no contiene: " + ", ".join(missing))
        return pd.DataFrame()

    for col in ["Promotor", "Cliente", "Descripcion", "Moneda", "Status"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    raw = df["Fecha"].astype(str).str.strip()
    dt = pd.to_datetime(raw, format="%d/%m/%y", errors="coerce")
    missing_dt = dt.isna()
    if missing_dt.any():
        dt.loc[missing_dt] = pd.to_datetime(raw.loc[missing_dt], format="%d/%m/%Y", errors="coerce")
    missing_dt = dt.isna()
    if missing_dt.any():
        dt.loc[missing_dt] = pd.to_datetime(raw.loc[missing_dt], dayfirst=True, errors="coerce")
    df["Fecha_OC"] = dt
    df = df[df["Fecha_OC"].notna()].copy()

    for col in ["TC", "Cotizado cliente"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    df["Moneda"] = df.get("Moneda", "MXN")
    df["Moneda"] = df["Moneda"].fillna("MXN").astype(str).str.upper()
    df["TC"] = pd.to_numeric(df.get("TC", 1.0), errors="coerce").fillna(1.0)
    df["Tipo_Cambio_Aplicado"] = df.apply(lambda r: r["TC"] if r["Moneda"] == "USD" else 1.0, axis=1)
    df["Importe_Pendiente_MXN"] = pd.to_numeric(df["Cotizado cliente"], errors="coerce").fillna(0) * df["Tipo_Cambio_Aplicado"]

    today = pd.Timestamp.today().normalize()
    df["Dias_Abiertos"] = (today - df["Fecha_OC"].dt.normalize()).dt.days.clip(lower=0)
    df["Periodo_OC"] = df["Fecha_OC"].dt.to_period("M").astype(str)
    df["Mes_OC"] = df["Fecha_OC"].dt.month.map(MONTHS_ES)
    df["Proyecto"] = df.get("Descripcion", "Sin descripción")
    df["Responsable"] = df.get("Promotor", "Sin responsable")

    def age_bucket(days):
        if days <= 30:
            return "🟢 0–30 días"
        if days <= 60:
            return "🟡 31–60 días"
        if days <= 90:
            return "🟠 61–90 días"
        return "🔴 Más de 90 días"

    df["Antigüedad"] = df["Dias_Abiertos"].apply(age_bucket)
    if "Id" in df.columns:
        df = df.drop_duplicates(subset=["Id"], keep="last")
    else:
        df = df.drop_duplicates(keep="last")
    return df.reset_index(drop=True)


@st.cache_data
def load_store(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        p = find_default_file(DEFAULT_STORE_FILES)
        if p is None:
            return pd.DataFrame()
        df = pd.read_csv(p)

    for col in ["Cliente", "Status", "Pago", "Facturado"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    for col in ["SubTotal", "Total", "Util $", "Tienda $", "Desc $", "Iva $"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_money)

    if "Fecha" not in df.columns:
        return pd.DataFrame()
    df["Fecha"] = parse_date_store(df["Fecha"])
    df = add_time_cols(df)
    df = df[(df["Fecha"] >= START_DATE) & (df["Fecha"] <= CUTOFF_DATE) & (df["Año"].isin(VALID_YEARS))].copy()

    # TIENDA: solo considerar ventas activas.
    # Regla de negocio: cualquier registro con Status/Estatus cancelado NO debe afectar ventas, utilidad, forecast ni consolidado.
    if "Status" in df.columns:
        df["Status_Normalizado"] = df["Status"].fillna("").astype(str).str.strip().str.upper()
        df = df[df["Status_Normalizado"].eq("ACTIVO")].copy()

    df["Ventas_MXN"] = pd.to_numeric(df.get("Total", 0), errors="coerce").fillna(0)
    df["Utilidad_Bruta_MXN"] = pd.to_numeric(df.get("Util $", 0), errors="coerce").fillna(0)
    df["Margen_Bruto_Pct"] = (df["Utilidad_Bruta_MXN"] / df["Ventas_MXN"].replace(0, pd.NA)) * 100
    df["Promotor"] = "JAVIER VILLANUEVA"
    df["Unidad"] = "Tienda"
    return df


@st.cache_data
def load_expenses(expense_file):
    """
    Lee gastos mensuales desde el Excel administrativo.
    Espera una hoja tipo 'RESUMEN 2026' con columnas:
    MES, GASTOS PROYECTOS y GASTOS TIENDA.
    """
    if expense_file is not None:
        xls = pd.ExcelFile(expense_file)
    else:
        p = find_default_file(DEFAULT_EXPENSE_FILES)
        if p is None:
            return pd.DataFrame(columns=["Año", "Mes_Num", "Mes", "Gasto_Proyectos", "Gasto_Tienda"])
        xls = pd.ExcelFile(p)

    sheet_name = next((s for s in xls.sheet_names if "RESUMEN" in str(s).upper()), xls.sheet_names[0])
    raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)

    header_idx = None
    for i in range(len(raw)):
        row_values = [str(v).strip().upper() for v in raw.iloc[i].tolist()]
        if "MES" in row_values and any("GASTOS PROYECTOS" in v for v in row_values) and any("GASTOS TIENDA" in v for v in row_values):
            header_idx = i
            break

    if header_idx is None:
        st.warning("No encontré las columnas 'GASTOS PROYECTOS' y 'GASTOS TIENDA' en el archivo de gastos.")
        return pd.DataFrame(columns=["Año", "Mes_Num", "Mes", "Gasto_Proyectos", "Gasto_Tienda"])

    headers = raw.iloc[header_idx].astype(str).str.strip().tolist()
    data = raw.iloc[header_idx + 1:].copy()
    data.columns = headers

    # quitar filas vacías o total
    data = data[data["MES"].notna()].copy()
    data["MES_NORM"] = data["MES"].astype(str).str.strip().str.upper()
    data = data[data["MES_NORM"].isin(MONTHS_FULL_TO_NUM.keys())].copy()

    data["Mes_Num"] = data["MES_NORM"].map(MONTHS_FULL_TO_NUM)
    data["Mes"] = data["Mes_Num"].map(MONTHS_ES)
    data["Año"] = 2026

    data["Gasto_Proyectos"] = data.get("GASTOS PROYECTOS", 0).apply(parse_money).fillna(0).astype(float)
    data["Gasto_Tienda"] = data.get("GASTOS TIENDA", 0).apply(parse_money).fillna(0).astype(float)

    return data[["Año", "Mes_Num", "Mes", "Gasto_Proyectos", "Gasto_Tienda"]].copy()


def expenses_dict(expenses_df, year, months, unidad):
    col = "Gasto_Proyectos" if unidad == "Proyectos" else "Gasto_Tienda"
    if expenses_df.empty or col not in expenses_df.columns:
        return {m: 0.0 for m in months}
    temp = expenses_df[(expenses_df["Año"] == year) & (expenses_df["Mes_Num"].isin(months))].copy()
    by_month = temp.groupby("Mes_Num")[col].sum().to_dict()
    return {m: float(by_month.get(m, 0.0)) for m in months}


def closed_months_for_year(df, year):
    months = sorted(df.loc[df["Año"] == year, "Mes_Num"].dropna().astype(int).unique().tolist())
    if not months:
        return []
    # Regla: si el último mes cargado está incompleto por corte futuro, se excluye solo si supera corte real.
    # Para 2026 el corte es mayo, así que mayo sí es mes cerrado del análisis solicitado.
    return months


def ytd_months_for_selected_year(selected_year):
    if selected_year == 2026:
        return [1,2,3,4,5]
    return list(range(1,13))


def yoy(curr, prev):
    if prev in [0, None] or pd.isna(prev):
        return None
    return ((curr - prev) / prev) * 100


def card(label, value, sub="", style=""):
    return f"""
    <div class="kpi-card {style}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


def trend_note(text):
    st.markdown(f'<div class="trend-note">{text}</div>', unsafe_allow_html=True)


def radar_interey(consol_fc, proj_fc, store_fc):
    """Radar INTEREY 3.0: lectura ejecutiva tipo consultoría con fortaleza, atención, riesgo y oportunidad."""
    ventas = consol_fc.get("ventas_ytd", 0)
    proj_share = (proj_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    store_share = (store_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    gap = consol_fc.get("gap", 0)
    cumplimiento = consol_fc.get("cumplimiento", 0)
    utilidad_neta_ytd = consol_fc.get("utilidad_neta_ytd", 0)
    utilidad_neta_proy = consol_fc.get("utilidad_neta_proy", 0)
    venta_req = consol_fc.get("venta_req", 0)

    emoji, forecast_style, forecast_status = status_from_pct(cumplimiento)

    # Fortaleza: unidad con mejor cumplimiento proyectado
    if store_fc.get("cumplimiento", 0) >= proj_fc.get("cumplimiento", 0):
        fortaleza_txt = f"Tienda proyecta {fmt_pct(store_fc.get('cumplimiento', 0))} de su meta anual."
        fortaleza_sub = f"Aporta {store_share:,.1f}% de los ingresos y mantiene lectura favorable contra objetivo."
    else:
        fortaleza_txt = f"Proyectos lidera el avance con {fmt_pct(proj_fc.get('cumplimiento', 0))} proyectado."
        fortaleza_sub = f"Representa {proj_share:,.1f}% de los ingresos acumulados."

    # Atención: utilidad neta real/proyectada
    if utilidad_neta_ytd < 0:
        atencion_txt = "La utilidad neta acumulada continúa en terreno negativo."
        atencion_sub = f"Resultado YTD: {fmt_money_compact(utilidad_neta_ytd)} después de gastos."
        atencion_class = "yellow"
    elif utilidad_neta_proy < 0:
        atencion_txt = "La utilidad neta proyectada aún requiere seguimiento."
        atencion_sub = f"Cierre estimado: {fmt_money_compact(utilidad_neta_proy)} con la tendencia actual."
        atencion_class = "yellow"
    else:
        atencion_txt = "La utilidad proyectada se mantiene positiva."
        atencion_sub = f"Cierre estimado: {fmt_money_compact(utilidad_neta_proy)}."
        atencion_class = "green"

    # Riesgo principal: unidad con menor cumplimiento
    if proj_fc.get("cumplimiento", 0) <= store_fc.get("cumplimiento", 0):
        riesgo_txt = f"Proyectos cerraría en {fmt_pct(proj_fc.get('cumplimiento', 0))} de su meta."
        riesgo_sub = f"Faltante proyectado de proyectos: {fmt_money_signed(proj_fc.get('gap', 0))}."
    else:
        riesgo_txt = f"Tienda cerraría en {fmt_pct(store_fc.get('cumplimiento', 0))} de su meta."
        riesgo_sub = f"Faltante proyectado de tienda: {fmt_money_signed(store_fc.get('gap', 0))}."

    # Oportunidad: venta requerida mensual consolidada
    if gap >= 0:
        oportunidad_txt = "La tendencia actual proyecta excedente contra meta."
        oportunidad_sub = f"Excedente estimado: {fmt_money_signed(gap)}."
        oportunidad_class = "green"
    else:
        oportunidad_txt = f"Incrementar ventas a {fmt_money(venta_req)} mensuales ayudaría a cerrar la brecha."
        oportunidad_sub = f"Faltante consolidado: {fmt_money_signed(gap)}."
        oportunidad_class = "red" if cumplimiento < 90 else "yellow"

    if cumplimiento >= 100:
        headline = "INTEREY proyecta cerrar por encima de la meta anual."
        headline_sub = "El ritmo actual indica cumplimiento comercial si se mantiene la tendencia."
    elif cumplimiento >= 90:
        headline = "INTEREY está cerca de la meta, pero necesita seguimiento comercial."
        headline_sub = "El cierre depende de sostener ventas y controlar gastos durante los meses restantes."
    else:
        headline = "INTEREY proyecta cerrar por debajo de la meta anual."
        headline_sub = "El foco debe estar en recuperar el faltante proyectado y proteger utilidad neta."

    html = f"""
    <div class="radar-card">
        <div class="radar-head">
            <div>
                <div class="radar-title">📡 Radar INTEREY 3.0</div>
                <div class="radar-subtitle">Lectura ejecutiva automática: fortalezas, riesgos, utilidad, oportunidad comercial y avance proyectado.</div>
            </div>
            <div class="radar-badge">{emoji} Estado general: {forecast_status}</div>
        </div>
        <div class="radar2-grid">
            <div class="radar2-main">
                <div class="radar2-main-label">Lectura principal</div>
                <div class="radar2-main-value">{headline}</div>
                <div class="radar2-main-sub">{headline_sub}</div>
            </div>
            <div class="radar2-tile green">
                <div class="radar2-label">🟢 Fortaleza</div>
                <div class="radar2-value">{fortaleza_txt}</div>
                <div class="radar2-text">{fortaleza_sub}</div>
            </div>
            <div class="radar2-tile {atencion_class}">
                <div class="radar2-label">🟡 Atención</div>
                <div class="radar2-value">{atencion_txt}</div>
                <div class="radar2-text">{atencion_sub}</div>
            </div>
            <div class="radar2-tile red">
                <div class="radar2-label">🔴 Riesgo principal</div>
                <div class="radar2-value">{riesgo_txt}</div>
                <div class="radar2-text">{riesgo_sub}</div>
            </div>
            <div class="radar2-tile {oportunidad_class}">
                <div class="radar2-label">🔵 Oportunidad</div>
                <div class="radar2-value">{oportunidad_txt}</div>
                <div class="radar2-text">{oportunidad_sub}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def status_from_pct(pct, green=100, yellow=90):
    try:
        pct = float(pct)
    except Exception:
        return "🔴", "red", "Riesgo alto"
    if pct >= green:
        return "🟢", "green", "En línea"
    if pct >= yellow:
        return "🟡", "yellow", "Riesgo moderado"
    return "🔴", "red", "Riesgo alto"


def compliance_text(pct):
    emoji, _, status = status_from_pct(pct)
    return f"{emoji} Cumplimiento proyectado: {fmt_pct(pct)} · {status}"


def gap_label_and_style(gap):
    if gap >= 0:
        return "🟢 Excedente proyectado", "green", "proyección arriba de meta"
    return "🔴 Faltante proyectado", "red", "proyección debajo de meta"


def fmt_money_signed(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    sign = "+" if x > 0 else ""
    return f"{sign}${x:,.0f}"


def fmt_money_compact(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    sign = "-" if x < 0 else ""
    ax = abs(x)
    if ax >= 1_000_000:
        return f"{sign}${ax/1_000_000:,.2f} M"
    if ax >= 1_000:
        return f"{sign}${ax/1_000:,.0f} K"
    return f"{sign}${ax:,.0f}"


def summary_metrics(df):
    ventas = df["Ventas_MXN"].sum() if not df.empty else 0
    utilidad = df["Utilidad_Bruta_MXN"].sum() if not df.empty else 0
    margen = utilidad / ventas * 100 if ventas else 0
    clientes = df["Cliente"].nunique() if "Cliente" in df.columns and not df.empty else 0
    ticket = ventas / clientes if clientes else 0
    return ventas, utilidad, margen, clientes, ticket


def expense_inputs(prefix, year, months):
    st.sidebar.markdown(f"### Gastos {prefix} {year}")
    expenses = {}
    cols = st.sidebar.columns(2)
    for idx, m in enumerate(months):
        with cols[idx % 2]:
            expenses[m] = st.number_input(
                f"{prefix} {MONTHS_ES[m]}", min_value=0.0, value=0.0, step=10000.0, format="%.0f", key=f"gasto_{prefix}_{year}_{m}"
            )
    return expenses


def forecast_block(label, df_ytd, gastos_dict, meta_mensual, months_ytd, multiplier=1):
    meses_count = max(len(months_ytd), 1)
    ventas_ytd = df_ytd["Ventas_MXN"].sum() if not df_ytd.empty else 0
    util_ytd = df_ytd["Utilidad_Bruta_MXN"].sum() if not df_ytd.empty else 0
    gasto_ytd = sum(float(gastos_dict.get(m, 0)) for m in months_ytd)
    utilidad_neta_ytd = util_ytd - gasto_ytd
    margen_neto_ytd = utilidad_neta_ytd / ventas_ytd * 100 if ventas_ytd else 0

    promedio_ventas = ventas_ytd / meses_count
    promedio_util = util_ytd / meses_count
    promedio_gasto = gasto_ytd / meses_count if meses_count else 0

    forecast_ventas = promedio_ventas * 12
    forecast_util = promedio_util * 12
    gasto_anual_proy = promedio_gasto * 12
    utilidad_neta_proy = forecast_util - gasto_anual_proy
    margen_neto_proy = utilidad_neta_proy / forecast_ventas * 100 if forecast_ventas else 0

    meta_anual = meta_mensual * 12 * multiplier
    cumplimiento = forecast_ventas / meta_anual * 100 if meta_anual else 0
    gap = forecast_ventas - meta_anual
    meses_restantes = max(12 - meses_count, 0)
    venta_req = (meta_anual - ventas_ytd) / meses_restantes if meses_restantes else 0
    return {
        "label": label,
        "ventas_ytd": ventas_ytd,
        "utilidad_bruta_ytd": util_ytd,
        "gasto_ytd": gasto_ytd,
        "utilidad_neta_ytd": utilidad_neta_ytd,
        "margen_neto_ytd": margen_neto_ytd,
        "forecast_ventas": forecast_ventas,
        "forecast_utilidad_bruta": forecast_util,
        "gasto_anual_proy": gasto_anual_proy,
        "utilidad_neta_proy": utilidad_neta_proy,
        "margen_neto_proy": margen_neto_proy,
        "meta_anual": meta_anual,
        "cumplimiento": cumplimiento,
        "gap": gap,
        "venta_req": venta_req,
        "meses_restantes": meses_restantes,
    }


def monthly_chart(df, title, ycol="Ventas_MXN"):
    if df.empty:
        st.info("No hay datos para graficar.")
        return
    monthly = df.groupby(["Año", "Mes_Num"], as_index=False).agg(Ventas_MXN=("Ventas_MXN", "sum"), Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN", "sum"))
    fig = px.line(monthly, x="Mes_Num", y=ycol, color="Año", markers=True, title=title)
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1,13)), ticktext=MONTH_ORDER))
    st.plotly_chart(fig, use_container_width=True)


def monthly_summary_table(df, title="Resumen mensual de ventas (MXN)", ycol="Ventas_MXN"):
    if df.empty:
        return
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-caption-premium">Valores mensuales por año · importes en MXN · incluye columna total para conciliación rápida.</div>', unsafe_allow_html=True)
    monthly = (
        df.groupby(["Año", "Mes_Num"], as_index=False)[ycol]
        .sum()
        .pivot(index="Año", columns="Mes_Num", values=ycol)
        .fillna(0)
    )
    for m in range(1, 13):
        if m not in monthly.columns:
            monthly[m] = 0
    monthly = monthly[[1,2,3,4,5,6,7,8,9,10,11,12]]
    monthly["Total"] = monthly.sum(axis=1)
    monthly = monthly.rename(columns=MONTHS_ES)
    monthly = monthly.reindex([y for y in VALID_YEARS if y in monthly.index])

    headers = ["Año"] + MONTH_ORDER + ["Total"]
    rows = []
    for year, row in monthly.iterrows():
        tr_class = ' class="highlight-row"' if int(year) == selected_year else ''
        tds = [f"<td>{int(year)}</td>"]
        for col in MONTH_ORDER:
            val = row.get(col, 0)
            tds.append(f"<td>{fmt_money(val) if pd.notna(val) and abs(float(val)) > 0.0001 else '-'}</td>")
        tds.append(f"<td class='total-col'>{fmt_money(row.get('Total', 0))}</td>")
        rows.append(f"<tr{tr_class}>" + "".join(tds) + "</tr>")
    html = """
    <div class="premium-table-wrap">
        <table class="premium-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{h}</th>" for h in headers),
        rows="".join(rows)
    )
    st.markdown(html, unsafe_allow_html=True)


def premium_engineer_table(prom_df):
    """Tabla premium HTML estable para Ranking Comercial INTEREY."""
    if prom_df.empty:
        st.info("No hay datos comparables de ingenieros para el filtro actual.")
        return

    table = prom_df.copy().sort_values("Ventas_MXN", ascending=False).reset_index(drop=True)
    headers = ["Ingeniero", "Ventas", "Utilidad bruta", "Margen", "Meta acumulada", "Avance", "Estado", "Alerta"]
    rows_html = []

    for idx, row in table.iterrows():
        avance = row.get("Cumplimiento_YTD_Pct", 0)
        if pd.notna(avance) and avance >= 100:
            estado = '<span class="status-good">🟢 En meta</span>'
        elif pd.notna(avance) and avance >= 80:
            estado = '<span class="status-warn">🟡 En seguimiento</span>'
        else:
            estado = '<span class="status-bad">🔴 Bajo meta</span>'

        alerta = str(row.get("Alerta", ""))
        if alerta == "Sin alerta":
            alerta_html = '<span class="status-good">Sin alerta</span>'
        elif "Margen" in alerta:
            alerta_html = f'<span class="status-warn">{alerta}</span>'
        else:
            alerta_html = f'<span class="status-bad">{alerta}</span>'

        ingeniero = str(row.get("Promotor", ""))
        if idx == 0:
            ingeniero = "🏆 " + ingeniero
            tr_class = ' class="highlight-row"'
        elif pd.notna(avance) and avance < 80:
            tr_class = ' class="risk-row"'
        elif pd.notna(avance) and avance < 100:
            tr_class = ' class="warn-row"'
        else:
            tr_class = ""

        cells = [
            ingeniero,
            fmt_money(row.get("Ventas_MXN", 0)),
            fmt_money(row.get("Utilidad_Bruta_MXN", 0)),
            fmt_pct(row.get("Margen_Bruto_Pct", 0)),
            fmt_money(row.get("Meta_YTD", 0)),
            fmt_pct(avance),
            estado,
            alerta_html,
        ]
        rows_html.append(f"<tr{tr_class}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")

    html = """
    <div class="premium-table-wrap">
        <table class="premium-table engineer-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{h}</th>" for h in headers),
        rows="".join(rows_html)
    )
    st.markdown(html, unsafe_allow_html=True)




def premium_simple_table(df, title, caption="", columns=None, row_class_fn=None):
    """Tabla HTML premium reusable para salidas ejecutivas.
    columns = [(col_original, "Etiqueta", "tipo")] donde tipo: text, money, pct, number
    """
    if df is None or df.empty:
        st.info("No hay datos para mostrar.")
        return

    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="table-caption-premium">{caption}</div>', unsafe_allow_html=True)

    if columns is None:
        columns = [(c, c, "text") for c in df.columns]

    def fmt_cell(value, kind):
        if kind == "money":
            return fmt_money(value)
        if kind == "money_signed":
            return fmt_money_signed(value)
        if kind == "pct":
            return fmt_pct(value)
        if kind == "number":
            try:
                return f"{float(value):,.0f}"
            except Exception:
                return str(value)
        return "" if pd.isna(value) else str(value)

    rows_html = []
    for idx, row in df.iterrows():
        tr_class = ""
        if row_class_fn is not None:
            cls = row_class_fn(row, idx)
            tr_class = f' class="{cls}"' if cls else ""
        tds = []
        for col, label, kind in columns:
            val = row.get(col, "")
            cell = fmt_cell(val, kind)
            if kind in ["money_signed"] and isinstance(val, (int, float)) and val < 0:
                cell = f'<span class="status-bad">{cell}</span>'
            tds.append(f"<td>{cell}</td>")
        rows_html.append(f"<tr{tr_class}>" + "".join(tds) + "</tr>")

    html = """
    <div class="premium-table-wrap">
        <table class="premium-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """.format(
        headers="".join(f"<th>{label}</th>" for _, label, _ in columns),
        rows="".join(rows_html)
    )
    st.markdown(html, unsafe_allow_html=True)



def render_executive_summary(consol_fc, proj_fc, store_fc):
    """Vista 0 tipo CEO: lectura ejecutiva sin exceso de gráficas ni scroll."""
    cumplimiento = consol_fc.get("cumplimiento", 0)
    emoji, style, status = status_from_pct(cumplimiento)
    gap = consol_fc.get("gap", 0)
    gap_label, gap_style, _ = gap_label_and_style(gap)
    ventas = consol_fc.get("ventas_ytd", 0)
    proj_share = (proj_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    store_share = (store_fc.get("ventas_ytd", 0) / ventas * 100) if ventas else 0
    monthly_needed = consol_fc.get("venta_req", 0)
    progress_width = max(0, min(float(cumplimiento), 100))

    if proj_fc.get("cumplimiento", 0) < store_fc.get("cumplimiento", 0):
        risk_unit = "Proyectos"
        risk_pct = proj_fc.get("cumplimiento", 0)
    else:
        risk_unit = "Tienda"
        risk_pct = store_fc.get("cumplimiento", 0)

    html = f"""
    <div class="exec-summary-wrap">
        <div class="exec-summary-title">🏠 Estado General INTEREY</div>
        <div class="exec-summary-sub">Vista CEO: resultado actual, avance proyectado, utilidad estimada, faltante y oportunidad mensual.</div>
        <div class="exec-progress-card">
            <div class="exec-progress-head">
                <div>
                    <div class="exec-progress-label">Cumplimiento proyectado contra meta anual</div>
                    <div class="exec-progress-value">{fmt_pct(cumplimiento)}</div>
                </div>
                <div class="exec-progress-status">{emoji} {status}<br><span style="font-weight:700;opacity:.82;">{fmt_money(consol_fc.get('forecast_ventas',0))} proyectados</span></div>
            </div>
            <div class="exec-progress-track"><div class="exec-progress-fill" style="width:{progress_width}%;"></div></div>
            <div class="exec-progress-foot">Meta anual consolidada: <b>{fmt_money(consol_fc.get('meta_anual',0))}</b> · {gap_label}: <b>{fmt_money_signed(gap)}</b></div>
        </div>
        <div class="exec-insights-grid">
            <div class="exec-insight">
                <div class="exec-insight-label">Composición</div>
                <div class="exec-insight-value">Proyectos {proj_share:,.1f}% · Tienda {store_share:,.1f}%</div>
                <div class="exec-insight-text">Participación de ingresos acumulados en el periodo seleccionado.</div>
            </div>
            <div class="exec-insight {gap_style}">
                <div class="exec-insight-label">Foco comercial</div>
                <div class="exec-insight-value">{fmt_money_signed(gap)}</div>
                <div class="exec-insight-text">Diferencia estimada entre la proyección de cierre y la meta anual.</div>
            </div>
            <div class="exec-insight {'red' if consol_fc.get('utilidad_neta_proy',0) < 0 else 'green'}">
                <div class="exec-insight-label">Utilidad estimada</div>
                <div class="exec-insight-value">{fmt_money(consol_fc.get('utilidad_neta_proy',0))}</div>
                <div class="exec-insight-text">Basado en tendencia actual de utilidad bruta y gastos cargados.</div>
            </div>
            <div class="exec-insight yellow">
                <div class="exec-insight-label">Oportunidad mensual</div>
                <div class="exec-insight-value">{fmt_money(monthly_needed)}</div>
                <div class="exec-insight-text">Venta promedio mensual requerida para alcanzar la meta anual.</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    mini = pd.DataFrame([
        {"Unidad":"🔵 Proyectos", "Ventas":proj_fc["ventas_ytd"], "Participación %":proj_share, "Cumplimiento %":proj_fc.get("cumplimiento",0), "Faltante/Excedente":proj_fc.get("gap",0)},
        {"Unidad":"🟢 Tienda", "Ventas":store_fc["ventas_ytd"], "Participación %":store_share, "Cumplimiento %":store_fc.get("cumplimiento",0), "Faltante/Excedente":store_fc.get("gap",0)},
    ])
    premium_simple_table(
        mini,
        "Mini comparativo ejecutivo",
        "Vista compacta para dirección: aportación de cada unidad y avance proyectado contra su meta.",
        columns=[
            ("Unidad", "Unidad", "text"),
            ("Ventas", "Ventas YTD", "money"),
            ("Participación %", "Participación", "pct"),
            ("Cumplimiento %", "Avance proyectado", "pct"),
            ("Faltante/Excedente", "Faltante / excedente", "money_signed"),
        ],
        row_class_fn=lambda row, idx: "highlight-row" if "Proyectos" in str(row.get("Unidad","")) else ""
    )


def render_dynamic_executive_view(view_name, fc, monthly_target_note=""):
    """Tarjetas dinámicas para evitar duplicar KPIs por unidad."""
    _, forecast_style, _ = status_from_pct(fc["cumplimiento"])
    gap_label, gap_style, gap_sub = gap_label_and_style(fc["gap"])
    net_style = "red" if fc["utilidad_neta_ytd"] < 0 else "green"
    net_proj_style = "red" if fc["utilidad_neta_proy"] < 0 else "green"

    if view_name == "Consolidado":
        ventas_label = "💰 Ventas consolidadas"
        utilidad_label = "📊 Utilidad bruta consolidada"
        gastos_label = "🧾 Gastos consolidados"
        neta_label = "🏁 Utilidad neta consolidada"
        forecast_label = "🎯 Proyección de cierre"
        meta_label = "Meta anual consolidada"
        ventas_sub = "Proyectos + Tienda"
        utilidad_sub = f"Margen bruto: {fmt_pct(fc.get('margen_bruto_ytd',0))}"
        gastos_sub = "Gastos desde archivo administrativo"
        meta_sub = "Proyectos + Tienda"
    elif view_name == "Proyectos":
        ventas_label = "💰 Ventas proyectos"
        utilidad_label = "📊 Utilidad bruta proyectos"
        gastos_label = "🧾 Gasto proyectos"
        neta_label = "🏁 Utilidad neta proyectos"
        forecast_label = "🎯 Proyección de cierre proyectos"
        meta_label = "Meta anual proyectos"
        ventas_sub = "Cotizado cliente × TC"
        utilidad_sub = f"Margen bruto: {fmt_pct((fc.get('utilidad_bruta_ytd',0) / fc.get('ventas_ytd',1) * 100) if fc.get('ventas_ytd',0) else 0)}"
        gastos_sub = "Gasto desde archivo administrativo"
        meta_sub = monthly_target_note
    else:
        ventas_label = "💰 Ventas tienda"
        utilidad_label = "📊 Utilidad tienda"
        gastos_label = "🧾 Gasto tienda"
        neta_label = "🏁 Utilidad neta tienda"
        forecast_label = "🎯 Proyección de cierre tienda"
        meta_label = "Meta anual tienda"
        ventas_sub = "Total · cancelados excluidos"
        utilidad_sub = f"Margen bruto: {fmt_pct((fc.get('utilidad_bruta_ytd',0) / fc.get('ventas_ytd',1) * 100) if fc.get('ventas_ytd',0) else 0)}"
        gastos_sub = "Gasto desde archivo administrativo"
        meta_sub = monthly_target_note

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(card(ventas_label, fmt_money(fc["ventas_ytd"]), ventas_sub), unsafe_allow_html=True)
    with c2: st.markdown(card(utilidad_label, fmt_money(fc["utilidad_bruta_ytd"]), utilidad_sub), unsafe_allow_html=True)
    with c3: st.markdown(card(gastos_label, fmt_money(fc["gasto_ytd"]), gastos_sub, "gray"), unsafe_allow_html=True)
    with c4: st.markdown(card(neta_label, fmt_money(fc["utilidad_neta_ytd"]), f"Margen neto: {fmt_pct(fc['margen_neto_ytd'])}", net_style), unsafe_allow_html=True)
    with c5: st.markdown(card(forecast_label, fmt_money(fc["forecast_ventas"]), compliance_text(fc["cumplimiento"]), forecast_style), unsafe_allow_html=True)

    st.markdown('<div class="kpi-spacer"></div>', unsafe_allow_html=True)
    d1,d2,d3,d4,d5 = st.columns(5)
    with d1: st.markdown(card(meta_label, fmt_money(fc["meta_anual"]), meta_sub, "gray"), unsafe_allow_html=True)
    with d2: st.markdown(card(gap_label, fmt_money_signed(fc["gap"]), gap_sub, gap_style), unsafe_allow_html=True)
    venta_req_style = "red" if fc["gap"] < 0 else "green"
    with d3: st.markdown(card("Venta requerida mensual", fmt_money(fc.get("venta_req", 0)), f"{int(fc.get('meses_restantes', 0))} meses restantes", venta_req_style), unsafe_allow_html=True)
    with d4: st.markdown(card("Utilidad bruta estimada", fmt_money(fc["forecast_utilidad_bruta"]), "Antes de gastos", "gray"), unsafe_allow_html=True)
    with d5: st.markdown(card("Utilidad estimada al cierre", fmt_money(fc["utilidad_neta_proy"]), f"Basado en tendencia · Margen: {fmt_pct(fc['margen_neto_proy'])}", net_proj_style), unsafe_allow_html=True)



def render_backlog_view(backlog_df, annual_project_target):
    st.markdown('<div class="section-title">📋 Backlog Ejecutivo</div>', unsafe_allow_html=True)
    trend_note("Proyectos con orden de compra aprobada, actualmente en ejecución y pendientes de facturación. El archivo mensual sustituye por completo al snapshot anterior.")

    if backlog_df is None or backlog_df.empty:
        st.info("No hay información de backlog. Carga el CSV en la barra lateral o agrega el archivo base en GitHub.")
        return

    total = float(backlog_df["Importe_Pendiente_MXN"].sum())
    abiertos = int(len(backlog_df))
    promedio = float(backlog_df["Dias_Abiertos"].mean()) if abiertos else 0
    oldest_idx = backlog_df["Dias_Abiertos"].idxmax()
    oldest = backlog_df.loc[oldest_idx]
    oldest_days = int(oldest["Dias_Abiertos"])
    oldest_client = str(oldest.get("Cliente", "Sin cliente"))
    oldest_amount = float(oldest.get("Importe_Pendiente_MXN", 0))

    critical = backlog_df[backlog_df["Dias_Abiertos"] > 90].copy()
    critical_count = int(len(critical))
    critical_amount = float(critical["Importe_Pendiente_MXN"].sum()) if critical_count else 0
    risk_pct = (critical_amount / total * 100) if total else 0
    coverage_pct = (total / annual_project_target * 100) if annual_project_target else 0

    client_summary = (
        backlog_df.groupby("Cliente", as_index=False)
        .agg(Importe=("Importe_Pendiente_MXN", "sum"), Proyectos=("Cliente", "size"))
        .sort_values("Importe", ascending=False)
    )
    top_client = str(client_summary.iloc[0]["Cliente"]) if not client_summary.empty else "Sin cliente"
    top_client_amount = float(client_summary.iloc[0]["Importe"]) if not client_summary.empty else 0
    top_client_share = (top_client_amount / total * 100) if total else 0
    healthy_count = int((backlog_df["Dias_Abiertos"] <= 30).sum())

    radar_html = f"""
    <div class="radar-card">
        <div class="radar-head">
            <div>
                <div class="radar-title">📡 Radar del Backlog</div>
                <div class="radar-subtitle">Lectura ejecutiva del ingreso pendiente, antigüedad, concentración y exposición financiera.</div>
            </div>
            <div class="radar-badge">{('🔴' if risk_pct >= 35 else '🟡' if risk_pct >= 20 else '🟢')} Riesgo financiero: {risk_pct:,.1f}%</div>
        </div>
        <div class="radar2-grid">
            <div class="radar2-main">
                <div class="radar2-main-label">Lectura principal</div>
                <div class="radar2-main-value">El backlog equivale al {coverage_pct:,.1f}% de la meta anual de Proyectos.</div>
                <div class="radar2-main-sub">Ingreso comprometido pendiente de facturar: <b>{fmt_money(total)}</b>.</div>
            </div>
            <div class="radar2-tile green">
                <div class="radar2-label">🟢 Fortaleza</div>
                <div class="radar2-value">{healthy_count:,} proyectos dentro de 30 días</div>
                <div class="radar2-text">Representan la parte más sana y reciente del backlog.</div>
            </div>
            <div class="radar2-tile yellow">
                <div class="radar2-label">🟡 Atención</div>
                <div class="radar2-value">Antigüedad promedio: {promedio:,.0f} días</div>
                <div class="radar2-text">Seguimiento recomendado para evitar que más proyectos migren a zona crítica.</div>
            </div>
            <div class="radar2-tile red">
                <div class="radar2-label">🔴 Riesgo</div>
                <div class="radar2-value">{critical_count:,} proyectos superan 90 días</div>
                <div class="radar2-text">Exposición acumulada: {fmt_money(critical_amount)}.</div>
            </div>
            <div class="radar2-tile {'red' if top_client_share >= 35 else 'yellow' if top_client_share >= 20 else 'green'}">
                <div class="radar2-label">🔵 Concentración</div>
                <div class="radar2-value">{top_client} concentra {top_client_share:,.1f}%</div>
                <div class="radar2-text">Importe pendiente del cliente: {fmt_money(top_client_amount)}.</div>
            </div>
        </div>
    </div>
    """
    st.markdown(radar_html, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(card("💰 Backlog total", fmt_money(total), "OC aprobadas pendientes de facturar"), unsafe_allow_html=True)
    with c2:
        st.markdown(card("📋 Proyectos abiertos", f"{abiertos:,}", "Actualmente en ejecución", "green"), unsafe_allow_html=True)
    with c3:
        avg_style = "red" if promedio > 90 else ("yellow" if promedio > 60 else "gray")
        st.markdown(card("⏳ Antigüedad promedio", f"{promedio:,.0f} días", "Desde la recepción de la OC", avg_style), unsafe_allow_html=True)
    with c4:
        old_style = "red" if oldest_days > 90 else ("orange" if oldest_days > 60 else "yellow")
        st.markdown(card("🔴 Proyecto más antiguo", f"{oldest_days:,} días", f"{oldest_client} · {fmt_money(oldest_amount)}", old_style), unsafe_allow_html=True)

    if critical_count:
        st.markdown(f"""
        <div class="backlog-alert">
            <div class="backlog-alert-title">🚨 Riesgo financiero detectado</div>
            <div class="backlog-alert-value">{critical_count:,} proyectos superan los 90 días y concentran {fmt_money(critical_amount)}.</div>
            <div class="backlog-alert-sub">Esto representa el <b>{risk_pct:,.1f}%</b> del backlog total pendiente de facturación.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Backlog sano: no existen proyectos con más de 90 días de antigüedad.")

    order = ["🟢 0–30 días", "🟡 31–60 días", "🟠 61–90 días", "🔴 Más de 90 días"]
    aging = backlog_df.groupby("Antigüedad", as_index=False).agg(
        Proyectos=("Antigüedad", "size"),
        Importe=("Importe_Pendiente_MXN", "sum")
    )
    aging["Antigüedad"] = pd.Categorical(aging["Antigüedad"], categories=order, ordered=True)
    aging = aging.sort_values("Antigüedad")

    a1, a2, a3, a4 = st.columns(4)
    age_cards = [("🟢 0–30 días", "green"), ("🟡 31–60 días", "yellow"), ("🟠 61–90 días", "orange"), ("🔴 Más de 90 días", "red")]
    for col, (bucket, style) in zip([a1, a2, a3, a4], age_cards):
        row = aging[aging["Antigüedad"] == bucket]
        count = int(row["Proyectos"].iloc[0]) if not row.empty else 0
        amount = float(row["Importe"].iloc[0]) if not row.empty else 0
        with col:
            st.markdown(card(bucket, f"{count:,} proyectos", fmt_money(amount), style), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Composición del backlog</div>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        fig_age = px.bar(aging, x="Antigüedad", y="Importe", text="Proyectos", title="Importe comprometido por antigüedad", category_orders={"Antigüedad": order})
        fig_age.update_traces(texttemplate="%{text} proyectos", textposition="outside")
        st.plotly_chart(fig_age, use_container_width=True)
    with g2:
        top_clients = client_summary.head(10).sort_values("Importe", ascending=True)
        fig_clients = px.bar(
            top_clients,
            x="Importe",
            y="Cliente",
            orientation="h",
            text="Proyectos",
            title="Top 10 clientes por ingreso pendiente",
            hover_data={"Importe": ":,.0f", "Proyectos": True},
        )
        fig_clients.update_traces(texttemplate="%{text} proyectos", textposition="outside")
        st.plotly_chart(fig_clients, use_container_width=True)

    table = backlog_df.copy().sort_values(["Dias_Abiertos", "Importe_Pendiente_MXN"], ascending=[False, False])
    table["Fecha_OC_Texto"] = table["Fecha_OC"].dt.strftime("%d/%m/%Y")
    premium_simple_table(
        table,
        "Detalle ejecutivo de proyectos con OC",
        "Ordenado del proyecto más antiguo al más reciente. El importe se expresa en MXN y las operaciones en USD utilizan el TC del archivo.",
        columns=[
            ("Antigüedad", "Semáforo", "text"),
            ("Cliente", "Cliente", "text"),
            ("Proyecto", "Proyecto", "text"),
            ("Responsable", "Responsable", "text"),
            ("Fecha_OC_Texto", "Fecha OC", "text"),
            ("Dias_Abiertos", "Días abiertos", "number"),
            ("Importe_Pendiente_MXN", "Importe pendiente", "money"),
        ],
        row_class_fn=lambda row, idx: "critical-row" if float(row.get("Dias_Abiertos", 0)) > 90 else ("attention-row" if float(row.get("Dias_Abiertos", 0)) > 60 else ("warn-row" if float(row.get("Dias_Abiertos", 0)) > 30 else "highlight-row"))
    )

# ---------- SIDEBAR ----------
st.sidebar.markdown("## Carga de archivos")
proj_upload = st.sidebar.file_uploader("Reporte Proyectos", type=["csv"], key="proj_upload")
store_upload = st.sidebar.file_uploader("Reporte Tienda", type=["csv"], key="store_upload")
expense_upload = st.sidebar.file_uploader("Archivo de gastos", type=["xlsx"], key="expense_upload")
backlog_upload = st.sidebar.file_uploader("Proyectos en ejecución (con OC)", type=["csv"], key="backlog_upload")
st.sidebar.caption("Si no subes archivos, el dashboard usará los archivos base de la misma carpeta. El CSV de proyectos en ejecución es un snapshot mensual y debe reemplazarse completo.")

projects = load_projects(proj_upload)
store = load_store(store_upload)
expenses = load_expenses(expense_upload)
backlog = load_backlog(backlog_upload)

if projects.empty and store.empty:
    st.error("No encontré datos. Sube los CSV de Proyectos y Tienda o colócalos en la misma carpeta del script.")
    st.stop()

years_available = sorted(set(projects.get("Año", pd.Series(dtype=int)).dropna().astype(int).unique().tolist() + store.get("Año", pd.Series(dtype=int)).dropna().astype(int).unique().tolist()))
years_available = [y for y in years_available if y in VALID_YEARS]
selected_year = st.sidebar.selectbox("Año principal", years_available, index=len(years_available)-1)
compare_years = st.sidebar.multiselect("Años a comparar", years_available, default=years_available)
months_available = ytd_months_for_selected_year(selected_year)
selected_months = st.sidebar.multiselect("Meses del año principal", list(range(1,13)), default=months_available)

st.sidebar.markdown("## Metas")
engineers = st.sidebar.number_input("Ingenieros proyectos considerados", min_value=1, value=ACTIVE_PROJECT_ENGINEERS_FOR_TARGET, step=1)
project_monthly_target = st.sidebar.number_input(f"Meta mensual proyectos {selected_year}", min_value=0.0, value=float(PROJECT_TARGETS.get(selected_year, 0)), step=50000.0, format="%.0f")
store_monthly_target = st.sidebar.number_input(f"Meta mensual tienda {selected_year}", min_value=0.0, value=float(STORE_TARGETS.get(selected_year, 0)), step=25000.0, format="%.0f")

months_ytd = selected_months
project_expenses = expenses_dict(expenses, selected_year, months_ytd, "Proyectos")
store_expenses = expenses_dict(expenses, selected_year, months_ytd, "Tienda")

st.sidebar.markdown("## Gastos automáticos")
if expenses.empty:
    st.sidebar.warning("No se cargó archivo de gastos. Los gastos se calcularán en $0.")
else:
    gastos_preview = expenses[(expenses["Año"] == selected_year) & (expenses["Mes_Num"].isin(months_ytd))].copy()
    st.sidebar.caption(f"Gasto proyectos YTD: {fmt_money(sum(project_expenses.values()))}")
    st.sidebar.caption(f"Gasto tienda YTD: {fmt_money(sum(store_expenses.values()))}")

# Filtros base comparativo
projects_base = projects[projects["Año"].isin(compare_years)].copy()
store_base = store[store["Año"].isin(compare_years)].copy()
projects_year = projects_base[(projects_base["Año"] == selected_year) & (projects_base["Mes_Num"].isin(selected_months))].copy()
store_year = store_base[(store_base["Año"] == selected_year) & (store_base["Mes_Num"].isin(selected_months))].copy()
combined_base = pd.concat([projects_base.assign(Unidad="Proyectos"), store_base.assign(Unidad="Tienda")], ignore_index=True, sort=False)
combined_year = pd.concat([projects_year.assign(Unidad="Proyectos"), store_year.assign(Unidad="Tienda")], ignore_index=True, sort=False)

proj_fc = forecast_block("Proyectos", projects_year, project_expenses, project_monthly_target, months_ytd, multiplier=engineers)
store_fc = forecast_block("Tienda", store_year, store_expenses, store_monthly_target, months_ytd, multiplier=1)
consol_fc = {
    "ventas_ytd": proj_fc["ventas_ytd"] + store_fc["ventas_ytd"],
    "utilidad_bruta_ytd": proj_fc["utilidad_bruta_ytd"] + store_fc["utilidad_bruta_ytd"],
    "gasto_ytd": proj_fc["gasto_ytd"] + store_fc["gasto_ytd"],
    "utilidad_neta_ytd": proj_fc["utilidad_neta_ytd"] + store_fc["utilidad_neta_ytd"],
    "forecast_ventas": proj_fc["forecast_ventas"] + store_fc["forecast_ventas"],
    "forecast_utilidad_bruta": proj_fc["forecast_utilidad_bruta"] + store_fc["forecast_utilidad_bruta"],
    "gasto_anual_proy": proj_fc["gasto_anual_proy"] + store_fc["gasto_anual_proy"],
    "utilidad_neta_proy": proj_fc["utilidad_neta_proy"] + store_fc["utilidad_neta_proy"],
    "meta_anual": proj_fc["meta_anual"] + store_fc["meta_anual"],
}
consol_fc["margen_neto_ytd"] = consol_fc["utilidad_neta_ytd"] / consol_fc["ventas_ytd"] * 100 if consol_fc["ventas_ytd"] else 0
consol_fc["margen_bruto_ytd"] = consol_fc["utilidad_bruta_ytd"] / consol_fc["ventas_ytd"] * 100 if consol_fc["ventas_ytd"] else 0
consol_fc["margen_neto_proy"] = consol_fc["utilidad_neta_proy"] / consol_fc["forecast_ventas"] * 100 if consol_fc["forecast_ventas"] else 0
consol_fc["cumplimiento"] = consol_fc["forecast_ventas"] / consol_fc["meta_anual"] * 100 if consol_fc["meta_anual"] else 0
consol_fc["gap"] = consol_fc["forecast_ventas"] - consol_fc["meta_anual"]
consol_fc["meses_restantes"] = max(12 - len(months_ytd), 0)
consol_fc["venta_req"] = (consol_fc["meta_anual"] - consol_fc["ventas_ytd"]) / consol_fc["meses_restantes"] if consol_fc["meses_restantes"] else 0

# ---------- HEADER ----------
months_label = ", ".join(MONTHS_ES[m] for m in selected_months)
here = Path(__file__).resolve().parent
logo_path = None
for logo_name in ["Logo Interey.png", "Logo_Interey.png", "logo_interey.png", "interey_logo.png"]:
    candidate = here / logo_name
    if candidate.exists():
        logo_path = str(candidate)
        break

st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
hc1, hc2, hc3 = st.columns([1.25, 5.2, 2.0])
with hc1:
    st.markdown('<div class="logo-box-premium">', unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown('<div style="font-weight:900;color:#123E70;font-size:1.4rem;">INTEREY</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with hc2:
    st.markdown('<div class="hero-kicker">INTEREY 360°</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Inteligencia Comercial y Financiera</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Soluciones en Telecomunicaciones y Seguridad</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-pill"><b>Año principal:</b> {selected_year} &nbsp;|&nbsp; <b>Meses analizados:</b> {months_label}</div>', unsafe_allow_html=True)
with hc3:
    st.markdown('<div class="hero-date"><b>Datos actualizados al</b><br><span style="font-size:1.25rem;font-weight:900;color:#0B1F4D;">31 Mayo 2026</span><br><span>Corte fijo: 01/ene/2024 al 31/may/2026</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
radar_interey(consol_fc, proj_fc, store_fc)

# ---------- VISTA EJECUTIVA DINÁMICA ----------
view_selected = st.radio(
    "Selecciona vista",
    ["Resumen Ejecutivo", "Consolidado", "Proyectos", "Tienda", "Ingresos Comprometidos"],
    horizontal=True,
    label_visibility="collapsed",
    key="vista_ejecutiva"
)

if view_selected == "Resumen Ejecutivo":
    render_dynamic_executive_view("Consolidado", consol_fc, "Proyectos + Tienda")
elif view_selected == "Consolidado":
    render_dynamic_executive_view("Consolidado", consol_fc, "Proyectos + Tienda")
elif view_selected == "Proyectos":
    render_dynamic_executive_view("Proyectos", proj_fc, f"{engineers} ing. × {fmt_money(project_monthly_target)} × 12")
elif view_selected == "Tienda":
    render_dynamic_executive_view("Tienda", store_fc, f"{fmt_money(store_monthly_target)} × 12")

# ---------- CONTENIDO DINÁMICO CONTROLADO POR LA VISTA MAESTRA ----------
if view_selected == "Resumen Ejecutivo":
    render_executive_summary(consol_fc, proj_fc, store_fc)
    trend_note("Resumen Ejecutivo no muestra tablas ni gráficas extensas. Para análisis detallado usa Consolidado, Proyectos o Tienda.")

elif view_selected == "Consolidado":
    st.markdown('<div class="section-title">Resultado corporativo</div>', unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=consol_fc["cumplimiento"],
        title={'text': "Cumplimiento proyectado vs meta consolidada"},
        gauge={
            'axis': {'range': [0, 150]},
            'bar': {'color': '#0B1F4D'},
            'steps': [
                {'range':[0,90],'color':'#FEE2E2'},
                {'range':[90,100],'color':'#FEF3C7'},
                {'range':[100,150],'color':'#DCFCE7'}
            ]
        }
    ))
    st.plotly_chart(gauge, use_container_width=True)
    trend_note("Se eliminó el puente de utilidad en esta vista para mantener el consolidado más limpio. La utilidad neta ya se resume en las tarjetas superiores y en el comparativo ejecutivo.")

    st.markdown('<div class="section-title">Evolución mensual consolidada</div>', unsafe_allow_html=True)
    monthly_chart(combined_base, "Ventas mensuales consolidadas", "Ventas_MXN")
    monthly_summary_table(combined_base, "Resumen mensual de ventas consolidadas (MXN)", "Ventas_MXN")

    st.markdown('<div class="section-title">Comparativo Proyectos vs Tienda</div>', unsafe_allow_html=True)
    comp = pd.DataFrame([
        {"Unidad":"Proyectos", "Ventas":proj_fc["ventas_ytd"], "Utilidad bruta":proj_fc["utilidad_bruta_ytd"], "Gastos":proj_fc["gasto_ytd"], "Utilidad neta":proj_fc["utilidad_neta_ytd"]},
        {"Unidad":"Tienda", "Ventas":store_fc["ventas_ytd"], "Utilidad bruta":store_fc["utilidad_bruta_ytd"], "Gastos":store_fc["gasto_ytd"], "Utilidad neta":store_fc["utilidad_neta_ytd"]},
    ])
    comp["Margen bruto %"] = comp["Utilidad bruta"] / comp["Ventas"].replace(0,pd.NA) * 100
    comp["Margen neto %"] = comp["Utilidad neta"] / comp["Ventas"].replace(0,pd.NA) * 100
    comp["Participación ventas %"] = comp["Ventas"] / comp["Ventas"].sum() * 100 if comp["Ventas"].sum() else 0

    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(comp, x="Unidad", y=["Ventas", "Utilidad bruta", "Utilidad neta"], barmode="group", title="Ventas, utilidad bruta y utilidad neta")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(comp, values="Ventas", names="Unidad", hole=.55, title="Participación en ventas")
        st.plotly_chart(fig, use_container_width=True)
    comp_show = comp.copy()
    comp_show["Unidad"] = comp_show["Unidad"].map({"Proyectos": "🔵 Proyectos", "Tienda": "🟢 Tienda"}).fillna(comp_show["Unidad"])
    premium_simple_table(
        comp_show,
        "Comparativo Ejecutivo de Unidades",
        "Lectura rápida de ventas, utilidad, gastos, margen y participación por unidad de negocio.",
        columns=[
            ("Unidad", "Unidad", "text"),
            ("Ventas", "Ventas", "money"),
            ("Utilidad bruta", "Utilidad bruta", "money"),
            ("Gastos", "Gastos", "money"),
            ("Utilidad neta", "Utilidad neta", "money_signed"),
            ("Margen bruto %", "Margen bruto", "pct"),
            ("Margen neto %", "Margen neto", "pct"),
            ("Participación ventas %", "Participación", "pct"),
        ],
        row_class_fn=lambda row, idx: "highlight-row" if "Proyectos" in str(row.get("Unidad","")) else ""
    )

elif view_selected == "Proyectos":
    st.markdown('<div class="section-title">Unidad de negocio: Proyectos</div>', unsafe_allow_html=True)
    trend_note("Esta vista muestra ventas mensuales, conciliación y desempeño comercial del equipo. Orlando Martínez y Ana Margarita Sahagún suman en KPIs corporativos, pero no participan en el comparativo de ingenieros.")

    monthly_chart(projects_base, "Ventas mensuales proyectos", "Ventas_MXN")
    monthly_summary_table(projects_base, "Resumen mensual de ventas proyectos (MXN)", "Ventas_MXN")

    st.markdown('<div class="section-title">Desempeño Comercial del Equipo</div>', unsafe_allow_html=True)
    performance_year = projects_year[~projects_year["Promotor"].fillna("").str.upper().isin(EXCLUDE_FROM_ENGINEER_ANALYSIS)].copy()
    performance_base = projects_base[~projects_base["Promotor"].fillna("").str.upper().isin(EXCLUDE_FROM_ENGINEER_ANALYSIS)].copy()

    if not performance_year.empty:
        prom = performance_year.groupby("Promotor", as_index=False).agg(
            Ventas_MXN=("Ventas_MXN","sum"),
            Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum"),
            Clientes=("Cliente","nunique"),
            Meses_Con_Venta=("Mes_Num","nunique")
        )
        prom["Margen_Bruto_Pct"] = prom["Utilidad_Bruta_MXN"] / prom["Ventas_MXN"].replace(0,pd.NA) * 100
        prom["Meta_YTD"] = project_monthly_target * len(months_ytd)
        prom["Cumplimiento_YTD_Pct"] = prom["Ventas_MXN"] / prom["Meta_YTD"].replace(0,pd.NA) * 100
        prom["Semaforo"] = prom["Cumplimiento_YTD_Pct"].apply(lambda x: "🟢 Cumple" if pd.notna(x) and x >= 100 else ("🟡 Cerca" if pd.notna(x) and x >= 80 else "🔴 Bajo meta"))

        def prom_alert(row):
            issues = []
            if pd.notna(row["Cumplimiento_YTD_Pct"]) and row["Cumplimiento_YTD_Pct"] < 80:
                issues.append("Bajo meta YTD")
            if pd.notna(row["Margen_Bruto_Pct"]) and row["Margen_Bruto_Pct"] < 20:
                issues.append("Margen bajo")
            return ", ".join(issues) if issues else "Sin alerta"

        prom["Alerta"] = prom.apply(prom_alert, axis=1)

        c_rank1, c_rank2 = st.columns([1.05, 1])
        with c_rank1:
            fig = px.bar(
                prom.sort_values("Ventas_MXN"), x="Ventas_MXN", y="Promotor", orientation="h",
                title="Ranking promotores por ventas",
                hover_data=["Utilidad_Bruta_MXN","Margen_Bruto_Pct","Clientes","Cumplimiento_YTD_Pct"]
            )
            st.plotly_chart(fig, use_container_width=True)
        with c_rank2:
            fig = px.scatter(
                prom, x="Ventas_MXN", y="Margen_Bruto_Pct", size="Utilidad_Bruta_MXN", color="Promotor",
                title="Ventas vs margen bruto por promotor",
                hover_data=["Clientes","Cumplimiento_YTD_Pct"]
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-title">Ranking Comercial INTEREY</div>', unsafe_allow_html=True)
        st.caption("Lectura ejecutiva por ingeniero: ventas acumuladas, utilidad bruta, margen y avance contra meta.")
        premium_engineer_table(prom)

        st.markdown('<div class="section-title">Heatmap mensual de cumplimiento por promotor</div>', unsafe_allow_html=True)
        prom_month = performance_base[(performance_base["Año"] == selected_year) & (performance_base["Mes_Num"].isin(months_ytd))].groupby(["Promotor","Mes_Num"], as_index=False).agg(Ventas_MXN=("Ventas_MXN","sum"), Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum"))
        prom_month["Cumplimiento_Pct"] = prom_month["Ventas_MXN"] / project_monthly_target * 100 if project_monthly_target else 0
        prom_month["Mes"] = prom_month["Mes_Num"].map(MONTHS_ES)
        heat_table = prom_month.pivot_table(index="Promotor", columns="Mes", values="Cumplimiento_Pct", aggfunc="mean").reindex(columns=[MONTHS_ES[m] for m in months_ytd])
        if not heat_table.empty:
            fig_heat = px.imshow(
                heat_table.fillna(0),
                labels=dict(x="Mes", y="Promotor", color="% Cumplimiento"),
                color_continuous_scale=[(0.0, "#DC2626"), (0.6, "#F59E0B"), (1.0, "#16A34A")],
                aspect="auto",
                zmin=0,
                zmax=max(float(prom_month["Cumplimiento_Pct"].max()) if not prom_month.empty else 100, 100)
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown('<div class="section-title">Detalle ejecutivo por ingeniero / promotor</div>', unsafe_allow_html=True)
        focus = st.selectbox("Selecciona ingeniero / promotor", sorted(performance_year["Promotor"].dropna().unique().tolist()), key="promotor_detalle_v40")
        focus_year = performance_year[performance_year["Promotor"] == focus].copy()
        f_ventas = focus_year["Ventas_MXN"].sum()
        f_util = focus_year["Utilidad_Bruta_MXN"].sum()
        f_margen = f_util / f_ventas * 100 if f_ventas else 0
        f_meta_ytd = project_monthly_target * len(months_ytd)
        f_cump = f_ventas / f_meta_ytd * 100 if f_meta_ytd else 0
        _, f_cump_style, f_cump_status = status_from_pct(f_cump, green=100, yellow=80)
        cdet = st.columns(5)
        with cdet[0]: st.markdown(card(f"Ventas · {focus}", fmt_money(f_ventas), "acumulado meses seleccionados"), unsafe_allow_html=True)
        with cdet[1]: st.markdown(card("Utilidad bruta", fmt_money(f_util), f"Margen: {fmt_pct(f_margen)}", "green" if f_util >= 0 else "red"), unsafe_allow_html=True)
        with cdet[2]: st.markdown(card("Meta YTD", fmt_money(f_meta_ytd), f"{fmt_money(project_monthly_target)} × {len(months_ytd)} meses", "gray"), unsafe_allow_html=True)
        with cdet[3]: st.markdown(card("Cumplimiento YTD", fmt_pct(f_cump), f"{f_cump_status}", f_cump_style), unsafe_allow_html=True)
        with cdet[4]: st.markdown(card("Diferencia vs meta", fmt_money_signed(f_ventas - f_meta_ytd), "positivo = arriba de meta", "green" if f_ventas >= f_meta_ytd else "red"), unsafe_allow_html=True)

        detail = prom_month[prom_month["Promotor"] == focus].copy().sort_values("Mes_Num")
        detail["Meta_Mensual"] = project_monthly_target
        detail["Diferencia_Meta_MXN"] = detail["Ventas_MXN"] - detail["Meta_Mensual"]
        detail["Estado"] = detail["Cumplimiento_Pct"].apply(lambda x: "Cumplió" if pd.notna(x) and x >= 100 else ("Cerca" if pd.notna(x) and x >= 80 else "No cumplió"))
        cdet_g1, cdet_g2 = st.columns(2)
        with cdet_g1:
            fig_focus = px.line(detail, x="Mes_Num", y="Ventas_MXN", markers=True, title=f"Ventas mensuales · {focus}")
            fig_focus.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1,13)), ticktext=MONTH_ORDER))
            fig_focus.add_hline(y=project_monthly_target, line_dash="dash", line_color="#475569")
            st.plotly_chart(fig_focus, use_container_width=True)
        with cdet_g2:
            fig_focus2 = px.bar(detail, x="Mes", y="Cumplimiento_Pct", title=f"Cumplimiento mensual · {focus}")
            fig_focus2.add_hline(y=100, line_dash="dash", line_color="#475569")
            st.plotly_chart(fig_focus2, use_container_width=True)
        show_detail = detail[["Mes","Ventas_MXN","Utilidad_Bruta_MXN","Meta_Mensual","Diferencia_Meta_MXN","Cumplimiento_Pct","Estado"]].copy()
        premium_simple_table(
            show_detail,
            "Detalle Mensual del Ingeniero Seleccionado",
            "Comparativo mensual contra meta: ventas, utilidad bruta, avance y diferencia.",
            columns=[
                ("Mes", "Mes", "text"),
                ("Ventas_MXN", "Ventas", "money"),
                ("Utilidad_Bruta_MXN", "Utilidad bruta", "money"),
                ("Meta_Mensual", "Meta mensual", "money"),
                ("Diferencia_Meta_MXN", "Diferencia vs meta", "money_signed"),
                ("Cumplimiento_Pct", "Avance", "pct"),
                ("Estado", "Estado", "text"),
            ],
            row_class_fn=lambda row, idx: "highlight-row" if str(row.get("Estado","")) == "Cumplió" else ("warn-row" if str(row.get("Estado","")) == "Cerca" else "risk-row")
        )
    else:
        st.info("No hay datos de ingenieros/promotores comparables para el filtro actual. Los KPIs corporativos de Proyectos sí pueden incluir Orlando Martínez y Ana Margarita Sahagún.")

elif view_selected == "Ingresos Comprometidos":
    render_backlog_view(backlog, project_monthly_target * 12 * engineers)

else:  # Tienda
    st.markdown('<div class="section-title">Unidad de negocio: Tienda</div>', unsafe_allow_html=True)
    trend_note("Esta vista muestra ventas mensuales, conciliación y clientes principales. Tienda usa Total como venta y excluye registros cancelados.")

    monthly_chart(store_base, "Ventas mensuales tienda", "Ventas_MXN")
    monthly_summary_table(store_base, "Resumen mensual de ventas tienda (MXN)", "Ventas_MXN")

    st.markdown('<div class="section-title">Clientes tienda</div>', unsafe_allow_html=True)
    if not store_year.empty:
        cli = store_year.groupby("Cliente", as_index=False).agg(Ventas_MXN=("Ventas_MXN","sum"), Utilidad_Bruta_MXN=("Utilidad_Bruta_MXN","sum"))
        cli["Margen_Bruto_Pct"] = cli["Utilidad_Bruta_MXN"] / cli["Ventas_MXN"].replace(0,pd.NA) * 100
        fig = px.bar(cli.sort_values("Ventas_MXN", ascending=False).head(10).sort_values("Ventas_MXN"), x="Ventas_MXN", y="Cliente", orientation="h", title="Top 10 clientes tienda")
        st.plotly_chart(fig, use_container_width=True)
        cli_show = cli.sort_values("Ventas_MXN", ascending=False).head(25).copy()
        premium_simple_table(
            cli_show,
            "Ranking Ejecutivo de Clientes Tienda",
            "Principales clientes por ventas, utilidad y margen dentro del periodo seleccionado.",
            columns=[
                ("Cliente", "Cliente", "text"),
                ("Ventas_MXN", "Ventas", "money"),
                ("Utilidad_Bruta_MXN", "Utilidad", "money"),
                ("Margen_Bruto_Pct", "Margen", "pct"),
            ],
            row_class_fn=lambda row, idx: "highlight-row" if idx == cli_show.index[0] else ""
        )
    else:
        st.info("No hay datos de tienda para el filtro actual.")

with st.expander("Auditoría avanzada de datos filtrados"):
    st.caption("Se muestran datos ya filtrados por fecha: 01/ene/2024 al 31/may/2026.")
    if view_selected == "Proyectos":
        cols = [c for c in ["Id","Fecha","Año","Mes_Num","Mes","Promotor","Cliente","Descripcion","Moneda","TC","Tipo_Cambio_Aplicado","Cotizado cliente","Ventas_MXN","Utilidad bruta","Utilidad_Bruta_MXN","Margen_Bruto_Pct"] if c in projects.columns]
        st.dataframe(projects[cols].sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
    elif view_selected == "Tienda":
        cols = [c for c in ["Fecha","Año","Mes_Num","Mes","Status","Status_Normalizado","Cliente","Pago","SubTotal","Ventas_MXN","Util $","Utilidad_Bruta_MXN","Margen_Bruto_Pct","Total"] if c in store.columns]
        st.dataframe(store[cols].sort_values("Fecha", ascending=False), use_container_width=True, hide_index=True)
    elif view_selected == "Ingresos Comprometidos":
        if backlog.empty:
            st.info("No hay datos de ingresos comprometidos para auditar.")
        else:
            cols = [c for c in ["Id","Fecha_OC","Dias_Abiertos","Antigüedad","Promotor","Cliente","Descripcion","Moneda","TC","Cotizado cliente","Importe_Pendiente_MXN","Status"] if c in backlog.columns]
            st.dataframe(backlog[cols].sort_values("Dias_Abiertos", ascending=False), use_container_width=True, hide_index=True)
    else:
        cols = [c for c in ["Unidad","Fecha","Año","Mes_Num","Mes","Promotor","Cliente","Ventas_MXN","Utilidad_Bruta_MXN","Margen_Bruto_Pct"] if c in combined_year.columns]
        st.dataframe(combined_year[cols].sort_values(["Unidad","Fecha"], ascending=[True,False]), use_container_width=True, hide_index=True)

with st.expander("ℹ️ Información metodológica"):
    st.markdown("""
    - Corte fijo de información: **01/ene/2024 al 31/may/2026**.
    - Proyectos usa **Cotizado cliente** para ventas y **Utilidad bruta** para utilidad.
    - Las operaciones en USD de Proyectos se convierten con **TC real por operación**.
    - Tienda usa **Total** para ventas y **Util $** para utilidad.
    - Tienda excluye registros con estatus **Cancelado**.
    - Los gastos se leen automáticamente desde el archivo administrativo, separados en **Proyectos** y **Tienda**.
    - Ingresos comprometidos usa el snapshot vigente de proyectos con **OC aprobada**, en ejecución y pendientes de facturar.
    - La antigüedad se calcula desde la fecha de recepción de la OC hasta la fecha actual.
    - El archivo de ingresos comprometidos **reemplaza** el snapshot anterior; no se acumula históricamente.
    """)

st.caption("Versión v51 · Backlog Ejecutivo · Radar de riesgo financiero y concentración · Radar INTEREY 3.0.")
