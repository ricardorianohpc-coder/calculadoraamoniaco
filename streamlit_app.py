import streamlit as st

# Configuración de la página del navegador
st.set_page_config(
    page_title="Modelo Científico de Emerson (1975) | ASIA ACUACULTURA SAS Cel 3004390818",
    page_icon="🐟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilo personalizado con CSS
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.title("🐟 Calculadora de Amoníaco en Tilapia")
st.markdown("### Modelo Científico de Emerson (1975) | ASIA ACUACULTURA SAS Cel 3004390818")
st.write("Esta herramienta móvil e interactiva permite separar las fracciones de amoníaco tóxico e ionizado a partir del pH, la temperatura y el TAN medido en tus tanques.")

# Barra Lateral - Entradas de Datos
st.sidebar.header("📋 Datos de Campo")
st.sidebar.write("Digita o ajusta los valores medidos en el tanque:")

temp = st.sidebar.slider(
    "Temperatura del Agua (°C)", 
    min_value=15.0, 
    max_value=35.0, 
    value=28.0, 
    step=0.5,
    help="La temperatura altera la constante de equilibrio químico."
)

ph = st.sidebar.slider(
    "pH del Agua", 
    min_value=6.0, 
    max_value=9.5, 
    value=7.8, 
    step=0.1,
    help="El pH es el factor más crítico. A mayor pH, el amonio se vuelve gas tóxico exponencialmente."
)

tan = st.sidebar.number_input(
    "Nitrógeno Amoniacal Total - TAN (mg/L)", 
    min_value=0.0, 
    max_value=10.0, 
    value=1.0, 
    step=0.1,
    help="Lectura directa obtenida del kit de reactivos comercial (API, Hach, etc.)."
)

# Constantes matemáticas fijas del modelo de Emerson (1975)
const_a = 0.09018
const_b = 2729.92
const_kelvin = 273.15

# Cálculos matemáticos de la disociación
pka = const_a + (const_b / (temp + const_kelvin))
pct_nh3 = 1 / (10**(pka - ph) + 1)
pct_nh4 = 1 - pct_nh3

# Especiación en miligramos por litro (mg/L)
nh3_tox = tan * pct_nh3
nh4_ion = tan * pct_nh4

# Sección de Constantes Ocultas en Expander
with st.sidebar.expander("🔬 Ver Constantes y Fórmulas"):
    st.write(f"**Constante a:** {const_a}")
    st.write(f"**Constante b:** {const_b}")
    st.write(f"**Constante Kelvin:** {const_kelvin}")
    st.write(f"**pKₐ calculado:** `{pka:.5f}`")
    st.write(f"**Fracción NH₃ (Tóxico):** `{pct_nh3*100:.3f}%`")
    st.write(f"**Fracción NH₄⁺ (Seguro):** `{pct_nh4*100:.3f}%`")

# Diagnóstico de Alerta Sanitaria según umbrales de tilapia
if nh3_tox < 0.02:
    status = "EXCELENTE (SEGURO)"
    color = "#2E7D32"  # Verde oscuro
    bg_color = "#E8F5E9"
    border_color = "#4CAF50"
    desc = "Condición óptima de confort. El amoníaco libre no afecta el crecimiento ni la conversión alimenticia de las tilapias."
elif nh3_tox < 0.05:
    status = "ACEPTABLE (VIGILANCIA)"
    color = "#F57F17"  # Naranja/Amarillo oscuro
    bg_color = "#FFFDE7"
    border_color = "#FBC02D"
    desc = "Rango normal para sistemas semi-intensivos o simbióticos. Mantener monitoreo rutinario."
elif nh3_tox < 0.10:
    status = "ESTRÉS SUBLETAL (ALARMA)"
    color = "#E65100"  # Naranja fuerte
    bg_color = "#FFE0B2"
    border_color = "#FB8C00"
    desc = "Provoca estrés agudo en peces. Disminuye la tasa de consumo de alimento y causa daños leves y paulatinos en branquias."
elif nh3_tox < 0.20:
    status = "PELIGRO (DAÑO BRANQUIAL)"
    color = "#C62828"  # Rojo
    bg_color = "#FFEBEE"
    border_color = "#E53935"
    desc = "Provoca daño tisular severo en el sistema branquial, asfixia osmótica, nado errático y letargo en superficie."
else:
    status = "CRÍTICO / LETAL"
    color = "#3E2723"  # Marrón / Negro rojizo
    bg_color = "#FFCDD2"
    border_color = "#B71C1C"
    desc = "Mortalidad aguda inminente y masiva en la población. Requiere intervención inmediata de emergencia."

# Tarjeta visual de Diagnóstico en HTML
st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 22px; border-radius: 10px; border-left: 8px solid {border_color}; margin-top: 10px; margin-bottom: 25px;">
        <h3 style="color: {color}; margin-top: 0; font-weight: bold;">ESTADO: {status}</h3>
        <p style="font-size: 17px; margin-bottom: 8px; color: #111;">
            Amoníaco Libre Tóxico (NH₃): <b>{nh3_tox:.4f} mg/L (ppm)</b>
        </p>
        <p style="font-size: 14px; line-height: 1.4; color: #333; margin-top: 5px;">
            {desc}
        </p>
    </div>
""", unsafe_allow_html=True)

# Visualización de Métricas Principales en columnas
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Gas Tóxico Libre (NH3)", 
        value=f"{nh3_tox:.4f} mg/L", 
        delta=f"{pct_nh3*100:.2f}% del TAN",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Ion Amonio Seguro (NH4+)", 
        value=f"{nh4_ion:.4f} mg/L", 
        delta=f"{pct_nh4*100:.2f}% del TAN"
    )

st.write("---")

# Secciones complementarias
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🛠️ Acciones Recomendadas")
    if status in ["EXCELENTE (SEGURO)", "ACEPTABLE (VIGILANCIA)"]:
        st.success("✅ **Todo bajo control.** Mantener rutinas de alimentación estándar, dosificación diaria de simbiótica y medición regular de oxígeno en los 5 horarios de protocolo.")
    elif status == "ESTRÉS SUBLETAL (ALARMA)":
        st.warning("⚠️ **Medidas Preventivas:**\n* Reducir la ración de alimento en un 20% a 30%.\n* Aumentar la aireación y circulación en los tanques.\n* Evaluar la adición de una ración ligera de melaza para estimular a las bacterias heterótrofas a asimilar el amonio.")
    else:
        st.error("🚨 **ACCIONES DE EMERGENCIA INMEDIATAS:**\n1. **Suspender la alimentación** por completo.\n2. **Aumentar la aireación** al máximo (encender sopladores o cascadas de respaldo).\n3. **Aplicar Sal común** (500 g por cada tonelada de agua en tanques) para mitigar el estrés osmótico y toxicidad por nitritos asociados.\n4. **Realizar recambio de agua** parcial si el sistema lo permite.\n5. **Adicionar melaza** de forma inmediata según las tablas de dosificación para transformar el amoníaco en biomasa bacteriana inocua.")

with col_b:
    st.subheader("📊 Tabla de Referencia")
    st.markdown("""
    | Rango NH₃ (mg/L) | Nivel de Riesgo | Estado de Peces |
    | :--- | :--- | :--- |
    | **< 0.02** | Excelente | Seguro / Confort |
    | **0.02 - 0.05** | Aceptable | Monitoreo normal |
    | **0.05 - 0.10** | Alerta | Estrés / Poco apetito |
    | **0.10 - 0.20** | Peligro | Asfixia / Daño branquial |
    | **> 0.20** | Crítico | Mortalidad masiva |
    """)

# Pie de página
st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Desarrollado para Piscícola Las Acacias • Basado en Emerson et al. (1975)</p>", unsafe_allow_html=True)
