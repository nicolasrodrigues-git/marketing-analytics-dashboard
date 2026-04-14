import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing · Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;500;600;700&display=swap');

#MainMenu, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: #080A0D; }
[data-testid="stSidebar"] { background: #0D1017; border-right: 1px solid rgba(255,255,255,0.06); }
section[data-testid="stSidebarContent"] { padding: 1.5rem 1rem; }

[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,229,160,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,160,0.015) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none; z-index: 0;
}

html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; color: #E8EDF5; }

[data-testid="stMetricLabel"] {
  font-family: 'DM Mono', monospace !important;
  font-size: 10px !important; letter-spacing: 0.1em !important;
  text-transform: uppercase !important; color: #4A5568 !important;
}
[data-testid="stMetricValue"] {
  font-family: 'DM Mono', monospace !important;
  font-size: 22px !important; font-weight: 500 !important; color: #E8EDF5 !important;
}
[data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace !important; font-size: 10px !important; }

[data-testid="stPlotlyChart"] {
  background: #111520; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px; padding: 4px;
}

[data-testid="stFileUploader"] {
  background: #111520; border: 1px solid rgba(0,229,160,0.2);
  border-radius: 10px; padding: 12px;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #4A5568; border-radius: 2px; }

[data-testid="stSidebar"] label {
  font-family: 'DM Mono', monospace !important;
  font-size: 10px !important; letter-spacing: 0.08em !important;
  text-transform: uppercase !important; color: #4A5568 !important;
}
[data-testid="stSidebar"] .stSlider { accent-color: #00E5A0; }

hr { border-color: rgba(255,255,255,0.06) !important; margin: 0 !important; }

[data-testid="stDownloadButton"] button {
  background: #111520 !important; border: 1px solid rgba(0,229,160,0.3) !important;
  color: #00E5A0 !important; font-family: 'DM Mono', monospace !important;
  font-size: 11px !important; letter-spacing: 0.06em !important;
  border-radius: 6px !important; padding: 6px 16px !important;
}
[data-testid="stDownloadButton"] button:hover {
  background: rgba(0,229,160,0.08) !important; border-color: #00E5A0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ─────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#8896A8", size=11),
    margin=dict(l=12, r=12, t=36, b=12),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
)

ACCENT  = "#00E5A0"
ACCENT2 = "#3D8BFF"
ACCENT3 = "#FF6B6B"
ACCENT4 = "#A78BFA"
ACCENT5 = "#FCD34D"
GRID    = "rgba(255,255,255,0.04)"
CHANNELS = {"Display": ACCENT, "Mobile": ACCENT2, "Video": ACCENT4, "Social": ACCENT5, "Search": ACCENT3}

# ── HELPERS ────────────────────────────────────────────────────────────────────
def fmt_usd(v):
    if abs(v) >= 1_000_000: return f"${v/1_000_000:.1f}M"
    if abs(v) >= 1_000: return f"${v/1_000:.1f}k"
    return f"${v:.2f}"

def fmt_k(v):
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.1f}k"
    return str(int(v))

def card_html(label, value, sub="", accent=False, warn=False):
    color = ACCENT if accent else (ACCENT3 if warn else "#E8EDF5")
    return f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;">
      <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.1em;
                  text-transform:uppercase;color:#4A5568;margin-bottom:8px;">{label}</div>
      <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:500;
                  color:{color};line-height:1;margin-bottom:4px;">{value}</div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#8896A8;">{sub}</div>
    </div>"""

def section_header(title, sub=""):
    st.markdown(f"""
    <div style="padding:20px 24px 12px;">
      <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.14em;
                  text-transform:uppercase;color:#00E5A0;margin-bottom:4px;">◈ {sub if sub else 'ANALYTICS'}</div>
      <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:600;color:#E8EDF5;">{title}</div>
    </div>""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, low_memory=False)
    df.columns = df.columns.str.strip().str.lower()
    return df

