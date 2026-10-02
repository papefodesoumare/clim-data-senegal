import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import base64

# ══════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CLIM DATA SENEGAL",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  ARRIÈRE-PLAN — motifs végétation + pluie (SVG encodé)
# ══════════════════════════════════════════════════════════════════════
BG_SVG = """
<svg xmlns='http://www.w3.org/2000/svg' width='420' height='420' viewBox='0 0 420 420'>
  <defs>
    <pattern id='leaf' x='0' y='0' width='120' height='120' patternUnits='userSpaceOnUse'>
      <path d='M30 80 Q40 55 60 50 Q50 70 40 80 Q35 85 30 80 Z'
            fill='%230B6E4F' opacity='0.055'/>
      <path d='M90 30 Q100 8 118 4 Q108 24 98 30 Q94 33 90 30 Z'
            fill='%230B6E4F' opacity='0.045'/>
    </pattern>
    <pattern id='rain' x='0' y='0' width='180' height='180' patternUnits='userSpaceOnUse'>
      <line x1='20' y1='10' x2='16' y2='26' stroke='%232E86AB' stroke-width='1.2'
            stroke-linecap='round' opacity='0.10'/>
      <line x1='70' y1='40' x2='66' y2='56' stroke='%232E86AB' stroke-width='1.2'
            stroke-linecap='round' opacity='0.09'/>
      <line x1='130' y1='70' x2='126' y2='86' stroke='%232E86AB' stroke-width='1.2'
            stroke-linecap='round' opacity='0.10'/>
      <line x1='50' y1='120' x2='46' y2='136' stroke='%232E86AB' stroke-width='1.2'
            stroke-linecap='round' opacity='0.09'/>
      <line x1='150' y1='140' x2='146' y2='156' stroke='%232E86AB' stroke-width='1.2'
            stroke-linecap='round' opacity='0.10'/>
    </pattern>
  </defs>
  <rect width='100%' height='100%' fill='url(%23leaf)'/>
  <rect width='100%' height='100%' fill='url(%23rain)'/>
</svg>
"""
BG_DATA = base64.b64encode(BG_SVG.encode("utf-8")).decode("utf-8")
BG_URL = f"data:image/svg+xml;base64,{BG_DATA}"

# ══════════════════════════════════════════════════════════════════════
#  CSS — design sobre, net, professionnel
# ══════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --primary: #0B6E4F;
    --primary-dark: #084D37;
    --primary-soft: #E6F4EF;
    --accent: #C8961E;
    --danger: #B02A37;
    --info: #1F6F9C;
    --bg: #F6F8F7;
    --card: #FFFFFF;
    --text: #1F2A24;
    --muted: #5B6660;
    --border: #E1E6E3;
    --shadow-sm: 0 1px 3px rgba(15,40,30,0.06), 0 1px 2px rgba(15,40,30,0.04);
    --shadow-md: 0 4px 14px rgba(15,40,30,0.08);
    --shadow-lg: 0 10px 28px rgba(15,40,30,0.12);
}}

/* --- Base --- */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
    color: var(--text);
    font-size: 15px;
}}
.stApp {{
    background-color: #F6F8F7;
    background-image: url("{BG_URL}");
    background-repeat: repeat;
    background-attachment: fixed;
    background-size: 420px 420px;
}}
.block-container {{
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1350px;
}}

/* --- En-tête --- */
.clim-header {{
    text-align: center;
    padding: 22px 0 34px 0;
    animation: fadeIn 0.7s ease-out;
}}
.clim-header h1 {{
    color: var(--primary);
    font-weight: 700;
    font-size: 2.35rem;
    letter-spacing: 0.5px;
    margin: 0;
}}
.clim-header p {{
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    margin-top: 10px;
    letter-spacing: 0.2px;
}}
.clim-header .rule {{
    height: 3px;
    width: 110px;
    margin: 18px auto 0 auto;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: 2px;
}}

/* --- Titres de sections --- */
h2, h3 {{
    color: var(--primary) !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
    margin-top: 2.2rem !important;
    margin-bottom: 1rem !important;
    padding: 6px 0 6px 14px;
    border-left: 4px solid var(--accent);
    transition: border-color 0.25s ease, padding-left 0.25s ease;
}}
h2:hover, h3:hover {{
    border-left-color: var(--primary);
    padding-left: 18px;
}}

