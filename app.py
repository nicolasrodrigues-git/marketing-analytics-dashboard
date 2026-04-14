import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing · Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS (Sua Identidade Visual Preservada) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;500;600;700&display=swap');
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: #080A0D; }
[data-testid="stSidebar"] { background: #0D1017; border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stAppViewContainer"]::before {
  content: ''; position: fixed; inset: 0;
  background-image: linear-gradient(rgba(0,229,160,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(0,229,160,0.015) 1px, transparent 1px);
  background-size: 48px 48px; pointer-events: none; z-index: 0;
}
html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; color: #E8EDF5; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 22px !important; color: #E8EDF5 !important; }
[data-testid="stPlotlyChart"] { background: #111520; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ─────────────────────────────────────────────────────────────────
ACCENT, ACCENT2, ACCENT3, ACCENT4, ACCENT5 = "#00E5A0", "#3D8BFF", "#FF6B6B", "#A78BFA", "#FCD34D"
GRID = "rgba(255,255,255,0.04)"
CHANNELS = {"Display": ACCENT, "Mobile": ACCENT2, "Video": ACCENT4, "Social": ACCENT5, "Search": ACCENT3}
DEFAULT_PATH = "data/marketing_raw.csv"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#8896A8", size=11),
    margin=dict(l=12, r=12, t=36, b=12),
)

# ── HELPERS ────────────────────────────────────────────────────────────────────
def fmt_usd(v):
    if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.1f}k"
    return f"${v:.2f}"

def fmt_k(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 1e3: return f"{v/1e3:.1f}k"
    return str(int(v))

def card_html(label, value, sub="", accent=False, warn=False):
    color = ACCENT if accent else (ACCENT3 if warn else "#E8EDF5")
    return f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;">
      <div style="font-family:'DM Mono';font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#4A5568;margin-bottom:8px;">{label}</div>
      <div style="font-family:'DM Mono';font-size:22px;font-weight:500;color:{color};line-height:1;margin-bottom:4px;">{value}</div>
      <div style="font-family:'DM Mono';font-size:10px;color:#8896A8;">{sub}</div>
    </div>"""

# ── LOAD & PROCESS ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file, low_memory=False)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

@st.cache_data
def process_data(df, ticket_medio, cvr_pct):
    if df.empty: return df
    d = df.copy()
    # Conversão numérica robusta
    for col in ["media_cost_usd", "clicks", "impressions", "approved_budget"]:
        if col in d.columns:
            d[col] = pd.to_numeric(d[col].astype(str).str.replace(",", ".").str.strip(), errors="coerce").fillna(0)
    
    cvr = cvr_pct / 100
    d["conversoes"] = d["clicks"] * cvr
    d["receita"]    = d["conversoes"] * ticket_medio
    # Evitando divisão por zero
    d["roas"] = np.where(d["media_cost_usd"] > 0, d["receita"] / d["media_cost_usd"], 0)
    d["cpc"]  = np.where(d["clicks"] > 0, d["media_cost_usd"] / d["clicks"], 0)
    d["ctr"]  = np.where(d["impressions"] > 0, (d["clicks"] / d["impressions"]) * 100, 0)
    return d

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='color:#00E5A0; font-size:10px; letter-spacing:0.1em;'>◈ CONFIGURAÇÕES</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Dataset CSV", type=["csv"])
    st.divider()
    ticket = st.number_input("Ticket médio (R$)", value=150.0, step=10.0)
    cvr_val = st.slider("CVR simulado (%)", 0.5, 10.0, 2.0, 0.1)
    meta_roas = st.slider("Meta ROAS", 1.0, 15.0, 4.0, 0.5)
    budget_goal = st.number_input("Budget mensal ($)", value=230000.0, step=1000.0)

# ── LÓGICA DE DADOS (CSV FIXO OU UPLOAD) ───────────────────────────────────────
if uploaded is not None:
    df_raw = load_data(uploaded)
else:
    if os.path.exists(DEFAULT_PATH):
        st.info("Using sample dataset. Upload your own CSV to customize the analysis.")
        df_raw = load_data(DEFAULT_PATH)
    else:
        st.error(f"Arquivo padrão não encontrado em: {DEFAULT_PATH}")
        st.stop()

# ── RENDERIZAÇÃO ───────────────────────────────────────────────────────────────
if not df_raw.empty:
    df = process_data(df_raw, ticket, cvr_val)
    
    # Métricas Principais
    total_gasto = df["media_cost_usd"].sum()
    total_cliques = df["clicks"].sum()
    total_conv = df["conversoes"].sum()
    total_receita = df["receita"].sum()
    roas_global = total_receita / total_gasto if total_gasto > 0 else 0
    
    # Cabeçalho e Barra de Budget
    st.markdown(f"""
    <div style="padding:10px 24px; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:20px;">
        <span style="font-family:'Syne'; font-weight:700; font-size:14px;">MARKETING<span style="color:#00E5A0;">ANALYTICS</span></span>
    </div>""", unsafe_allow_html=True)

    # Gráfico de progresso do Budget
    pct_budget = min(total_gasto / budget_goal * 100, 100)
    color_b = ACCENT3 if pct_budget > 90 else ACCENT
    st.markdown(f"""
    <div style="background:#111520; border-radius:8px; padding:15px 24px; margin: 0 24px 20px; border: 1px solid rgba(255,255,255,0.05);">
        <div style="display:flex; justify-content:space-between; font-family:'DM Mono'; font-size:11px; color:#8896A8; margin-bottom:8px;">
            <span>BUDGET CONSUMIDO</span>
            <span>{pct_budget:.1f}% — {fmt_usd(total_gasto)} / {fmt_usd(budget_goal)}</span>
        </div>
        <div style="width:100%; height:4px; background:rgba(255,255,255,0.06); border-radius:2px;">
            <div style="width:{pct_budget}%; height:100%; background:{color_b}; border-radius:2px;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Grid de Cards
    st.markdown('<div style="padding:0 24px;">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(card_html("Investimento", fmt_usd(total_gasto), accent=True), unsafe_allow_html=True)
    with c2: st.markdown(card_html("ROAS Global", f"{roas_global:.2f}x", f"Meta: {meta_roas}x", warn=roas_global < meta_roas), unsafe_allow_html=True)
    with c3: st.markdown(card_html("Receita Est.", fmt_usd(total_receita)), unsafe_allow_html=True)
    with c4: st.markdown(card_html("Conversões", fmt_k(total_conv)), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Aqui você pode continuar colando as funções de gráficos (chart_cpc_mensal, etc) ---
    st.success("Análise carregada com sucesso!")
else:
    st.warning("O dataset está vazio ou não pôde ser processado.")