@st.cache_data
def process_data(df, ticket_medio, cvr_pct, meta_roas):
    d = df.copy()
    for col in ["media_cost_usd", "clicks", "impressions", "approved_budget"]:
        if col in d.columns:
            d[col] = pd.to_numeric(
                d[col].astype(str).str.replace(",", ".").str.strip().replace("", None),
                errors="coerce"
            )
    cvr = cvr_pct / 100
    d["conversoes"] = d["clicks"].fillna(0) * cvr
    d["receita"]    = d["conversoes"] * ticket_medio
    d["roas"]       = d["receita"] / d["media_cost_usd"].replace(0, None)
    d["cpc"]        = d["media_cost_usd"] / d["clicks"].replace(0, None)
    d["ctr"]        = (d["clicks"] / d["impressions"].replace(0, None)) * 100
    d["cpm"]        = (d["media_cost_usd"] / d["impressions"].replace(0, None)) * 1000
    d["cpa"]        = d["media_cost_usd"] / d["conversoes"].replace(0, None)
    return d

# ── TOPBAR ─────────────────────────────────────────────────────────────────────
def render_topbar(periodo="Mai–Dez 2022"):
    st.markdown(f"""
    <div style="position:sticky;top:0;z-index:100;background:rgba(8,10,13,0.95);
                backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,0.06);
                padding:0 24px;height:52px;display:flex;align-items:center;justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;letter-spacing:.12em;color:#E8EDF5;">
          MARKETING<span style="color:#00E5A0;">ANALYTICS</span>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:10px;padding:3px 8px;
                    border-radius:3px;border:1px solid #00E5A0;color:#00E5A0;letter-spacing:.06em;">CAMPAIGN DATASET</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;font-family:'DM Mono',monospace;font-size:11px;color:#8896A8;">
        <span style="width:6px;height:6px;border-radius:50%;background:#00E5A0;box-shadow:0 0 6px #00E5A0;display:inline-block;"></span>
        {periodo}
      </div>
    </div>""", unsafe_allow_html=True)