/* --- Sidebar clair, texte bien lisible --- */
section[data-testid="stSidebar"] {{
    background: #FFFFFF;
    border-right: 1px solid var(--border);
    box-shadow: 2px 0 12px rgba(15,40,30,0.04);
}}
section[data-testid="stSidebar"] * {{
    color: var(--text) !important;
}}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: var(--primary) !important;
    border-left-color: var(--accent) !important;
    background: transparent !important;
    padding-left: 12px !important;
}}
section[data-testid="stSidebar"] label {{
    color: var(--muted) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    transition: all 0.22s ease;
}}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div:hover {{
    border-color: var(--primary) !important;
    box-shadow: 0 4px 12px rgba(11,110,79,0.12);
}}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {{
    color: var(--text) !important;
}}
section[data-testid="stSidebar"] .stSelectbox svg {{
    fill: var(--primary) !important;
}}

/* --- DataFrames --- */
div[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: box-shadow 0.28s ease, transform 0.28s ease;
    background: var(--card);
}}
div[data-testid="stDataFrame"]:hover {{
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}}

/* --- Métriques --- */
div[data-testid="stMetric"] {{
    background: var(--card);
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}}
div[data-testid="stMetric"]::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent 40%, rgba(11,110,79,0.06) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-top-color: var(--primary);
}}
div[data-testid="stMetric"]:hover::after {{
    opacity: 1;
}}
div[data-testid="stMetric"] label {{
    color: var(--muted) !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
    color: var(--primary) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
}}

/* --- Graphiques Plotly --- */
div[data-testid="stPlotlyChart"] {{
    background: var(--card);
    border-radius: 14px;
    padding: 12px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    transition: all 0.32s ease;
}}
div[data-testid="stPlotlyChart"]:hover {{
    box-shadow: var(--shadow-md);
    transform: translateY(-3px);
    border-color: rgba(11,110,79,0.35);
}}

/* --- Carte Folium --- */
iframe[title="streamlit_folium.st_folium"] {{
    border-radius: 14px;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
    transition: all 0.32s ease;
    background: var(--card);
}}
iframe[title="streamlit_folium.st_folium"]:hover {{
    box-shadow: var(--shadow-lg);
    border-color: rgba(11,110,79,0.35);
    transform: translateY(-3px);
}}

/* --- Captions --- */
div[data-testid="stCaptionContainer"] p {{
    color: var(--muted) !important;
    font-style: normal;
    background: var(--primary-soft);
    padding: 9px 14px;
    border-radius: 8px;
    border-left: 3px solid var(--primary);
    font-size: 0.88rem;
}}

