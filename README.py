import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
import os
import base64
from pathlib import Path

# Función para limpiar caracteres incompatibles
def limpiar_pdf_texto(texto):
    reemplazos = {
        "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
        "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
        "⁰": "0", "¹": "1", "²": "2", "³": "3",
        "°": " grados ", "º": "", "“": '"', "”": '"',
        "‘": "'", "’": "'", "–": "-", "—": "-", "•": "-",
        "→": "->", "←": "<-", "⇒": "=>", "≠": "!=", "≥": ">=", "≤": "<=",
        "✓": "OK", "✅": "OK", "❌": "NO"
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    return texto

# Configuración general
st.set_page_config(page_title="LTS Lab Analyzer", layout="wide")
LOGO_PATH = "logopetrogas.png"

# Estilo visual
st.markdown("""
    <style>
        .stApp { background-color: #1e1e1e; color: white; }
        .stButton>button, .stDownloadButton>button {
            background-color: #0d6efd; color: white; border-radius: 8px; border: none;
        }
        input, textarea, .stTextInput, .stTextArea, .stNumberInput input {
            background-color: #2e2e2e !important; color: white !important; border: 1px solid #555 !important;
        }
        .stSelectbox div { background-color: #2e2e2e !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo
if Path(LOGO_PATH).exists():
    with open(LOGO_PATH, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <div style='text-align:center;'>
            <img src='data:image/png;base64,{logo_base64}' width='200'/>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ No se encontró el logo 'logopetrogas.png'")

# Título
st.markdown("<h2 style='text-align:center;'>🧪 LTS Lab Analyzer</h2>", unsafe_allow_html=True)

# Clase PDF
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

# Función para exportar PDF

def exportar_pdf(nombre, operador, explicacion, resultados, observaciones):
    pdf = PDF()
    pdf.add_page()
    pdf.add_section("Operador", limpiar_pdf_texto(operador))
    pdf.add_section("Explicación técnica", limpiar_pdf_texto(explicacion))
    pdf.add_section("Resultados", {k: limpiar_pdf_texto(str(v)) for k, v in resultados.items()})
    pdf.add_section("Observaciones", limpiar_pdf_texto(observaciones or "Sin observaciones."))
    output = pdf.output(dest='S').encode('latin-1', errors='ignore')
    st.download_button("⬇️ Descargar informe PDF", data=BytesIO(output), file_name=nombre, mime="application/pdf")

# 🧾 BIENVENIDA PROFESIONAL - LTS Lab Analyzer

st.markdown("---")
st.markdown("<h3 style='text-align:center;'>👋 Bienvenido al sistema de análisis de laboratorio de planta LTS</h3>", unsafe_allow_html=True)

st.markdown("""
#### 🧾 1. Objetivo General de la App

Esta herramienta permite:

- Registrar y validar análisis físico-químicos del laboratorio.
- Generar informes PDF oficiales con logo institucional.
- Controlar parámetros operativos clave para la eficiencia de planta.
- Interpretar los resultados frente a especificaciones técnicas.

#### 📘 2. Instrucciones Paso a Paso

1. Seleccioná el análisis desde la pestaña correspondiente (Gas, Gasolina, MEG, etc.).
2. Ingresá los valores medidos del análisis.
3. Completá el nombre del operador y las observaciones si las hubiera.
4. Presioná el botón **📊 Analizar** para verificar cumplimiento.
5. Descargá el informe en PDF con un clic.

#### 🧪 3. Módulos Incluidos y Parámetros

- **Gas Natural**: H₂S y CO₂
- **Gasolina Estabilizada**: TVR, sales, agua y sedimentos
- **MEG / TEG**: pH, concentración, cloruros
- **Agua Desmineralizada**: cloruros
- **Aminas**: concentración, cloruros, carga ácida

#### 🎓 4. Importancia de los Parámetros

- **Altos H₂S** → riesgo de corrosión severa y toxicidad.
- **CO₂ elevado** → caída de pH y corrosión en equipos.
- **Cloruros altos** → incrustaciones, corrosión, fallas térmicas.
- **TVR alto** → riesgo de sobrepresión.
- **pH fuera de rango** → descomposición de solventes.
- **Cargas ácidas altas** → saturación del sistema de aminas.

#### 📂 5. Trazabilidad

Cada informe PDF incluye:

- Nombre del operador
- Fecha y hora del análisis
- Parámetros medidos
- Validación por especificación ✅❌
- Observaciones cargadas por el operador
- Logo oficial de la empresa

#### 🧑‍🏫 6. Modo de uso recomendado

- Compatible con navegadores web (Chrome, Edge, etc.).
- Puede ejecutarse en Streamlit Cloud o en una PC local.
- Ideal para uso en laboratorio de planta LTS con acceso a instrumentos y archivos.
""")


# PESTAÑAS PARA LOS MÓDULOS
tabs = st.tabs([
    "Gas Natural",
    "Gasolina Estabilizada",
    "MEG",
    "TEG",
    "Agua Desmineralizada",
    "Aminas"
])

# GAS NATURAL – con limpieza de caracteres y exportación PDF
with tabs[0]:
    st.subheader("🔥 Análisis de Gas Natural")
    st.markdown("Evaluación de gases ácidos H₂S y CO₂ para control de corrosión y cumplimiento normativo.")
    st.markdown("""
    **📌 Rangos esperados:**
    - H₂S ≤ 2.1 ppm  
    - CO₂ ≤ 2.0 %
    """)
    st.latex("H_2S \\leq 2.1\\ ppm \\quad\\quad CO_2 \\leq 2\\ \\%")

with tabs[0]:
    st.subheader("🔥 Análisis de Gas Natural")
    st.markdown("Evaluación de gases ácidos H2S y CO2 para control de corrosión y cumplimiento normativo.")
    st.latex("H_2S \\leq 2.1\\ ppm \\quad\\quad CO_2 \\leq 2\\ \\%")

    h2s = st.number_input("H₂S (ppm)", 0.0, step=0.1, key="h2s_gas")
    co2 = st.number_input("CO₂ (%)", 0.0, step=0.1, key="co2_gas")
    operador = st.text_input("👤 Operador", key="op_gas")
    obs = st.text_area("📝 Observaciones", key="obs_gas")

    if st.button("📊 Analizar Gas"):
        resultados = {
            "H2S (ppm)": f"{h2s} - {'OK' if h2s <= 2.1 else 'NO'}",
            "CO2 (%)": f"{co2} - {'OK' if co2 <= 2 else 'NO'}"
        }

        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))

        exportar_pdf(
            f"GasNatural_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            limpiar_pdf_texto(operador),
            limpiar_pdf_texto("Evaluación de H2S y CO2 en gas tratado."),
            {k: limpiar_pdf_texto(str(v)) for k, v in resultados.items()},
            limpiar_pdf_texto(obs)
        )

# ⛽ GASOLINA ESTABILIZADA
with tabs[1]:
    st.subheader("⛽ Análisis de Gasolina Estabilizada")
    st.markdown("Validación de parámetros críticos para evitar corrosión y sobrepresión.")
    st.markdown("""
    **📌 Rangos esperados:**
    - TVR ≤ 12 psia  
    - Sales ≤ 100 mg/m²  
    - Agua y sedimentos ≤ 1 %
    """)

with tabs[1]:
    st.subheader("⛽ Análisis de Gasolina Estabilizada")
    st.markdown("Validación de parámetros críticos para evitar corrosión y sobrepresión.")

    tvr = st.number_input("TVR (psia)", 0.0, step=0.1, key="tvr_gasolina")
    sales = st.number_input("Sales (mg/m²)", 0.0, step=0.1, key="sales_gasolina")
    agua = st.number_input("Agua y sedimentos (%)", 0.0, step=0.1, key="agua_gasolina")
    operador = st.text_input("👤 Operador", key="op_gasolina")
    obs = st.text_area("📝 Observaciones", key="obs_gasolina")

    if st.button("📊 Analizar Gasolina"):
        resultados = {
            "TVR": f"{tvr} - {'✅' if tvr <= 12 else '❌'}",
            "Sales": f"{sales} - {'✅' if sales <= 100 else '❌'}",
            "Agua y sedimentos": f"{agua} - {'✅' if agua <= 1 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(
            f"Gasolina_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            operador,
            "Evaluación de TVR, sales y sedimentos en gasolina estabilizada.",
            resultados,
            obs
        )
# 🧪 MEG
with tabs[2]:
    st.subheader("🧪 Análisis de MEG")
    st.markdown("Análisis del inhibidor de formación de hidratos en el sistema. Control de corrosión y salinidad.")
    st.markdown("""
    **📌 Rangos esperados:**
    - pH entre 6.5 y 8  
    - Concentración entre 60 y 84 %  
    - Cloruros ≤ 50 ppm
    """)

with tabs[2]:
    st.subheader("🧪 Análisis de MEG")
    st.markdown("Análisis del inhibidor de formación de hidratos en el sistema. Control de corrosión y salinidad.")

    ph_meg = st.number_input("pH", 0.0, 14.0, step=0.01, key="ph_meg")
    conc_meg = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1, key="conc_meg")
    cl_meg = st.number_input("Cloruros (ppm)", 0.0, step=0.1, key="cl_meg")
    operador = st.text_input("👤 Operador", key="op_meg")
    obs = st.text_area("📝 Observaciones", key="obs_meg")

    if st.button("📊 Analizar MEG"):
        resultados = {
            "pH": f"{ph_meg} - {'✅' if 6.5 <= ph_meg <= 8 else '❌'}",
            "Concentración": f"{conc_meg} - {'✅' if 60 <= conc_meg <= 84 else '❌'}",
            "Cloruros": f"{cl_meg} - {'✅' if cl_meg <= 50 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(
            f"MEG_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            operador,
            "Evaluación del MEG (inhibidor de hidratos) en planta LTS.",
            resultados,
            obs
        )

# 🧪 TEG
with tabs[3]:
    st.subheader("🧪 Análisis de TEG")
    st.markdown("Control del glicol utilizado para deshidratación de gas natural.")
    st.markdown("""
    **📌 Rangos esperados:**
    - pH entre 6.5 y 8.5  
    - Concentración ≥ 99 %  
    - Cloruros ≤ 50 ppm
    """)

with tabs[3]:
    st.subheader("🧪 Análisis de TEG")
    st.markdown("Control del glicol utilizado para deshidratación de gas natural.")

    ph_teg = st.number_input("pH", 0.0, 14.0, step=0.01, key="ph_teg")
    conc_teg = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1, key="conc_teg")
    cl_teg = st.number_input("Cloruros (ppm)", 0.0, step=0.1, key="cl_teg")
    operador = st.text_input("👤 Operador", key="op_teg")
    obs = st.text_area("📝 Observaciones", key="obs_teg")

    if st.button("📊 Analizar TEG"):
        resultados = {
            "pH": f"{ph_teg} - {'✅' if 6.5 <= ph_teg <= 8.5 else '❌'}",
            "Concentración": f"{conc_teg} - {'✅' if 99 <= conc_teg <= 100 else '❌'}",
            "Cloruros": f"{cl_teg} - {'✅' if cl_teg <= 50 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(
            f"TEG_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            operador,
            "Evaluación del TEG utilizado para deshidratación de gas.",
            resultados,
            obs
        )
# 💧 AGUA DESMINERALIZADA
with tabs[4]:
    st.subheader("💧 Análisis de Agua Desmineralizada")
    st.markdown("Evaluación del agua utilizada en calderas o procesos sensibles. Cloruros bajos son esenciales para evitar corrosión.")
    st.markdown("""
    **📌 Rango esperado:**
    - Cloruros ≤ 10 ppm
    """)

with tabs[4]:
    st.subheader("💧 Análisis de Agua Desmineralizada")
    st.markdown("Evaluación del agua utilizada en calderas o procesos sensibles. Cloruros bajos son esenciales para evitar corrosión.")

    cl_agua = st.number_input("Cloruros (ppm)", 0.0, step=0.1, key="cl_agua")
    operador = st.text_input("👤 Operador", key="op_agua")
    obs = st.text_area("📝 Observaciones", key="obs_agua")

    if st.button("📊 Analizar Agua"):
        resultados = {
            "Cloruros": f"{cl_agua} - {'✅' if cl_agua <= 10 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(
            f"AguaDemi_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            operador,
            "Control de cloruros en agua desmineralizada para evitar incrustaciones y corrosión.",
            resultados,
            obs
        )

# ☠️ AMINAS
with tabs[5]:
    st.subheader("☠️ Análisis de Aminas")
    st.markdown("Evaluación del solvente amínico para remoción de gases ácidos como CO₂ y H₂S. Control clave en unidades de endulzamiento.")
    st.markdown("""
    **📌 Rangos esperados:**
    - Concentración entre 48 y 52 %  
    - Cloruros en amina ≤ 1000 ppm  
    - Cloruros en caldera ≤ 10 ppm  
    - Carga ácida amina pobre ≤ 0.025 mol/mol  
    - Carga ácida amina rica ≤ 0.45 mol/mol
    """)

with tabs[5]:
    st.subheader("☠️ Análisis de Aminas")
    st.markdown("Evaluación del solvente amínico para remoción de gases ácidos como CO₂ y H₂S. Control clave en unidades de endulzamiento.")

    conc_aminas = st.number_input("Concentración (%wt)", 0.0, 100.0, step=0.1, key="conc_aminas")
    cl_aminas = st.number_input("Cloruros en amina (ppm)", 0.0, step=1.0, key="cl_aminas")
    cl_caldera = st.number_input("Cloruros en caldera (ppm)", 0.0, step=0.1, key="cl_caldera")
    carga_pobre = st.number_input("Carga ácida amina pobre (mol/mol)", 0.0, step=0.001, key="carga_pobre")
    carga_rica = st.number_input("Carga ácida amina rica (mol/mol)", 0.0, step=0.01, key="carga_rica")
    operador = st.text_input("👤 Operador", key="op_aminas")
    obs = st.text_area("📝 Observaciones", key="obs_aminas")

    if st.button("📊 Analizar Aminas"):
        resultados = {
            "Concentración": f"{conc_aminas} - {'✅' if 48 <= conc_aminas <= 52 else '❌'}",
            "Cloruros en amina": f"{cl_aminas} - {'✅' if cl_aminas <= 1000 else '❌'}",
            "Cloruros en caldera": f"{cl_caldera} - {'✅' if cl_caldera <= 10 else '❌'}",
            "Carga ácida pobre": f"{carga_pobre} - {'✅' if carga_pobre <= 0.025 else '❌'}",
            "Carga ácida rica": f"{carga_rica} - {'✅' if carga_rica <= 0.45 else '❌'}"
        }
        st.dataframe(pd.DataFrame(resultados.items(), columns=["Parámetro", "Valor"]))
        exportar_pdf(
            f"Aminas_{operador}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            operador,
            "Evaluación de aminas en procesos de remoción de CO₂/H₂S. Control de corrosión, carga ácida y sales.",
            resultados,
            obs
        )