# ── BUDGET BAR ─────────────────────────────────────────────────────────────────
def render_budget_bar(gasto, budget):
    pct = min(gasto / budget * 100, 100) if budget else 0
    color = ACCENT3 if pct > 90 else ACCENT
    st.markdown(f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);
                border-radius:8px;padding:12px 20px;margin:0 24px 16px;
                display:flex;align-items:center;gap:16px;">
      <div style="font-family:'DM Mono',monospace;font-size:11px;color:#8896A8;white-space:nowrap;">BUDGET CONSUMIDO</div>
      <div style="flex:1;height:4px;background:rgba(255,255,255,0.06);border-radius:2px;overflow:hidden;">
        <div style="height:100%;width:{pct:.1f}%;background:{color};border-radius:2px;"></div>
      </div>
      <div style="font-family:'DM Mono',monospace;font-size:12px;font-weight:500;color:{color};white-space:nowrap;">{pct:.1f}%</div>
      <div style="font-family:'DM Mono',monospace;font-size:11px;color:#8896A8;white-space:nowrap;">{fmt_usd(gasto)} / {fmt_usd(budget)}</div>
    </div>""", unsafe_allow_html=True)

# ── CHARTS ─────────────────────────────────────────────────────────────────────
def chart_cpc_mensal(df):
    if "time" not in df.columns: return None
    df2 = df.copy()
    df2["time"] = pd.to_datetime(df2["time"], errors="coerce")
    df2 = df2.dropna(subset=["time", "media_cost_usd", "clicks"])
    df2["mes"] = df2["time"].dt.to_period("M").astype(str)
    agg = df2.groupby("mes").apply(lambda x: x["media_cost_usd"].sum() / x["clicks"].sum()).reset_index(name="cpc").sort_values("mes")
    pico_idx = agg["cpc"].idxmax()
    min_idx  = agg["cpc"].idxmin()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=agg["mes"], y=agg["cpc"], mode="lines+markers",
        line=dict(color=ACCENT, width=2),
        marker=dict(size=6, color=[ACCENT3 if i == pico_idx else (ACCENT if i == min_idx else "#4A5568") for i in agg.index], line=dict(width=0)),
        fill="tozeroy", fillcolor="rgba(0,229,160,0.06)",
        hovertemplate="<b>%{x}</b><br>CPC: $%{y:.4f}<extra></extra>",
    ))
    fig.add_annotation(x=agg.loc[pico_idx, "mes"], y=agg.loc[pico_idx, "cpc"],
        text=f"Pico ${agg.loc[pico_idx,'cpc']:.2f}", showarrow=True,
        arrowhead=0, arrowcolor=ACCENT3, font=dict(color=ACCENT3, size=10), ax=0, ay=-30)
    fig.add_annotation(x=agg.loc[min_idx, "mes"], y=agg.loc[min_idx, "cpc"],
        text=f"Mín ${agg.loc[min_idx,'cpc']:.2f}", showarrow=True,
        arrowhead=0, arrowcolor=ACCENT, font=dict(color=ACCENT, size=10), ax=0, ay=30)
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="CPC mensal — evolução Mai–Dez 2022", font=dict(size=11, color="#8896A8"), x=0),
        height=240, xaxis=dict(gridcolor=GRID, zerolinecolor=GRID), yaxis=dict(gridcolor=GRID, zerolinecolor=GRID))
    return fig

def chart_canal_ctr_cpc(df):
    if "channel_name" not in df.columns: return None
    agg = df.groupby("channel_name").agg(ctr=("ctr", "mean"), cpc=("cpc", "mean")).reset_index().dropna()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    cores = [CHANNELS.get(c, ACCENT2) for c in agg["channel_name"]]
    fig.add_trace(go.Bar(
        x=agg["channel_name"], y=agg["ctr"], name="CTR %",
        marker_color=cores, opacity=0.7,
        hovertemplate="<b>%{x}</b><br>CTR: %{y:.2f}%<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=agg["channel_name"], y=agg["cpc"], name="CPC $", mode="lines+markers",
        line=dict(color=ACCENT5, width=2), marker=dict(size=7, color=ACCENT5),
        hovertemplate="<b>%{x}</b><br>CPC: $%{y:.4f}<extra></extra>",
    ), secondary_y=True)
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="CTR × CPC por canal", font=dict(size=11, color="#8896A8"), x=0),
        height=240, yaxis=dict(title="CTR (%)", gridcolor=GRID),
        yaxis2=dict(title="CPC ($)", gridcolor="rgba(0,0,0,0)"))
    return fig

def chart_pareto(df):
    if "campaign_item_id" not in df.columns: return None
    agg = df.groupby("campaign_item_id")["clicks"].sum().reset_index()
    agg = agg.sort_values("clicks", ascending=False).reset_index(drop=True)
    agg["pct_acum"] = agg["clicks"].cumsum() / agg["clicks"].sum() * 100
    agg["rank_pct"] = (agg.index + 1) / len(agg) * 100
    corte_80 = agg[agg["pct_acum"] <= 80].tail(1)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=agg["rank_pct"], y=agg["clicks"],
        marker_color=ACCENT, opacity=0.4, name="Cliques",
        hovertemplate="Top %{x:.0f}% campanhas<br>Cliques: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=agg["rank_pct"], y=agg["pct_acum"], name="% acumulado", yaxis="y2",
        line=dict(color=ACCENT4, width=2),
        hovertemplate="%{x:.0f}% das campanhas → %{y:.1f}% dos cliques<extra></extra>",
    ))
    fig.add_hline(y=80, line_dash="dot", line_color=ACCENT3,
                  annotation_text="80%", annotation_font_color=ACCENT3, yref="y2")
    if not corte_80.empty:
        fig.add_vline(x=corte_80["rank_pct"].values[0], line_dash="dot", line_color=ACCENT3, opacity=0.5)
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Pareto — concentração de cliques por campanha", font=dict(size=11, color="#8896A8"), x=0),
        height=260,
        xaxis=dict(title="% de campanhas (ranking)", gridcolor=GRID),
        yaxis=dict(title="Cliques", gridcolor=GRID),
        yaxis2=dict(title="% acumulado", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)", range=[0, 105]))
    return fig

def chart_weekday(df):
    if "weekday_cat" not in df.columns: return None
    df2 = df.copy()
    df2["periodo"] = df2["weekday_cat"].str.strip().str.lower().apply(
        lambda x: "Weekend" if str(x).startswith(("sat", "sun", "week_end")) else "Weekday")
    agg = df2.groupby("periodo").agg(gasto=("media_cost_usd", "sum"), cliques=("clicks", "mean")).reset_index()
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Gasto total ($)", "Média de cliques"], horizontal_spacing=0.12)
    for i, col in enumerate(["gasto", "cliques"]):
        fig.add_trace(go.Bar(
            x=agg["periodo"], y=agg[col], marker_color=[ACCENT, ACCENT2], opacity=0.8,
            showlegend=False, hovertemplate=f"<b>%{{x}}</b><br>%{{y:,.0f}}<extra></extra>",
        ), row=1, col=i+1)
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Weekday vs Weekend — gasto 5.7× maior, resultado igual", font=dict(size=11, color="#8896A8"), x=0),
        height=220)
    fig.update_annotations(font_size=10, font_color="#8896A8")
    return fig

def chart_setembro_canal(df):
    if "time" not in df.columns or "channel_name" not in df.columns: return None
    df2 = df.copy()
    df2["time"] = pd.to_datetime(df2["time"], errors="coerce")
    df2 = df2.dropna(subset=["time"])
    set_df = df2[df2["time"].dt.month == 9]
    if set_df.empty: return None
    agg = set_df.groupby("channel_name").apply(
        lambda x: x["media_cost_usd"].sum() / x["clicks"].sum()
    ).reset_index(name="cpc_set").sort_values("cpc_set")
    cores = [CHANNELS.get(c, ACCENT2) for c in agg["channel_name"]]
    fig = go.Figure(go.Bar(
        x=agg["cpc_set"], y=agg["channel_name"], orientation="h",
        marker_color=cores, opacity=0.8,
        hovertemplate="<b>%{y}</b><br>CPC set: $%{x:.4f}<extra></extra>",
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="CPC Setembro por canal — janela de oportunidade Mobile", font=dict(size=11, color="#8896A8"), x=0),
        height=220, xaxis_title="CPC ($)",
        xaxis=dict(gridcolor=GRID), yaxis=dict(gridcolor=GRID))
    return fig

def chart_fadiga(df):
    if "no_of_days" not in df.columns: return None
    df2 = df.copy()
    df2["no_of_days"] = pd.to_numeric(df2["no_of_days"], errors="coerce")
    df2 = df2.dropna(subset=["no_of_days"])
    df2["faixa"] = pd.cut(df2["no_of_days"], bins=[0, 7, 15, 9999],
        labels=["Curto\n0–7d", "Médio\n8–15d", "Longo\n+15d"])
    agg = df2.groupby("faixa", observed=True).agg(ctr=("ctr", "mean"), cpc=("cpc", "mean")).reset_index().dropna()
    cores = [ACCENT2, ACCENT, ACCENT3]
    fig = make_subplots(rows=1, cols=2, subplot_titles=["CTR médio (%)", "CPC médio ($)"], horizontal_spacing=0.12)
    for i, col in enumerate(["ctr", "cpc"]):
        fmt = ".2f" if col == "ctr" else ".3f"
        fig.add_trace(go.Bar(
            x=agg["faixa"].astype(str), y=agg[col], marker_color=cores, opacity=0.8,
            showlegend=False, hovertemplate=f"<b>%{{x}}</b><br>%{{y:{fmt}}}<extra></extra>",
        ), row=1, col=i+1)
    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text="Fadiga de criativo — ciclo de vida ideal: 15 dias", font=dict(size=11, color="#8896A8"), x=0),
        height=220)
    fig.update_annotations(font_size=10, font_color="#8896A8")
    return fig

def chart_funil(total_imp, total_clicks, total_conv, total_receita):
    stages = [
        ("Impressões", total_imp, ACCENT2),
        ("Cliques", total_clicks, ACCENT),
        ("Conversões", total_conv, ACCENT4),
        ("Receita $", total_receita, ACCENT5),
    ]
    max_v = total_imp if total_imp > 0 else 1
    html = '<div style="display:flex;flex-direction:column;gap:12px;padding:4px 0;">'
    for label, val, color in stages:
        pct = min(val / max_v * 100, 100)
        fmt = fmt_k(val) if label != "Receita $" else fmt_usd(val)
        html += f"""
        <div style="display:flex;align-items:center;gap:10px;">
          <div style="font-family:'DM Mono',monospace;font-size:10px;color:#8896A8;width:75px;text-align:right;flex-shrink:0;">{label}</div>
          <div style="flex:1;height:30px;background:rgba(255,255,255,0.03);border-radius:4px;overflow:hidden;">
            <div style="height:100%;width:{max(pct,0.5):.1f}%;background:{color}22;border-left:2px solid {color};
                        display:flex;align-items:center;padding-left:8px;">
              <span style="font-family:'DM Mono',monospace;font-size:10px;font-weight:500;color:{color};white-space:nowrap;">{fmt}</span>
            </div>
          </div>
          <div style="font-family:'DM Mono',monospace;font-size:10px;color:#8896A8;width:48px;text-align:right;flex-shrink:0;">{pct:.1f}%</div>
        </div>"""
    html += "</div>"
    return html

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.12em;
                text-transform:uppercase;color:#00E5A0;margin-bottom:16px;">◈ CONFIGURAÇÕES</div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Dataset CSV", type=["csv"],
                                help="Exporte do PostgreSQL: \\COPY marketing_campaign TO 'arquivo.csv' CSV HEADER")
    st.divider()
    ticket = st.number_input("Ticket médio (R$)", min_value=1.0, value=150.0, step=10.0)
    cvr    = st.slider("CVR simulado (%)", 0.5, 10.0, 2.0, 0.1)
    meta   = st.slider("Meta ROAS", 1.0, 15.0, 4.0, 0.5)
    budget = st.number_input("Budget mensal ($)", min_value=1000.0, value=230000.0, step=10000.0)
    st.divider()
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;font-size:9px;color:#4A5568;line-height:1.8;">
    EXPORTAR CSV DO POSTGRES<br><br>
    \\COPY marketing_campaign<br>
    TO 'dados.csv' CSV HEADER
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
render_topbar()

# ── TELA DE BOAS VINDAS ────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:center;
                min-height:70vh;flex-direction:column;gap:24px;padding:40px;text-align:center;">

      <div style="font-family:'DM Mono',monospace;font-size:64px;font-weight:300;
                  color:rgba(0,229,160,0.12);line-height:1;">◈</div>

      <div>
        <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:700;
                    color:#E8EDF5;margin-bottom:8px;">Marketing Analytics</div>
        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#4A5568;letter-spacing:.08em;">
          CAMPAIGN DATASET · MAI–DEZ 2022
        </div>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:520px;width:100%;">
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;">
          <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#00E5A0;">72.6k</div>
          <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-top:4px;">CAMPANHAS</div>
        </div>
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;">
          <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#3D8BFF;">5</div>
          <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-top:4px;">CANAIS</div>
        </div>
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;">
          <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:500;color:#A78BFA;">0.11</div>
          <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-top:4px;">PEARSON</div>
        </div>
      </div>

      <div style="font-family:'DM Mono',monospace;font-size:11px;color:#4A5568;max-width:380px;line-height:1.8;">
        Faça upload do CSV no painel lateral<br>
        <span style="color:#8896A8;">← clique na seta no canto superior esquerdo</span>
      </div>

      <div style="background:rgba(0,229,160,0.04);border:1px solid rgba(0,229,160,0.12);
                  border-radius:10px;padding:16px 24px;max-width:480px;text-align:left;">
        <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.12em;
                    text-transform:uppercase;color:#00E5A0;margin-bottom:10px;">◈ PRINCIPAIS INSIGHTS</div>
        <div style="font-family:'Syne',sans-serif;font-size:13px;color:#8896A8;line-height:1.9;">
          · 10% das campanhas geram 81,7% dos cliques (Pareto)<br>
          · Budget ↑ não garante cliques ↑ (Pearson 0,11)<br>
          · Mobile em set/2022: menor CPC histórico ($0,13)
        </div>
      </div>

    </div>""", unsafe_allow_html=True)
    st.stop()