/* --- Scrollbar --- */
::-webkit-scrollbar {{ width: 9px; height: 9px; }}
::-webkit-scrollbar-track {{ background: #EEF2F0; }}
::-webkit-scrollbar-thumb {{
    background: #B9C7C1;
    border-radius: 8px;
    border: 2px solid #EEF2F0;
}}
::-webkit-scrollbar-thumb:hover {{
    background: var(--primary);
}}

/* --- Animation d'apparition au scroll --- */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.element-container {{
    animation: fadeIn 0.55s ease-out;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  EN-TÊTE
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="clim-header">
    <h1>CLIM DATA SENEGAL</h1>
    <p>Indice de vulnérabilité climatique des ménages agricoles</p>
    <div class="rule"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  CHARGEMENT DES DONNÉES
# ══════════════════════════════════════════════════════════════════════
df = pd.read_csv("../data/processed/menages_avec_indice_vulnerabilite.csv")
df_climat = pd.read_csv("../data/raw/climat_fictif.csv")
df_ndvi = pd.read_csv("../data/raw/ndvi_fictif.csv")

# ══════════════════════════════════════════════════════════════════════
#  APERÇU DES DONNÉES
# ══════════════════════════════════════════════════════════════════════
st.subheader("Aperçu des données")
st.dataframe(df.head(10), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
#  CARTE DE VULNÉRABILITÉ
# ══════════════════════════════════════════════════════════════════════
st.subheader("Carte de vulnérabilité par région")

vulnerabilite_par_region = (
    df.groupby("region")[["indice_vulnerabilite"]].mean().reset_index()
)
vulnerabilite_par_region["indice_vulnerabilite"] = (
    vulnerabilite_par_region["indice_vulnerabilite"].round(2)
)

coordonnees_regions = {
    "Dakar": (14.6928, -17.4467), "Thies": (14.7833, -16.9167),
    "Diourbel": (14.6521, -16.2340), "Fatick": (14.3390, -16.4110),
    "Kaolack": (14.0167, -16.2500), "Kaffrine": (14.1059, -15.5508),
    "Kolda": (12.8833, -14.9500), "Sedhiou": (12.7081, -15.5569),
    "Ziguinchor": (12.5833, -16.2719), "Louga": (15.6173, -16.2240),
    "Saint-Louis": (16.0179, -16.4896), "Matam": (15.6170, -13.3330),
    "Tambacounda": (13.7707, -13.6673), "Kedougou": (12.5605, -12.1747),
}

carte = folium.Map(
    location=[14.5, -14.5], zoom_start=7,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri"
)

def choisir_couleur(indice):
    if indice >= 0.6:
        return "#B02A37"
    elif indice >= 0.45:
        return "#C8961E"
    return "#0B6E4F"

for index, ligne in vulnerabilite_par_region.iterrows():
    lat, lon = coordonnees_regions[ligne["region"]]
    couleur = choisir_couleur(ligne["indice_vulnerabilite"])
    folium.CircleMarker(
        location=[lat, lon],
        radius=13,
        popup=folium.Popup(
            f"<b>{ligne['region']}</b><br>Indice : {ligne['indice_vulnerabilite']}",
            max_width=200
        ),
        tooltip=f"{ligne['region']} — {ligne['indice_vulnerabilite']}",
        color=couleur,
        weight=2,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.72,
    ).add_to(carte)

st_folium(carte, width=1200, height=500)

# ══════════════════════════════════════════════════════════════════════
#  COMPARAISON DES RÉGIONS
# ══════════════════════════════════════════════════════════════════════
st.subheader("Comparaison des régions")

vulnerabilite_triee = vulnerabilite_par_region.sort_values(
    "indice_vulnerabilite", ascending=False
)

fig = px.bar(
    vulnerabilite_triee,
    x="region",
    y="indice_vulnerabilite",
    color="indice_vulnerabilite",
    color_continuous_scale=["#0B6E4F", "#C8961E", "#B02A37"],
    title="Indice de vulnérabilité moyen par région",
    text="indice_vulnerabilite",
)
fig.update_traces(
    textposition="outside",
    marker_line_width=0,
    hovertemplate="<b>%{x}</b><br>Indice : %{y:.2f}<extra></extra>",
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1F2A24", size=13),
    title_font=dict(size=16, color="#0B6E4F", family="Inter"),
    margin=dict(l=20, r=20, t=60, b=20),
    coloraxis_showscale=False,
    xaxis=dict(showgrid=False, tickangle=-35, title=None),
    yaxis=dict(gridcolor="#EDF1EF", zeroline=False, title=None),
)
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
#  FILTRES (SIDEBAR)
# ══════════════════════════════════════════════════════════════════════
st.sidebar.markdown("### Filtres")
st.sidebar.markdown("---")

liste_regions = ["Toutes les regions"] + sorted(df["region"].unique().tolist())
region_choisie = st.sidebar.selectbox("Choisir une région", liste_regions)

st.sidebar.markdown("---")
st.sidebar.markdown("### Légende")
st.sidebar.markdown("""
<div style="font-size:0.88rem; line-height:1.9; color:#1F2A24;">
  <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
       background:#0B6E4F;margin-right:8px;"></span>Faible — indice &lt; 0.45</div>
  <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
       background:#C8961E;margin-right:8px;"></span>Moyen — 0.45 ≤ indice &lt; 0.6</div>
  <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
       background:#B02A37;margin-right:8px;"></span>Élevé — indice ≥ 0.6</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  DÉTAIL DES MÉNAGES
# ══════════════════════════════════════════════════════════════════════
st.subheader("Détail des ménages")

if region_choisie != "Toutes les regions":
    df_filtre = df[df["region"] == region_choisie]
    st.write(f"Ménages dans la région : **{region_choisie}** — {len(df_filtre)} ménages")
else:
    df_filtre = df
    st.write(f"Tous les ménages — {len(df_filtre)} ménages")

st.dataframe(df_filtre, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Indice moyen", round(df_filtre["indice_vulnerabilite"].mean(), 2))
col2.metric("Revenu moyen (FCFA)", f"{int(df_filtre['revenu_agricole_fcfa'].mean()):,}")
col3.metric("Dépendance à la pluie", f"{int(df_filtre['depend_pluie'].mean() * 100)} %")

# ══════════════════════════════════════════════════════════════════════
#  ÉVOLUTION DE LA PLUVIOMÉTRIE
# ══════════════════════════════════════════════════════════════════════
st.subheader("Évolution de la pluviométrie")

if region_choisie != "Toutes les regions":
    df_climat_filtre = df_climat[df_climat["region"] == region_choisie]
else:
    df_climat_filtre = df_climat[df_climat["region"] == df_climat["region"].unique()[0]]
    st.caption(
        f"Affichage pour {df_climat_filtre['region'].iloc[0]} "
        "(choisissez une région précise pour changer)"
    )

df_climat_filtre = df_climat_filtre.copy()
df_climat_filtre["date"] = pd.to_datetime(
    df_climat_filtre["annee"].astype(str) + "-" + df_climat_filtre["mois"].astype(str)
)
df_climat_filtre = df_climat_filtre.sort_values("date")

fig_climat = px.line(
    df_climat_filtre,
    x="date",
    y="precipitation_mm",
    title="Précipitations mensuelles (2020–2024)",
    markers=True,
)
fig_climat.update_traces(
    line=dict(color="#1F6F9C", width=2.5),
    marker=dict(size=7, color="#0B6E4F", line=dict(width=1.5, color="white")),
    hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f} mm<extra></extra>",
)
fig_climat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1F2A24", size=13),
    title_font=dict(size=16, color="#1F6F9C", family="Inter"),
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(gridcolor="#EDF1EF", zeroline=False, title=None),
    hovermode="x unified",
)
st.plotly_chart(fig_climat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
#  ÉVOLUTION DU NDVI
# ══════════════════════════════════════════════════════════════════════
st.subheader("Évolution de l'indice de végétation (NDVI)")

if region_choisie != "Toutes les regions":
    df_ndvi_filtre = df_ndvi[df_ndvi["region"] == region_choisie]
else:
    df_ndvi_filtre = df_ndvi[df_ndvi["region"] == df_ndvi["region"].unique()[0]]

df_ndvi_filtre = df_ndvi_filtre.copy()
df_ndvi_filtre["date"] = pd.to_datetime(
    df_ndvi_filtre["annee"].astype(str) + "-" + df_ndvi_filtre["mois"].astype(str)
)
df_ndvi_filtre = df_ndvi_filtre.sort_values("date")

fig_ndvi = px.line(
    df_ndvi_filtre,
    x="date",
    y="ndvi",
    title="NDVI mensuel (2020–2024)",
    markers=True,
)
fig_ndvi.update_traces(
    line=dict(color="#0B6E4F", width=2.5),
    marker=dict(size=7, color="#C8961E", line=dict(width=1.5, color="white")),
    hovertemplate="<b>%{x|%b %Y}</b><br>NDVI : %{y:.3f}<extra></extra>",
)
fig_ndvi.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1F2A24", size=13),
    title_font=dict(size=16, color="#0B6E4F", family="Inter"),
    margin=dict(l=20, r=20, t=60, b=20),
    xaxis=dict(showgrid=False, title=None),
    yaxis=dict(gridcolor="#EDF1EF", zeroline=False, title=None),
    hovermode="x unified",
)
st.plotly_chart(fig_ndvi, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════
#  PIED DE PAGE
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding: 40px 0 20px 0; color:#5B6660; font-size:0.85rem;">
    <div style="height:2px; width:60px; margin:0 auto 14px auto;
                background:linear-gradient(90deg,#0B6E4F,#C8961E);
                border-radius:2px;"></div>
    <b style="color:#0B6E4F;">CLIM DATA SENEGAL</b> — Indice de vulnérabilité climatique<br>
    Données 2020–2024
</div>
""", unsafe_allow_html=True)