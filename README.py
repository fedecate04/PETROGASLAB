# LTS LAB ANALYZER - VERSIÓN PROFESIONAL PEDAGÓGICA
# LTS LAB ANALYZER - APP COMPLETA CON PESTAÑAS Y ESTILO PROFESIONAL

import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
import os

# CONFIGURACIÓN
st.set_page_config(page_title="LTS Lab Analyzer", layout="wide")
LOGO_PATH = "logopetrogas.png"

# ESTILO OSCURO Y PERSONALIZADO
st.markdown("""
    <style>
        .stApp { background-color: #1e1e1e; color: white; }
        .stButton>button, .stDownloadButton>button {
            background-color: #0d6efd;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        input, textarea, .stTextInput, .stTextArea, .stNumberInput input {
            background-color: #2e2e2e !important;
            color: white !important;
            border: 1px solid #555 !important;
        }
        .stSelectbox div, .stNumberInput input {
            background-color: #2e2e2e !important;
            color: white !important;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# LOGO CENTRADO
st.markdown("<div style='text-align:center;'><img src='logopetrogas.png' width='200'/></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>🧪 LTS Lab Analyzer</h2>", unsafe_allow_html=True)
st.markdown("Aplicación profesional y pedagógica para análisis de laboratorio en plantas LTS.", unsafe_allow_html=True)

# PDF UTILIDAD
class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 33)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "INFORME DE ANÁLISIS DE LABORATORIO", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, "R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Confidencial - Uso interno PETROGAS", 0, 0, "C")

    def add_section(self, title, content):
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, title, 0, 1)
        self.set_font("Arial", "", 10)
        if isinstance(content, dict):
            for k, v in content.items():
                self.cell(0, 8, f"{k}: {v}", 0, 1)
        else:
            self.multi_cell(0, 8, str(content))
        self.ln(2)

def exportar_pdf(nombre, operador, explicacion, resultados, observaciones):
    pdf = PDF()
    pdf.add_page()
    pdf.add_section("Operador", operador)
    pdf.add_section("Explicación técnica", explicacion)
    pdf.add_section("Resultados", resultados)
    pdf.add_section("Observaciones", observaciones or "Sin observaciones.")
    output = pdf.output(dest='S').encode('latin-1', errors='ignore')
    st.download_button("⬇️ Descargar informe PDF", data=BytesIO(output), file_name=nombre, mime="application/pdf")

# PESTAÑAS PARA LOS MÓDULOS
tabs = st.tabs(["Gas Natural", "Gasolina Estabilizada", "MEG", "TEG", "Agua Desmineralizada", "Aminas"])

# GAS NATURAL
with tabs[0]:
    st.subheader("🔥 Análisis de Gas Natural")
    st.markdown("Evaluación de gases ácidos H₂S y CO₂ para control de corrosión y cumplimiento normativo.")
    st.latex("H_2S \\leq 2.1\\ ppm \\quad\\quad CO_2 \\leq 2\\ \\%")
    h2s = st.number_input("H₂S (ppm)", 0.0, step=0.1)
    co2 = st.number_input("CO₂ (%)", 0.0, step=0.1)
    operador = st.text_input("👤 Operador", key="op_gas")
    obs = st.text_area("📝 Observaciones", key="obs_gas")
    if st.button("📊 Analizar Gas"):
        resultados = {
            "H₂S (ppm)": f"{h2s} - {'✅' if h2s <= 2.1 else '❌'}",
            "CO₂ (%)": f"{co2} - {'✅' if co2 <= 2 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"GasNatural_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Evaluación de H₂S y CO₂ en gas tratado.", resultados, obs)

# GASOLINA
with tabs[1]:
    st.subheader("⛽ Análisis de Gasolina Estabilizada")
    tvr = st.number_input("TVR (psia)", 0.0, step=0.1)
    sales = st.number_input("Sales (mg/m²)", 0.0, step=0.1)
    agua = st.number_input("Agua y sedimentos (%)", 0.0, step=0.1)
    operador = st.text_input("👤 Operador", key="op_gasolina")
    obs = st.text_area("📝 Observaciones", key="obs_gasolina")
    if st.button("📊 Analizar Gasolina"):
        resultados = {
            "TVR": f"{tvr} - {'✅' if tvr <= 12 else '❌'}",
            "Sales": f"{sales} - {'✅' if sales <= 100 else '❌'}",
            "Agua y sedimentos": f"{agua} - {'✅' if agua <= 1 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"Gasolina_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Evaluación de TVR, sales y sedimentos en gasolina estabilizada.", resultados, obs)

# MEG
with tabs[2]:
    st.subheader("🧪 Análisis de MEG")
    ph = st.number_input("pH", 0.0, 14.0, step=0.01)
    conc = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1)
    cl = st.number_input("Cloruros (ppm)", 0.0, step=0.1)
    operador = st.text_input("👤 Operador", key="op_meg")
    obs = st.text_area("📝 Observaciones", key="obs_meg")
    if st.button("📊 Analizar MEG"):
        resultados = {
            "pH": f"{ph} - {'✅' if 6.5 <= ph <= 8 else '❌'}",
            "Concentración": f"{conc} - {'✅' if 60 <= conc <= 84 else '❌'}",
            "Cloruros": f"{cl} - {'✅' if cl <= 50 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"MEG_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Evaluación de inhibidor de hidratos MEG.", resultados, obs)

# TEG
with tabs[3]:
    st.subheader("🧪 Análisis de TEG")
    ph = st.number_input("pH", 0.0, 14.0, step=0.01)
    conc = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1)
    cl = st.number_input("Cloruros (ppm)", 0.0, step=0.1)
    operador = st.text_input("👤 Operador", key="op_teg")
    obs = st.text_area("📝 Observaciones", key="obs_teg")
    if st.button("📊 Analizar TEG"):
        resultados = {
            "pH": f"{ph} - {'✅' if 6.5 <= ph <= 8.5 else '❌'}",
            "Concentración": f"{conc} - {'✅' if 99 <= conc <= 100 else '❌'}",
            "Cloruros": f"{cl} - {'✅' if cl <= 50 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"TEG_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Evaluación del glicol para deshidratación de gas.", resultados, obs)

# AGUA DESMINERALIZADA
with tabs[4]:
    st.subheader("💧 Agua Desmineralizada")
    cl = st.number_input("Cloruros (ppm)", 0.0, step=0.1)
    operador = st.text_input("👤 Operador", key="op_agua")
    obs = st.text_area("📝 Observaciones", key="obs_agua")
    if st.button("📊 Analizar Agua"):
        resultados = {
            "Cloruros": f"{cl} - {'✅' if cl <= 10 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"AguaDemi_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Control de cloruros en agua desmineralizada.", resultados, obs)

# AMINAS
with tabs[5]:
    st.subheader("☠️ Análisis de Aminas")
    conc = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1)
    cl_amina = st.number_input("Cloruros en amina (ppm)", 0.0, step=1.0)
    cl_caldera = st.number_input("Cloruros en caldera (ppm)", 0.0, step=0.1)
    carga_pobre = st.number_input("Carga ácida amina pobre (mol/mol)", 0.0, step=0.001)
    carga_rica = st.number_input("Carga ácida amina rica (mol/mol)", 0.0, step=0.01)
    operador = st.text_input("👤 Operador", key="op_aminas")
    obs = st.text_area("📝 Observaciones", key="obs_aminas")
    if st.button("📊 Analizar Aminas"):
        resultados = {
            "Concentración": f"{conc} - {'✅' if 48 <= conc <= 52 else '❌'}",
            "Cloruros en amina": f"{cl_amina} - {'✅' if cl_amina <= 1000 else '❌'}",
            "Cloruros en caldera": f"{cl_caldera} - {'✅' if cl_caldera <= 10 else '❌'}",
            "Carga ácida pobre": f"{carga_pobre} - {'✅' if carga_pobre <= 0.025 else '❌'}",
            "Carga ácida rica": f"{carga_rica} - {'✅' if carga_rica <= 0.45 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(f"Aminas_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", operador,
            "Evaluación de solvente amínico para remoción de gases ácidos.", resultados, obs)