# ── LOAD & PROCESS ─────────────────────────────────────────────────────────────
df_raw = load_data(uploaded)
df     = process_data(df_raw, ticket, cvr, meta)

total_gasto   = df["media_cost_usd"].sum()
total_cliques = df["clicks"].sum()
total_imp     = df["impressions"].sum()
total_conv    = df["conversoes"].sum()
total_receita = df["receita"].sum()
roas_global   = total_receita / total_gasto if total_gasto else 0
cpa_medio     = total_gasto / total_conv if total_conv else 0
ctr_medio     = (total_cliques / total_imp * 100) if total_imp else 0
corr_val      = df[["approved_budget", "clicks"]].dropna().corr().iloc[0, 1] if "approved_budget" in df.columns else None

# ══════════════════════════════════════════════════════════════════════════════
# PRIMEIRA DOBRA
# ══════════════════════════════════════════════════════════════════════════════
section_header("Visão Executiva", "PRIMEIRA DOBRA · FINANCEIRO")
render_budget_bar(total_gasto, budget)

st.markdown('<div style="padding:0 24px 16px;">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5, gap="small")
roas_ok = roas_global >= meta
with c1: st.markdown(card_html("Investimento Total", fmt_usd(total_gasto), f"{total_gasto/budget*100:.1f}% do budget", accent=True), unsafe_allow_html=True)
with c2: st.markdown(card_html("ROAS Global", f"{roas_global:.2f}x", f"{'↑' if roas_ok else '↓'} meta {meta:.1f}x", accent=roas_ok, warn=not roas_ok), unsafe_allow_html=True)
with c3: st.markdown(card_html("Receita Estimada", fmt_usd(total_receita), f"Ticket R${ticket:.0f} · CVR {cvr:.1f}%"), unsafe_allow_html=True)
with c4: st.markdown(card_html("CPA Médio", fmt_usd(cpa_medio), "custo por conversão"), unsafe_allow_html=True)
with c5:
    corr_txt = f"Pearson {corr_val:.4f}" if corr_val is not None else "—"
    st.markdown(card_html("Correlação Budget×Clicks", f"{corr_val:.2f}" if corr_val is not None else "—", corr_txt, warn=(corr_val is not None and abs(corr_val) < 0.3)), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="padding:0 24px 16px;">', unsafe_allow_html=True)
col_big1, col_big2, col_big3 = st.columns([1, 1, 1], gap="small")

with col_big1:
    st.markdown(f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:18px;height:260px;">
      <div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8896A8;margin-bottom:14px;">CONVERSÕES ESTIMADAS</div>
      <div style="font-family:'DM Mono',monospace;font-size:52px;font-weight:300;color:#E8EDF5;line-height:1;">{fmt_k(total_conv)}</div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#00E5A0;letter-spacing:.15em;text-transform:uppercase;margin-top:8px;">CVR {cvr:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with col_big2:
    st.markdown(f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:18px;height:260px;">
      <div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8896A8;margin-bottom:14px;">ALCANCE</div>
      <div style="font-family:'DM Mono',monospace;font-size:42px;font-weight:300;color:#E8EDF5;line-height:1;">{fmt_k(total_imp)}</div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#00E5A0;letter-spacing:.12em;text-transform:uppercase;margin-bottom:16px;">IMPRESSÕES TOTAL</div>
      <div style="display:flex;align-items:baseline;gap:8px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);">
        <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:300;">{ctr_medio:.2f}%</div>
        <div style="font-family:'DM Mono',monospace;font-size:10px;color:#8896A8;letter-spacing:.08em;">CTR MÉDIO GLOBAL</div>
      </div>
    </div>""", unsafe_allow_html=True)

with col_big3:
    funil_html = chart_funil(total_imp, total_cliques, total_conv, total_receita)
    st.markdown(f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:18px;height:260px;">
      <div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8896A8;margin-bottom:14px;">FUNIL DE CONVERSÃO</div>
      {funil_html}
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEGUNDA DOBRA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:0 24px;"><hr style="border-color:rgba(255,255,255,0.06);"></div>', unsafe_allow_html=True)
section_header("Análise Operacional", "SEGUNDA DOBRA · EFICIÊNCIA DE CANAIS")
st.markdown('<div style="padding:0 24px 16px;">', unsafe_allow_html=True)

r1c1, r1c2 = st.columns([3, 2], gap="small")
with r1c1:
    fig = chart_cpc_mensal(df)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with r1c2:
    fig = chart_canal_ctr_cpc(df)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

fig = chart_pareto(df)
if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

r3c1, r3c2, r3c3 = st.columns(3, gap="small")
with r3c1:
    fig = chart_weekday(df)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with r3c2:
    fig = chart_setembro_canal(df)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with r3c3:
    fig = chart_fadiga(df)
    if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"""
<div style="background:#111520;border:1px solid rgba(0,229,160,0.15);border-radius:10px;padding:18px;margin-top:4px;">
  <div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:#00E5A0;margin-bottom:12px;">◈ CONCLUSÕES ESTRATÉGICAS</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
    <div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-bottom:4px;">PARETO</div>
      <div style="font-family:'Syne',sans-serif;font-size:13px;color:#E8EDF5;line-height:1.6;">
        10% das campanhas geram 81,7% dos cliques. Foco nos vencedores, não no volume.
      </div>
    </div>
    <div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-bottom:4px;">CORRELAÇÃO</div>
      <div style="font-family:'Syne',sans-serif;font-size:13px;color:#E8EDF5;line-height:1.6;">
        Budget ↑ não garante cliques ↑ (Pearson {f"{corr_val:.2f}" if corr_val else "~0.11"}).
        Qualidade do criativo manda mais.
      </div>
    </div>
    <div>
      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;margin-bottom:4px;">OPORTUNIDADE</div>
      <div style="font-family:'Syne',sans-serif;font-size:13px;color:#E8EDF5;line-height:1.6;">
        Mobile em setembro: $0,13/clique. Weekend 5,7× mais barato com mesmo resultado.
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:0 24px;"><hr style="border-color:rgba(255,255,255,0.06);margin:8px 0;"></div>', unsafe_allow_html=True)
st.markdown('<div style="padding:0 24px 16px;">', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:.12em;
            text-transform:uppercase;color:#4A5568;margin-bottom:12px;padding-top:8px;">
◈ DADOS BRUTOS — DOWNLOAD
</div>""", unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns(4, gap="small")
with fc1:
    st.download_button("⬇ Dataset completo", df_raw.to_csv(index=False).encode("utf-8"), "marketing_campaign_raw.csv", "text/csv")
with fc2:
    agg_canal = df.groupby("channel_name").agg(
        gasto=("media_cost_usd", "sum"), cliques=("clicks", "sum"),
        impressoes=("impressions", "sum"), ctr_medio=("ctr", "mean"),
        cpc_medio=("cpc", "mean"), conversoes=("conversoes", "sum"), receita=("receita", "sum"),
    ).reset_index() if "channel_name" in df.columns else pd.DataFrame()
    if not agg_canal.empty:
        st.download_button("⬇ Resumo por canal", agg_canal.to_csv(index=False).encode("utf-8"), "resumo_canal.csv", "text/csv")
with fc3:
    if "campaign_item_id" in df.columns:
        agg_camp = df.groupby("campaign_item_id").agg(
            gasto=("media_cost_usd", "sum"), cliques=("clicks", "sum"),
            ctr=("ctr", "mean"), cpc=("cpc", "mean"),
        ).reset_index().sort_values("cliques", ascending=False)
        st.download_button("⬇ Top campanhas", agg_camp.to_csv(index=False).encode("utf-8"), "top_campanhas.csv", "text/csv")

st.markdown(f"""
<div style="font-family:'DM Mono',monospace;font-size:10px;color:#4A5568;padding:16px 0 8px;line-height:2;">
  Marketing Campaign Dataset · {len(df_raw):,} registros · 35 colunas · Mai–Dez 2022<br>
  Ticket médio simulado: R${ticket:.0f} · CVR: {cvr:.1f}% · Meta ROAS: {meta:.1f}x
</div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
