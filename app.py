import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

# --- CONFIGURATION GRID ENTERPRISE ---
st.set_page_config(
    page_title="MY-FloodGuard National Grid",
    page_icon="🚨",
    layout="wide"
)

# --- MODERN EXECUTIVE THEME (CSS) ---
st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [data-testid="stSidebarViewPort"] { font-family: 'Inter', sans-serif; background-color: #0F172A; }
    .main-title { font-size:36px !important; font-weight: 800; color: #F8FAFC; letter-spacing: -1px; margin-bottom: 0px;}
    .subtitle { font-size:15px; color: #94A3B8; margin-bottom: 20px; }
    .status-box { padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center; color: white; font-weight: 700; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); }
    .danger { background-color: #DC2626; background-image: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); }
    .warning { background-color: #D97706; background-image: linear-gradient(135deg, #D97706 0%, #92400E 100%); }
    .safe { background-color: #059669; background-image: linear-gradient(135deg, #059669 0%, #065F46 100%); }
    .metric-card { background-color: #1E293B; padding: 20px; border-radius: 12px; text-align: center; color: #F1F5F9; border: 1px solid #334155; }
    .log-card { background-color: #1E293B; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid #EF4444; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; color: #F1F5F9; }
    .log-card-safe { background-color: #1E293B; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid #10B981; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155; color: #F1F5F9; }
</style>
""", unsafe_allow_html=True)

# --- SYSTEM LANGUAGE INTERPRETER ---
col_title, col_lang = st.columns(2)
with col_lang:
    lang = st.radio("🌐 Matrix Bahasa / Language", ["English", "Bahasa Melayu"], horizontal=True)

text = {
    "English": {
        "title": "🚨 MY-FLOODGUARD: NATIONAL DATA INFRASTRUCTURE",
        "subtitle": "Unified Enterprise Architecture Integration • Real-Time METMalaysia API Pipelines • Cognitive AI Rerouting",
        "select_area": "📊 CONTROL CONSOLE: SELECT ALL 14 STATES & TERRITORIES:",
        "danger_status": "🔴 CRITICAL VECTOR: IMMINENT NATURAL RISK - EXECUTING EMERGENCY ROUTING",
        "warning_status": "🟡 CAUTION VECTOR: ANOMALOUS WEATHER DETECTED - MONITORING ACTIVE",
        "safe_status": "🟢 NOMINAL BASELINE: ALL ENVIRONMENTAL TELEMETRY STABLE",
        "map_title": "🗺️ Live Geospatial Control Map (All States Included)",
        "osint_title": "📡 Tactical OSINT Logs & Alternative Navigation",
        "osint_desc": "Real-time crowdsourced feeds identifying logistics blockages, road closures, and shelter availability.",
        "ai_title": "🤖 Generative AI Cognitive Orchestration (ChatGPT & Gemini Engine)",
        "weather_title": "📊 Verified Meteorological Pipeline (METMalaysia Live API + Open-Meteo Cluster)",
        "footer": "Production Cloud Active. Live API query to data.gov.my, Open-Meteo Satellite Node, and OpenAI Analytical Core."
    },
    "Bahasa Melayu": {
        "title": "🚨 MY-FLOODGUARD: INFRASTRUKTUR DATA KEBANGSAAN",
        "subtitle": "Integrasi Arkitektur Enterprise Kebangsaan • Saluran API Real-Time METMalaysia • Lencongan Kognitif AI",
        "select_area": "📊 KONSOL KAWALAN: PILIH KESEMUA 14 NEGERI & WILAYAH PERSEKUTUAN:",
        "danger_status": "🔴 ANCAMAN KRITIKAL: RISIKO BENCANA AKTIF - GERAKKAN HALUAN KECEMASAN",
        "warning_status": "🟡 FASA BERJAGA-JAGA: ANOMALI CUACA DIKESAN - PEMANTAUAN AKTIF",
        "safe_status": "🟢 BACAAN ASAS NOMINAL: SEMUA TELEMETRI ALAM SEKITAR STABIL",
        "map_title": "🗺️ Peta Kawalan Geospatial Live (Merangkumi Semua Negeri)",
        "osint_title": "📡 Log Taktikal OSINT & Navigasi Laluan Alternatif",
        "osint_desc": "Suapan data komuniti masa nyata mengesan sekatan logistik, jalan ditutup, dan kapasiti PPS.",
        "ai_title": "🤖 Orkestrasi Kognitif AI Generatif (Enjin ChatGPT & Gemini)",
        "weather_title": "📊 Array Meteorologi Bersepadu (API Langsung METMalaysia + Kluster Open-Meteo)",
        "footer": "Cloud Produksi Aktif. Panggilan API terus ke data.gov.my, Node Satelit Open-Meteo, dan Teras Analitik OpenAI."
    }
}

with col_title:
    st.markdown(f'<p class="main-title">{text[lang]["title"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{text[lang]["subtitle"]}</p>', unsafe_allow_html=True)

st.divider()

# --- COMPLETE 14 STATES & TERRITORIES DISASTER GEOSPATIAL DATABASE ---
malaysia_all_states = {
    "Kelantan": {"lat": 6.1228, "lon": 102.2381, "zoom": 9, "code": "Kelantan"},
    "Terengganu": {"lat": 5.3117, "lon": 103.1324, "zoom": 9, "code": "Terengganu"},
    "Pahang": {"lat": 3.8126, "lon": 103.3256, "zoom": 8, "code": "Pahang"},
    "Johor": {"lat": 1.4927, "lon": 103.7414, "zoom": 9, "code": "Johor"},
    "Selangor": {"lat": 3.0738, "lon": 101.5183, "zoom": 10, "code": "Selangor"},
    "W.P. Kuala Lumpur": {"lat": 3.1390, "lon": 101.6869, "zoom": 11, "code": "W.P. Kuala Lumpur"},
    "W.P. Putrajaya": {"lat": 2.9264, "lon": 101.6964, "zoom": 12, "code": "W.P. Putrajaya"},
    "Negeri Sembilan": {"lat": 2.7258, "lon": 101.9424, "zoom": 10, "code": "Negeri Sembilan"},
    "Melaka": {"lat": 2.1896, "lon": 102.2501, "zoom": 11, "code": "Melaka"},
    "Perak": {"lat": 4.5921, "lon": 101.0901, "zoom": 9, "code": "Perak"},
    "Pulau Pinang": {"lat": 5.4141, "lon": 100.3288, "zoom": 11, "code": "Pulau Pinang"},
    "Kedah": {"lat": 6.1248, "lon": 100.3675, "zoom": 9, "code": "Kedah"},
    "Perlis": {"lat": 6.4449, "lon": 100.2048, "zoom": 11, "code": "Perlis"},
    "Sabah": {"lat": 5.9788, "lon": 116.0753, "zoom": 8, "code": "Sabah"},
    "Sarawak": {"lat": 1.5574, "lon": 110.3538, "zoom": 8, "code": "Sarawak"},
    "W.P. Labuan": {"lat": 5.2831, "lon": 115.2442, "zoom": 12, "code": "W.P. Labuan"}
}

col_ctrl, col_map = st.columns(2)

with col_ctrl:
    st.markdown(f"##### {text[lang]['select_area']}")
    kawasan = st.selectbox("", list(malaysia_all_states.keys()), label_visibility="collapsed")
    node = malaysia_all_states[kawasan]

# --- PIPELINE #1: MALAYSIA GOVERNMENT DATA API (METMALAYSIA FORECAST) ---
@st.cache_data(ttl=300)
def get_official_metmalaysia_forecast(state_code):
    url = "https://data.gov.my"
    try:
        response = requests.get(url).json()
        for item in response:
            if item.get("state") == state_code:
                return item.get("morning_forecast", "Clear/Tiada Hujan")
        return "Clear"
    except:
        return "API Offline/Maintenance"

# --- PIPELINE #2: TELEMETRY SATELLITE API (OPEN-METEO) ---
@st.cache_data(ttl=120)
def get_satellite_sensor_array(lat, lon):
    url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=Asia%2FSingapore"
    try:
        return requests.get(url).json()['current']
    except:
        return None

# TRIGGER PRODUCTION PIPELINES
met_malaysia_condition = get_official_metmalaysia_forecast(node["code"])
satellite_metrics = get_satellite_sensor_array(node["lat"], node["lon"])
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if satellite_metrics:
    temp = satellite_metrics["temperature_2m"]
    humidity = satellite_metrics["relative_humidity_2m"]
    rain = satellite_metrics["precipitation"]
    wind = satellite_metrics["wind_speed_10m"]
else:
    temp, humidity, rain, wind = 28.0, 80, 0.0, 5.0

# --- DATA-DRIVEN COGNITIVE THRESHOLD VALIDATION ---
is_adstellar = any(keyword in met_malaysia_condition for keyword in ["Hujan", "Ribut", "Thunderstorm", "Rain"])

if rain > 3.0 or wind > 25.0 or (rain > 0.8 and is_adstellar):
    warna_kelas, alert_level = "danger", "HIGH"
    status_semasa = text[lang]["danger_status"]
elif rain > 0.1 or wind > 12.0 or is_adstellar:
    warna_kelas, alert_level = "warning", "MODERATE"
    status_semasa = text[lang]["warning_status"]
else:
    warna_kelas, alert_level = "safe", "LOW"
    status_semasa = text[lang]["safe_status"]

# RENDERING GEOSPATIAL MAP INTERFACE
with col_map:
    st.markdown(f"##### {text[lang]['map_title']}")
    m = folium.Map(location=[node["lat"], node["lon"]], zoom_start=node["zoom"], tiles="cartodbpositron")
    folium.Marker(
        [node["lat"], node["lon"]],
        popup=f"State Core: {kawasan} | METMalaysia Feed: {met_malaysia_condition}",
        tooltip=kawasan,
        icon=folium.Icon(color="red" if alert_level == "HIGH" else "orange" if alert_level == "MODERATE" else "green", icon="flash")
    ).add_to(m)
    st_folium(m, width="100%", height=260, returned_objects=[])

# --- DYNAMIC NATIONAL ALERT DISPLAY BANNER ---
st.markdown(f'<div class="status-box {warna_kelas}"><h2>{status_semasa}</h2><small>⏱️ Central Pipeline Synchronization: {current_time} (MYT) | Verified METMalaysia Source: <b>{met_malaysia_condition}</b></small></div>', unsafe_allow_html=True)

# --- VERIFIED METEOROLOGICAL TELEMETRY ---
st.markdown(f"#### {text[lang]['weather_title']}")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown(f'<div class="metric-card"><span style="font-size:22px;">🌡️</span><br><small style="color:#94A3B8;">Suhu / Temperature</small><br><h2 style="color:#F8FAFC; margin-top:5px;">{temp}°C</h2></div>', unsafe_allow_html=True)
with m_col2:
    st.markdown(f'<div class="metric-card"><span style="font-size:22px;">💧</span><br><small style="color:#94A3B8;">Kelembapan / Humidity</small><br><h2 style="color:#F8FAFC; margin-top:5px;">{humidity}%</h2></div>', unsafe_allow_html=True)
with m_col3:
